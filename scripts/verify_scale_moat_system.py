#!/usr/bin/env python3
"""verify_scale_moat_system.py — verify the moat-systems index exists."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "moat" / "INDEX.md"


def main() -> int:
    if not INDEX.exists():
        print(f"SCALE_MOAT_SYSTEM=fail reason=missing path={INDEX.relative_to(ROOT)}")
        return 1
    print("SCALE_MOAT_SYSTEM=pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
