#!/usr/bin/env python3
"""Verify the Dealix marketing documentation surface.

Checks that docs/marketing/ contains at least eight markdown documents.

Exit 0 on success, 1 on failure.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETING_DIR = REPO_ROOT / "docs" / "marketing"
MIN_DOCS = 8


def main() -> int:
    if not MARKETING_DIR.exists():
        print(f"docs/marketing/ missing at {MARKETING_DIR}")
        return 1
    docs = [p for p in MARKETING_DIR.glob("*.md") if p.is_file()]
    print("Dealix marketing-system verification")
    print("-" * 40)
    print(f"  docs/marketing/ : {len(docs)} (min {MIN_DOCS})")
    for path in sorted(docs):
        print(f"    - {path.name}")
    print("-" * 40)
    if len(docs) >= MIN_DOCS:
        print("summary: PASS")
        return 0
    print("summary: FAIL — not enough marketing docs")
    return 1


if __name__ == "__main__":
    sys.exit(main())
