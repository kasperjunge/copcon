from copcon.core.report import ReportFormatter

def test_report_formatter_basic():
    project_name = "test_project"
    directory_tree = "test_project\n└── dir1\n    └── file1.py"
    file_contents = {
        "dir1/file1.py": "print('Hello')"
    }
    
    formatter = ReportFormatter(project_name, directory_tree, file_contents)
    report = formatter.format()
    
    expected_report = "\n".join([
        "Directory Structure:",
        "test_project",
        "test_project",
        "└── dir1",
        "    └── file1.py",
        "\nFile Contents:",
        "\nFile: dir1/file1.py",
        "----------------------------------------",
        "print('Hello')",
        "----------------------------------------"
    ])
    
    assert report == expected_report, "Formatted report does not match expected output."

def test_report_formatter_multiple_files():
    project_name = "test_project"
    directory_tree = "test_project\n├── dir1\n│   ├── file1.py\n│   └── file2.py\n└── file3.py"
    file_contents = {
        "dir1/file1.py": "print('File 1')",
        "dir1/file2.py": "print('File 2')",
        "file3.py": "print('File 3')"
    }
    
    formatter = ReportFormatter(project_name, directory_tree, file_contents)
    report = formatter.format()
    
    expected_report = "\n".join([
        "Directory Structure:",
        "test_project",
        "test_project",
        "├── dir1",
        "│   ├── file1.py",
        "│   └── file2.py",
        "└── file3.py",
        "\nFile Contents:",
        "\nFile: dir1/file1.py",
        "----------------------------------------",
        "print('File 1')",
        "----------------------------------------",
        "\nFile: dir1/file2.py",
        "----------------------------------------",
        "print('File 2')",
        "----------------------------------------",
        "\nFile: file3.py",
        "----------------------------------------",
        "print('File 3')",
        "----------------------------------------"
    ])
    
    assert report == expected_report, "Formatted report with multiple files does not match expected output."

def test_report_formatter_empty_files():
    project_name = "empty_project"
    directory_tree = "empty_project"
    file_contents = {}
    
    formatter = ReportFormatter(project_name, directory_tree, file_contents)
    report = formatter.format()
    
    expected_report = "\n".join([
        "Directory Structure:",
        "empty_project",
        "empty_project",
        "\nFile Contents:"
    ])
    
    assert report == expected_report, "Formatted report with no files does not match expected output."

def test_report_formatter_write_to_file(temp_dir):
    project_name = "test_project"
    directory_tree = "test_project\n└── file.py"
    file_contents = {
        "file.py": "print('Test')"
    }
    
    formatter = ReportFormatter(project_name, directory_tree, file_contents)
    report = formatter.format()
    
    output_file = temp_dir / "output.txt"
    formatter.write_to_file(report, output_file)
    
    # Read back the file and compare
    with output_file.open('r', encoding='utf-8') as f:
        content = f.read()
    
    assert content == report, "Content written to file does not match the formatted report."
