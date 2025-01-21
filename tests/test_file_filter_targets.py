import pytest
from pathlib import Path
from copcon.core.file_filter import FileFilter
from copcon.exceptions import FileReadError

@pytest.fixture
def non_empty_copcontarget_file(tmp_path):
    target_file = tmp_path / ".copcontarget"
    target_file.write_text("*.py\n")
    return target_file

@pytest.fixture
def empty_copcontarget_file(tmp_path):
    target_file = tmp_path / ".copcontarget"
    target_file.write_text("")
    return target_file

def test_file_filter_with_non_empty_copcontarget(non_empty_copcontarget_file, tmp_path):
    # Create a FileFilter with a non-empty .copcontarget
    file_filter = FileFilter(user_target_path=non_empty_copcontarget_file)
    
    # target_spec should be set because the file is non-empty
    assert file_filter.target_spec is not None

    # Create a Python file that should match the target pattern
    py_file = tmp_path / "test.py"
    py_file.write_text("print('hello')")
    # Since *.py is allowed by the target, this file should not be ignored
    assert not file_filter.should_ignore(py_file)

    # Create a non-Python file that should not match the target pattern
    txt_file = tmp_path / "readme.txt"
    txt_file.write_text("content")
    # Since *.txt does not match the *.py target, this file should be ignored
    assert file_filter.should_ignore(txt_file)

def test_file_filter_with_empty_copcontarget(empty_copcontarget_file):
    # Create a FileFilter with an empty .copcontarget
    file_filter = FileFilter(user_target_path=empty_copcontarget_file)

    # target_spec should be None because the .copcontarget file was empty
    assert file_filter.target_spec is None
