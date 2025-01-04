from typing import Dict
from copcon.utils.logger import logger
from pathlib import Path

class ReportFormatter:
    def __init__(self, project_name: str, directory_tree: str, file_contents: Dict[str, str]):
        self.project_name = project_name
        self.directory_tree = directory_tree
        self.file_contents = file_contents

    def format(self) -> str:
        report = [
            "Directory Structure:",
            self.project_name,
            self.directory_tree,
            "\nFile Contents:"
        ]
        for relative_path, content in self.file_contents.items():
            report.extend([
                f"\nFile: {relative_path}",
                "-" * 40,
                content,
                "-" * 40
            ])
        return "\n".join(report)

    def write_to_file(self, report: str, output_file: Path):
        try:
            with output_file.open('w', encoding='utf-8') as f:
                f.write(report)
            logger.info(f"Output written to {output_file}")
        except Exception as e:
            logger.error(f"Error writing to file {output_file}: {e}")
            raise
