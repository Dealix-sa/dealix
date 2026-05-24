#!/usr/bin/env python3
"""Verify the market attack system."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, must_exist, print_and_exit  # noqa: E402

REQUIRED = [
    "apps/web/app/market-attack/page.tsx",
    "scripts/generate_beachhead_sector_scorecard.py",
    "scripts/generate_strategic_account_list.py",
    "scripts/generate_offer_market_fit_report.py",
    "scripts/generate_objection_intelligence_report.py",
    "scripts/generate_partner_pipeline_report.py",
    ".github/workflows/dealix-market-attack-system.yml",
]


def main() -> int:
    result = VerifyResult(name="Market Attack System", passed=True)
    must_exist(REQUIRED, result)
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
