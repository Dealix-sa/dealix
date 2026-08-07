#!/usr/bin/env python3
"""Merge researched sector target CSVs into the founder's intake list.

Reads every data/outreach/research/*.csv (produced by sector research) and merges
them into data/outreach/saudi_target_intake.csv, de-duplicating by normalized
company name. The intake list stays local (gitignored). Never sends anything,
never invents data — it only consolidates rows that already exist.

Usage:
    python3 scripts/merge_research_targets.py
    python3 scripts/merge_research_targets.py --dry-run
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RESEARCH_DIR = REPO_ROOT / "data" / "outreach" / "research"
INTAKE = REPO_ROOT / "data" / "outreach" / "saudi_target_intake.csv"
FIELDS = ["company", "sector", "city", "contact_name", "contact_email", "language", "signal_note", "priority"]
VALID_SECTORS = {"real_estate", "clinic", "logistics", "training", "marketing_agency", "b2b_services"}


def _norm(name: str) -> str:
    return re.sub(r"\s+", " ", (name or "").strip().lower())


def read_csv_rows(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(r for r in fh if not r.lstrip().startswith("#"))
        for row in reader:
            row = {(k or "").strip(): (v or "").strip() for k, v in row.items()}
            if row.get("company") and row.get("sector"):
                rows.append(row)
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not RESEARCH_DIR.exists():
        print(f"لا يوجد مجلد بحث: {RESEARCH_DIR}")
        return 1

    merged: dict[str, dict] = {}
    skipped_bad_sector = 0

    # Existing intake first (preserve any emails the founder already filled).
    if INTAKE.exists():
        for row in read_csv_rows(INTAKE):
            merged[_norm(row["company"])] = {k: row.get(k, "") for k in FIELDS}

    sources = sorted(RESEARCH_DIR.glob("*.csv"))
    per_source: dict[str, int] = {}
    for src in sources:
        count = 0
        for row in read_csv_rows(src):
            if row.get("sector") not in VALID_SECTORS:
                skipped_bad_sector += 1
                continue
            key = _norm(row["company"])
            clean = {k: row.get(k, "") for k in FIELDS}
            if key in merged:
                # Fill a missing email if this source has one; keep existing otherwise.
                if not merged[key].get("contact_email") and clean.get("contact_email"):
                    merged[key]["contact_email"] = clean["contact_email"]
            else:
                merged[key] = clean
                count += 1
        per_source[src.name] = count

    rows = sorted(merged.values(), key=lambda r: (r.get("priority") or "3", r.get("sector") or ""))
    with_email = sum(1 for r in rows if r.get("contact_email"))

    print(f"المصادر: {len(sources)}")
    for name, c in per_source.items():
        print(f"  {name}: +{c} جديدة")
    print(f"الإجمالي بعد الدمج: {len(rows)} شركة  ({with_email} منها بإيميل، الباقي تأكّده من الموقع)")
    if skipped_bad_sector:
        print(f"تُخطّيت {skipped_bad_sector} صفوف بقطاع غير صالح")

    if args.dry_run:
        print("\n[dry-run] لم يُكتب شيء.")
        return 0

    INTAKE.parent.mkdir(parents=True, exist_ok=True)
    with INTAKE.open("w", encoding="utf-8", newline="") as fh:
        fh.write("# قائمة استهداف مدموجة من بحث القطاعات — تأكّد من كل إيميل قبل الإرسال.\n")
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nكُتبت: {INTAKE}")
    print("التالي:  make outreach   ثم راجع وأرسل بنفسك.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
