#!/usr/bin/env python3
"""Verify the Finance, Pricing, Capital OS artifacts are in place."""
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED = [
    "docs/finance/FINANCE_PRICING_CAPITAL_OS.md",
    "docs/finance/PRICING_ARCHITECTURE.md",
    "docs/finance/DISCOUNT_POLICY.md",
    "docs/finance/UNIT_ECONOMICS_SYSTEM.md",
    "docs/finance/CASH_DISCIPLINE_SYSTEM.md",
    "docs/finance/PAYMENT_PATH_SYSTEM.md",
    "docs/revenue/BAD_REVENUE_FILTER_V2.md",
    "ops_runtime/finance_v2.py",
    "scripts/generate_finance_command_report.py",
    "scripts/generate_pricing_review.py",
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
        print("Finance/Pricing OS verification FAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: Finance/Pricing/Capital OS is in place.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
