"""
Auto-discovery of a .copconignore file.

This module provides functionality to walk upward from a given directory in
search of a .copconignore file. If found, the path to this file is returned.
Otherwise, None is returned.

Usage:
    from pathlib import Path
    from copcon.core.autodiscover import discover_copconignore

    directory = Path("/some/project/path")
    ignore_path = discover_copconignore(directory)
    if ignore_path:
        print(f"Discovered .copconignore at: {ignore_path}")
    else:
        print("No .copconignore found.")
"""

from pathlib import Path
from typing import Optional
from copcon.utils.logger import logger

def discover_copconignore(directory: Path) -> Optional[Path]:
    """
    Attempt to walk upward from 'directory' to find a .copconignore file.
    Returns the file's Path if discovered, or None if not found.
    """
    current = directory.resolve()
    while True:
        possible_ignore = current / ".copconignore"
        if possible_ignore.exists() and possible_ignore.is_file():
            logger.debug(f"Auto-discovered .copconignore at {possible_ignore}")
            return possible_ignore

        if current.parent == current:
            break
        current = current.parent

    return None
