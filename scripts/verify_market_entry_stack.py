#!/usr/bin/env python3
"""Verify Dealix market-entry-stack: positioning + intelligence + offers + delivery."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = [
    "docs/positioning/DEALIX_POSITIONING.md",
    "docs/positioning/SAUDI_B2B_NARRATIVE.md",
    "docs/intelligence/SAUDI_B2B_MARKET_MAP.md",
    "docs/intelligence/SECTOR_RANKING_SYSTEM.md",
    "docs/intelligence/ICP_SEGMENTATION_SYSTEM.md",
    "docs/product/DEALIX_PRODUCT_LADDER.md",
    "docs/revenue/REVENUE_FACTORY_OS.md",
    "docs/revenue/SAMPLE_FACTORY.md",
    "docs/revenue/PROPOSAL_FACTORY.md",
    "docs/delivery/ULTIMATE_DELIVERY_OS.md",
    "docs/finance/ULTIMATE_FINANCE_OS.md",
    "docs/customer_success/CUSTOMER_SUCCESS_OS.md",
    "docs/ops/DEALIX_MARKET_ENTRY_OPERATING_STACK.md",
]


def main() -> int:
    missing = [f for f in REQUIRED if not (REPO / f).exists()]
    print("[market-entry-stack]")
    print(f"  missing: {len(missing)}")
    for m in missing:
        print(f"    - {m}")
    print("RESULT:", "FAIL" if missing else "PASS")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
