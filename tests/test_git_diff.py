import subprocess
from pathlib import Path
import pytest
from typer.testing import CliRunner
from copcon.cli import app

runner = CliRunner()

def fake_git_diff_success(*args, **kwargs):
    """
    Simulate a successful 'git diff HEAD' command.
    Returns a CompletedProcess with fake stdout.
    """
    from subprocess import CompletedProcess
    return CompletedProcess(args, 0, stdout="fake diff output", stderr="")

def fake_git_diff_failure(*args, **kwargs):
    """
    Simulate a failure in the 'git diff HEAD' command.
    Raises a CalledProcessError.
    """
    raise subprocess.CalledProcessError(returncode=1, cmd=args[0], output="", stderr="error")

@pytest.fixture
def project_dir(tmp_path: Path) -> Path:
    """
    Creates a minimal project directory with a dummy file.
    """
    d = tmp_path / "project"
    d.mkdir()
    # Create a dummy file to ensure some file content exists
    (d / "dummy.txt").write_text("Dummy content")
    return d

def test_cli_git_diff_success(project_dir: Path, monkeypatch):
    """
    Test that when the --git-diff flag is enabled and git diff runs successfully,
    the report includes the git diff output and the success message contains the git diff token row.
    """
    monkeypatch.setattr(subprocess, "run", fake_git_diff_success)
    output_file = project_dir / "report.txt"
    result = runner.invoke(app, [str(project_dir), "--output-file", str(output_file), "--git-diff"])
    assert result.exit_code == 0, f"CLI exited with error: {result.output}"

    report_content = output_file.read_text(encoding="utf-8")
    # Check that the report includes the Git Diff section and the fake output
    assert "Git Diff:" in report_content
    assert "fake diff output" in report_content

    # Also check that the success message (printed to console) contains a row for "git diff"
    # (Note: This string check is case-insensitive.)
    assert "git diff" in result.output.lower()

def test_cli_git_diff_failure(project_dir: Path, monkeypatch):
    """
    Test that when the git diff command fails, the report includes an appropriate error note.
    """
    monkeypatch.setattr(subprocess, "run", fake_git_diff_failure)
    output_file = project_dir / "report.txt"
    result = runner.invoke(app, [str(project_dir), "--output-file", str(output_file), "--git-diff"])
    assert result.exit_code == 0, f"CLI exited with error: {result.output}"

    report_content = output_file.read_text(encoding="utf-8")
    # The report should include the Git Diff section and a note indicating failure.
    assert "Git Diff:" in report_content
    assert "[Git diff could not be generated:" in report_content

    # Also, check that the success message includes a row for "git diff"
    assert "git diff" in result.output.lower()
