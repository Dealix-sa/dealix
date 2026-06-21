#!/usr/bin/env python3
"""
Score all prospects in ledgers/prospects.csv using company.intake.intake_engine.

Adds/updates confidence based on score:
  >= 70 → high
  >= 50 → medium
  < 50  → low

Writes updated ledger in place.
Usage:
    python scripts/founder/score_targets.py
    python scripts/founder/score_targets.py --dry-run
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

PROSPECTS = ROOT / "ledgers" / "prospects.csv"

SCHEMA = [
    "company_name", "sector", "city", "website", "source_url",
    "contact_page_url", "public_email", "phone", "linkedin_url",
    "verification_status", "confidence", "pain_hypothesis",
    "dealix_angle", "recommended_product", "message_stage",
    "next_action", "owner_decision",
]


def _confidence(s: int) -> str:
    if s >= 70:
        return "high"
    if s >= 50:
        return "medium"
    return "low"


def main() -> int:
    parser = argparse.ArgumentParser(description="Score all prospects")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    from company.intake import intake_engine

    if not PROSPECTS.exists():
        print("WARN: ledgers/prospects.csv not found. Run import_targets.py first.")
        return 0

    with PROSPECTS.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    updated = 0
    for row in rows:
        intake_row = {
            "weekly_leads": "",
            "main_problem": row.get("pain_hypothesis", ""),
            "sector": row.get("sector", ""),
            "whatsapp": row.get("phone", ""),
            "budget_range": "",
        }
        s = intake_engine.score(intake_row)
        conf = _confidence(s)
        if row.get("confidence") != conf:
            row["confidence"] = conf
            updated += 1

        if not row.get("recommended_product"):
            rec = intake_engine.recommend(intake_row)
            row["recommended_product"] = rec

    if args.dry_run:
        print(f"DRY RUN — would update confidence for {updated} rows.")
        return 0

    with PROSPECTS.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    print(f"SCORE_OK: {len(rows)} prospects scored, {updated} confidence values updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
