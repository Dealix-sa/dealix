"""Open today's daily brief, creating it from the template if missing.

Usage:
    python scripts/ceo/daily_brief.py
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "dealix-ops-private"
TEMPLATE = ROOT / "docs" / "founder" / "DAILY_COMMAND_BRIEF.md"
TARGET = PRIVATE / "founder" / "daily_brief.md"


def main() -> int:
    if not PRIVATE.exists():
        print("[daily] dealix-ops-private not staged. Run `make stage` first.")
        return 1

    today = dt.date.today().isoformat()
    if not TARGET.exists():
        body = TEMPLATE.read_text(encoding="utf-8")
        body = body.replace("yyyy-mm-dd", today)
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        TARGET.write_text(body, encoding="utf-8")
        print(f"[daily] created {TARGET.relative_to(ROOT)} for {today}")
    else:
        print(f"[daily] {TARGET.relative_to(ROOT)} exists; opening as-is")

    print()
    print("> What is the one revenue action today?")
    print(f">   open: {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
