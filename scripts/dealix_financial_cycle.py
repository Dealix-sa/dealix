#!/usr/bin/env python3
"""Dealix Financial autonomy cycle — CLI runner (cron-able).

Runs the weekly autonomous financial cycle and prints a bilingual
summary. Nothing is sent, nothing is charged, nothing is refunded.
Every high-stakes signal becomes a pending approval for the founder.

Usage:
    python3 scripts/dealix_financial_cycle.py
    python3 scripts/dealix_financial_cycle.py --cadence weekly
    python3 scripts/dealix_financial_cycle.py --period-end 2026-05-31 --cadence monthly

Exit codes:
    0 = cycle completed cleanly
    1 = cycle completed with warnings (friction events emitted)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.financial_autonomy.financial_cycle import (  # noqa: E402
    FinancialCycleReport,
    run_financial_cycle,
)


def _print_summary(report: FinancialCycleReport) -> None:
    metrics = report.metrics
    print(f"== {report.title_en} ==")
    print(f"   {report.title_ar}")
    print(f"cycle_id:   {report.cycle_id}")
    print(f"period_end: {report.period_end}")
    print(f"cadence:    {report.cadence}")
    print("--- metrics / المقاييس ---")
    print(f"  MRR / إيراد شهري:        {metrics.get('mrr_sar', 0)} SAR")
    print(f"  ARR / إيراد سنوي:        {metrics.get('arr_sar', 0)} SAR")
    print(f"  NRR / NRR:               {metrics.get('nrr_pct', 0)}%")
    print(f"  churn / انسحاب شهري:     {metrics.get('churn_pct_monthly', 0)}%")
    print(f"  ARPA / متوسط:           {metrics.get('arpa_sar', 0)} SAR")
    print(f"  active customers / نشطون: {metrics.get('customers_active', 0)}")
    print(f"  gross margin / هامش:     {metrics.get('gross_margin_pct', 0)}%")
    print(f"  LTV (est.) / LTV تقدير:  {metrics.get('ltv_sar', 0)} SAR")
    print(
        "  CAC payback (est.) / استرداد CAC تقدير: "
        f"{metrics.get('cac_payback_months', 0)} months"
    )
    print(
        "  runway (est.) / مدرّج تقدير: "
        f"{metrics.get('runway_months', 0)} months"
    )
    print(
        "  capital assets / أصول رأس المال: "
        f"{metrics.get('capital_assets_this_period', 0)}"
    )
    print(f"anomalies / شذوذ:         {len(report.anomalies)}")
    for a in report.anomalies:
        print(f"  - [{a.get('severity')}] {a.get('kind')}: {a.get('evidence_en', '')}")
        print(f"    {a.get('evidence_ar', '')}")
    print(f"threshold violations / مخالفات: {len(report.threshold_violations)}")
    for v in report.threshold_violations:
        rule = v.get("rule", {})
        print(
            f"  - [{rule.get('severity')}] {rule.get('rule_id')}: "
            f"observed={v.get('observed_value')} action={v.get('action_on_violation')}"
        )
    print(
        "approvals pending / موافقات معلّقة: "
        f"{report.approvals_pending.get('count', 0)}"
    )
    if report.warnings:
        print(f"--- warnings ({len(report.warnings)}) ---")
        for w in report.warnings:
            print(f"  ! {w}")
    if report.report_paths:
        print("--- report files ---")
        for key, value in report.report_paths.items():
            print(f"  {key}: {value}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Dealix Financial autonomy cycle (weekly + monthly)."
    )
    parser.add_argument(
        "--period-end",
        default=None,
        help="Period end date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--cadence",
        default="weekly",
        choices=["weekly", "monthly"],
        help="Cycle cadence",
    )
    parser.add_argument(
        "--customer-id",
        default="dealix_financial",
        help="Tenant scope for the cycle",
    )
    args = parser.parse_args(argv)

    report = run_financial_cycle(
        period_end=args.period_end,
        cadence=args.cadence,
        customer_id=args.customer_id,
    )
    _print_summary(report)
    return 1 if report.warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
