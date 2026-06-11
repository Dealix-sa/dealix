#!/usr/bin/env python3
"""
Dealix Lead Scorer
Scores leads by fit, pain clarity, budget signal, and urgency.
Outputs JSON with scores and tier.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

def score_lead(lead: dict) -> dict:
    fit = min(lead.get("fit", 0), 40)
    pain = min(lead.get("pain_clarity", 0), 30)
    budget = min(lead.get("budget_signal", 0), 20)
    urgency = min(lead.get("urgency", 0), 10)
    total = fit + pain + budget + urgency
    tier = "A" if total >= 80 else "B" if total >= 60 else "C" if total >= 40 else "D"
    return {
        **lead,
        "score": total,
        "tier": tier,
        "scored_at": datetime.utcnow().isoformat() + "Z",
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["demo", "production"], default="demo")
    parser.add_argument("--input", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if args.mode == "demo":
        leads = [
            {"id": "demo-001", "company": "Acme Saudi", "sector": "B2B Services", "fit": 35, "pain_clarity": 28, "budget_signal": 18, "urgency": 8},
            {"id": "demo-002", "company": "Beta Clinic", "sector": "Healthcare", "fit": 30, "pain_clarity": 22, "budget_signal": 15, "urgency": 5},
            {"id": "demo-003", "company": "Gamma Logistics", "sector": "Logistics", "fit": 25, "pain_clarity": 20, "budget_signal": 12, "urgency": 8},
        ]
    else:
        inp = Path(args.input) if args.input else REPO / "data" / "imports" / "leads_scored.json"
        if not inp.exists():
            print("[FAIL] No input leads file for production mode.")
            return
        leads = json.loads(inp.read_text(encoding="utf-8"))
        if isinstance(leads, dict):
            leads = leads.get("leads", [])

    scored = [score_lead(l) for l in leads]
    out_path = Path(args.output) if args.output else REPO / "business" / "crm" / "exports" / f"leads-scored-{datetime.utcnow().strftime('%Y-%m-%d')}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(scored, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[PASS] Scored {len(scored)} leads. Output: {out_path}")
    for s in scored:
        print(f"  {s['id']} {s['company']}: {s['score']} ({s['tier']})")

if __name__ == "__main__":
    main()
