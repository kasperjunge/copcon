# from typer.testing import CliRunner
# from copcon.cli import app
# from unittest.mock import patch
# from copcon.core.clipboard import ClipboardManager

# runner = CliRunner()

# def test_cli_success_copy_to_clipboard(temp_dir, copconignore_file):
#     # Create files
#     (temp_dir / "file1.py").write_text("print('Hello')")
#     (temp_dir / "file2.log").write_text("This is a log file.")  # Should be ignored

#     # Expected counts
#     expected_directories = 1  # temp_dir
#     expected_files = 1        # file1.py
#     expected_chars = len("print('Hello')")

#     # Mock ClipboardManager.copy
#     with patch.object(ClipboardManager, 'copy') as mock_copy:
#         result = runner.invoke(app, [str(temp_dir)])
#         assert result.exit_code == 0
#         mock_copy.assert_called_once()

# def test_cli_success_write_to_file(temp_dir, copconignore_file):
#     # Create files
#     (temp_dir / "file1.py").write_text("print('Hello')")
#     (temp_dir / "file2.log").write_text("This is a log file.")  # Should be ignored

#     # Expected counts
#     expected_directories = 1  # temp_dir
#     expected_files = 1        # file1.py
#     expected_chars = len("print('Hello')")

#     output_file = temp_dir / "output.txt"

#     result = runner.invoke(app, [str(temp_dir), "--output-file", str(output_file)])
#     assert result.exit_code == 0
#     assert output_file.exists(), "Output file should be created."

#     # Verify file content
#     content = output_file.read_text()
#     assert "file1.py" in content, "file1.py should be in the report."
#     assert "file2.log" not in content, "file2.log should be ignored in the report."

# def test_cli_with_custom_copconignore(temp_dir, copconignore_file, additional_ignore_file):
#     # Create files
#     (temp_dir / "file1.py").write_text("print('Hello')")
#     (temp_dir / "secret.txt").write_text("This is a secret.")  # Should be ignored by additional_ignore_file
#     (temp_dir / "build").mkdir()
#     (temp_dir / "build" / "build_file.py").write_text("print('Build')")

#     # Expected counts
#     expected_directories = 1  # temp_dir
#     expected_files = 1        # file1.py
#     expected_chars = len("print('Hello')")

#     # Initialize with custom .copconignore
#     result = runner.invoke(app, [
#         str(temp_dir),
#         "--copconignore", str(additional_ignore_file)
#     ])
#     assert result.exit_code == 0

# def test_cli_invalid_directory():
#     # Provide a non-existent directory
#     result = runner.invoke(app, ["/non/existent/directory"])
#     assert result.exit_code != 0


# def test_cli_help():
#     result = runner.invoke(app, ["--help"])
#     assert result.exit_code == 0
#     assert "Usage:" in result.output
#     assert "--depth" in result.output
#     assert "--exclude-hidden" in result.output
#     assert "--ignore-dirs" in result.output
#     assert "--ignore-files" in result.output
#     assert "--copconignore" in result.output
#     assert "--output-file" in result.output

# def test_cli_no_files_to_process(temp_dir, copconignore_file):
#     # Initialize FileFilter to ignore all files
#     (temp_dir / "file1.py").write_text("print('Hello')")

#     # Create a .copconignore that ignores all files
#     copconignore_path = temp_dir / ".copconignore"
#     copconignore_path.write_text("*.py")

#     # Initialize FileContentReader
#     result = runner.invoke(app, [str(temp_dir)])
#     assert result.exit_code == 0
#     assert "file1.py" not in result.output, "file1.py should be ignored in the report."
