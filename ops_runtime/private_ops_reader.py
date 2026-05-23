import csv
from pathlib import Path


class PrivateOpsReader:
    """Reads operating CSVs from a private ops directory.

    The private ops repo lives outside the public repo (e.g. ../dealix-ops-private)
    so real customer / revenue / trust data never enters the public tree.
    """

    def __init__(self, root):
        self.root = Path(root)

    def read_csv(self, relative_path):
        path = self.root / relative_path
        if not path.exists():
            return []
        with path.open(encoding="utf-8") as handle:
            return list(csv.DictReader(handle))
