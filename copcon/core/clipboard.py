"""Clipboard Management for Copcon.

This module provides functionality to interact with the system clipboard, allowing Copcon
to copy generated reports directly to the clipboard.
"""

import pyperclip
from copcon.exceptions import ClipboardError
from copcon.utils.logger import logger


class ClipboardManager:
    """Manages clipboard operations for Copcon.

    Provides methods to copy text to the system clipboard.
    """

    def copy(self, text: str):
        """Copy text to the system clipboard.

        Args:
            text (str): The text to copy to the clipboard.

        Raises:
            ClipboardError: If the clipboard operation fails.
        """
        try:
            pyperclip.copy(text)
        except pyperclip.PyperclipException as e:
            logger.error(f"Error copying to clipboard: {e}")
            raise ClipboardError(f"Error copying to clipboard: {e}")
