"""End-of-day evidence capture.

- Appends a row to dealix-ops-private/founder/founder_time_log.md.
- Touches the daily brief so the file's mtime reflects the close.

Usage:
    python scripts/ceo/close_day.py
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "dealix-ops-private"
TIME_LOG = PRIVATE / "founder" / "founder_time_log.md"
DAILY = PRIVATE / "founder" / "daily_brief.md"


CLOSE_BLOCK = """\
- date: {date}
  total_hours:
  revenue:
  delivery:
  trust:
  build:
  admin:
  notes: ""
"""


def main() -> int:
    if not PRIVATE.exists():
        print("[close] dealix-ops-private not staged. Run `make stage` first.")
        return 1

    today = dt.date.today().isoformat()
    TIME_LOG.parent.mkdir(parents=True, exist_ok=True)
    if TIME_LOG.exists():
        existing = TIME_LOG.read_text(encoding="utf-8")
    else:
        existing = "# Founder Time Log\n\n> See docs/founder/FOUNDER_TIME_ACCOUNTING.md.\n\n"
    if today in existing:
        print(f"[close] {today} already present in {TIME_LOG.relative_to(ROOT)}")
    else:
        existing += "\n" + CLOSE_BLOCK.format(date=today)
        TIME_LOG.write_text(existing, encoding="utf-8")
        print(f"[close] appended {today} to {TIME_LOG.relative_to(ROOT)}")

    if DAILY.exists():
        DAILY.touch()
        print(f"[close] touched {DAILY.relative_to(ROOT)}")

    print()
    print("> What evidence was captured today?")
    print("> What goes on tomorrow's Kill List?")
    return 0


if __name__ == "__main__":
    sys.exit(main())
