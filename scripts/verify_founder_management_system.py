#!/usr/bin/env python3
"""Verify the founder management system."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, must_exist, print_and_exit  # noqa: E402

REQUIRED = [
    "apps/web/app/founder-leverage/page.tsx",
    "apps/web/app/strategy/page.tsx",
    "apps/web/app/capital-allocation/page.tsx",
    "apps/web/app/advisor/page.tsx",
    "scripts/generate_founder_leverage_report.py",
    "scripts/generate_strategy_scorecard.py",
    "scripts/generate_capital_allocation_report.py",
    "scripts/generate_monthly_advisor_update.py",
    ".github/workflows/dealix-founder-management-system.yml",
]


def main() -> int:
    result = VerifyResult(name="Founder Management System", passed=True)
    must_exist(REQUIRED, result)
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
