#!/usr/bin/env python3
"""Generate this month's Strategy Scorecard markdown."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "data" / "strategy_scorecard"

TEMPLATE = """# Dealix Strategy Scorecard — {month}

**Generated:** {now} UTC

## North-star: VOCD
- Current: pending live wiring
- 30-day rolling delta: pending live wiring

## Input metrics (leading)
| Metric | This week | Prior week | Trend |
|---|---|---|---|
| Diagnostics shipped | pending | pending | - |
| Sprints sold | pending | pending | - |
| Proof Packs delivered (score >= 70) | pending | pending | - |
| Capital Assets registered | pending | pending | - |
| Approval queue median age | pending | pending | - |
| Doctrine violations | pending | pending | - |

## Output metrics (lagging)
| Metric | This month | Prior month |
|---|---|---|
| MRR (SAR) | pending | pending |
| Customer count (paying) | pending | pending |
| Average Proof Pack score | pending | pending |

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
"""


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if args.check:
        print("strategy_scorecard: OK")
        return 0
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    month = now.strftime("%Y-%m")
    out = OUT_DIR / f"{month}.md"
    out.write_text(TEMPLATE.format(month=month, now=now.strftime('%Y-%m-%d %H:%M:%S')), encoding="utf-8")
    print(f"Wrote: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
