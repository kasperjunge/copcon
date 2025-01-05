"""File Filtering for Copcon.

This module provides functionality to filter files and directories based on ignore patterns
specified in `.copconignore` files and additional user-defined patterns.
"""

from pathlib import Path
from typing import List, Set, Optional
import pathspec
from copcon.exceptions import FileReadError
from copcon.utils.logger import logger
import importlib.resources as pkg_resources

class FileFilter:
    """Filters files and directories based on ignore patterns.

    Combines internal and user-specified ignore patterns to determine whether a file or
    directory should be excluded from processing.
    """

    def __init__(
        self,
        additional_dirs: Optional[List[str]] = None,
        additional_files: Optional[List[str]] = None,
        user_ignore_path: Optional[Path] = None,
    ):
        """
        Initialize the FileFilter.

        Args:
            additional_dirs (List[str], optional): Additional directory names to ignore.
            additional_files (List[str], optional): Additional file names to ignore.
            user_ignore_path (Path, optional): Path to a user-specified `.copconignore` file.

        Raises:
            FileReadError: If there is an error reading ignore files.
        """

        # Load default ignore patterns from internal .copconignore
        self.ignore_spec = self._load_internal_copconignore()

        # Load additional ignore patterns from user-specified .copconignore
        if user_ignore_path and user_ignore_path.exists():
            try:
                with user_ignore_path.open() as f:
                    user_patterns = [line.strip() for line in f if line.strip() and not line.startswith("#")]
                user_spec = pathspec.PathSpec.from_lines("gitwildmatch", user_patterns)
                self.ignore_spec = self.ignore_spec + user_spec  # Combine specs
                logger.debug(f"Loaded user ignore patterns from {user_ignore_path}")
            except Exception as e:
                logger.error(f"Error reading user ignore file {user_ignore_path}: {e}")
                raise FileReadError(f"Error reading user ignore file {user_ignore_path}: {e}")

        # Add additional directories and files to ignore
        if additional_dirs:
            self.ignore_dirs = set(additional_dirs)
        else:
            self.ignore_dirs = set()

        if additional_files:
            self.ignore_files = set(additional_files)
        else:
            self.ignore_files = set()

    def _load_internal_copconignore(self) -> pathspec.PathSpec:
        """Load internal ignore patterns from the package's .copconignore file.

        Returns:
            pathspec.PathSpec: The compiled path specification.

        Raises:
            FileReadError: If there is an error loading the internal ignore file.
        """

        try:
            with pkg_resources.open_text('copcon.core', '.copconignore') as f:
                patterns = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
            logger.debug("Loaded internal .copconignore patterns.")
            return spec
        except Exception as e:
            logger.error(f"Error loading internal .copconignore: {e}")
            raise FileReadError(f"Error loading internal .copconignore: {e}")

    def should_ignore(self, path: Path) -> bool:
        """Determine whether a given file or directory should be ignored.

        Args:
            path (Path): The file or directory path to check.

        Returns:
            bool: True if the path should be ignored, False otherwise.
        """

        path_str = str(path)
        if path.is_dir():
            path_str += "/"
        # Check against internal and user-specified ignore patterns
        if self.ignore_spec.match_file(path_str):
            return True
        # Check additional directories and files
        if path.is_dir() and path.name in self.ignore_dirs:
            return True
        if path.is_file() and path.name in self.ignore_files:
            return True
        return False
