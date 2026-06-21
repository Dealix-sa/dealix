#!/usr/bin/env python3
"""Lead qualification and warm-intro targeting system."""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "company" / "runtime"
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)


# Saudi B2B sectors with highest conversion potential for Dealix
PRIORITY_SECTORS = {
    "real_estate": {
        "name_ar": "عقار",
        "pain": "العملاء والعروض يحتاجون pipeline ومتابعة منظمة",
        "offer": "Sales Pipeline OS",
        "weight": 10,  # Highest priority (most pain, highest CAC acceptance)
    },
    "distribution": {
        "name_ar": "توزيع وتجارة",
        "pain": "الطلبيات والتجار يحتاجون تنظيم ومتابعة يومية",
        "offer": "Revenue Pipeline OS",
        "weight": 9,
    },
    "saas": {
        "name_ar": "برمجيات وIT",
        "pain": "المبيعات بحاجة CRM وfollow-up منظم",
        "offer": "Growth Engine OS",
        "weight": 8,
    },
    "agencies": {
        "name_ar": "وكالات تسويق واستشارات",
        "pain": "العملاء والمشاريع بحاجة إدارة وتقارير",
        "offer": "Client Command Center OS",
        "weight": 7,
    },
    "restaurants": {
        "name_ar": "مطاعم وضيافة",
        "pain": "التقييمات والشكاوى بحاجة رد سريع ومتابعة",
        "offer": "Review Intelligence OS",
        "weight": 6,
    },
}


def score_warm_intro_potential(row: dict[str, str], sector_weight: int = 10) -> int:
    """Score a lead for warm-intro quality (0-100 scale).

    Warm intro quality = contact info + decision maker signals + pain alignment + sector weight.
    """
    score = 20  # Base score

    # Contact signals (critical for warm intro)
    if row.get("phone"):
        score += 25  # Must have phone for WhatsApp
    if row.get("website"):
        score += 10  # Website = likely established

    # Establishment signals
    try:
        count = int(float(row.get("user_rating_count") or 0))
        if count >= 100:
            score += 15  # Well-established, likely decision maker accessible
        elif count >= 50:
            score += 10
        elif count >= 20:
            score += 5
    except (ValueError, TypeError):
        pass

    # Rating signals (high rating = trustworthy contact point)
    try:
        rating = float(row.get("rating") or 0)
        if rating >= 4.5:
            score += 10  # Well-reviewed = good brand = accessible leadership
        elif rating >= 4.0:
            score += 5
    except (ValueError, TypeError):
        pass

    # Sector weight (strategic priority)
    score += sector_weight // 2

    return min(score, 100)


def qualify_leads_from_csv(csv_path: Path) -> list[dict[str, str]]:
    """Read real leads CSV and qualify for warm-intro outreach.

    Returns: List of top-scoring leads ready for founder manual verification + WhatsApp.
    """
    if not csv_path.exists():
        return []

    qualified = []
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row or not row.get('phone'):
                    continue

                # Get sector weight
                sector = row.get('segment', '').lower()
                sector_weight = PRIORITY_SECTORS.get(sector, {}).get('weight', 5)

                # Score for warm-intro potential
                score = score_warm_intro_potential(row, sector_weight)

                # Only include if score > 50 and has phone + name
                if score >= 50 and row.get('company_name'):
                    row['warm_intro_score'] = str(score)
                    row['qualified_date'] = datetime.now().isoformat()
                    qualified.append(row)
    except (IOError, OSError, csv.Error, UnicodeDecodeError):
        return []

    # Sort by score descending
    qualified.sort(key=lambda r: int(r.get('warm_intro_score', 0)), reverse=True)

    return qualified[:50]  # Top 50 leads per day


def deduplicate_targets(
    existing_targets: list[dict[str, str]],
    new_candidates: list[dict[str, str]]
) -> list[dict[str, str]]:
    """Merge new candidates with existing targets, avoiding duplicates.

    Returns: Updated list of unique targets.
    """
    existing_names = {t.get('company_name', '').strip().lower() for t in existing_targets}
    existing_phones = {t.get('phone', '').strip() for t in existing_targets if t.get('phone')}

    unique_new = []
    for candidate in new_candidates:
        name = candidate.get('company_name', '').strip().lower()
        phone = candidate.get('phone', '').strip()

        if name not in existing_names and phone not in existing_phones:
            unique_new.append(candidate)

    return existing_targets + unique_new


def read_existing_targets() -> list[dict[str, str]]:
    """Read existing warm intro targets CSV."""
    csv_path = RUNTIME_DIR / "warm_intro_targets.csv"

    if not csv_path.exists():
        return []

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader) if reader else []
    except (IOError, OSError, csv.Error, UnicodeDecodeError):
        return []


def format_for_warm_intro_targets(candidate: dict[str, str]) -> dict[str, str]:
    """Convert real lead to warm intro targets format."""
    # Extract first name from company name (for WhatsApp greeting)
    company = candidate.get('company_name', '')
    # Try to extract person name if present, else use company
    name = company.split()[0] if company else "Manager"

    return {
        'id': '',  # Will be assigned by parent script
        'name': name,
        'company': company,
        'role': 'Decision Maker',  # Assume decision maker until proven otherwise
        'sector': candidate.get('segment_name_ar', ''),
        'phone': candidate.get('phone', ''),
        'status': 'Ready',
        'date_sent': '',
        'outcome': '',
        'objection': '',
        'next_step': '',
        'notes': f"Score: {candidate.get('warm_intro_score', 0)} | {candidate.get('pain_angle', '')}",
    }


def generate_daily_lead_report(
    qualified_leads: list[dict[str, str]]
) -> str:
    """Generate markdown report of qualified leads for founder review."""
    report = [
        "# Dealix Daily Qualified Leads Report",
        "",
        f"Generated: {datetime.now().isoformat()}",
        f"Qualified leads (ready for WhatsApp): {len(qualified_leads)}",
        "",
        "## Top Candidates for Warm Intro Outreach",
        "",
        "| # | Company | Sector | Phone | Offer | Score | Action |",
        "|---:|---|---|---|---|---:|---|",
    ]

    for i, lead in enumerate(qualified_leads[:20], start=1):
        company = lead.get('company_name', '—')
        sector = lead.get('segment_name_ar', '—')
        phone = lead.get('phone', '—')
        offer = lead.get('recommended_offer', '—').replace(' OS', '')
        score = lead.get('warm_intro_score', '—')

        report.append(
            f"| {i} | {company} | {sector} | {phone} | {offer} | {score} | "
            f"[WhatsApp](https://wa.me/{phone.replace('+', '').replace(' ', '')}) |"
        )

    report.extend([
        "",
        "## Instructions for Founder",
        "",
        "1. Review the top 10 companies above",
        "2. Identify which ones you have warm intros for (or can get one)",
        "3. Copy their details to `/warm_intro_targets.csv`",
        "4. Send first WhatsApp during morning ritual (8:15 AM)",
        "",
    ])

    return "\n".join(report) + "\n"


def main() -> int:
    """Main lead qualification workflow."""
    print("🔍 Dealix Lead Qualification Engine")
    print("=" * 50)

    # Step 1: Try to read real leads from today's Google Places query
    today = datetime.now().isoformat()[:10]
    real_leads_path = RUNTIME_DIR / "places" / today / "real_leads.csv"

    if real_leads_path.exists():
        print(f"📊 Found real leads: {real_leads_path}")
        qualified = qualify_leads_from_csv(real_leads_path)
        print(f"✅ Qualified {len(qualified)} leads for warm intro potential")
    else:
        print(f"⚠️  No real leads found for today. Using fallback prospects.")
        qualified = []

    # Step 2: Read existing targets
    existing_targets = read_existing_targets()
    print(f"📋 Existing targets: {len(existing_targets)}")

    # Step 3: Deduplicate and merge
    # (For now, just show what we have; don't auto-merge without founder approval)

    # Step 4: Generate report for founder review
    if qualified:
        report = generate_daily_lead_report(qualified)
        report_path = RUNTIME_DIR / f"daily_qualified_leads_{today}.md"
        report_path.write_text(report, encoding='utf-8')
        print(f"📄 Report generated: {report_path}")

    # Step 5: Save qualified leads JSON (for AI agents to reference)
    if qualified:
        qualified_json = RUNTIME_DIR / f"qualified_leads_{today}.json"
        with open(qualified_json, 'w', encoding='utf-8') as f:
            json.dump(qualified, f, ensure_ascii=False, indent=2)
        print(f"💾 Qualified leads JSON: {qualified_json}")

    print("\n✅ Lead qualification complete")
    print(f"Next step: Founder reviews report and adds to warm_intro_targets.csv")

    return 0


if __name__ == '__main__':
    exit(main())
