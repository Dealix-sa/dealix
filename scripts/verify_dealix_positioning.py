#!/usr/bin/env python3
"""Wave 2 gate — Dealix positioning / platform-truth verification.

Confirms the foundation documents that encode *what Dealix is* (and refuses to
be) are present and non-empty. Prints PASS/FAIL and exits non-zero on failure so
it can gate CI.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = (
    "docs/00_foundation/DEALIX_POSITIONING.md",
    "docs/00_foundation/DEALIX_CONSTITUTION.md",
    "docs/00_foundation/NON_NEGOTIABLES.md",
    "docs/00_foundation/OPERATING_EQUATION.md",
    "docs/00_foundation/WHAT_DEALIX_REFUSES.md",
    "docs/00_foundation/GOOD_REVENUE_BAD_REVENUE.md",
)


def main() -> int:
    print("== Dealix Positioning Verification ==")
    failures: list[str] = []
    for rel in REQUIRED:
        path = REPO / rel
        if not path.is_file():
            failures.append(f"MISSING  {rel}")
            continue
        if path.stat().st_size < 20:
            failures.append(f"EMPTY    {rel}")
            continue
        print(f"  ok  {rel}")

    if failures:
        print("\nRESULT: FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("\nRESULT: PASS — positioning foundation present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
