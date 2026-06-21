#!/usr/bin/env python3
"""
Import prospect targets into ledgers/prospects.csv.

Sources checked (in order):
  1. CSV file passed via --file argument
  2. company/lead_research/*/web_lead_research.csv (auto-discovered, newest 3)
  3. founder_os/output/*/daily_targets.csv (auto-discovered, newest 3)

Deduplicates by company_name+website. Never overwrites do_not_contact rows.
Usage:
    python scripts/founder/import_targets.py
    python scripts/founder/import_targets.py --file data/new_leads.csv
    python scripts/founder/import_targets.py --file data/new_leads.csv --dry-run
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROSPECTS = ROOT / "ledgers" / "prospects.csv"

SCHEMA = [
    "company_name", "sector", "city", "website", "source_url",
    "contact_page_url", "public_email", "phone", "linkedin_url",
    "verification_status", "confidence", "pain_hypothesis",
    "dealix_angle", "recommended_product", "message_stage",
    "next_action", "owner_decision",
]

PROTECTED_STATUSES = {"do_not_contact", "sent", "replied"}


def _key(row: dict) -> str:
    return (row.get("company_name") or "").strip().lower()


def _dedup_key(row: dict) -> str:
    name = (row.get("company_name") or "").strip().lower()
    site = (row.get("website") or "").strip().lower()
    return f"{name}|{site}"


def read_prospects() -> list[dict[str, str]]:
    if not PROSPECTS.exists():
        PROSPECTS.parent.mkdir(parents=True, exist_ok=True)
        return []
    with PROSPECTS.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_prospects(rows: list[dict[str, str]]) -> None:
    with PROSPECTS.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def normalize_row(raw: dict[str, str]) -> dict[str, str]:
    row: dict[str, str] = {}
    for field in SCHEMA:
        row[field] = raw.get(field) or raw.get(field.replace("_", " "), "")
    if not row["company_name"]:
        row["company_name"] = (
            raw.get("company") or raw.get("title") or raw.get("name") or ""
        )
    if not row["verification_status"]:
        row["verification_status"] = "new"
    if not row["owner_decision"]:
        row["owner_decision"] = "review"
    if not row["pain_hypothesis"]:
        row["pain_hypothesis"] = (
            raw.get("pain_angle") or raw.get("snippet") or raw.get("notes") or ""
        )
    if not row["recommended_product"]:
        row["recommended_product"] = (
            raw.get("recommended_offer") or raw.get("core_offer") or raw.get("offer") or ""
        )
    if not row["sector"]:
        row["sector"] = raw.get("segment") or ""
    if not row["phone"]:
        row["phone"] = raw.get("contact") or ""
    return row


def collect_sources(extra_file: Path | None) -> list[Path]:
    paths: list[Path] = []
    if extra_file and extra_file.exists():
        paths.append(extra_file)
    lead_dir = ROOT / "company" / "lead_research"
    if lead_dir.exists():
        paths += sorted(lead_dir.glob("*/web_lead_research.csv"))[-3:]
    founder_dir = ROOT / "founder_os" / "output"
    if founder_dir.exists():
        paths += sorted(founder_dir.glob("*/daily_targets.csv"))[-3:]
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Import targets into prospects ledger")
    parser.add_argument("--file", type=Path, help="CSV file to import")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    existing = read_prospects()
    seen = {_dedup_key(r) for r in existing if r.get("verification_status") not in PROTECTED_STATUSES}
    protected = {_dedup_key(r) for r in existing if r.get("verification_status") in PROTECTED_STATUSES}

    sources = collect_sources(args.file)
    if not sources:
        print("WARN: No source files found. Pass --file or populate company/lead_research/.")
        return 0

    new_rows: list[dict[str, str]] = []
    skipped_dup = 0
    skipped_protected = 0

    for src in sources:
        try:
            with src.open("r", encoding="utf-8-sig", newline="") as f:
                for raw in csv.DictReader(f):
                    row = normalize_row(raw)
                    if not row["company_name"]:
                        continue
                    dk = _dedup_key(row)
                    if dk in protected:
                        skipped_protected += 1
                        continue
                    if dk in seen:
                        skipped_dup += 1
                        continue
                    seen.add(dk)
                    new_rows.append(row)
        except Exception as e:
            print(f"WARN: could not read {src}: {e}")

    print(f"Sources scanned:     {len(sources)}")
    print(f"New targets found:   {len(new_rows)}")
    print(f"Duplicates skipped:  {skipped_dup}")
    print(f"Protected skipped:   {skipped_protected}")

    if args.dry_run:
        print("DRY RUN — no changes written.")
        for r in new_rows[:5]:
            print(f"  Would add: {r['company_name']} ({r['sector']}) — {r['website']}")
        return 0

    all_rows = existing + new_rows
    write_prospects(all_rows)
    print(f"IMPORT_OK: {PROSPECTS} now has {len(all_rows)} rows ({len(new_rows)} added).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
