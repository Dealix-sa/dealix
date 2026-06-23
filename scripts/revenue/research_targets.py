#!/usr/bin/env python3
"""Research target companies — stub, no external APIs.

This module is a manual research helper. It never scrapes, never calls any
external API, and never sends anything externally. It only provides a
structured checklist and a template so an operator can manually research
target companies and record findings with a traceable ``source_url``.

Usage:
    python scripts/revenue/research_targets.py            # print checklist
    python scripts/revenue/research_targets.py --template  # write template CSV
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import LEDGER_SCHEMAS, REPO_ROOT, ensure_ledgers, today_str, write_csv

RESEARCH_CHECKLIST = [
    "1. اختر مصدرًا واحدًا عامًا فقط (موقع شركة، دليل أعمال عام).",
    "2. ابحث يدويًا عن شركة سعودية عاملة لها موقع/تواصل عام.",
    "3. انسخ: company_name, sector, city, website, source_url.",
    "4. اكتب pain_hypothesis بناءً على الموقع العام فقط — لا تخمن بيانات خاصة.",
    "5. حدد verification_status: placeholder / partial / verified_public.",
    "6. تأكد أن source_url يبدأ بـ http ويمكن تتبعه.",
    "7. لا تضف بيانات شخصية حساسة (رقم هوية، عنوان منزل، تاريخ ميلاد).",
    "8. احفظ الصف في ledgers/prospects.csv بعد التحقق من validate_targets.py.",
]

TEMPLATE_ROW: dict[str, str] = {
    "company_name": "",
    "sector": "",
    "city": "",
    "website": "",
    "source_url": "",
    "verification_status": "",
    "owner_decision": "",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Research target companies (stub, no external APIs)")
    parser.add_argument("--template", action="store_true", help="Write an empty prospects template CSV")
    parser.add_argument("--output", default="ledgers/prospects.csv")
    args = parser.parse_args()

    print(f"Dealix Target Research — {today_str()}")
    print("=" * 60)
    print("This is a manual research helper. No external APIs. No scraping. No send.")
    print()
    for item in RESEARCH_CHECKLIST:
        print(item)

    if args.template:
        ensure_ledgers()
        out_path = REPO_ROOT / args.output
        fields = LEDGER_SCHEMAS["prospects"]
        write_csv(out_path, [], fields)
        print(f"\nWrote empty template to {out_path}")
        print("Fill it manually, then run validate_targets.py to verify source_url.")

    return 0


if __name__ == "__main__":
    sys.exit(main())