#!/usr/bin/env python3
"""Dealix Full Ops autonomous cycle — CLI runner (cron-able).

Runs the unified daily Full Ops cycle and prints a bilingual summary.
Everything is deterministic up to an approval gate: nothing is sent and
nothing is charged. Drafts and external actions are queued as pending
approvals for the founder.

Usage:
    python3 scripts/dealix_full_ops_cycle.py
    python3 scripts/dealix_full_ops_cycle.py --on-date 2026-05-18
    python3 scripts/dealix_full_ops_cycle.py --leads path/to/leads.json

Cron example (07:30 KSA = 04:30 UTC daily):
    30 4 * * * cd /home/user/dealix && python3 scripts/dealix_full_ops_cycle.py

Exit codes:
    0 = cycle completed (founder reviews + approves pending items)
    1 = cycle completed with warnings (friction events emitted)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.full_ops.autonomous_cycle import (  # noqa: E402
    CycleReport,
    run_cycle,
)


def _load_leads(path: str | None) -> list[dict] | None:
    if not path:
        return None
    raw = Path(path).read_text(encoding="utf-8")
    data = json.loads(raw)
    if isinstance(data, dict) and "leads" in data:
        data = data["leads"]
    if not isinstance(data, list):
        raise ValueError("leads file must be a JSON list or {'leads': [...]}")
    return [dict(item) for item in data]


def _print_summary(report: CycleReport) -> None:
    stages = report.stages
    qualified = stages.get("qualified", {})
    print(f"== {report.title_en} ==")
    print(f"   {report.title_ar}")
    print(f"cycle_id: {report.cycle_id}")
    print(f"date:     {report.on_date}")
    print("--- stages / المراحل ---")
    print(f"  intake / استقبال:        {stages.get('intake', 0)}")
    print(f"  enriched / إثراء:        {stages.get('enriched', 0)}")
    print(f"  scored / تصنيف:          {stages.get('scored', 0)}")
    print(
        f"  qualified / تأهيل:       accept={qualified.get('accept', 0)} "
        f"diagnostic={qualified.get('diagnostic', 0)} "
        f"reject={qualified.get('reject', 0)}"
    )
    print(f"  drafts / مسوّدات:         {stages.get('drafts', 0)}")
    print(f"  proof_events / إثبات:    {stages.get('proof_events', 0)}")
    print(
        f"approvals pending / موافقات معلّقة: "
        f"{report.approvals_pending.get('count', 0)}"
    )
    print(f"work items / عناصر عمل:    {report.work_items.get('count', 0)}")
    print("--- next actions / الإجراءات التالية ---")
    for action in report.next_actions:
        print(f"  - {action['en']}")
        print(f"    {action['ar']}")
    if report.warnings:
        print(f"--- warnings ({len(report.warnings)}) ---")
        for warning in report.warnings:
            print(f"  ! {warning}")
    if report.report_paths:
        print("--- report files ---")
        for key, value in report.report_paths.items():
            print(f"  {key}: {value}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dealix Full Ops autonomous cycle")
    parser.add_argument("--on-date", default=None, help="cycle date (YYYY-MM-DD)")
    parser.add_argument("--leads", default=None, help="path to a leads JSON file")
    parser.add_argument(
        "--customer-id",
        default="dealix_full_ops",
        help="tenant scope for the cycle",
    )
    args = parser.parse_args(argv)

    leads = _load_leads(args.leads)
    report = run_cycle(
        leads=leads,
        on_date=args.on_date,
        customer_id=args.customer_id,
    )
    _print_summary(report)
    return 1 if report.warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
