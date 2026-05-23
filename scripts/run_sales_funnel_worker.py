#!/usr/bin/env python3
"""Sales funnel worker — read-only.

Reads sales/proposal_queue.csv and outreach/outreach_queue.csv and prints a
funnel snapshot to stdout. Never sends anything externally.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import Counter
from pathlib import Path
from typing import List

DEFAULT_ROOT = os.environ.get("PRIVATE_OPS", "/opt/dealix-ops-private")


def count_by(path: Path, column: str) -> Counter:
    counter: Counter = Counter()
    if not path.exists():
        return counter
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            counter[(row.get(column) or "").strip() or "(unknown)"] += 1
    return counter


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=DEFAULT_ROOT)
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    proposals = count_by(root / "sales/proposal_queue.csv", "status")
    outreach = count_by(root / "outreach/outreach_queue.csv", "status")
    print("Dealix sales funnel snapshot")
    print("-" * 40)
    print("proposals by status:")
    for status, count in sorted(proposals.items()):
        print(f"  {status:<20} {count}")
    print("outreach queue by status:")
    for status, count in sorted(outreach.items()):
        print(f"  {status:<20} {count}")
    print(f"source root: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
