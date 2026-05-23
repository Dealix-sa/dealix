"""Verify that the CEO Business Score system is wired into the repo."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED = [
    "docs/founder/CEO_BUSINESS_AUDIT.md",
    "ops_runtime/business_audit.py",
    "scripts/generate_ceo_business_score.py",
]


def main() -> int:
    failures = []
    for rel in REQUIRED:
        path = REPO_ROOT / rel
        if not path.exists():
            failures.append(f"Missing: {rel}")
        elif path.stat().st_size < 100:
            failures.append(f"Too short: {rel}")

    if failures:
        print("CEO business score verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: CEO business score system is ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
