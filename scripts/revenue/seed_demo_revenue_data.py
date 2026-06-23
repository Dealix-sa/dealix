#!/usr/bin/env python3
"""Seed demo prospects into ledgers/prospects.csv when ledgers are empty.

This is a stub for local development and testing only — no external APIs are
called. Every demo prospect includes a valid ``source_url`` because we never
create a prospect without a traceable public source. This script never sends
anything externally; it only writes to local ledgers.

Usage:
    python scripts/revenue/seed_demo_revenue_data.py
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import (
    LEDGER_SCHEMAS,
    REPO_ROOT,
    ensure_ledgers,
    load_csv,
    today_str,
    write_csv,
)

# Demo prospects — all with valid source_url (no source, no entry).
# These are fictional companies used only for local testing. Each has a
# traceable public source URL so the pipeline can run end-to-end.
DEMO_PROSPECTS: list[dict[str, str]] = [
    {
        "company_name": "Najd Logistics",
        "sector": "logistics",
        "city": "Riyadh",
        "website": "https://najd-logistics.example.com",
        "source_url": "https://najd-logistics.example.com/about",
        "verification_status": "verified_public",
        "owner_decision": "pending",
    },
    {
        "company_name": "Hijaz Real Estate",
        "sector": "real_estate",
        "city": "Jeddah",
        "website": "https://hijaz-re.example.com",
        "source_url": "https://hijaz-re.example.com/contact",
        "verification_status": "partial",
        "owner_decision": "pending",
    },
    {
        "company_name": "Tihama Clinics Group",
        "sector": "clinics",
        "city": "Dammam",
        "website": "https://tihama-clinics.example.com",
        "source_url": "https://tihama-clinics.example.com/locations",
        "verification_status": "verified_public",
        "owner_decision": "pending",
    },
    {
        "company_name": "Yamama Restaurants",
        "sector": "restaurants",
        "city": "Riyadh",
        "website": "https://yamama-rest.example.com",
        "source_url": "https://yamama-rest.example.com/about-us",
        "verification_status": "placeholder",
        "owner_decision": "pending",
    },
    {
        "company_name": "Madar Training Institute",
        "sector": "training",
        "city": "Riyadh",
        "website": "https://madar-training.example.com",
        "source_url": "https://madar-training.example.com/courses",
        "verification_status": "partial",
        "owner_decision": "pending",
    },
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed demo revenue prospects if ledgers are empty")
    parser.add_argument("--force", action="store_true", help="Seed even if prospects already exist")
    args, _unknown = parser.parse_known_args()

    ensure_ledgers()
    prospects_path = REPO_ROOT / "ledgers" / "prospects.csv"
    existing = load_csv(prospects_path)

    if existing and not args.force:
        print(f"Prospects ledger already has {len(existing)} rows — skipping seed.")
        print("Use --force to overwrite with demo data.")
        return 0

    fields = LEDGER_SCHEMAS["prospects"]
    write_csv(prospects_path, DEMO_PROSPECTS, fields)
    print(f"Seeded {len(DEMO_PROSPECTS)} demo prospects into {prospects_path}")
    print(f"All prospects have valid source_url — date {today_str()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())