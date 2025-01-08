import pytest
from pathlib import Path
from typer.testing import CliRunner

from copcon.cli import app

@pytest.fixture
def runner():
    return CliRunner()


def test_cli_autodiscover_local_copconignore(tmp_path: Path, runner: CliRunner):
    """
    Test that if the user does NOT pass --copconignore,
    Copcon automatically discovers .copconignore by walking up the directory tree.
    We confirm the final report (written to a file) includes or excludes certain files.
    """
    # Directory:
    #  tmp_path
    #   ├─ .copconignore   ( *.md )
    #   └─ subproject
    #       ├─ README.md   (should be ignored)
    #       └─ main.py     (should be included)
    #

    # 1) Create .copconignore in parent
    parent_ignore = tmp_path / ".copconignore"
    parent_ignore.write_text("*.md\n", encoding="utf-8")

    # 2) Create subdirectory + some files
    subproject = tmp_path / "subproject"
    subproject.mkdir()
    readme_file = subproject / "README.md"
    readme_file.write_text("Markdown file that should be ignored", encoding="utf-8")
    main_file = subproject / "main.py"
    main_file.write_text("print('I am included')", encoding="utf-8")

    # 3) We'll have Copcon write the report into a file instead of printing
    output_report = subproject / "report.txt"

    result = runner.invoke(
        app,
        [
            str(subproject),
            "--output-file",
            str(output_report),
        ],
    )
    assert result.exit_code == 0, f"CLI failed unexpectedly: {result.output}"

    # 4) Read the report file
    report_content = output_report.read_text(encoding="utf-8")

    # 5) The report should NOT contain "README.md" (ignored),
    #    but it should contain "main.py" (included).
    assert "README.md" not in report_content, "README.md should be ignored if .copconignore is discovered."
    assert "main.py" in report_content, "main.py should not be ignored."


def test_cli_no_autodiscover_if_option_is_provided(tmp_path: Path, runner: CliRunner):
    """
    If the user explicitly passes --copconignore, that should override auto-discovery.
    We'll confirm the final report includes or excludes the correct files.
    """
    # Directory structure:
    #  tmp_path
    #   ├─ .copconignore          (ignores *.md)
    #   ├─ explicit_ignore_file   (ignores *.py)
    #   └─ child
    #       ├─ file.md  (should be included in final report, because parent's ignore is overridden)
    #       └─ file.py  (should be ignored by explicit_ignore_file)
    #

    # 1) .copconignore in parent ignoring *.md
    parent_ignore = tmp_path / ".copconignore"
    parent_ignore.write_text("*.md\n", encoding="utf-8")

    # 2) explicit_ignore_file ignoring *.py
    explicit_ignore_file = tmp_path / "explicit_ignore_file"
    explicit_ignore_file.write_text("*.py\n", encoding="utf-8")

    # 3) child directory with .md and .py
    child = tmp_path / "child"
    child.mkdir()
    file_md = child / "file.md"
    file_md.write_text("some markdown", encoding="utf-8")
    file_py = child / "file.py"
    file_py.write_text("print('test')", encoding="utf-8")

    # 4) We pass --copconignore = explicit_ignore_file
    output_report = child / "report.txt"
    result = runner.invoke(
        app,
        [
            "--copconignore",
            str(explicit_ignore_file),
            str(child),
            "--output-file",
            str(output_report),
        ],
    )
    assert result.exit_code == 0, f"CLI failed unexpectedly: {result.output}"

    # 5) Check the final report
    report_content = output_report.read_text(encoding="utf-8")
    # Because we used explicit_ignore_file, *.py is ignored => "file.py" should not appear
    assert "file.py" not in report_content, "file.py should be ignored via the explicit .copconignore override"
    # Because parent's .copconignore is overridden, *.md is not ignored
    assert "file.md" in report_content, "file.md should not be ignored (parent's .copconignore is bypassed)"


def test_cli_no_copconignore_found(tmp_path: Path, runner: CliRunner):
    """
    If no --copconignore is provided and none is found,
    Copcon uses only internal patterns. We'll confirm a normal file is included.
    """
    # Directory:
    #   tmp_path
    #     └─ project
    #         └─ random_file.txt (should appear in the final report)
    #
    # No .copconignore => fallback to internal only.

    project = tmp_path / "project"
    project.mkdir()
    random_file = project / "random_file.txt"
    random_file.write_text("Hello, no ignore file here", encoding="utf-8")

    output_report = project / "report.txt"
    result = runner.invoke(
        app,
        [
            str(project),
            "--output-file",
            str(output_report),
        ],
    )
    assert result.exit_code == 0, f"CLI failed unexpectedly: {result.output}"

    report_content = output_report.read_text(encoding="utf-8")

    # Because there's no .copconignore discovered, "random_file.txt" is not ignored
    assert "random_file.txt" in report_content, "Should not be ignored since no .copconignore was found."
