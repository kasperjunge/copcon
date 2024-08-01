import pytest
from typer.testing import CliRunner
from pathlib import Path
import shutil
from copcon.main import app, generate_tree, get_file_content

runner = CliRunner()


@pytest.fixture
def temp_dir(tmp_path):
    # Create a temporary directory structure
    (tmp_path / "file1.txt").touch()
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "file2.txt").touch()
    yield tmp_path
    # Clean up after the test
    shutil.rmtree(tmp_path)


def test_generate_tree(temp_dir):
    # Test the generate_tree function
    tree = generate_tree(temp_dir)
    tree_lines = set(tree.strip().split("\n"))

    # Check for the presence of expected elements
    assert any(
        "file1.txt" in line for line in tree_lines
    ), "file1.txt not found in tree"
    assert any("subdir" in line for line in tree_lines), "subdir not found in tree"
    assert any(
        "file2.txt" in line for line in tree_lines
    ), "file2.txt not found in tree"

    # Check the total number of lines
    assert len(tree_lines) == 3, f"Expected 3 lines, got {len(tree_lines)}"

    # Check the structure
    assert "├── subdir" in tree_lines, "Expected '├── subdir' in tree"
    assert "│   └── file2.txt" in tree_lines, "Expected '│   └── file2.txt' in tree"
    assert "└── file1.txt" in tree_lines, "Expected '└── file1.txt' in tree"


def test_get_file_content(temp_dir):
    # Test with a text file
    text_file = temp_dir / "text_file.txt"
    text_file.write_text("Hello, World!")
    assert get_file_content(text_file) == "Hello, World!"

    # Test with a binary file
    binary_file = temp_dir / "binary_file.bin"
    binary_file.write_bytes(b"\x00\x01\x02\x03")
    content = get_file_content(binary_file)
    assert "[Binary file]" in content
    assert "Size: 4 bytes" in content


def test_main_command(temp_dir, monkeypatch):
    # Mock the copy_to_clipboard function
    mock_called = False

    def mock_copy_to_clipboard(text):
        nonlocal mock_called
        mock_called = True

    monkeypatch.setattr("copcon.main.copy_to_clipboard", mock_copy_to_clipboard)

    # Run the CLI command
    result = runner.invoke(app, [str(temp_dir)])
    assert result.exit_code == 0
    assert (
        "Directory structure and file contents have been copied to clipboard."
        in result.stdout
    )

    # Check if copy_to_clipboard was called
    assert mock_called, "copy_to_clipboard was not called"
