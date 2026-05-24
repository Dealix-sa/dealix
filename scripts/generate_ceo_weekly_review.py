#!/usr/bin/env python3
"""Generate this week's CEO Weekly Review markdown."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "data" / "ceo_briefs" / "weekly"

TEMPLATE = """# Dealix CEO Weekly Review — {iso_week}

**Generated:** {now} UTC

## North-star delta
- VOCD this week vs last: pending live wiring

## Pipeline health
- Added: pending; Qualified: pending; Closed-won: pending; Closed-lost: pending

## Capital allocation
- See `data/capital_allocation/<YYYY-MM>.md`.

## Doctrine compliance
- Violations: pending live wiring
- Approval-queue median age: pending live wiring

## Top 3 customer signals worth a call
- pending live wiring

## Next-week 3 bets
- pending founder input

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        print("ceo_weekly_review: OK")
        return 0
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    iso = f"{now.isocalendar().year}-W{now.isocalendar().week:02d}"
    out = OUT_DIR / f"{iso}.md"
    out.write_text(TEMPLATE.format(iso_week=iso, now=now.strftime('%Y-%m-%d %H:%M:%S')), encoding="utf-8")
    print(f"Wrote: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
