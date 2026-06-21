#!/usr/bin/env python3
"""
Validate prospects ledger — enforces quality gates before drafts are generated.

Checks:
  - source_url must be present
  - company_name must be present
  - verification_status must be a known value
  - owner_decision must be a known value
  - do_not_contact rows are never promoted

Promotes rows that pass all checks from 'new'/'needs_research' to 'ready_for_review'
ONLY when source_url, company_name, and pain_hypothesis are all present.

Usage:
    python scripts/founder/validate_targets.py
    python scripts/founder/validate_targets.py --promote
    python scripts/founder/validate_targets.py --dry-run
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PROSPECTS = ROOT / "ledgers" / "prospects.csv"
SUPPRESSION = ROOT / "ledgers" / "suppression_list.csv"

SCHEMA = [
    "company_name", "sector", "city", "website", "source_url",
    "contact_page_url", "public_email", "phone", "linkedin_url",
    "verification_status", "confidence", "pain_hypothesis",
    "dealix_angle", "recommended_product", "message_stage",
    "next_action", "owner_decision",
]

VALID_STATUSES = {
    "new", "needs_research", "ready_for_review",
    "approved_to_send", "sent", "replied", "not_fit", "do_not_contact",
}
VALID_DECISIONS = {"review", "approve", "hold", "reject", "do_not_contact"}


def load_suppression() -> set[str]:
    suppressed: set[str] = set()
    if not SUPPRESSION.exists():
        return suppressed
    try:
        with SUPPRESSION.open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                val = (row.get("company_name") or row.get("email") or row.get("phone") or "").strip().lower()
                if val:
                    suppressed.add(val)
    except Exception:
        pass
    return suppressed


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate prospect targets")
    parser.add_argument("--promote", action="store_true", help="Auto-promote qualifying rows to ready_for_review")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    if not PROSPECTS.exists():
        print("WARN: ledgers/prospects.csv not found.")
        return 0

    with PROSPECTS.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    suppressed = load_suppression()
    errors: list[str] = []
    warnings: list[str] = []
    promoted = 0
    suppression_hits = 0

    for i, row in enumerate(rows, 1):
        name = row.get("company_name", "").strip()
        status = row.get("verification_status", "").strip()
        decision = row.get("owner_decision", "").strip()

        # Suppression check
        name_lower = name.lower()
        if name_lower in suppressed:
            suppression_hits += 1
            row["verification_status"] = "do_not_contact"
            row["owner_decision"] = "do_not_contact"
            warnings.append(f"Row {i} '{name}': matched suppression list → do_not_contact")
            continue

        # Skip protected rows
        if status in ("do_not_contact",):
            continue

        # Required fields
        if not name:
            errors.append(f"Row {i}: missing company_name")
        if not row.get("source_url", "").strip():
            errors.append(f"Row {i} '{name}': missing source_url (required for verification)")

        # Valid enum values
        if status and status not in VALID_STATUSES:
            errors.append(f"Row {i} '{name}': unknown verification_status '{status}'")
        if decision and decision not in VALID_DECISIONS:
            errors.append(f"Row {i} '{name}': unknown owner_decision '{decision}'")

        # Auto-promote
        if args.promote and status in ("new", "needs_research", ""):
            if (name and row.get("source_url", "").strip() and row.get("pain_hypothesis", "").strip()):
                row["verification_status"] = "ready_for_review"
                promoted += 1

    print(f"Validated: {len(rows)} rows")
    print(f"Suppression hits: {suppression_hits}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    if args.promote:
        print(f"Promoted to ready_for_review: {promoted}")

    for e in errors:
        print(f"  ERROR: {e}")
    for w in warnings:
        print(f"  WARN:  {w}")

    if args.dry_run:
        print("DRY RUN — no changes written.")
        return 1 if errors else 0

    with PROSPECTS.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    if errors:
        print("VALIDATE_FAIL: fix errors above before generating drafts.")
        return 1

    print("VALIDATE_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
