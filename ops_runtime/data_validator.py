#!/usr/bin/env python3
"""Validate private ops CSVs against their JSON schemas.

Validation is intentionally tolerant: missing private ops directories are
reported but do not crash, because the public repo cannot assume the private
tree exists in CI.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


SCHEMA_MAP = {
    "pipeline/pipeline_tracker.csv": "schemas/pipeline.schema.json",
    "revenue/revenue_action_log.csv": "schemas/revenue_action.schema.json",
    "sales/proposal_tracker.csv": "schemas/proposal.schema.json",
    "evidence/execution_evidence_ledger.csv": "schemas/evidence.schema.json",
    "finance/unit_economics.csv": "schemas/unit_economics.schema.json",
    "content/content_calendar.csv": "schemas/content.schema.json",
    "partners/partner_tracker.csv": "schemas/partner.schema.json",
}


def required_columns(schema_path: Path) -> list[str]:
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    return list(data.get("required", []))


def validate_csv(csv_path: Path, schema_path: Path) -> list[str]:
    errors: list[str] = []
    if not csv_path.exists():
        return [f"missing: {csv_path}"]
    required = required_columns(schema_path)
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return [f"no header: {csv_path}"]
        missing_cols = [c for c in required if c not in reader.fieldnames]
        if missing_cols:
            errors.append(f"{csv_path}: missing columns {missing_cols}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="../dealix-ops-private", help="Private ops root path")
    args = parser.parse_args()

    public_root = Path(__file__).resolve().parents[1]
    private_root = Path(args.root).resolve()

    if not private_root.exists():
        print(f"WARN: private root missing: {private_root}")
        print("Run scripts/bootstrap_private_ops.py to scaffold it.")
        return 0

    failures: list[str] = []
    for rel_csv, rel_schema in SCHEMA_MAP.items():
        csv_path = private_root / rel_csv
        schema_path = public_root / rel_schema
        if not schema_path.exists():
            failures.append(f"schema missing: {rel_schema}")
            continue
        failures.extend(validate_csv(csv_path, schema_path))

    if failures:
        print("Data validator: issues found:")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: All private ops CSVs validate against their schemas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
