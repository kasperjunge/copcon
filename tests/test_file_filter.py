import pytest
from copcon.core.file_filter import FileFilter
from copcon.exceptions import FileReadError

def test_file_filter_with_internal_copconignore(temp_dir, copconignore_file):
    # Initialize FileFilter without user-specified ignore file
    file_filter = FileFilter(
        additional_dirs=None,
        additional_files=None,
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
        additional_dirs=["additional_dir"],
        additional_files=["additional_file.txt"],
        user_ignore_path=additional_ignore_file
    )
    
    # Define paths to test
    included_dir = temp_dir / "included_dir"
    additional_excluded_dir = temp_dir / "build"
    included_file = temp_dir / "included_file.py"
    additional_excluded_file = temp_dir / "secret.txt"
    
    # Create directories and files
    included_dir.mkdir()
    additional_excluded_dir.mkdir()
    included_file.touch()
    additional_excluded_file.touch()
    
    # Assertions
    assert not file_filter.should_ignore(included_dir), "Included directory should not be ignored."
    assert file_filter.should_ignore(additional_excluded_dir), "Additional excluded directory should be ignored."
    assert not file_filter.should_ignore(included_file), "Included file should not be ignored."
    assert file_filter.should_ignore(additional_excluded_file), "Additional excluded file should be ignored."

def test_file_filter_with_combined_ignores(temp_dir, copconignore_file, additional_ignore_file):
    # Initialize FileFilter with both internal and user-specified ignore patterns
    file_filter = FileFilter(
        additional_dirs=["build"],
        additional_files=["secret.txt"],
        user_ignore_path=copconignore_file  # User-specified .copconignore
    )
    
    # Define paths to test
    included_dir = temp_dir / "included_dir"
    excluded_dir = temp_dir / "__pycache__"
    additional_excluded_dir = temp_dir / "build"
    included_file = temp_dir / "included_file.py"
    excluded_file = temp_dir / "poetry.lock"
    additional_excluded_file = temp_dir / "secret.txt"
    
    # Create directories and files
    included_dir.mkdir()
    excluded_dir.mkdir()
    additional_excluded_dir.mkdir()
    included_file.touch()
    excluded_file.touch()
    additional_excluded_file.touch()
    
    # Assertions
    assert not file_filter.should_ignore(included_dir), "Included directory should not be ignored."
    assert file_filter.should_ignore(excluded_dir), "Internal excluded directory should be ignored."
    assert file_filter.should_ignore(additional_excluded_dir), "Additional excluded directory should be ignored."
    assert not file_filter.should_ignore(included_file), "Included file should not be ignored."
    assert file_filter.should_ignore(excluded_file), "Internal excluded file should be ignored."
    assert file_filter.should_ignore(additional_excluded_file), "Additional excluded file should be ignored."

def test_file_filter_invalid_copconignore_no_exception(temp_dir):
    # Create an invalid .copconignore file
    invalid_ignore_path = temp_dir / ".copconignore"
    invalid_ignore_path.write_text("**/invalid[")
    
    # Initialize FileFilter
    try:
        file_filter = FileFilter(
            additional_dirs=None,
            additional_files=None,
            user_ignore_path=invalid_ignore_path
        )
    except FileReadError:
        pytest.fail("FileReadError was raised for an invalid .copconignore pattern, but it should have been treated as a literal.")
    
    # Verify that the invalid pattern is present in the spec
    # Not directly possible, but ensure that no files are unexpectedly ignored
    # Create a file that matches the invalid pattern treated literally
    invalid_matched_file = temp_dir / "invalid[.txt"
    invalid_matched_file.touch()
    
    # The file should be ignored as per the literal pattern "**/invalid[" matches "invalid[" at the end
    # However, "invalid[.txt" does not exactly match "**/invalid[", so it should not be ignored
    assert not file_filter.should_ignore(invalid_matched_file), "Invalid pattern should be treated as a literal and not ignore files."
