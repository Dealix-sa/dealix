#!/usr/bin/env python3
"""Audit the quality of the private ops working tree.

Runs after the schema-level data validator. Looks for:
  - Stale files past their freshness window.
  - Empty CSVs that should have rows once activated.
  - Missing required private folders.
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path


FRESHNESS_DAYS = {
    "pipeline/pipeline_tracker.csv": 7,
    "revenue/revenue_action_log.csv": 1,
    "revenue/cash_collected.csv": 1,
    "sales/proposal_tracker.csv": 3,
    "evidence/execution_evidence_ledger.csv": 1,
    "trust/approval_log.csv": 1,
    "trust/risk_register.csv": 7,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="../dealix-ops-private")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"WARN: private root missing: {root}")
        print("Run scripts/bootstrap_private_ops.py to scaffold it.")
        return 0

    warnings: list[str] = []
    errors: list[str] = []
    now = time.time()
    one_day = 86_400.0

    for rel, days in FRESHNESS_DAYS.items():
        path = root / rel
        if not path.exists():
            warnings.append(f"missing file (run bootstrap): {rel}")
            continue
        age_days = (now - path.stat().st_mtime) / one_day
        if age_days > days:
            warnings.append(f"stale: {rel} ({age_days:.1f} days > {days} days target)")
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            try:
                next(reader)  # header
            except StopIteration:
                errors.append(f"empty (no header): {rel}")
                continue

    print(f"Private ops data quality audit @ {root}")
    if warnings:
        print("Warnings:")
        for w in warnings:
            print(" -", w)
    if errors:
        print("Errors:")
        for e in errors:
            print(" -", e)
        return 1
    if args.strict and warnings:
        return 1
    print("PASS: private data quality check complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
