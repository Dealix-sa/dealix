#!/usr/bin/env python3
"""verify_marketing_system.py — verify the launch/marketing surface index exists."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "launch" / "INDEX.md"


def main() -> int:
    if not INDEX.exists():
        print(f"MARKETING_SYSTEM=fail reason=missing path={INDEX.relative_to(ROOT)}")
        return 1
    text = INDEX.read_text(encoding="utf-8")
    required_markers = ["launch_report", "weekly_content"]
    if not any(m in text for m in required_markers):
        print(f"MARKETING_SYSTEM=fail reason=index_empty")
        return 1
    print("MARKETING_SYSTEM=pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
