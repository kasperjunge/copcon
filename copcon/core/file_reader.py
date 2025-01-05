"""File Reading for Copcon.

This module provides functionality to read the contents of files in the project directory,
handling both text and binary files appropriately.
"""

from pathlib import Path
from typing import Dict, List
from copcon.core.file_filter import FileFilter
from copcon.exceptions import FileReadError
from copcon.utils.logger import logger

class FileContentReader:
    """Reads and manages the contents of files in the project directory.

    Handles reading text files and providing placeholders for binary files. Keeps track of
    the total number of characters processed.
    """

    def __init__(self, base_directory: Path, file_filter: FileFilter, exclude_hidden: bool):
        """
        Initialize the FileContentReader.

        Args:
            base_directory (Path): The root directory of the project to read files from.
            file_filter (FileFilter): The file filter to determine which files to read.
            exclude_hidden (bool): Whether to exclude hidden files and directories.

        Attributes:
            total_chars (int): The total number of characters in all read files.
        """
 
        self.base_directory = base_directory
        self.file_filter = file_filter
        self.exclude_hidden = exclude_hidden
        self.total_chars = 0  # Initialize total characters

    def read_all(self) -> Dict[str, str]:
        """Read all applicable files in the base directory.

        Returns:
            Dict[str, str]: A dictionary mapping relative file paths to their contents.

        Raises:
            FileReadError: If any file read operations fail.
        """

        file_contents = {}
        errors: List[FileReadError] = []
        for file_path in self.base_directory.rglob("*"):
            if file_path.is_file():
                if self.exclude_hidden and self._is_hidden(file_path):
                    continue
                if self.file_filter.should_ignore(file_path):
                    continue
                try:
                    content = self._read_file(file_path)
                    relative_path = str(file_path.relative_to(self.base_directory))
                    file_contents[relative_path] = content
                    self.total_chars += len(content)
                except FileReadError as e:
                    logger.warning(f"Skipping file {file_path}: {e}")
                    errors.append(e)
        if errors:
            raise FileReadError(f"Encountered errors while reading files: {[str(e) for e in errors]}")
        return file_contents

    def _is_hidden(self, path: Path) -> bool:
        """Check if a file or directory is hidden.

        Args:
            path (Path): The path to check.

        Returns:
            bool: True if the path is hidden, False otherwise.
        """

        return any(part.startswith(".") for part in path.parts)

    def _read_file(self, file_path: Path) -> str:
        """Read the contents of a file.

        Args:
            file_path (Path): The path to the file to read.

        Returns:
            str: The content of the file or a placeholder for binary files.

        Raises:
            FileReadError: If the file cannot be read.
        """

        try:
            # Detect if file is binary
            if self._is_binary(file_path):
                size = file_path.stat().st_size
                return f"[Binary file] Size: {size} bytes"
            else:
                return file_path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise FileReadError(f"Error reading file {file_path}: {e}")

    def _is_binary(self, file_path: Path) -> bool:
        """Determine if a file is binary.

        Args:
            file_path (Path): The path to the file to check.

        Returns:
            bool: True if the file is binary, False otherwise.

        Raises:
            FileReadError: If there is an error detecting the file type.
        """
        try:
            with file_path.open('rb') as f:
                chunk = f.read(1024)
                if b'\0' in chunk:
                    return True
            return False
        except Exception as e:
            logger.error(f"Error detecting binary for file {file_path}: {e}")
            raise FileReadError(f"Error detecting binary for file {file_path}: {e}")
