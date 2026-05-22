"""CLI for the daily Customer Success autonomy cycle.

Runs ``run_customer_success_cycle`` and prints a bilingual summary.
Exits 0 on success, 1 if the cycle produced warnings.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.customer_success_autonomy import (  # noqa: E402
    CustomerSuccessCycleReport,
    run_customer_success_cycle,
)


def _parse_customer_ids(raw: str | None) -> list[str] | None:
    if not raw:
        return None
    return [c.strip() for c in raw.split(",") if c.strip()]


def _print(report: CustomerSuccessCycleReport) -> None:
    s = report.summary
    print("=" * 72)
    print(f"  {report.title_ar}")
    print(f"  {report.title_en}")
    print(f"  cycle_id: {report.cycle_id}")
    print("=" * 72)
    print("الملخّص / Summary")
    print(f"  active_customers:    {s.get('active_customers', 0)}")
    print(f"  opportunities_total: {s.get('opportunities_total', 0)}")
    print(f"  at_risk:             {s.get('at_risk', 0)}")
    print(f"  expansion_ready:     {s.get('expansion_ready', 0)}")
    print(f"  renewals_due:        {s.get('renewals_due', 0)}")
    print(f"  nps_detractors:      {s.get('nps_detractors', 0)}")
    print(f"approvals_created:   {report.approvals_created}")
    print(f"work_items_created:  {report.work_items_created}")

    if report.opportunities:
        print("\n--- opportunities / الفرص ---")
        for opp in report.opportunities[:10]:
            print(
                f"  [{opp.get('urgency', 'normal')}] {opp.get('type', '')} — "
                f"{opp.get('customer_id', '')}"
            )

    if report.warnings:
        print("\n--- warnings / تحذيرات ---")
        for w in report.warnings[:10]:
            print(f"  - {w}")

    print("\n--- report files ---")
    print(f"  json: {report.report_paths.get('json', '')}")
    print(f"  md:   {report.report_paths.get('md', '')}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Run the daily Customer Success autonomy cycle."
    )
    p.add_argument("--on-date", default=None, help="ISO date (YYYY-MM-DD).")
    p.add_argument(
        "--customer-ids",
        default=None,
        help="Comma-separated list of customer ids to include.",
    )
    args = p.parse_args(argv)

    report = run_customer_success_cycle(
        customer_ids=_parse_customer_ids(args.customer_ids),
        on_date=args.on_date,
    )
    _print(report)
    return 1 if report.warnings else 0


if __name__ == "__main__":
    sys.exit(main())
