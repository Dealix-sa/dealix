#!/usr/bin/env python3
"""Verify the growth system pages + scripts are present."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, must_exist, print_and_exit  # noqa: E402


REQUIRED = [
    "apps/web/app/distribution/page.tsx",
    "apps/web/app/campaigns/page.tsx",
    "scripts/generate_weekly_growth_review.py",
    "scripts/generate_message_performance_report.py",
    "scripts/generate_campaign_command_report.py",
]


def main() -> int:
    result = VerifyResult(name="Growth System", passed=True)
    must_exist(REQUIRED, result)
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
