from copcon.core.file_tree import FileTreeGenerator
from copcon.core.file_filter import FileFilter

def test_file_tree_with_no_ignores(temp_dir):
    # Initialize FileFilter with no ignore patterns
    file_filter = FileFilter(
        additional_dirs=None,
        additional_files=None,
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
