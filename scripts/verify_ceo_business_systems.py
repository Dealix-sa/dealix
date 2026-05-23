#!/usr/bin/env python3
"""Verify Dealix CEO business systems — docs presence, size, and required terms.

Usage:
    python scripts/verify_ceo_business_systems.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
    "docs/operating_rhythm/CEO_OPERATING_MODEL.md",
    "docs/operating_rhythm/CEO_KPI_TREE.md",
    "docs/operating_rhythm/MANAGEMENT_CADENCE.md",
    "docs/operating_finance/FINANCIAL_MODEL_V1.md",
    "docs/operating_finance/CAPITAL_ALLOCATION_SYSTEM_V1.md",
    "docs/company/DEALIX_GROWTH_SYSTEM.md",
]

MIN_SIZE_BYTES = 300

TERM_CHECKS: dict[str, list[str]] = {
    "docs/operating_finance/FINANCIAL_MODEL_V1.md": [
        "cash_collected",
        "MRR",
        "runway",
        "gross_margin",
    ],
    "docs/company/DEALIX_GROWTH_SYSTEM.md": [
        "Lead",
        "DM",
        "Reply",
        "Sample",
        "Proposal",
        "Payment",
    ],
    "docs/operating_rhythm/CEO_KPI_TREE.md": [
        "Cash Collected",
        "MRR",
        "Proposals Sent",
    ],
    "docs/operating_rhythm/MANAGEMENT_CADENCE.md": [
        "Daily",
        "Weekly",
        "Monthly",
        "Quarterly",
    ],
}


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_DOCS:
        path = REPO_ROOT / rel
        if not path.exists():
            failures.append(f"Missing: {rel}")
            continue
        size = path.stat().st_size
        if size < MIN_SIZE_BYTES:
            failures.append(f"Too short ({size} bytes): {rel}")

    for rel, terms in TERM_CHECKS.items():
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for term in terms:
            if term not in text:
                failures.append(f"{rel} missing required term: {term!r}")

    if failures:
        print("CEO business systems verification failed:")
        for failure in failures:
            print(f"  FAIL: {failure}")
        return 1

    print("PASS: CEO business systems are ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
