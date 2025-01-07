import pytest
from copcon.core.file_reader import FileContentReader
from copcon.core.file_filter import FileFilter
from copcon.exceptions import FileReadError

def test_file_content_reader_with_text_files(temp_dir, copconignore_file):
    # Initialize FileFilter
    file_filter = FileFilter(
        additional_dirs=None,
        additional_files=None,
        user_ignore_path=copconignore_file
    )
    
    # Create files
    text_file = temp_dir / "file1.py"
    text_file.write_text("print('Hello, World!')")
    ignored_file = temp_dir / "file2.log"
    ignored_file.write_text("This is a log file.")
    
    # Initialize FileContentReader
    reader = FileContentReader(base_directory=temp_dir, file_filter=file_filter, exclude_hidden=True)
    contents = reader.read_all()
    
    # Assertions
    assert "file1.py" in contents, "file1.py should be read."
    assert "file2.log" not in contents, "file2.log should be ignored."

def test_file_content_reader_with_binary_files(temp_dir, copconignore_file):
    # Initialize FileFilter
    file_filter = FileFilter(
        additional_dirs=None,
        additional_files=None,
        user_ignore_path=copconignore_file
    )
    
    # Create binary file
    binary_file = temp_dir / "image.png"
    binary_file.write_bytes(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00')
    
    # Initialize FileContentReader
    reader = FileContentReader(base_directory=temp_dir, file_filter=file_filter, exclude_hidden=True)
    contents = reader.read_all()
    
    # Assertions
    assert "image.png" in contents, "image.png should be read."
    expected_placeholder = "[Binary file] Size: 17 bytes"
    assert contents["image.png"] == expected_placeholder, "Binary file should have a placeholder with size."

def test_file_content_reader_with_hidden_files(temp_dir, copconignore_file):
    # Initialize FileFilter
    file_filter = FileFilter(
        additional_dirs=None,
        additional_files=None,
        user_ignore_path=None  # No user-specified ignore
    )
    
    # Create hidden files and directories
    hidden_dir = temp_dir / ".hidden_dir"
    hidden_dir.mkdir()
    hidden_file = temp_dir / ".hidden_file.py"
    hidden_file.write_text("print('This is hidden')")
    visible_file = temp_dir / "visible_file.py"
    visible_file.write_text("print('This is visible')")
    
    # Initialize FileContentReader with exclude_hidden=True
    reader = FileContentReader(base_directory=temp_dir, file_filter=file_filter, exclude_hidden=True)
    contents = reader.read_all()
    
    # Assertions
    assert ".hidden_dir" not in contents, ".hidden_dir should be excluded."
    assert ".hidden_file.py" not in contents, ".hidden_file.py should be excluded."
    assert "visible_file.py" in contents, "visible_file.py should be included."

def test_file_content_reader_error_handling(temp_dir):
    # Initialize FileFilter
    file_filter = FileFilter(
        additional_dirs=None,
        additional_files=None,
        user_ignore_path=None
    )
    
    # Create a file with restricted permissions (simulate read error)
    restricted_file = temp_dir / "restricted_file.py"
    restricted_file.touch()
    # Remove read permissions
    restricted_file.chmod(0o000)
    
    # Initialize FileContentReader
    reader = FileContentReader(base_directory=temp_dir, file_filter=file_filter, exclude_hidden=True)
    
    # Attempt to read files and expect a warning but not a crash
    with pytest.raises(FileReadError):
        reader.read_all()
    
    # Restore permissions for cleanup
    restricted_file.chmod(0o644)
