#!/usr/bin/env python3
"""Verify the scale / moat system."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, must_exist, print_and_exit  # noqa: E402

REQUIRED = [
    "apps/web/app/moat/page.tsx",
    "apps/web/app/playbooks/page.tsx",
    "apps/web/app/proof-library/page.tsx",
    "apps/web/app/partner-ecosystem/page.tsx",
    "apps/web/app/productization/page.tsx",
    "apps/web/app/customer-success/page.tsx",
    "scripts/generate_moat_scorecard.py",
    "scripts/generate_proof_library_report.py",
    "scripts/generate_partner_ecosystem_report.py",
    "scripts/generate_productization_pipeline_report.py",
    "scripts/generate_expansion_report.py",
    ".github/workflows/dealix-scale-moat-system.yml",
]


def main() -> int:
    result = VerifyResult(name="Scale / Moat System", passed=True)
    must_exist(REQUIRED, result)
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
