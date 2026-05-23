"""End-of-day 'advance the company' check.

Prompts the founder to confirm:
  - the one revenue action moved
  - evidence captured
  - any decision logged
  - any approval cleared

Does not require interactive input; prints a structured checklist and
records a timestamped marker file.
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "dealix-ops-private"


CHECKLIST = """\
> Advance check — {date}
>
> [ ] One revenue action moved
> [ ] Evidence captured (file or ledger updated)
> [ ] At least one decision logged or none required
> [ ] Approval queue not stale (> 7 days old)
> [ ] Trust check: no overclaim, no private-data-in-public, no A4 attempts

If any unchecked: do not close the day. Fix it.
"""


def main() -> int:
    if not PRIVATE.exists():
        print("[advance] dealix-ops-private not staged. Run `make stage` first.")
        return 1

    today = dt.date.today().isoformat()
    marker = PRIVATE / "founder" / "advance_log.md"
    if marker.exists():
        body = marker.read_text(encoding="utf-8")
    else:
        body = "# Advance Log\n\n"
    if today not in body:
        body += f"- {today} advance check run\n"
        marker.write_text(body, encoding="utf-8")

    print(CHECKLIST.format(date=today))
    print(f"[advance] logged in {marker.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
