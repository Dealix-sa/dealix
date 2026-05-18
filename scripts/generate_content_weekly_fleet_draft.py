#!/usr/bin/env python3
"""Generate content fleet draft scaffold."""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/content_drafts"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write", action="store_true")
    p.add_argument("--daily", action="store_true")
    args = p.parse_args()
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    md = f"# مسودة محتوى · {day}\n\n> مسودة فقط — SOAEN قبل النشر\n"
    if args.write:
        OUT.mkdir(parents=True, exist_ok=True)
        suffix = "daily" if args.daily else "weekly"
        path = OUT / f"{day}_{suffix}_fleet.md"
        path.write_text(md + "\n", encoding="utf-8")
        print(f"WROTE {path}")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
