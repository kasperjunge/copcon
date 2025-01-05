"""Command-Line Interface for Copcon.

This module defines the CLI commands and options using Typer for the Copcon application.
"""

import typer
from pathlib import Path
from copcon.core.file_tree import FileTreeGenerator
from copcon.core.file_filter import FileFilter
from copcon.core.file_reader import FileContentReader
from copcon.core.report import ReportFormatter
from copcon.core.clipboard import ClipboardManager
from copcon.exceptions import ClipboardError, FileReadError
from copcon.utils.logger import logger

app = typer.Typer()


@app.command()
def main(
    directory: Path = typer.Argument(..., help="The directory to process"),
    depth: int = typer.Option(-1, help="Depth of directory tree to display (-1 for unlimited)"),
    exclude_hidden: bool = typer.Option(True, help="Exclude hidden files and directories"),
    ignore_dirs: list[str] = typer.Option(None, help="Additional directories to ignore"),
    ignore_files: list[str] = typer.Option(None, help="Additional files to ignore"),
    copconignore: Path = typer.Option(None, help="Path to .copconignore file"),
    output_file: Path = typer.Option(None, help="Output file path (if not using clipboard)"),
):
    """Generate a report of directory structure and file contents, then copy it to clipboard.

    Args:
        directory (Path): The directory to process.
        depth (int): Depth of directory tree to display (-1 for unlimited).
        exclude_hidden (bool): Exclude hidden files and directories.
        ignore_dirs (List[str], optional): Additional directories to ignore.
        ignore_files (List[str], optional): Additional files to ignore.
        copconignore (Path, optional): Path to a custom .copconignore file.
        output_file (Path, optional): Output file path to save the report instead of copying to clipboard.
    """
    try:
        if not directory.exists() or not directory.is_dir():
            raise FileReadError(f"{directory} is not a valid directory.")

        # Determine the .copconignore path
        user_copconignore = None
        if copconignore:
            if copconignore.exists() and copconignore.is_file():
                user_copconignore = copconignore
                logger.debug(f"Using user-specified .copconignore at {user_copconignore}")
            else:
                logger.warning(f"Specified .copconignore file {copconignore} does not exist or is not a file.")
        else:
            # Look for .copconignore in the current working directory
            potential_ignore = Path.cwd() / ".copconignore"
            if potential_ignore.exists() and potential_ignore.is_file():
                user_copconignore = potential_ignore
                logger.debug(f"Found user-defined .copconignore at {user_copconignore}")

        # Initialize FileFilter with the determined .copconignore path
        file_filter = FileFilter(
            additional_dirs=ignore_dirs,
            additional_files=ignore_files,
            user_ignore_path=user_copconignore
        )

        # Generate directory tree
        tree_generator = FileTreeGenerator(directory, depth, file_filter)
        directory_tree = tree_generator.generate()

        # Read file contents
        reader = FileContentReader(directory, file_filter, exclude_hidden)
        file_contents = reader.read_all()

        # Format report
        formatter = ReportFormatter(directory.name, directory_tree, file_contents)
        report = formatter.format()

        # Calculate total characters
        total_chars = reader.total_chars
        # Get directory and file counts
        directory_count = tree_generator.directory_count
        file_count = tree_generator.file_count

        # Prepare formatted counts with commas for readability
        formatted_directory_count = f"{directory_count:,}"
        formatted_file_count = f"{file_count:,}"
        formatted_total_chars = f"{total_chars:,}"

        # Prepare success message components
        copconignore_info = ""
        if file_filter.has_user_defined_ignore():
            copconignore_info = "A user-defined `.copconignore` file was found and applied.\n"
        else:
            copconignore_info = "Consider creating a `.copconignore` file in your project root to customize exclusions.\n"

        # Output
        if output_file:
            formatter.write_to_file(report, output_file)
            typer.echo(
                f"🎉 Success! Copcon has processed:\n"
                f"📁 {formatted_directory_count} directories\n"
                f"📄 {formatted_file_count} files\n"
                f"📝 {formatted_total_chars} characters\n\n"
                # f"{copconignore_info}"
                f"The report has been written to `{output_file}`. You can now open or share it as needed. 🚀\n"
                "If you find Copcon useful, please consider leaving a star on: github.com/kasperjunge/copcon ⭐"
            )
        else:
            clipboard = ClipboardManager()
            clipboard.copy(report)
            typer.echo(
                f"🎉 Success! Copcon has processed:\n\n"
                f"📁 {formatted_directory_count} directories\n"
                f"📄 {formatted_file_count} files\n"
                f"📝 {formatted_total_chars} characters\n\n"
                # f"{copconignore_info}"
                f"The report has been copied to your clipboard. You can now paste it into your preferred AI assistant 🚀\n\n"
                "If you find Copcon useful, please consider leaving a star on: github.com/kasperjunge/copcon ⭐"
            )

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
