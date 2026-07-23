#!/usr/bin/env python3
"""Generate approval-first outreach drafts from a seed prospect CSV.

This script does NOT send messages. It creates a review queue for the founder.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "prospects" / "icp_seed_accounts_saudi.csv"
OUTPUT_DIR = ROOT / "reports" / "daily_growth"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT = OUTPUT_DIR / f"outreach_queue_{datetime.now().strftime('%Y-%m-%d')}.csv"

@dataclass
class Prospect:
    company: str
    sector: str
    city: str
    website: str
    public_contact: str
    likely_pain: str
    best_offer: str
    priority: str
    notes: str


def load_prospects() -> list[Prospect]:
    if not INPUT.exists():
        raise SystemExit(f"Missing input file: {INPUT}")
    with INPUT.open("r", encoding="utf-8-sig", newline="") as f:
        return [Prospect(**row) for row in csv.DictReader(f)]


def draft_message(p: Prospect) -> str:
    return (
        f"السلام عليكم، لاحظنا أن {p.company} تعمل في مجال {p.sector} في {p.city}. "
        f"غالبًا أحد أكبر فرص النمو عندكم هو: {p.likely_pain}. "
        f"في Dealix نقدر نبدأ معكم بـ {p.best_offer}: تشخيص/تنظيم فرص ومتابعة ورسائل قابلة للمراجعة بدون إرسال آلي أو وعود غير واقعية. "
        f"هل يناسبكم نرسل لكم ملخص تشخيص بسيط يوضح أين ممكن تتحسن المتابعة والمبيعات؟"
    )


def main() -> None:
    prospects = sorted(load_prospects(), key=lambda p: (p.priority != "High", p.company.lower()))
    fields = [
        "date", "company", "sector", "city", "website", "public_contact",
        "likely_pain", "best_offer", "priority", "draft_message",
        "approval_status", "outcome", "follow_up_due", "notes"
    ]
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for p in prospects[:25]:
            writer.writerow({
                "date": datetime.now().date().isoformat(),
                "company": p.company,
                "sector": p.sector,
                "city": p.city,
                "website": p.website,
                "public_contact": p.public_contact,
                "likely_pain": p.likely_pain,
                "best_offer": p.best_offer,
                "priority": p.priority,
                "draft_message": draft_message(p),
                "approval_status": "needs_founder_review",
                "outcome": "pending",
                "follow_up_due": "",
                "notes": p.notes,
            })
    print(f"Created approval queue: {OUTPUT}")
    print("Rule: review manually before any external outreach. This script never sends messages.")

if __name__ == "__main__":
    main()
