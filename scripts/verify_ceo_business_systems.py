"""Verify the full CEO Business Systems surface (audit + score + CLI)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED = [
    "docs/founder/CEO_BUSINESS_AUDIT.md",
    "ops_runtime/__init__.py",
    "ops_runtime/business_audit.py",
    "scripts/generate_ceo_business_score.py",
    "scripts/verify_ceo_business_score.py",
    "dealix_cli/__init__.py",
    "dealix_cli/__main__.py",
    "dealix_cli/commands.py",
    ".github/workflows/dealix-business-systems.yml",
]


def main() -> int:
    failures = []
    for rel in REQUIRED:
        path = REPO_ROOT / rel
        if not path.exists():
            failures.append(f"Missing: {rel}")
        elif path.stat().st_size < 50:
            failures.append(f"Too short: {rel}")

    if failures:
        print("CEO business systems verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: CEO business systems are wired.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
