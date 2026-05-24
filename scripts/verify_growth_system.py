#!/usr/bin/env python3
"""verify_growth_system.py — verify the growth surface index exists."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "growth" / "INDEX.md"


def main() -> int:
    if not INDEX.exists():
        print(f"GROWTH_SYSTEM=fail reason=missing path={INDEX.relative_to(ROOT)}")
        return 1
    text = INDEX.read_text(encoding="utf-8")
    # The index must at least mention the canonical growth modules.
    required_markers = ["autonomous_growth", "self_growth_os", "growth_beast"]
    missing = [m for m in required_markers if m not in text]
    if missing:
        print(f"GROWTH_SYSTEM=fail reason=index_missing_refs missing={','.join(missing)}")
        return 1
    print("GROWTH_SYSTEM=pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
