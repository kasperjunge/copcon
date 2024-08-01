# Copcon

Copcon (Copy Context) is a CLI tool that generates a report of a directory's structure and file contents, then copies it to the clipboard.

## Note

This tool is designed for macOS only, as it uses the `pbcopy` command for clipboard operations.

## Installation

To install Copcon, make sure you have Python 3.7+ and Poetry installed. Then, clone this repository and run:

```
poetry install
```

## Usage

After installation, you can use the `copcon` command:

```
copcon /path/to/your/directory
```

Options:

- `--depth INTEGER`: Depth of directory tree to display (-1 for unlimited)
- `--exclude-hidden / --no-exclude-hidden`: Exclude hidden files and directories (default: True)
- `--ignore-dirs TEXT`: Additional directories to ignore (can be used multiple times)

For help, use:

```
copcon --help
```

By default, Copcon ignores the following directories:
`__pycache__`, `.venv`, `node_modules`, `.git`, `.idea`, `.vscode`, `build`, `dist`, `target`

You can add more directories to ignore using the `--ignore-dirs` option:

```
copcon /path/to/your/directory --ignore-dirs my_ignore_dir --ignore-dirs another_ignore_dir
```

## Development

To run tests:

```
poetry run pytest
```

## License

[MIT License](LICENSE)
# copcon
