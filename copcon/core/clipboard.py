import pyperclip
import typer
from copcon.exceptions import ClipboardError
from copcon.utils.logger import logger


class ClipboardManager:
    def copy(self, text: str):
        try:
            pyperclip.copy(text)
        except pyperclip.PyperclipException as e:
            logger.error(f"Error copying to clipboard: {e}")
            raise ClipboardError(f"Error copying to clipboard: {e}")
