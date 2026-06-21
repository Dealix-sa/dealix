#!/usr/bin/env python3
"""
Manual target research workflow helper. Does NOT scrape.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import REPO_ROOT, load_csv, today_str

REQUIRED_COLUMNS = {"company", "sector", "city", "source_url", "verification_status", "confidence"}

CHECKLIST = [
    "1. افتح مصدرًا واحدًا فقط من data/outreach/target_sources.example.csv",
    "2. ابحث يدويًا عن شركة عاملة في السعودية ولها موقع/تواصل عام",
    "3. انسخ: company, sector, city, website, public_contact, source_url",
    "4. اكتب pain_hypothesis بناءً على الموقع العام (لا تخمن بيانات خاصة)",
    "5. حدد confidence: 0.3 placeholder, 0.5 partial, 0.7 verified_public",
    "6. حدد verification_status: placeholder / partial / verified_public",
    "7. لا تضف بيانات شخصية حساسة (رقم هوية، عنوان منزل، تاريخ ميلاد)",
    "8. احفظ الصف في data/outreach/research_queue.csv",
]


def validate_csv(path: Path) -> list[str]:
    issues: list[str] = []
    rows = load_csv(path)
    if not rows:
        return [f"Empty or missing file: {path}"]
    fields = set(rows[0].keys())
    missing = REQUIRED_COLUMNS - fields
    if missing:
        issues.append(f"Missing columns {missing}")
    for idx, row in enumerate(rows, start=2):
        for col in REQUIRED_COLUMNS:
            if not row.get(col, "").strip():
                issues.append(f"Row {idx}: empty {col}")
        try:
            conf = float(row.get("confidence", "0"))
            if not 0 <= conf <= 1:
                issues.append(f"Row {idx}: confidence must be 0-1")
        except ValueError:
            issues.append(f"Row {idx}: confidence must be numeric")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Manual target research workflow")
    parser.add_argument("--validate", help="Validate a CSV file")
    args = parser.parse_args()

    print(f"Dealix Manual Target Research Workflow — {today_str()}")
    print("=" * 60)
    for item in CHECKLIST:
        print(item)

    if args.validate:
        issues = validate_csv(REPO_ROOT / args.validate)
        if issues:
            print("\n❌ Validation issues:")
            for issue in issues:
                print(f"  {issue}")
            return 1
        print("\n✅ CSV validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
