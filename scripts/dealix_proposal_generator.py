#!/usr/bin/env python3
"""
Dealix Proposal Generator
=========================
Generates a bilingual (AR/EN) proposal for a lead, ready for founder review.

Usage:
  python3 scripts/dealix_proposal_generator.py \
    --company "شركة نجم للعقارات" \
    --contact "أحمد العتيبي" \
    --sector real_estate \
    --tier sprint          # sprint | revenue_os | command_center | delivery_os | review_os

  python3 scripts/dealix_proposal_generator.py --list-sectors

Doctrine: Generates drafts only. Nothing sends automatically. Founder reviews before any delivery.
"""

from __future__ import annotations

import argparse
import json
import random
import string
import sys
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PITCHES_FILE = REPO_ROOT / "data/outreach/sector_pitches.json"
TEMPLATES_DIR = REPO_ROOT / "data/templates"
OUTPUT_DIR = REPO_ROOT / "reports/proposals"

TIER_MAP = {
    "sprint": {
        "label_ar": "برنامج الأسبوع المكثف",
        "label_en": "7-Day Sprint",
        "setup": 499,
        "monthly": 0,
        "template": "proposal_499_sar_ar.md",
        "currency": "SAR",
    },
    "revenue_os": {
        "label_ar": "Revenue OS",
        "label_en": "Revenue OS",
        "setup": 18_000,
        "monthly": 5_000,
        "template": "proposal_revenue_os_ar.md",
        "currency": "SAR",
    },
    "command_center": {
        "label_ar": "Command Center OS",
        "label_en": "Command Center OS",
        "setup": 35_000,
        "monthly": 9_000,
        "template": "proposal_command_center_ar.md",
        "currency": "SAR",
    },
    "delivery_os": {
        "label_ar": "Delivery OS",
        "label_en": "Delivery OS",
        "setup": 25_000,
        "monthly": 6_000,
        "template": "proposal_revenue_os_ar.md",  # reuse revenue_os structure
        "currency": "SAR",
    },
    "review_os": {
        "label_ar": "Review & Reputation OS",
        "label_en": "Review & Reputation OS",
        "setup": 12_000,
        "monthly": 3_500,
        "template": "proposal_revenue_os_ar.md",  # reuse revenue_os structure
        "currency": "SAR",
    },
}

SECTOR_TIER_RECOMMENDATION = {
    "real_estate": "review_os",
    "clinic": "review_os",
    "logistics": "command_center",
    "training": "delivery_os",
    "marketing_agency": "revenue_os",
    "b2b_services": "revenue_os",
}


def _load_pitches() -> dict:
    if not PITCHES_FILE.exists():
        print(f"[ERROR] Sector pitches not found: {PITCHES_FILE}")
        sys.exit(1)
    with PITCHES_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def _proposal_id() -> str:
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"DLX-{date.today().strftime('%Y%m%d')}-{suffix}"


def _fill_template(template_text: str, fields: dict) -> str:
    result = template_text
    for key, value in fields.items():
        result = result.replace("{{" + key + "}}", str(value))
    return result


def generate_proposal(
    company: str,
    contact: str,
    sector: str,
    tier_key: str,
    custom_kpi_ar: str = "تحسين مؤشر رئيسي يتفق عليه في جلسة الاستلام",
    current_response_time: str = "24 ساعة أو أكثر",
    dry_run: bool = False,
) -> Path | None:
    pitches = _load_pitches()
    sectors = pitches.get("sectors", {})

    if sector not in sectors:
        print(f"[ERROR] Unknown sector: {sector}. Use --list-sectors.")
        sys.exit(1)
    if tier_key not in TIER_MAP:
        print(f"[ERROR] Unknown tier: {tier_key}. Choose from: {', '.join(TIER_MAP)}")
        sys.exit(1)

    sector_data = sectors[sector]
    tier = TIER_MAP[tier_key]
    recommended = SECTOR_TIER_RECOMMENDATION.get(sector, "revenue_os")

    template_path = TEMPLATES_DIR / tier["template"]
    if not template_path.exists():
        print(f"[ERROR] Template not found: {template_path}")
        sys.exit(1)

    template_text = template_path.read_text(encoding="utf-8")
    proposal_id = _proposal_id()
    today = date.today()
    proposed_start = today + timedelta(days=7)
    expiry = today + timedelta(days=14)

    fields = {
        "company_name": company,
        "contact_name": contact,
        "date": today.strftime("%Y-%m-%d"),
        "sector_ar": sector_data["label_ar"],
        "sector_en": sector_data["label_en"],
        "pain_ar": sector_data["pain_ar"],
        "pain_en": sector_data["pain_en"],
        "proposal_id": proposal_id,
        "proposed_start_date": proposed_start.strftime("%Y-%m-%d"),
        "expiry_date": expiry.strftime("%Y-%m-%d"),
        "custom_kpi_ar": custom_kpi_ar,
        "current_response_time": current_response_time,
        "payment_url": "[رابط الدفع — يُضاف قبل الإرسال]",
        "target_hours_saved": "5",
        "target_response_rate": "40",
        "pain_statement_ar": sector_data["pain_ar"],
        "pain_statement_en": sector_data["pain_en"],
    }

    filled = _fill_template(template_text, fields)

    if dry_run:
        print("=" * 70)
        print(f"[DRY RUN] Proposal preview — {proposal_id}")
        print("=" * 70)
        print(filled[:2000] + ("\n...[truncated]" if len(filled) > 2000 else ""))
        print("=" * 70)
        return None

    out_dir = OUTPUT_DIR / today.strftime("%Y-%m-%d")
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in company)
    out_file = out_dir / f"{safe_name}_{tier_key}_{proposal_id}.md"
    out_file.write_text(filled, encoding="utf-8")

    # Print summary for founder
    print()
    print("━" * 65)
    print("📋 PROPOSAL GENERATED — REQUIRES FOUNDER REVIEW")
    print("━" * 65)
    print(f"  Company     : {company}")
    print(f"  Contact     : {contact}")
    print(f"  Sector      : {sector_data['label_ar']} ({sector_data['label_en']})")
    print(f"  Tier        : {tier['label_ar']} ({tier['label_en']})")
    print(f"  Setup       : {tier['setup']:,} SAR")
    if tier["monthly"]:
        print(f"  Monthly     : {tier['monthly']:,} SAR/mo")
    print(f"  Proposal ID : {proposal_id}")
    print(f"  Valid Until : {expiry}")
    print(f"  File        : {out_file}")
    if tier_key != recommended:
        print()
        print(f"  ⚠️  Note: recommended tier for {sector} is '{recommended}'.")
        print(f"     Selling the diagnostic first is always better.")
    print()
    print("  NEXT STEPS (founder checklist):")
    print("  [ ] Review pain_ar and custom_kpi_ar — customize to the lead")
    print("  [ ] Add payment_url before sending")
    print("  [ ] Run free diagnostic first if not done yet")
    print("  [ ] Send only after explicit founder approval")
    print("━" * 65)
    print()

    return out_file


def list_sectors(pitches: dict) -> None:
    print()
    print("Available sectors:")
    print()
    sectors = pitches.get("sectors", {})
    recs = SECTOR_TIER_RECOMMENDATION
    for key, data in sectors.items():
        recommended = recs.get(key, "revenue_os")
        tier = TIER_MAP[recommended]
        print(f"  {key:<20} {data['label_ar']} / {data['label_en']}")
        print(f"  {'':20} Recommended: {recommended} — {tier['setup']:,} SAR setup + {tier['monthly']:,}/mo")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a bilingual Dealix proposal (founder review required before sending)"
    )
    parser.add_argument("--company", help="Company name (Arabic or English)")
    parser.add_argument("--contact", help="Contact person name", default="الاسم")
    parser.add_argument("--sector", help="Sector key (use --list-sectors to see options)")
    parser.add_argument(
        "--tier",
        choices=list(TIER_MAP.keys()),
        default=None,
        help="Offer tier (default: recommended for sector)",
    )
    parser.add_argument(
        "--kpi",
        help="Custom KPI in Arabic for the proposal",
        default="تحسين مؤشر رئيسي يتفق عليه في جلسة الاستلام",
    )
    parser.add_argument("--response-time", default="24 ساعة أو أكثر", help="Current response time for the lead")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing file")
    parser.add_argument("--list-sectors", action="store_true", help="Show all available sectors")

    args = parser.parse_args()
    pitches = _load_pitches()

    if args.list_sectors:
        list_sectors(pitches)
        return

    if not args.company or not args.sector:
        parser.error("--company and --sector are required (or use --list-sectors)")

    tier_key = args.tier or SECTOR_TIER_RECOMMENDATION.get(args.sector, "revenue_os")

    generate_proposal(
        company=args.company,
        contact=args.contact,
        sector=args.sector,
        tier_key=tier_key,
        custom_kpi_ar=args.kpi,
        current_response_time=args.response_time,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
