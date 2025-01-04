from pathlib import Path
from typing import Optional
from copcon.core.file_filter import FileFilter

class FileTreeGenerator:
    def __init__(
        self,
        directory: Path,
        depth: int,
        file_filter: FileFilter,
    ):
        self.directory = directory
        self.depth = depth
        self.file_filter = file_filter
        self.directory_count = 0  # Initialize directory count
        self.file_count = 0       # Initialize file count

    def generate(self, current_dir: Optional[Path] = None, current_depth: int = 0, prefix: str = "") -> str:
        if current_dir is None:
            current_dir = self.directory
            self.directory_count = 1  # Count the root directory

        if self.depth != -1 and current_depth > self.depth:
            return ""

        output = []
        try:
            contents = sorted(current_dir.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        except Exception as e:
            output.append(f"{prefix}Error accessing {current_dir}: {e}")
            return "\n".join(output)

        visible_contents = [path for path in contents if not self.file_filter.should_ignore(path)]

        for i, path in enumerate(visible_contents):
            is_last = i == len(visible_contents) - 1
            connector = "└── " if is_last else "├── "
            output.append(f"{prefix}{connector}{path.name}")
            if path.is_dir():
                self.directory_count += 1  # Increment directory count
                extension = "    " if is_last else "│   "
                subtree = self.generate(path, current_depth + 1, prefix + extension)
                if subtree:
                    output.append(subtree)
            else:
                self.file_count += 1  # Increment file count

        return "\n".join(output)
