# Copcon

Copcon (Copy Context) is a CLI tool that generates a report of a directory's structure and file contents, then copies it to the clipboard. It's designed to quickly capture and share the context of a project or directory.

## Features

- Generate a directory tree structure
- Capture file contents
- Customizable depth for directory traversal
- Ability to exclude hidden files and directories
- Option to ignore specific directories and files
- Copies the generated report to the clipboard

## Installation

You can install Copcon directly from PyPI:

```
pip install copcon
```

Alternatively, if you want to install from source:

1. Clone the repository
2. Ensure you have Poetry installed
3. Run `poetry install` in the project directory

## Usage

After installation, you can use the `copcon` command:

```
copcon /path/to/your/directory
```

Options:

- `--depth INTEGER`: Depth of directory tree to display (-1 for unlimited)
- `--exclude-hidden / --no-exclude-hidden`: Exclude hidden files and directories (default: True)
- `--ignore-dirs TEXT`: Additional directories to ignore (can be used multiple times)
- `--ignore-files TEXT`: Additional files to ignore (can be used multiple times)

For help, use:

```
copcon --help
```

By default, Copcon ignores the following directories:
`__pycache__`, `.venv`, `node_modules`, `.git`, `.idea`, `.vscode`, `build`, `dist`, `target`

And the following files:
`poetry.lock`, `package-lock.json`, `Cargo.lock`, `.DS_Store`, `yarn.lock`

You can add more directories or files to ignore using the `--ignore-dirs` and `--ignore-files` options:

```
copcon /path/to/your/directory --ignore-dirs my_ignore_dir --ignore-files my_ignore_file.txt
```

## Note

This tool is designed for macOS only, as it uses the `pbcopy` command for clipboard operations.

## Development

To set up the development environment:

1. Ensure you have Python 3.11+ and Poetry installed
2. Clone the repository
3. Run `poetry install` to install dependencies

To run tests (once tests are implemented):

```
poetry run pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
