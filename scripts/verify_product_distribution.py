#!/usr/bin/env python3
"""Verify Dealix productization and offer-ladder docs are present."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = [
    "docs/product/DEALIX_PRODUCT_LADDER.md",
    "docs/product/PRODUCT_DISTRIBUTION_OS.md",
    "docs/product/PRODUCT_POSITIONING.md",
    "docs/product/OFFER_PACKAGING.md",
    "docs/product/PRICING_GUARDRAILS.md",
    "docs/product/SALES_SCRIPTS.md",
    "docs/product/PROPOSAL_TEMPLATE_SYSTEM.md",
    "docs/product/CHECKOUT_AND_ONBOARDING_FLOW.md",
    "docs/product/CUSTOMER_PORTAL_ROADMAP.md",
]


def main() -> int:
    missing = [f for f in REQUIRED if not (REPO / f).exists()]
    print("[product-distribution]")
    print(f"  missing files: {len(missing)}")
    for m in missing:
        print(f"    - {m}")
    print("RESULT:", "FAIL" if missing else "PASS")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
