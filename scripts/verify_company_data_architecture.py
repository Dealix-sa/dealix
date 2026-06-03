#!/usr/bin/env python3
"""Verify the Company Data Architecture is in place."""
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED = [
    "docs/data/COMPANY_DATA_ARCHITECTURE.md",
    "docs/data/DATA_PRIVACY_BOUNDARY.md",
    "docs/data/DATA_FRESHNESS_POLICY.md",
    "docs/data/REVENUE_DATA_MODEL.md",
    "schemas/pipeline.schema.json",
    "schemas/revenue_action.schema.json",
    "schemas/proposal.schema.json",
    "schemas/client.schema.json",
    "schemas/evidence.schema.json",
    "schemas/unit_economics.schema.json",
    "schemas/content.schema.json",
    "schemas/partner.schema.json",
    "ops_runtime/data_validator.py",
    "scripts/audit_private_data_quality.py",
    "scripts/export_company_snapshot.py",
    "scripts/bootstrap_private_ops.py",
]


def main() -> int:
    failures: list[str] = []
    for rel in REQUIRED:
        p = Path(rel)
        if not p.exists():
            failures.append(f"Missing: {rel}")
        elif p.stat().st_size < 30:
            failures.append(f"Too short: {rel}")
    if failures:
        print("Company Data Architecture verification FAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: Company Data Architecture is in place.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
