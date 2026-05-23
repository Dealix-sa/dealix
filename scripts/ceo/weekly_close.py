"""Run the weekly CEO close.

- Ensures `dealix-ops-private/founder/weekly_ceo_review.md` exists for the week.
- Refreshes the master dashboard.
- Prints the weekly scorecard prompts.
"""

from __future__ import annotations

import datetime as dt
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "dealix-ops-private"
TEMPLATE = ROOT / "docs" / "founder" / "WEEKLY_CEO_REVIEW.md"
DASHBOARD = ROOT / "scripts" / "ceo" / "dashboard.py"


def main() -> int:
    if not PRIVATE.exists():
        print("[weekly] dealix-ops-private not staged. Run `make stage` first.")
        return 1

    today = dt.date.today()
    monday = today - dt.timedelta(days=today.weekday())
    friday = monday + dt.timedelta(days=4)
    week_id = friday.isoformat()
    week_dir = PRIVATE / "founder" / "weekly_reviews"
    week_dir.mkdir(parents=True, exist_ok=True)
    target = week_dir / f"week_ending_{week_id}.md"

    if not target.exists():
        body = TEMPLATE.read_text(encoding="utf-8")
        body = body.replace("yyyy-mm-dd", week_id)
        target.write_text(body, encoding="utf-8")
        print(f"[weekly] created {target.relative_to(ROOT)}")
    else:
        print(f"[weekly] {target.relative_to(ROOT)} already exists")

    print("\n[weekly] refreshing master dashboard…")
    subprocess.run([sys.executable, str(DASHBOARD)], check=False)

    print("\n[weekly] Score this week:")
    print("  - Cash collected vs target")
    print("  - DMs / Replies / Proposals / Paid")
    print("  - Build / Fix / Kill / Defer / Continue (one each)")
    print("  - Pattern of the week (one sentence)")
    print("  - Next week's North Star (one sentence)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
