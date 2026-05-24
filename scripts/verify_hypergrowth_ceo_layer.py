#!/usr/bin/env python3
"""Verify the hypergrowth CEO layer."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, must_exist, print_and_exit  # noqa: E402

REQUIRED = [
    "apps/web/app/ceo/page.tsx",
    "apps/web/app/ceo-os/page.tsx",
    "apps/web/app/metrics/page.tsx",
    "scripts/generate_ceo_daily_brief.py",
    "scripts/generate_ceo_weekly_review.py",
    "scripts/generate_revenue_forecast.py",
    ".github/workflows/dealix-hypergrowth-ceo-layer.yml",
]


def main() -> int:
    result = VerifyResult(name="Hypergrowth CEO Layer", passed=True)
    must_exist(REQUIRED, result)
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
