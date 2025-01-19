from pathlib import Path

default_copconignore_path = Path(__file__).parent / ".copconignore"


def read_copconignore_patterns(path: Path) -> list[str]:
    with path.open() as file:
        return [
            line.strip() for line in file if line.strip() and not line.startswith("#")
        ]
