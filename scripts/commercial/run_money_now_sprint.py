#!/usr/bin/env python3
"""Generate the Money Now Sprint founder action plan (draft-only).

Produces today's top closeable offer, up to 10 target prospect slots, draft
messages, a manual payment checklist, an evidence-event checklist, a proof-pack
delivery checklist, and a follow-up queue. Nothing is sent or charged.

Usage:
    python scripts/commercial/run_money_now_sprint.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.strategy_execution import money_now


def main() -> int:
    plan = money_now.build_plan()
    outputs = money_now.write_plan(plan)

    print("MONEY_NOW_SPRINT=OK")
    print("MODE=draft-only")
    print(f"TOP_OFFER={plan.top_offer['name']} ({plan.top_offer['price_sar']} SAR)")
    print(f"PROSPECT_SLOTS={len(plan.prospects)}")
    print(f"RECOGNIZED_REVENUE_SAR={plan.recognized_revenue_sar}")
    for key, path in outputs.items():
        print(f"REPORT_{key.upper()}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
