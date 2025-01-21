"""
Auto-discovery of a .copconignore and .copcontarget file.

This module provides functionality to walk upward from a given directory in
search of a .copconignore or .copcontarget file. If found, the path to these
files is returned. Otherwise, None is returned.
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

def discover_copcontarget(directory: Path) -> Optional[Path]:
    """
    Attempt to walk upward from 'directory' to find a .copcontarget file.
    Returns the file's Path if discovered, or None if not found.
    """
    current = directory.resolve()
    while True:
        possible_target = current / ".copcontarget"
        if possible_target.exists() and possible_target.is_file():
            logger.debug(f"Auto-discovered .copcontarget at {possible_target}")
            return possible_target

        if current.parent == current:
            break
        current = current.parent

    return None
