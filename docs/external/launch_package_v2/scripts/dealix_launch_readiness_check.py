#!/usr/bin/env python3
"""Dealix launch readiness checker.

Checks for files that make the business launchable: website pages, pricing docs,
prospect workflow, compliance notes, and daily growth reports.
"""
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "docs/PRICING_AND_PACKAGING_V6.md",
    "docs/launch/DEALIX_FULL_LAUNCH_MASTER_PLAN_AR.md",
    "docs/launch/OFFER_PACKAGES_PUBLIC_AR.md",
    "docs/launch/WEBSITE_CONVERSION_BLUEPRINT_AR.md",
    "docs/launch/DAILY_PROSPECTING_OPERATING_SYSTEM_AR.md",
    "data/prospects/icp_seed_accounts_saudi.csv",
    "scripts/dealix_daily_prospect_drafts.py",
    "landing/dealix_full_website_ar.html",
]

OPTIONAL_STRONG = [
    "frontend/src/app/[locale]/services/page.tsx",
    "frontend/src/app/[locale]/custom-ai-systems/page.tsx",
    ".github/workflows/dealix-daily-growth-os.yml",
]


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def main() -> int:
    missing = [p for p in REQUIRED if not exists(p)]
    optional_missing = [p for p in OPTIONAL_STRONG if not exists(p)]

    print("Dealix Launch Readiness")
    print("========================")
    for p in REQUIRED:
        print(("✅" if exists(p) else "❌"), p)
    print("\nStrong optional:")
    for p in OPTIONAL_STRONG:
        print(("✅" if exists(p) else "⚠️"), p)

    if missing:
        print("\nNOT READY: missing required files.")
        return 1
    if optional_missing:
        print("\nREADY FOR MANUAL LAUNCH, but production polish remains.")
        return 0
    print("\nREADY: launch package present.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
