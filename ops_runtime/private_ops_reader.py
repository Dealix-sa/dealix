from pathlib import Path
import csv


class PrivateOpsReader:
    def __init__(self, private_ops_path: str):
        self.root = Path(private_ops_path)

    def read_csv(self, relative_path: str):
        path = self.root / relative_path
        if not path.exists():
            return []
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def read_text(self, relative_path: str) -> str:
        path = self.root / relative_path
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")

    def exists(self, relative_path: str) -> bool:
        return (self.root / relative_path).exists()
