import pytest
from pathlib import Path
import tempfile

@pytest.fixture
def temp_dir():
    """
    Creates a temporary directory for testing and cleans up after the test.
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)

@pytest.fixture
def copconignore_file(temp_dir):
    """
    Creates a .copconignore file within the temporary directory with predefined patterns.
    """
    ignore_content = """
    # Ignore all log files
    *.log

    # Ignore the temp directory and all its contents
    temp/

    # Ignore all .tmp files in any directory
    **/*.tmp
    """
    ignore_path = temp_dir / ".copconignore"
    ignore_path.write_text(ignore_content.strip())
    return ignore_path

@pytest.fixture
def additional_ignore_file(temp_dir):
    """
    Creates an additional ignore file for testing custom ignore patterns.
    """
    ignore_content = """
    # Additional ignore patterns
    secret.txt
    build/
    """
    ignore_path = temp_dir / "custom_ignore"
    ignore_path.write_text(ignore_content.strip())
    return ignore_path
