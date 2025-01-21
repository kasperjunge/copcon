"""File Filtering for Copcon.

This module provides functionality to filter files and directories based on ignore patterns
specified in `.copconignore` files and additional user-defined patterns. It also supports
a `.copcontarget` file to target specific directories and files.
"""

from pathlib import Path
from typing import List, Optional
import pathspec
from copcon.exceptions import FileReadError
from copcon.utils.logger import logger
import importlib.resources as pkg_resources


class FileFilter:
    """Filters files and directories based on ignore and target patterns.

    Combines internal, user-specified ignore patterns, and target patterns to determine
    whether a file or directory should be excluded from processing.
    """

    def __init__(
        self,
        additional_dirs: Optional[List[str]] = None,
        additional_files: Optional[List[str]] = None,
        user_ignore_path: Optional[Path] = None,
        user_target_path: Optional[Path] = None,
    ):
        """
        Initialize the FileFilter.

        Args:
            additional_dirs (List[str], optional): Additional directory names to ignore.
            additional_files (List[str], optional): Additional file names to ignore.
            user_ignore_path (Path, optional): Path to a user-specified `.copconignore` file.
            user_target_path (Path, optional): Path to a user-specified `.copcontarget` file.

        Raises:
            FileReadError: If there is an error reading ignore or target files.
        """
        # Load internal patterns
        self.ignore_spec = self._load_internal_copconignore()
        self.user_defined = False  # Flag to indicate if user-defined .copconignore was loaded

        # Load user-specified ignore patterns if any
        if user_ignore_path and user_ignore_path.exists():
            try:
                with user_ignore_path.open() as f:
                    user_patterns = [line.strip() for line in f if line.strip() and not line.startswith("#")]
                user_spec = pathspec.PathSpec.from_lines("gitwildmatch", user_patterns)
                self.ignore_spec = self.ignore_spec + user_spec  # Merge user patterns
                self.user_defined = True  # Set flag as user-defined .copconignore is loaded
                logger.debug(f"Loaded user ignore patterns from {user_ignore_path}")
            except Exception as e:
                logger.error(f"Error reading user ignore file {user_ignore_path}: {e}")
                raise FileReadError(f"Error reading user ignore file {user_ignore_path}: {e}")

        # Load target patterns if a .copcontarget file is provided
        self.target_spec = None
        if user_target_path and user_target_path.exists():
            try:
                with user_target_path.open() as f:
                    target_patterns = [line.strip() for line in f if line.strip() and not line.startswith("#")]
                if target_patterns:
                    self.target_spec = pathspec.PathSpec.from_lines("gitwildmatch", target_patterns)
                    logger.debug(f"Loaded target patterns from {user_target_path}")
                else:
                    logger.debug(f"No patterns found in {user_target_path}, ignoring .copcontarget.")
            except Exception as e:
                logger.error(f"Error reading user target file {user_target_path}: {e}")
                raise FileReadError(f"Error reading user target file {user_target_path}: {e}")

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
        path_str = str(path.relative_to(path.anchor))
        if path.is_dir():
            path_str += "/"

        # Apply .copcontarget: if target_spec exists and path does not match, ignore it.
        if self.target_spec is not None and not self.target_spec.match_file(path_str):
            return True

        # Check against internal and user-specified ignore patterns
        if self.ignore_spec.match_file(path_str):
            return True

        # Check additional directories and files
        if path.is_dir() and path.name in self.ignore_dirs:
            return True
        if path.is_file() and path.name in self.ignore_files:
            return True
        return False

    def has_user_defined_ignore(self) -> bool:
        """Check if a user-defined .copconignore was loaded.

        Returns:
            bool: True if a user-defined .copconignore was loaded, False otherwise.
        """
        return self.user_defined
