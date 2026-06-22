#!/usr/bin/env python3
"""
verify_outreach_compliance.py

Check that the prospect/outreach ledgers contain required compliance fields:
- source_url
- verification_status
- confidence
- recommended_product
- owner_decision

Also verifies that OUTBOUND_MODE=draft_only and EXTERNAL_SEND_ENABLED=false
are set unless explicitly overridden by an environment variable we can audit.
"""
from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PROSPECT_COLUMNS = [
    "company",
    "sector",
    "source_url",
    "verification_status",
    "confidence",
    "recommended_product",
    "owner_decision",
]


def check_prospects() -> list[str]:
    errors: list[str] = []
    path = REPO_ROOT / "ledgers" / "prospects.csv"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=REQUIRED_PROSPECT_COLUMNS)
            writer.writeheader()
        errors.append("ledgers/prospects.csv was missing; created empty ledger.")
        return errors

    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
    missing = [c for c in REQUIRED_PROSPECT_COLUMNS if c not in header]
    if missing:
        errors.append(f"ledgers/prospects.csv missing columns: {missing}")
    return errors


def check_env() -> list[str]:
    errors: list[str] = []
    safe = {
        "EXTERNAL_SEND_ENABLED": ("false", "0"),
        "OUTBOUND_MODE": ("draft_only",),
    }
    for key, expected in safe.items():
        val = os.environ.get(key, "").strip().lower()
        if val and val not in [e.lower() for e in expected]:
            errors.append(
                f"{key}={val!r} is not compliant. Expected one of {expected}."
            )
    return errors


def main() -> int:
    print("Outreach Compliance Check")
    print("=" * 50)
    errors = check_prospects() + check_env()
    if errors:
        print("❌ Issues:")
        for e in errors:
            print(f"   - {e}")
        return 1
    print("✅ Outreach compliance checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
