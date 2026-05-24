#!/usr/bin/env python3
"""Generate this month's Revenue Forecast markdown (read-only)."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "data" / "revenue_forecast"

TEMPLATE = """# Dealix Revenue Forecast — {month}

**Generated:** {now} UTC
**Horizon:** 6 months rolling

## Assumptions
| Variable | Default |
|---|---|
| Diagnostic -> Sprint conversion | 30% |
| Sprint -> Retainer conversion | 25% |
| Retainer net retention (monthly) | 0.90 |
| Sprint ARPU | SAR 499 |
| Retainer ARPU (monthly) | SAR 3,999 |

## Forecast
Pending live wiring against Moyasar + Proof Pack store.

| Month | Diagnostics | Sprints | Retainers | One-time SAR | MRR SAR |
|---|---|---|---|---|---|
| +0 | pending | pending | pending | pending | pending |
| +1 | pending | pending | pending | pending | pending |
| +2 | pending | pending | pending | pending | pending |
| +3 | pending | pending | pending | pending | pending |
| +4 | pending | pending | pending | pending | pending |
| +5 | pending | pending | pending | pending | pending |

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
"""


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if args.check:
        print("revenue_forecast: OK")
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
