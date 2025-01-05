"""Directory Tree Generation for Copcon.

This module provides functionality to generate a visual representation of the project's
directory structure.
"""

from pathlib import Path
from typing import Optional
from copcon.core.file_filter import FileFilter

class FileTreeGenerator:
    """Generates a tree-like directory structure for a given directory.

    Traverses the directory up to a specified depth and applies file filters to exclude
    certain files and directories.
    """

    def __init__(
        self,
        directory: Path,
        depth: int,
        file_filter: FileFilter,
    ):
        """
        Initialize the FileTreeGenerator.

        Args:
            directory (Path): The root directory to generate the tree from.
            depth (int): The maximum depth to traverse (-1 for unlimited).
            file_filter (FileFilter): The file filter to determine which files and directories to include.

        Attributes:
            directory_count (int): The total number of directories processed.
            file_count (int): The total number of files processed.
        """
        self.directory = directory
        self.depth = depth
        self.file_filter = file_filter
        self.directory_count = 0  # Initialize directory count
        self.file_count = 0       # Initialize file count

    def generate(self, current_dir: Optional[Path] = None, current_depth: int = 0, prefix: str = "") -> str:
        """Generate the directory tree as a string.

        Args:
            current_dir (Path, optional): The current directory being traversed.
            current_depth (int): The current depth in the directory tree.
            prefix (str): The prefix string for the current level of the tree.

        Returns:
            str: The generated directory tree as a string.
        """

        if current_dir is None:
            current_dir = self.directory
            self.directory_count = 1  # Count the root directory

        if self.depth != -1 and current_depth > self.depth:
            return ""

        output = []
        try:
            contents = sorted(current_dir.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        except Exception as e:
            output.append(f"{prefix}Error accessing {current_dir}: {e}")
            return "\n".join(output)

        visible_contents = [path for path in contents if not self.file_filter.should_ignore(path)]

        for i, path in enumerate(visible_contents):
            is_last = i == len(visible_contents) - 1
            connector = "└── " if is_last else "├── "
            output.append(f"{prefix}{connector}{path.name}")
            if path.is_dir():
                self.directory_count += 1  # Increment directory count
                extension = "    " if is_last else "│   "
                subtree = self.generate(path, current_depth + 1, prefix + extension)
                if subtree:
                    output.append(subtree)
            else:
                self.file_count += 1  # Increment file count

        return "\n".join(output)
