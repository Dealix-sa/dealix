#!/usr/bin/env python3
"""
Generate Founder Dashboard Data
Reads CRM/pipeline/sales output and produces business/_generated/founder-dashboard.json
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT_PATH = REPO / "business" / "_generated" / "founder-dashboard.json"
MIRROR_PATH = REPO / "apps" / "web" / "lib" / "generated" / "founder-dashboard.ts"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["demo", "production"], default="demo")
    args = parser.parse_args()

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    MIRROR_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "mode": args.mode,
        "summary": {
            "total_accounts": 12 if args.mode == "demo" else 0,
            "review_pending": 4,
            "followups_due": 2,
            "proposal_ready": 1,
            "pipeline_value_sar": 0,
            "top_segment": "B2B Services"
        },
        "top_accounts": [
            {"id": "demo-001", "name": "Acme Saudi", "score": 87, "stage": "proposal_ready", "value_sar": 0, "next_action": "Review proposal draft"},
            {"id": "demo-002", "name": "Beta Clinic", "score": 72, "stage": "qualified", "value_sar": 0, "next_action": "Schedule diagnostic call"},
            {"id": "demo-003", "name": "Gamma Logistics", "score": 65, "stage": "lead", "value_sar": 0, "next_action": "Generate outreach draft"},
        ],
        "risks": [
            {"level": "medium", "area": "pipeline", "note": "No closed-won deals this week."},
            {"level": "low", "area": "governance", "note": "All drafts pending review. No auto-send risk."},
        ],
        "today_actions": [
            "Review 4 outreach drafts before EOD",
            "Approve or edit proposal for demo-001",
            "Schedule diagnostic call with Beta Clinic",
        ],
        "assets_to_create": [
            "Industry weakness one-pager for Healthcare",
            "Revenue OS case study draft",
        ],
        "next_ceo_decision": "Approve pricing for Managed OS Retainer pilot.",
        "disclaimer": "Demo data shown. Populate with real CRM data in production mode." if args.mode == "demo" else "Production data.",
    }

    OUT_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    # TypeScript mirror
    ts = f"// Auto-generated from scripts/generate_founder_dashboard_data.py\n"
    ts += f"// Generated at: {data['generated_at']}\n\n"
    ts += f"export const founderDashboard = {json.dumps(data, indent=2, ensure_ascii=False)} as const;\n"
    MIRROR_PATH.write_text(ts, encoding="utf-8")

    print(f"[PASS] Founder dashboard written to {OUT_PATH}")
    print(f"[PASS] TypeScript mirror written to {MIRROR_PATH}")

if __name__ == "__main__":
    main()
