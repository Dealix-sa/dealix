#!/usr/bin/env python3
"""Verify the Dealix growth + intelligence documentation surface.

Checks that the combined count of markdown documents in docs/growth/ and
docs/intelligence/ meets the minimum threshold (10).

Exit 0 on success, 1 on failure.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GROWTH_DIR = REPO_ROOT / "docs" / "growth"
INTELLIGENCE_DIR = REPO_ROOT / "docs" / "intelligence"
MIN_DOCS = 10


def count_docs(directory: Path) -> int:
    if not directory.exists():
        return 0
    return sum(1 for p in directory.glob("*.md") if p.is_file())


def main() -> int:
    growth = count_docs(GROWTH_DIR)
    intel = count_docs(INTELLIGENCE_DIR)
    total = growth + intel
    print("Dealix growth-system verification")
    print("-" * 40)
    print(f"  docs/growth/        : {growth}")
    print(f"  docs/intelligence/  : {intel}")
    print(f"  combined            : {total} (min {MIN_DOCS})")
    print("-" * 40)
    if total >= MIN_DOCS:
        print("summary: PASS")
        return 0
    print("summary: FAIL — not enough docs in growth + intelligence")
    return 1


if __name__ == "__main__":
    sys.exit(main())
