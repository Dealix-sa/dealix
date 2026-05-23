#!/usr/bin/env python3
"""Surface open trust flags and incidents."""
from __future__ import annotations

import csv
import os
import sys
from pathlib import Path


def _runtime_dir() -> Path:
    return Path(os.getenv("PRIVATE_OPS") or os.getenv("DEALIX_PRIVATE_OPS_DIR") or "/opt/dealix-ops-private").expanduser()


def main() -> int:
    base = _runtime_dir()
    flags = base / "trust" / "trust_flags.csv"
    if not flags.exists():
        print(f"SKIP: {flags} missing")
        return 0
    n = 0
    with flags.open("r", encoding="utf-8", newline="") as fh:
        for _ in csv.DictReader(fh):
            n += 1
    print(f"[trust_flags] open={n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
