#!/usr/bin/env python3
"""Dealix monthly board-memo cycle — CLI runner (cron-able on 1st of month).

Runs the monthly board-memo cycle and prints a bilingual summary.
The memo is never shared automatically — it is queued for founder
approval before any distribution.

Usage:
    python3 scripts/dealix_board_memo_cycle.py --month 2026-05

Exit codes:
    0 = memo built (sections complete)
    1 = memo built but warnings emitted or sections incomplete
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.financial_autonomy.board_memo_cycle import (  # noqa: E402
    BoardMemoReport,
    run_board_memo_cycle,
)


def _print_summary(report: BoardMemoReport) -> None:
    print(f"== Board Memo — {report.month} ==")
    print(f"   مذكّرة المجلس — {report.month}")
    print(f"generated_at: {report.generated_at}")
    print(f"approval_id:  {report.approval_id}")
    print(f"sections_complete / اكتمال الأقسام: {report.sections_complete}")
    if report.missing_sections:
        print(f"missing_sections / أقسام ناقصة: {report.missing_sections}")
    print("--- sections / الأقسام ---")
    for idx, slug in enumerate(report.section_order, start=1):
        block = report.sections.get(slug, {})
        title_en = block.get("title_en", slug)
        title_ar = block.get("title_ar", slug)
        body_en = (block.get("body_en") or "—").strip().splitlines()[0]
        body_ar = (block.get("body_ar") or "—").strip().splitlines()[0]
        print(f"  {idx:2d}. {title_en} / {title_ar}")
        print(f"      EN: {body_en}")
        print(f"      AR: {body_ar}")
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
        description="Dealix monthly board-memo cycle."
    )
    parser.add_argument(
        "--month",
        required=True,
        help="Month to build the memo for (YYYY-MM)",
    )
    args = parser.parse_args(argv)

    try:
        report = run_board_memo_cycle(month=args.month)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    _print_summary(report)
    if report.warnings or not report.sections_complete:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
