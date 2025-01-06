# Copcon 🐎

<div style="display: flex; gap: 10px;">
  <a href="https://github.com/kasperjunge/copcon/actions">
    <img src="https://github.com/kasperjunge/copcon/actions/workflows/publish-pypi.yml/badge.svg" alt="Build">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
  <a href="https://pypi.org/project/copcon/">
    <img src="https://img.shields.io/pypi/v/copcon.svg" alt="PyPI Version">
  </a>
</div>


Copcon is a CLI tool that effortlessly copies your project's directory structure and file contents directly to the clipboard, ideal for working with AI chatbots.


[Read the docs here](https://kasperjunge.github.io/copcon/)

## Overview

Copcon (Copy Context) is a CLI tool designed to generate a comprehensive report of a project's directory structure and file contents. This report can be used to provide context to large language models (LLMs) like ChatGPT, facilitating more informed and accurate responses based on your codebase.

#### Features

- **Directory Tree Generation**: Creates a visual representation of your project's directory structure.
- **File Content Capture**: Includes the contents of files, with options to handle binary files appropriately.
- **Customizable Traversal Depth**: Specify how deep the directory traversal should go.
- **Exclusion Options**: Exclude hidden files/directories and specify additional patterns to ignore.
- **Clipboard Integration**: Optionally copy the generated report directly to the clipboard.
- **File Output**: Save the report to a specified file instead of copying to the clipboard.

## Installation

```bash
pip install copcon

```

## Usage

After installation, use the `copcon` command to generate a report of your project.

### Basic Command

Generate a report and copy it to the clipboard:

```bash
copcon /path/to/your/project
```

### Options

- `--depth INTEGER`: Specify the depth of directory traversal (`-1` for unlimited). Default is `-1`.
- `--exclude-hidden / --no-exclude-hidden`: Toggle exclusion of hidden files and directories. Default is `--exclude-hidden`.
- `--ignore-dirs TEXT`: Additional directories to ignore. Can be used multiple times.
- `--ignore-files TEXT`: Additional files to ignore. Can be used multiple times.
- `--copconignore PATH`: Path to a custom `.copconignore` file.
- `--output-file PATH`: Specify an output file path to save the report instead of copying to the clipboard.

### Example Commands

#### Generate a Report with Default Settings (most commonly used)

```bash
copcon /path/to/your/project
```

#### Generate a Report with Custom Depth and Exclusions

```bash
copcon /path/to/your/project --depth 2 --ignore-dirs tests --ignore-files *.md
```

#### Output the Report to a File

```bash
copcon /path/to/your/project --output-file report.txt
```

## .copconignore Configuration

Copcon supports a `.copconignore` file to specify patterns for files and directories to exclude from the report. This file should be placed in the root of your project directory.

### Syntax

The `.copconignore` follows the [gitignore](https://git-scm.com/docs/gitignore) syntax, allowing for flexible pattern matching.

### Example `.copconignore`:

```
# Ignore all log files
*.log

# Ignore the temp directory and all its contents
temp/

# Ignore all .tmp files in any directory
**/*.tmp
```

## Report Format

Copcon generates a report structured into two main sections:

1. **Directory Structure**: A tree-like representation of your project's directories and files.
2. **File Contents**: The contents of each file, with binary files indicated appropriately.

### Example Report:

```
Directory Structure:
your_project_name
├── folder1
│   ├── file1.py
│   └── file2.py
├── folder2
│   └── file3.py
└── main.py

File Contents:

File: folder1/file1.py
----------------------------------------
[Content of file1.py]
----------------------------------------

File: folder1/file2.py
----------------------------------------
[Content of file2.py]
----------------------------------------

File: folder2/file3.py
----------------------------------------
[Content of file3.py]
----------------------------------------

File: main.py
----------------------------------------
[Content of main.py]
----------------------------------------
```

## Platform Support

Copcon is compatible with the following operating systems:

- **macOS**
- **Windows**
- **Linux** (requires `xclip` or a similar package)

### Linux Clipboard Support

To enable clipboard functionality on Linux, install `xclip`:

```bash
sudo apt install xclip
```

## Development

### Setting Up the Development Environment

1. Ensure you have Python 3.11+ and uv installed.
2. Clone the repository:

    ```bash
    git clone https://github.com/kasperjunge/copcon.git
    cd copcon
    ```

3. Install dependencies:

    ```bash
    uv sync
    ```

4. Run tests:

    ```bash
    uv run pytest
    ```


## Contributing

Contributions are welcome. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:

    ```bash
    git checkout -b feature/your-feature-name
    ```

3. Commit your changes with clear messages.
4. Push to your fork and submit a Pull Request.

### Guidelines

- Adhere to PEP 8 coding standards.
- Include tests for new features or bug fixes.
- Update documentation as necessary.

## License

This project is licensed under the [MIT License](LICENSE).

## Changelog

All notable changes to this project are documented in the [CHANGELOG](CHANGELOG.md).
