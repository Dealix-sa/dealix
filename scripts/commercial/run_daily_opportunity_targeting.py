#!/usr/bin/env python3
"""Run the daily Saudi Opportunity targeting cycle (draft-only).

Pipeline: collect -> normalize -> score -> segment -> draft -> queue -> report.
Nothing is sent. Outreach drafts land in the approval queue only.

Usage:
    python scripts/commercial/run_daily_opportunity_targeting.py --mode draft-only --limit 50
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.opportunity_graph.pipeline import run_daily_targeting
from dealix.opportunity_graph.reports import write_daily_report
from dealix.opportunity_graph.store import get_store


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Daily Saudi Opportunity targeting (draft-only).")
    parser.add_argument(
        "--mode",
        default="draft-only",
        choices=["draft-only"],
        help="Only draft-only is supported. Live send is disabled by policy.",
    )
    parser.add_argument("--limit", type=int, default=50, help="Max companies to score this cycle.")
    parser.add_argument("--draft-top", type=int, default=20, help="Draft outreach for the top N companies.")
    parser.add_argument("--no-report", action="store_true", help="Skip writing the daily markdown report.")
    args = parser.parse_args(argv)

    store = get_store()
    summary = run_daily_targeting(
        store=store,
        limit=args.limit,
        mode=args.mode,
        draft_top=args.draft_top,
    )

    print("Daily Saudi Opportunity targeting — draft-only")
    for key in (
        "total_companies_scored",
        "hot",
        "warm",
        "research",
        "not_fit",
        "new_drafts",
        "pending_approvals",
        "approved_drafts",
    ):
        print(f"  {key:22s}: {summary[key]}")

    if not args.no_report:
        report_path = write_daily_report(store=store)
        print(f"Daily report: {report_path}")

    print("No messages sent. Drafts await founder approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
