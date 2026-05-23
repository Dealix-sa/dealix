#!/usr/bin/env python3
"""Trust flags worker — read-only.

Summarizes trust/trust_flags.csv and trust/incidents.csv. Never sends
anything externally.
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


def tally(path: Path, column: str) -> Counter:
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
    flags_by_severity = tally(root / "trust/trust_flags.csv", "severity")
    incidents_by_status = tally(root / "trust/incidents.csv", "status")
    print("Dealix trust flags snapshot")
    print("-" * 40)
    print("trust flags by severity:")
    for sev, count in sorted(flags_by_severity.items()):
        print(f"  {sev:<12} {count}")
    print("incidents by status:")
    for status, count in sorted(incidents_by_status.items()):
        print(f"  {status:<12} {count}")
    print(f"source root: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
