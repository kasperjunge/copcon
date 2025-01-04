from unittest.mock import patch
from copcon.core.clipboard import ClipboardManager

def test_clipboard_manager_copy_success():
    clipboard_text = "Test clipboard content"
    
    with patch('copcon.core.clipboard.pyperclip.copy') as mock_copy:
        clipboard = ClipboardManager()
        clipboard.copy(clipboard_text)
        mock_copy.assert_called_once_with(clipboard_text)
