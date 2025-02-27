from copcon.core.file_tree import FileTreeGenerator
from copcon.core.file_filter import FileFilter
from pathlib import Path

def test_file_tree_with_no_ignores(temp_dir):
    # Initialize FileFilter with no ignore patterns
    file_filter = FileFilter(
        user_ignore_path=None
    )
    
    # Create directory structure
    # /temp_dir
    # ├── dir1
    # │   └── file1.py
    # ├── dir2
    # │   └── file2.py
    # └── file3.py
    
    dir1 = temp_dir / "dir1"
    dir1.mkdir()
    (dir1 / "file1.py").touch()
    dir2 = temp_dir / "dir2"
    dir2.mkdir()
    (dir2 / "file2.py").touch()
    (temp_dir / "file3.py").touch()
    
    # Initialize FileTreeGenerator
    tree_generator = FileTreeGenerator(temp_dir, depth=-1, file_filter=file_filter)
    directory_tree = tree_generator.generate()
    
    # Assertions
    assert tree_generator.directory_count == 3, "Should count three directories (temp_dir, dir1, dir2)."
    assert tree_generator.file_count == 3, "Should count three files."
    assert "dir1" in directory_tree, "dir1 should be present in the tree."
    assert "file1.py" in directory_tree, "file1.py should be present in the tree."
    assert "dir2" in directory_tree, "dir2 should be present in the tree."
    assert "file2.py" in directory_tree, "file2.py should be present in the tree."
    assert "file3.py" in directory_tree, "file3.py should be present in the tree."

def test_ignored_directory_tree_display(tmp_path: Path):
    """
    Test that ignored directories appear in the tree but their contents don't.
    
    Directory structure:
    tmp_path/
    ├── src/
    │   ├── main.py
    │   └── util.py
    └── node_modules/
        ├── package1/
        │   └── index.js
        └── package2/
            └── index.js
    """
    # Set up test directory structure
    src = tmp_path / "src"
    src.mkdir()
    (src / "main.py").write_text("print('main')")
    (src / "util.py").write_text("print('util')")
    
    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()
    package1 = node_modules / "package1"
    package1.mkdir()
    (package1 / "index.js").write_text("console.log('pkg1')")
    package2 = node_modules / "package2"
    package2.mkdir()
    (package2 / "index.js").write_text("console.log('pkg2')")
    
    # Create a FileFilter that ignores node_modules
    class TestFileFilter(FileFilter):
        def should_ignore(self, path: Path) -> bool:
            return "node_modules" in path.parts
    
    # Generate tree
    generator = FileTreeGenerator(
        directory=tmp_path,
        depth=-1,
        file_filter=TestFileFilter()
    )
    tree = generator.generate()
    
    # Verify the output
    expected_tree = "\n".join([
        f"{tmp_path.name}",
        "├── node_modules",  # Directory shows up but no contents
        "└── src",
        "    ├── main.py",
        "    └── util.py"
    ])
    
    assert tree == expected_tree, f"Tree doesn't match expected output.\nGot:\n{tree}\nExpected:\n{expected_tree}"
    
    # Verify counts
    assert generator.directory_count == 2  # root and src (node_modules is ignored)
    assert generator.file_count == 2      # main.py and util.py



def test_ignored_directory_tree_display(tmp_path: Path):
    """
    Test that an ignored directory appears in the tree with the marker,
    and its contents are not displayed.

    Directory structure:
    tmp_path/
    ├── src/
    │   ├── main.py
    │   └── util.py
    └── node_modules/
        ├── package1/
        │   └── index.js
        └── package2/
            └── index.js
    """
    # Set up test directory structure
    src = tmp_path / "src"
    src.mkdir()
    (src / "main.py").write_text("print('main')")
    (src / "util.py").write_text("print('util')")

    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()
    package1 = node_modules / "package1"
    package1.mkdir()
    (package1 / "index.js").write_text("console.log('pkg1')")
    package2 = node_modules / "package2"
    package2.mkdir()
    (package2 / "index.js").write_text("console.log('pkg2')")

    # Create a FileFilter that ignores node_modules
    class TestFileFilter(FileFilter):
        def should_ignore(self, path: Path) -> bool:
            # If any part of the path equals 'node_modules', mark as ignored
            return "node_modules" in path.parts

    # Generate tree with our custom filter
    generator = FileTreeGenerator(
        directory=tmp_path,
        depth=-1,
        file_filter=TestFileFilter()
    )
    tree = generator.generate()

    # Expected tree: note that the generator returns only the children of tmp_path,
    # so the root directory name is not included.
    expected_tree = "\n".join([
        "├── node_modules/ (contents not displayed)",
        "└── src/",
        "    ├── main.py",
        "    └── util.py"
    ])

    assert tree == expected_tree, f"Tree output does not match expected.\nGot:\n{tree}\nExpected:\n{expected_tree}"

    # Verify counts: root directory is counted, plus src is recursed (node_modules is not recursed)
    # Here, we expect: root (counted when generate() is first called) + src directory.
    # Thus, directory_count should be 3 (root, src, and src's implicit subdirectories if any; node_modules is counted but its children are not recursed)
    # In this structure: root, src, node_modules -> 3 directories.
    assert generator.directory_count == 3, f"Expected 3 directories, got {generator.directory_count}"
    # Files in src only:
    assert generator.file_count == 2, f"Expected 2 files, got {generator.file_count}"