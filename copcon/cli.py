"""Command-Line Interface for Copcon.

This module defines the CLI commands and options using Typer for the Copcon application.
"""

import typer
from pathlib import Path

import tiktoken

from copcon.core.file_tree import FileTreeGenerator
from copcon.core.file_filter import FileFilter
from copcon.core.file_reader import FileContentReader
from copcon.core.report import ReportFormatter
from copcon.core.clipboard import ClipboardManager
from copcon.messages import get_success_message
from copcon.exceptions import ClipboardError, FileReadError
from copcon.utils.logger import logger

app = typer.Typer()

@app.command()
def main(
    directory: Path = typer.Argument(...),
    depth: int = typer.Option(-1),
    exclude_hidden: bool = typer.Option(True),
    ignore_dirs: list[str] = typer.Option(None),
    ignore_files: list[str] = typer.Option(None),
    copconignore: Path = typer.Option(None),
    output_file: Path = typer.Option(None),
):
    try:
        # (Validation, creation of FileFilter, etc. remain the same)
        file_filter = FileFilter(
            additional_dirs=ignore_dirs,
            additional_files=ignore_files,
            user_ignore_path=copconignore
        )

        # 1) Generate directory tree
        tree_generator = FileTreeGenerator(directory, depth, file_filter)
        directory_tree = tree_generator.generate()

        # 2) Read file contents
        reader = FileContentReader(directory, file_filter, exclude_hidden)
        file_contents = reader.read_all()

        # 3) Format textual report
        formatter = ReportFormatter(directory.name, directory_tree, file_contents)
        report = formatter.format()

        # 4) Count tokens and build extension token distribution
        total_tokens = 0
        extension_token_map = {}

        encoder = tiktoken.get_encoding("cl100k_base")
        for rel_path, content in file_contents.items():
            tokens_for_file = len(encoder.encode(content))
            total_tokens += tokens_for_file

            file_name = Path(rel_path).name
            if "." in file_name:
                idx = file_name.index(".")
                extension = file_name[idx:]
            else:
                extension = "(no extension)"

            extension_token_map[extension] = extension_token_map.get(extension, 0) + tokens_for_file

        # 5) Write the textual report or copy it
        if output_file:
            formatter.write_to_file(report, output_file)
        else:
            ClipboardManager().copy(report)

        # 6) Show success message
        success_msg = get_success_message(
            directory_count=tree_generator.directory_count,
            file_count=tree_generator.file_count,
            total_tokens=total_tokens,
            extension_token_map=extension_token_map,
            output_file=str(output_file) if output_file else None,
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
