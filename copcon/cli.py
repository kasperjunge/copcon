import typer
from pathlib import Path
import subprocess
import tiktoken

from copcon.core.file_tree import FileTreeGenerator
from copcon.core.file_filter import FileFilter
from copcon.core.file_reader import FileContentReader
from copcon.core.report import ReportFormatter
from copcon.core.clipboard import ClipboardManager
from copcon.core.autodiscover import discover_copconignore, discover_copcontarget
from copcon.messages import get_success_message
from copcon.exceptions import ClipboardError, FileReadError
from copcon.utils.logger import logger

app = typer.Typer()

@app.command(no_args_is_help=True)
def main(
    directory: Path = typer.Argument(...),
    depth: int = typer.Option(-1),
    exclude_hidden: bool = typer.Option(True),
    copconignore: Path = typer.Option(None),
    output_file: Path = typer.Option(None),
    git_diff: bool = typer.Option(False, "-g", "--git-diff", help="Include git diff in the context report")
):
    """
    Copcon CLI entry point.

    Behavior:
      - If --copconignore is passed, we use that path directly.
      - Otherwise, we try discover_copconignore(directory) to see if there's a .copconignore.
      - If none is found, we only apply internal .copconignore patterns.
      - Additionally, if a .copcontarget is discovered, it's applied before .copconignore.
      - If the --git-diff flag is provided, the output of 'git diff HEAD' will be appended
        to the context report and its token count added to the token spend report.
    """

    # Keep track of the actual .copconignore path we end up using
    used_copconignore_path: Path | None = None

    # (1) If user did not specify --copconignore, attempt auto-discovery
    if copconignore is None:
        discovered = discover_copconignore(directory)
        if discovered:
            copconignore = discovered  # use the discovered path

    # Discover .copcontarget
    discovered_target = discover_copcontarget(directory)

    # Assign final used path
    used_copconignore_path = copconignore

    try:
        # Build a FileFilter with target support
        file_filter = FileFilter(
            user_ignore_path=copconignore,
            user_target_path=discovered_target
        )

        # Generate directory tree
        tree_generator = FileTreeGenerator(directory, depth, file_filter)
        directory_tree = tree_generator.generate()

        # Read file contents
        reader = FileContentReader(directory, file_filter, exclude_hidden)
        file_contents = reader.read_all()

        # Format the textual report from file structure and contents
        formatter = ReportFormatter(directory.name, directory_tree, file_contents)
        report = formatter.format()

        # If git_diff flag is enabled, run git diff and append its output
        git_diff_output = ""
        if git_diff:
            try:
                result = subprocess.run(
                    ["git", "diff", "HEAD"],
                    cwd=directory,
                    capture_output=True,
                    text=True,
                    check=True
                )
                git_diff_output = result.stdout.strip()
            except Exception as e:
                git_diff_output = f"[Git diff could not be generated: {e}]"
            report += "\n\nGit Diff:\n" + git_diff_output

        # Count tokens & build extension token distribution
        total_tokens = 0
        extension_token_map = {}
        encoder = tiktoken.get_encoding("cl100k_base")

        for rel_path, content in file_contents.items():
            tokens_for_file = len(encoder.encode(content))
            total_tokens += tokens_for_file

            file_name = Path(rel_path).name
            if "." in file_name:
                idx = file_name.rindex(".")
                extension = f"*{file_name[idx:]}"  # use wildcard to indicate all such files
            else:
                extension = "(no extension)"

            extension_token_map[extension] = extension_token_map.get(extension, 0) + tokens_for_file

        # If git diff output is present, count its tokens and add to the token map
        if git_diff:
            tokens_for_git_diff = len(encoder.encode(git_diff_output))
            total_tokens += tokens_for_git_diff
            extension_token_map["git diff"] = tokens_for_git_diff

        # Write or copy the textual report
        if output_file:
            formatter.write_to_file(report, output_file)
        else:
            ClipboardManager().copy(report)

        # Display success message with updated token spend report
        success_msg = get_success_message(
            directory_count=tree_generator.directory_count,
            file_count=tree_generator.file_count,
            total_tokens=total_tokens,
            extension_token_map=extension_token_map,
            output_file=str(output_file) if output_file else None,
            copconignore_path=str(used_copconignore_path) if used_copconignore_path else None,
            copcontarget_path=str(discovered_target) if discovered_target else None,
        )
        typer.echo(success_msg)

    except FileReadError as fre:
        logger.error(f"File read error: {fre}")
        raise typer.Exit(code=1)
    except ClipboardError as ce:
        logger.error(f"Clipboard error: {ce}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.exception("An unexpected error occurred.")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

