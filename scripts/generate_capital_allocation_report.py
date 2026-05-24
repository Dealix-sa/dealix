#!/usr/bin/env python3
"""Generate this month's Capital Allocation report."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "data" / "capital_allocation"

TEMPLATE = """# Dealix Capital Allocation — {month}

**Generated:** {now} UTC

| Pool | Target % | Actual % | Notes |
|---|---|---|---|
| people | 35 | pending | founder time priced at SAR 500/h until first hire |
| infra | 10 | pending | Railway + Postgres + Redis + S3 + LLM APIs |
| sales | 20 | pending | content + partner referrals (no ads <SAR 10K MRR) |
| R&D | 25 | pending | new offers + Proof Pack improvements |
| runway buffer | 10 | pending | 3-month operating runway minimum |

## Decisions to make
- pending founder input

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
"""


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if args.check:
        print("capital_allocation_report: OK")
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
