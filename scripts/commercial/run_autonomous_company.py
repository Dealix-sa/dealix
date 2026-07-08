#!/usr/bin/env python3
"""Run one autonomous cycle of the Dealix Autonomous Company OS.

Loads durable memory, ingests warm leads, decides the next-best action per deal,
computes KPIs + forecast, and writes the Command Room (HTML + markdown). Draft-only:
nothing is sent, published, or charged.

Usage:
    python scripts/commercial/run_autonomous_company.py [--top 10] [--seed-inbox]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.autonomous_company import company_os, state


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix Autonomous Company cycle")
    parser.add_argument("--top", type=int, default=10, help="Top N ranked actions")
    parser.add_argument(
        "--seed-inbox",
        action="store_true",
        help="Write an empty inbox template if none exists (no fake data).",
    )
    args = parser.parse_args()

    if args.seed_inbox:
        path = state.seed_example_inbox()
        print(f"INBOX_TEMPLATE={path.relative_to(ROOT)}")

    try:
        result = company_os.run_cycle(top_n=args.top, write=True)
    except RuntimeError as exc:
        print("AUTONOMOUS_COMPANY=ABORT")
        print(f"UNSAFE: {exc}")
        return 2

    k = result.kpis
    print("AUTONOMOUS_COMPANY=OK")
    print(f"NEW_LEADS_INGESTED={result.added_leads}")
    print(f"TOTAL_DEALS={k.total_deals}")
    print(f"ACTIVE_DEALS={k.active_deals}")
    print(f"STALLED_DEALS={k.stalled_deals}")
    print(f"RECOGNIZED_REVENUE_SAR={k.recognized_revenue_sar}")
    print(f"WEIGHTED_PIPELINE_SAR={round(k.weighted_pipeline_sar)}")
    print(f"APPROVALS_PENDING={len(result.decision.approvals)}")
    for key, path in result.outputs.items():
        print(f"REPORT_{key.upper()}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
