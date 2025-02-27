import pytest
from copcon.core.file_filter import FileFilter
from copcon.exceptions import FileReadError

def test_file_filter_with_internal_copconignore(temp_dir, copconignore_file):
    # Initialize FileFilter without user-specified ignore file
    file_filter = FileFilter(
        user_ignore_path=None  # Should load internal .copconignore
    )
    
    # Define paths to test
    included_dir = temp_dir / "included_dir"
    excluded_dir = temp_dir / "__pycache__"
    included_file = temp_dir / "included_file.py"
    excluded_file = temp_dir / "poetry.lock"
    
    # Create directories and files
    included_dir.mkdir()
    excluded_dir.mkdir()
    included_file.touch()
    excluded_file.touch()
    
    # Assertions
    assert not file_filter.should_ignore(included_dir), "Included directory should not be ignored."
    assert file_filter.should_ignore(excluded_dir), "Excluded directory should be ignored."
    assert not file_filter.should_ignore(included_file), "Included file should not be ignored."
    assert file_filter.should_ignore(excluded_file), "Excluded file should be ignored."

def test_file_filter_with_user_copconignore(temp_dir, copconignore_file, additional_ignore_file):
    # Initialize FileFilter with user-specified ignore file
    file_filter = FileFilter(
        user_ignore_path=additional_ignore_file
    )
    
    # Define paths to test
    included_dir = temp_dir / "included_dir"
    excluded_dir = temp_dir / "build"  # This should be in the additional_ignore_file
    included_file = temp_dir / "included_file.py"
    excluded_file = temp_dir / "secret.txt"  # This should be in the additional_ignore_file
    
    # Create directories and files
    included_dir.mkdir()
    excluded_dir.mkdir()
    included_file.touch()
    excluded_file.touch()
    
    # Assertions
    assert not file_filter.should_ignore(included_dir), "Included directory should not be ignored."
    assert file_filter.should_ignore(excluded_dir), "Excluded directory should be ignored."
    assert not file_filter.should_ignore(included_file), "Included file should not be ignored."
    assert file_filter.should_ignore(excluded_file), "Excluded file should be ignored."

def test_file_filter_with_combined_ignores(temp_dir, copconignore_file):
    # Initialize FileFilter with both internal and user-specified ignore patterns
    file_filter = FileFilter(
        user_ignore_path=copconignore_file  # User-specified .copconignore
    )
    
    # Define paths to test
    included_dir = temp_dir / "included_dir"
    excluded_dir = temp_dir / "__pycache__"  # Should be ignored by internal patterns
    build_dir = temp_dir / "build"  # Should be ignored by user patterns
    included_file = temp_dir / "included_file.py"
    excluded_file = temp_dir / "poetry.lock"  # Should be ignored by internal patterns
    secret_file = temp_dir / "secret.txt"  # Should be ignored by user patterns
    
    # Create directories and files
    included_dir.mkdir()
    excluded_dir.mkdir()
    build_dir.mkdir()
    included_file.touch()
    excluded_file.touch()
    secret_file.touch()
    
    # Assertions
    assert not file_filter.should_ignore(included_dir), "Included directory should not be ignored."
    assert file_filter.should_ignore(excluded_dir), "Internal excluded directory should be ignored."
    assert file_filter.should_ignore(build_dir), "User excluded directory should be ignored."
    assert not file_filter.should_ignore(included_file), "Included file should not be ignored."
    assert file_filter.should_ignore(excluded_file), "Internal excluded file should be ignored."
    # assert file_filter.should_ignore(secret_file), "User excluded file should be ignored."

def test_file_filter_invalid_copconignore_no_exception(temp_dir):
    # Create an invalid .copconignore file
    invalid_ignore_path = temp_dir / ".copconignore"
    invalid_ignore_path.write_text("**/invalid[")
    
    # Initialize FileFilter
    try:
        file_filter = FileFilter(
            user_ignore_path=invalid_ignore_path
        )
    except FileReadError:
        pytest.fail("FileReadError was raised for an invalid .copconignore pattern, but it should have been treated as a literal.")
    
    # Verify that the invalid pattern is present in the spec
    invalid_matched_file = temp_dir / "invalid[.txt"
    invalid_matched_file.touch()
    
    assert not file_filter.should_ignore(invalid_matched_file), "Invalid pattern should be treated as a literal and not ignore files."
