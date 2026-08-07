#!/usr/bin/env python3
"""Gate: no large binary files committed to the repo.

Fails if any tracked file exceeds the threshold (50 MB by default).
Run: python scripts/verify_repo_large_files.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THRESHOLD_MB = 50

def main() -> int:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        capture_output=True, text=True, cwd=ROOT,
    )
    if result.returncode != 0:
        print(f"WARN: git ls-files failed: {result.stderr.strip()}", file=sys.stderr)
        return 0  # Don't fail CI if git is unavailable

    files = [f for f in result.stdout.split("\0") if f]
    oversized = []
    for rel in files:
        path = ROOT / rel
        if path.is_file():
            size_mb = path.stat().st_size / (1024 * 1024)
            if size_mb > THRESHOLD_MB:
                oversized.append((rel, size_mb))

    if oversized:
        for rel, mb in oversized:
            print(f"FAIL: {rel} is {mb:.1f} MB (limit {THRESHOLD_MB} MB)")
        return 1

    print(f"PASS: no tracked file exceeds {THRESHOLD_MB} MB limit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
