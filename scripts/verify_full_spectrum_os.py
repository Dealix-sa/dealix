"""Verify the full-spectrum Dealix OS doc layout.

For each stage 0..15, asserts at least one docs/<N>_*/ directory exists.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    docs = REPO_ROOT / "docs"
    if not docs.exists():
        print("FAIL docs/ missing")
        return 1

    failures: list[int] = []
    for stage in range(0, 16):
        prefix = f"{stage:02d}_"
        matches = [p for p in docs.iterdir() if p.is_dir() and p.name.startswith(prefix)]
        if matches:
            print(f"PASS stage {stage:02d} — {len(matches)} dir(s): {matches[0].name}")
        else:
            print(f"FAIL stage {stage:02d} — no docs/{prefix}*/ directory found")
            failures.append(stage)

    if failures:
        print(f"\nverify_full_spectrum_os: FAIL ({len(failures)} stages missing)")
        return 1
    print("\nverify_full_spectrum_os: PASS (stages 0-15 covered)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
