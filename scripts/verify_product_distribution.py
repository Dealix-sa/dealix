#!/usr/bin/env python3
"""
Verify the Dealix Product Marketing & Distribution layer.

Checks:
- Required product + revenue docs exist.
- Offer ladder and product distribution CSVs exist with required columns.
- All seven rungs are represented in the offer ladder.
- No row carries banned claims.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
    "docs/product/DEALIX_PRODUCT_LADDER.md",
    "docs/product/PRODUCT_DISTRIBUTION_OS.md",
    "docs/product/PRODUCT_POSITIONING.md",
    "docs/product/OFFER_PACKAGING.md",
    "docs/product/PRICING_GUARDRAILS.md",
    "docs/revenue/REVENUE_FACTORY_OS.md",
    "docs/revenue/SAMPLE_FACTORY.md",
    "docs/revenue/PROPOSAL_FACTORY.md",
    "docs/finance/PAYMENT_CAPTURE_OS.md",
    "docs/delivery/DELIVERY_QA_OS.md",
    "docs/client_success/RETENTION_REFERRAL_OS.md",
    "docs/proof/PROOF_APPROVAL_OS.md",
]

REQUIRED_CSVS = {
    "data/seeds/product/offer_ladder.csv": [
        "rung", "name", "positioning", "price_band",
        "upsell_to", "proof_required", "owner", "status", "source",
    ],
    "data/seeds/product/product_distribution.csv": [
        "rung", "channel", "allocation", "kpi", "owner", "status", "source",
    ],
}

BANNED = [
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed leads",
    "guaranteed results",
    "guaranteed close rate",
]


def main() -> int:
    failures: list[str] = []
    passes: list[str] = []

    for doc in REQUIRED_DOCS:
        if (ROOT / doc).exists():
            passes.append(f"doc exists: {doc}")
        else:
            failures.append(f"MISSING doc: {doc}")

    for csv_path, required_cols in REQUIRED_CSVS.items():
        path = ROOT / csv_path
        if not path.exists():
            failures.append(f"MISSING CSV: {csv_path}")
            continue
        with path.open("r", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            try:
                header = next(reader)
            except StopIteration:
                failures.append(f"empty CSV: {csv_path}")
                continue
            missing_cols = [c for c in required_cols if c not in header]
            if missing_cols:
                failures.append(f"CSV {csv_path} missing columns: {missing_cols}")
            else:
                passes.append(f"CSV columns OK: {csv_path}")
            for row in reader:
                joined = " ".join(row).lower()
                for banned in BANNED:
                    if re.search(rf"\b{re.escape(banned.lower())}\b", joined):
                        failures.append(f"banned claim '{banned}' in row of {csv_path}")

    # Check all 7 rungs are present in offer_ladder.csv
    ladder_csv = ROOT / "data/seeds/product/offer_ladder.csv"
    if ladder_csv.exists():
        with ladder_csv.open("r", encoding="utf-8") as fh:
            rungs = {row["rung"] for row in csv.DictReader(fh)}
        expected = {str(i) for i in range(1, 8)}
        if not expected.issubset(rungs):
            failures.append(f"offer_ladder.csv missing rungs: {sorted(expected - rungs)}")
        else:
            passes.append("offer_ladder.csv contains all 7 rungs")

    print(f"PASSED: {len(passes)}")
    for p in passes:
        print(f"  - {p}")
    print()
    print(f"FAILED: {len(failures)}")
    for f in failures:
        print(f"  - {f}")
    if failures:
        import os
        if os.environ.get("GITHUB_ACTIONS") == "true":
            for f in failures[:10]:
                msg = f.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
                print(f"::error title=Product verifier failure::{msg}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
