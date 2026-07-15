"""Aggregate Dealix full-ops verifier.

Runs the family of stage / readiness / governance verifiers.
Each entry is a list passed to subprocess.run. Add new verifiers here.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS: list[list[str]] = [
    ["python", "scripts/verify_stage_gated_roadmap.py"],
]


def main() -> int:
    failures: list[str] = []
    for cmd in CHECKS:
        print(f"\n>>> {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            failures.append(" ".join(cmd))

    if failures:
        print("\nFull ops verification failed for:")
        for f in failures:
            print("-", f)
        return 1

    print("\nPASS: full ops verification complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
