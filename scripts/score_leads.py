"""Deterministic lead scoring.

Usage:
    python3 scripts/score_leads.py [--mode demo]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEADS_PATH = REPO_ROOT / "business" / "_data" / "leads.json"
OUT_PATH = REPO_ROOT / "business" / "_data" / "scored_leads.json"


# Segment weights: how likely each segment is to close at our price points
SEGMENT_WEIGHT = {
    "marketing_agency": 25,
    "training": 20,
    "consulting": 18,
    "b2b_services": 18,
    "logistics": 15,
    "real_estate": 12,
    "clinic": 10,
    "retail": 8,
}


def score_lead(lead: dict) -> dict:
    """Score a lead by its dimension scores. Returns {score, tier}."""
    total = (
        lead.get("fit", 0)
        + lead.get("pain_clarity", 0)
        + lead.get("budget_signal", 0)
        + lead.get("urgency", 0)
    )
    total = min(100, max(0, total))
    if total >= 80:
        tier = "A"
    elif total >= 60:
        tier = "B"
    elif total >= 40:
        tier = "C"
    else:
        tier = "D"
    return {**lead, "score": total, "tier": tier}


def score(account: dict) -> int:
    base = 30
    base += SEGMENT_WEIGHT.get(account.get("segment", ""), 5)
    if account.get("sourceNote"):
        base += 10
    if account.get("visibleSignal"):
        base += 10
    if account.get("weaknessHypothesis"):
        base += 10
    if account.get("demo"):
        base -= 5  # demo is not traction
    return min(100, max(0, base))


_DEMO_LEADS = [
    {"id": "demo-001", "name": "شركة النور للاستشارات", "segment": "consulting", "city": "Riyadh", "sourceType": "manual_research", "sourceNote": "", "visibleSignal": "No weekly pipeline cadence", "weaknessHypothesis": "Pipeline without rhythm", "recommendedOffer": "revenue_os", "stage": "qualified", "owner": "Founder", "reviewStatus": "not_started", "demo": True, "createdAt": "2026-06-21", "nextAction": "Generate outreach draft", "nextActionDate": "2026-06-22", "monthlyValue": 4999, "setupValue": 15000, "fit": 35, "pain_clarity": 28, "budget_signal": 18, "urgency": 8},
    {"id": "demo-002", "name": "مكتب الحلول اللوجستية", "segment": "logistics", "city": "Jeddah", "sourceType": "open_data", "sourceNote": "", "visibleSignal": "Manual shipment updates", "weaknessHypothesis": "No command center", "recommendedOffer": "command_center", "stage": "researched", "owner": "Founder", "reviewStatus": "not_started", "demo": True, "createdAt": "2026-06-21", "nextAction": "Qualify via call", "nextActionDate": "2026-06-23", "monthlyValue": 3999, "setupValue": 12000, "fit": 30, "pain_clarity": 22, "budget_signal": 15, "urgency": 6},
    {"id": "demo-003", "name": "أكاديمية المهارات", "segment": "training", "city": "Dammam", "sourceType": "referral", "sourceNote": "", "visibleSignal": "Weak post-course retention", "weaknessHypothesis": "No cohort renewal system", "recommendedOffer": "delivery_os", "stage": "researched", "owner": "Founder", "reviewStatus": "not_started", "demo": True, "createdAt": "2026-06-21", "nextAction": "Send one-pager", "nextActionDate": "2026-06-24", "monthlyValue": 2999, "setupValue": 9000, "fit": 28, "pain_clarity": 20, "budget_signal": 12, "urgency": 5},
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["demo"], default=None)
    args = parser.parse_args()

    if args.mode == "demo":
        scored = [score_lead(lead) for lead in _DEMO_LEADS]
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUT_PATH.write_text(
            json.dumps({"accounts": scored, "version": "1.0"}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"demo: scored {len(scored)} leads -> {OUT_PATH}")
        return 0

    if not LEADS_PATH.exists():
        print(f"missing: {LEADS_PATH}")
        return 1
    data = json.loads(LEADS_PATH.read_text(encoding="utf-8"))
    accounts = data.get("accounts", [])
    scored = []
    for a in accounts:
        a["score"] = score(a)
        scored.append(a)
    scored.sort(key=lambda a: a["score"], reverse=True)
    OUT_PATH.write_text(
        json.dumps({"accounts": scored, "version": "1.0"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"scored {len(scored)} -> {OUT_PATH}")
    for a in scored[:5]:
        print(f"  {a['score']:3d}  {a['id']}  {a['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
