#!/usr/bin/env python3
"""Dealix Strategic Autonomy cycle — CLI runner (cron-able).

Runs the CEO/board-tier strategic autonomy cycle and prints a bilingual
summary. Strategic decisions are RECOMMENDED autonomously; irreversible
moves (KILL / HIRE / RAISE_PRICE / CREATE_BUSINESS_UNIT /
CREATE_VENTURE_CANDIDATE) are never auto-executed — they are routed to
the founder approval queue.

Usage:
    python3 scripts/dealix_strategic_cycle.py
    python3 scripts/dealix_strategic_cycle.py --on-date 2026-06-15
    python3 scripts/dealix_strategic_cycle.py --cadence monthly
    python3 scripts/dealix_strategic_cycle.py --cadence gate --no-delegate

Cron example (Sunday 05:00 UTC weekly):
    0 5 * * 0 cd /home/user/dealix && python3 scripts/dealix_strategic_cycle.py

Exit codes:
    0 = cycle completed clean
    1 = cycle completed with warnings (friction events emitted)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.strategy_autonomy.strategic_cycle import (  # noqa: E402
    StrategicCycleReport,
    run_strategic_cycle,
)


def _print_summary(report: StrategicCycleReport) -> None:
    s = report.signal_snapshot
    print(f"== {report.title_en} ==")
    print(f"   {report.title_ar}")
    print(f"cycle_id: {report.cycle_id}")
    print(f"date:     {report.on_date}")
    print(f"cadence:  {report.cadence}")
    print("--- signals / الإشارات ---")
    print(f"  days since launch / أيام منذ الإطلاق: {s.get('days_since_launch', 0)}")
    print(f"  revenue / الإيراد التراكمي:           {s.get('total_revenue_sar', 0)} SAR")
    print(f"  mrr / الإيراد الشهري:                 {s.get('mrr_sar', 0)} SAR")
    print(f"  retainers / الاشتراكات:               {s.get('retainer_count', 0)}")
    print(f"  proof score / درجة الإثبات:           {s.get('proof_score', 0)}")
    print(f"  governance risk / مخاطر الحوكمة:      {s.get('governance_risk_index', 0)}")
    due = [g for g in report.gate_evaluations if g.get("due")]
    print(f"--- gates / البوابات ---")
    print(f"  due / مستحقّة: {len(due)} / {len(report.gate_evaluations)}")
    for g in due:
        verdict = "pass" if g.get("passed") else "fail"
        print(f"  - {g.get('gate_id')}: {g.get('decision_type')} ({verdict})")
    print(f"--- decisions / القرارات ({len(report.decisions)}) ---")
    for d in report.decisions:
        flag = " [approval-gated / خلف موافقة]" if d.get("irreversible") else ""
        print(
            f"  - {d.get('decision_type')} -> {d.get('target')} "
            f"[{d.get('status')}]{flag}"
        )
    print(
        f"approvals pending / موافقات معلّقة: "
        f"{report.approvals_pending.get('count', 0)}"
    )
    print(f"delegated cycles / دورات مفوّضة:    {len(report.delegated_cycles)}")
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
    parser = argparse.ArgumentParser(
        description="Dealix strategic autonomy cycle"
    )
    parser.add_argument("--on-date", default=None, help="cycle date (YYYY-MM-DD)")
    parser.add_argument(
        "--cadence",
        default="weekly",
        choices=["weekly", "monthly", "gate"],
        help="cycle cadence",
    )
    parser.add_argument(
        "--customer-id",
        default="dealix_strategic",
        help="tenant scope for the cycle",
    )
    parser.add_argument(
        "--no-delegate",
        action="store_true",
        help="do not delegate reversible decisions to the Full Ops cycle",
    )
    args = parser.parse_args(argv)

    report = run_strategic_cycle(
        on_date=args.on_date,
        customer_id=args.customer_id,
        cadence=args.cadence,
        delegate_full_ops=not args.no_delegate,
    )
    _print_summary(report)
    return 1 if report.warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
