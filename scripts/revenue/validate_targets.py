#!/usr/bin/env python3
"""Validate that prospects have a valid source_url — no source, no entry.

This script never sends anything externally. It only reads ledgers and
reports validation issues. A prospect without a valid ``source_url`` is
rejected because we refuse to act on data we cannot trace back to a
public, verifiable source.

Usage:
    python scripts/revenue/validate_targets.py [--input ledgers/prospects.csv]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import LEDGER_SCHEMAS, REPO_ROOT, load_csv, today_str

REQUIRED_FIELDS = ("company_name", "sector", "city", "source_url", "verification_status")


def validate_rows(rows: list[dict[str, str]]) -> tuple[list[str], list[dict[str, str]]]:
    """Validate a list of prospect rows.

    Returns a tuple of (issues, valid_rows). A row is valid only when it has a
    non-empty ``source_url`` that starts with ``http``. Empty prospect lists
    are rejected (no source, no entry).
    """
    issues: list[str] = []
    valid: list[dict[str, str]] = []

    if not rows:
        issues.append("No prospects to validate — prospects list is empty")
        return issues, valid

    for idx, row in enumerate(rows, start=1):
        source = (row.get("source_url") or "").strip()

        if not source:
            issues.append(
                f"Row {idx} ({row.get('company_name', '?')}): missing source_url — no source, no entry"
            )
            continue

        if not source.startswith("http"):
            issues.append(
                f"Row {idx} ({row.get('company_name', '?')}): source_url must start with http — got '{source}'"
            )
            continue

        # Source URL is valid — keep the row
        valid.append(row)

    return issues, valid


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate prospects require source_url")
    parser.add_argument("--input", default="ledgers/prospects.csv")
    args = parser.parse_args()

    input_path = REPO_ROOT / args.input
    rows = load_csv(input_path)

    print(f"Dealix target validation — {today_str()}")
    print(f"Input: {input_path}")
    print("-" * 60)

    # Check header has source_url
    if rows:
        header_fields = set(rows[0].keys())
        schema_fields = set(LEDGER_SCHEMAS["prospects"])
        missing = schema_fields - header_fields
        if missing:
            print(f"❌ Missing required columns: {sorted(missing)}")
            return 1

    issues, valid = validate_rows(rows)
    if issues:
        print(f"❌ {len(issues)} validation issue(s):")
        for issue in issues:
            print(f"  {issue}")
        print(f"\nValid prospects: {len(valid)} / {len(rows)}")
        return 1

    print(f"✅ All {len(valid)} prospects have valid source_url.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
