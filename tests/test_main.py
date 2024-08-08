import pytest
from typer.testing import CliRunner
from pathlib import Path
import shutil
from copcon.main import app, generate_tree, get_file_content, parse_copconignore, should_ignore

runner = CliRunner()

@pytest.fixture
def temp_dir(tmp_path):
    # Create a temporary directory structure
    (tmp_path / "file1.txt").touch()
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "file2.txt").touch()
    (tmp_path / "subdir" / "file3.log").touch()
    (tmp_path / "temp").mkdir()
    (tmp_path / "temp" / "temp_file.tmp").touch()
    yield tmp_path
    # Clean up after the test
    shutil.rmtree(tmp_path)

@pytest.fixture
def copconignore_file(temp_dir):
    ignore_file = temp_dir / ".copconignore"
    ignore_file.write_text("*.log\ntemp/\n**/*.tmp")
    return ignore_file

def test_generate_tree(temp_dir):
    # Test the generate_tree function
    tree = generate_tree(temp_dir)
    print("Generated tree:")
    print(tree)
    
    tree_lines = set(tree.strip().split("\n"))

    # Check for the presence of expected elements
    assert any("file1.txt" in line for line in tree_lines), "file1.txt not found in tree"
    assert any("subdir" in line for line in tree_lines), "subdir not found in tree"
    assert any("file2.txt" in line for line in tree_lines), "file2.txt not found in tree"
    assert any("file3.log" in line for line in tree_lines), "file3.log not found in tree"
    assert any("temp" in line for line in tree_lines), "temp not found in tree"
    assert any("temp_file.tmp" in line for line in tree_lines), "temp_file.tmp not found in tree"

    # Check the total number of lines
    assert len(tree_lines) == 6, f"Expected 6 lines, got {len(tree_lines)}"

    # Check the structure
    assert "├── subdir" in tree_lines, "Expected '├── subdir' in tree"
    assert "│   ├── file2.txt" in tree_lines, "Expected '│   ├── file2.txt' in tree"
    assert "│   └── file3.log" in tree_lines, "Expected '│   └── file3.log' in tree"
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

def test_should_ignore():
    patterns = ["*.log", "temp/", "**/*.tmp"]
    assert should_ignore(Path("file.log"), patterns) == True, "should ignore .log files"
    assert should_ignore(Path("temp"), patterns) == True, "should ignore 'temp' directory"
    assert should_ignore(Path("temp/"), patterns) == True, "should ignore 'temp/' directory"
    assert should_ignore(Path("subdir/file.tmp"), patterns) == True, "should ignore .tmp files in subdirectories"
    assert should_ignore(Path("file.txt"), patterns) == False, "should not ignore .txt files"
    assert should_ignore(Path("subdir/file.txt"), patterns) == False, "should not ignore .txt files in subdirectories"


def test_parse_copconignore(copconignore_file):
    patterns = parse_copconignore(copconignore_file)
    assert patterns == ["*.log", "temp/", "**/*.tmp"]

def test_parse_copconignore_non_existent_file(tmp_path):
    non_existent_file = tmp_path / "non_existent_file"
    patterns = parse_copconignore(non_existent_file)
    assert patterns == [], "Expected empty list for non-existent file"

def test_generate_tree_with_ignore_patterns(temp_dir, copconignore_file):
    ignore_patterns = parse_copconignore(copconignore_file)
    tree = generate_tree(temp_dir, ignore_patterns=ignore_patterns)
    tree_lines = tree.strip().split("\n")

    assert any("file1.txt" in line for line in tree_lines), "file1.txt should be in the tree"
    assert any("subdir" in line for line in tree_lines), "subdir should be in the tree"
    assert any("file2.txt" in line for line in tree_lines), "file2.txt should be in the tree"
    assert not any("file3.log" in line for line in tree_lines), "file3.log should not be in the tree"
    assert not any("temp" in line for line in tree_lines), "temp directory should not be in the tree"
    assert not any("temp_file.tmp" in line for line in tree_lines), "temp_file.tmp should not be in the tree"

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

def test_main_command_with_copconignore(temp_dir, copconignore_file, monkeypatch):
    # Mock the copy_to_clipboard function
    mock_called = False
    def mock_copy_to_clipboard(text):
        nonlocal mock_called
        mock_called = True
        print(f"Clipboard content:\n{text}")  # Add this line for debugging
        assert "file1.txt" in text, "file1.txt should be in the clipboard content"
        assert "file2.txt" in text, "file2.txt should be in the clipboard content"
        assert "file3.log" not in text, "file3.log should not be in the clipboard content"
        assert "temp" not in text, "temp directory should not be in the clipboard content"
        assert "temp_file.tmp" not in text, "temp_file.tmp should not be in the clipboard content"

    monkeypatch.setattr("copcon.main.copy_to_clipboard", mock_copy_to_clipboard)

    # Run the CLI command
    result = runner.invoke(app, [str(temp_dir)])
    print(f"Command output:\n{result.output}")  # Add this line for debugging
    assert result.exit_code == 0, f"Command failed with error: {result.output}"
    assert "Directory structure and file contents have been copied to clipboard." in result.stdout

    # Check if copy_to_clipboard was called with the expected content
    assert mock_called, "copy_to_clipboard was not called"

def test_main_command_with_custom_copconignore(temp_dir, monkeypatch):
    # Create a custom .copconignore file
    custom_ignore_file = temp_dir / "custom_ignore"
    custom_ignore_file.write_text("*.txt")

    # Mock the copy_to_clipboard function
    mock_called = False
    def mock_copy_to_clipboard(text):
        nonlocal mock_called
        mock_called = True
        assert "file1.txt" not in text
        assert "file2.txt" not in text
        assert "file3.log" in text
        assert "temp" in text
        assert "temp_file.tmp" in text

    monkeypatch.setattr("copcon.main.copy_to_clipboard", mock_copy_to_clipboard)

    # Run the CLI command with custom .copconignore file
    result = runner.invoke(app, [str(temp_dir), "--copconignore", str(custom_ignore_file)])
    assert result.exit_code == 0
    assert "Directory structure and file contents have been copied to clipboard." in result.stdout

    # Check if copy_to_clipboard was called with the expected content
    assert mock_called, "copy_to_clipboard was not called"
