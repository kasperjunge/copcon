import typer
from pathlib import Path
from typing import Optional, List
import subprocess
import mimetypes

app = typer.Typer()

# Default directories to ignore
DEFAULT_IGNORE_DIRS = {
    "__pycache__",
    ".venv",
    "node_modules",
    ".git",
    ".idea",
    ".vscode",
    "build",
    "dist",
    "target",
}

# Default files to ignore
DEFAULT_IGNORE_FILES = {
    "poetry.lock",
    "package-lock.json",
    "Cargo.lock",
    ".DS_Store",
    "yarn.lock",
}


def generate_tree(
    directory: Path,
    prefix: str = "",
    depth: int = -1,
    ignore_dirs: set = DEFAULT_IGNORE_DIRS,
    ignore_files: set = DEFAULT_IGNORE_FILES,
) -> str:
    if depth == 0:
        return ""

    output = []
    contents = list(directory.iterdir())
    contents.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

    for i, path in enumerate(contents):
        if path.is_dir() and path.name in ignore_dirs:
            continue
        if path.is_file() and path.name in ignore_files:
            continue

        is_last = i == len(contents) - 1
        current_prefix = "└── " if is_last else "├── "
        output.append(f"{prefix}{current_prefix}{path.name}")

        if path.is_dir():
            extension = "    " if is_last else "│   "
            output.append(
                generate_tree(
                    path,
                    prefix + extension,
                    depth - 1 if depth > 0 else -1,
                    ignore_dirs,
                    ignore_files,
                )
            )

    return "\n".join(output)


def get_file_content(file_path: Path) -> str:
    try:
        mime_type, _ = mimetypes.guess_type(str(file_path))

        # Check if the file is a text file
        if mime_type and (
            mime_type.startswith("text/")
            or mime_type in ["application/json", "application/xml"]
        ):
            return file_path.read_text()
        else:
            # For binary files, return file information instead of content
            file_size = file_path.stat().st_size
            return f"[Binary file]\nType: {mime_type or 'Unknown'}\nSize: {file_size} bytes"
    except Exception as e:
        return f"Error reading file: {file_path}\nError: {str(e)}\n"


def copy_to_clipboard(text: str):
    process = subprocess.Popen(
        "pbcopy", env={"LANG": "en_US.UTF-8"}, stdin=subprocess.PIPE
    )
    process.communicate(text.encode("utf-8"))


@app.command()
def main(
    directory: Path = typer.Argument(..., help="The directory to process"),
    depth: Optional[int] = typer.Option(
        -1, help="Depth of directory tree to display (-1 for unlimited)"
    ),
    exclude_hidden: bool = typer.Option(
        True, help="Exclude hidden files and directories"
    ),
    ignore_dirs: Optional[List[str]] = typer.Option(
        None, help="Additional directories to ignore"
    ),
    ignore_files: Optional[List[str]] = typer.Option(
        None, help="Additional files to ignore"
    ),
):
    """
    Generate a report of directory structure and file contents, then copy it to clipboard.
    """
    if not directory.is_dir():
        typer.echo(f"Error: {directory} is not a valid directory.", err=True)
        raise typer.Exit(code=1)

    dirs_to_ignore = DEFAULT_IGNORE_DIRS.copy()
    if ignore_dirs:
        dirs_to_ignore.update(ignore_dirs)

    files_to_ignore = DEFAULT_IGNORE_FILES.copy()
    if ignore_files:
        files_to_ignore.update(ignore_files)

    output = []
    output.append("Directory Structure:")
    output.append(directory.name)
    output.append(
        generate_tree(
            directory,
            depth=depth,
            ignore_dirs=dirs_to_ignore,
            ignore_files=files_to_ignore,
        )
    )
    output.append("\nFile Contents:")

    for file_path in directory.rglob("*"):
        if file_path.is_file():
            if exclude_hidden and (
                file_path.name.startswith(".")
                or any(part.startswith(".") for part in file_path.parts)
            ):
                continue
            if any(ignore_dir in file_path.parts for ignore_dir in dirs_to_ignore):
                continue
            if file_path.name in files_to_ignore:
                continue
            relative_path = file_path.relative_to(directory)
            output.append(f"\nFile: {relative_path}")
            output.append("-" * 40)
            output.append(get_file_content(file_path))
            output.append("-" * 40)

    full_output = "\n".join(output)
    copy_to_clipboard(full_output)

    typer.echo("Directory structure and file contents have been copied to clipboard.")


if __name__ == "__main__":
    app()
