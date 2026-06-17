#!/usr/bin/env python3
"""Pilot Delivery Orchestrator — 14-day sprint execution and proof event logging."""

import csv
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "company" / "runtime"
PILOTS_DIR = RUNTIME_DIR / "pilots"
PILOTS_DIR.mkdir(parents=True, exist_ok=True)


# 14-Day Pilot Delivery Schedule
DELIVERY_SCHEDULE = {
    "day_1": {
        "phase": "Onboarding & Setup",
        "founder_tasks": [
            "Client intake call (30 min) — understand their current process, pain points",
            "Data mapping — decide what customer data to load into Dealix",
            "First dashboard setup — create team, add prospects, configure automation",
        ],
        "hours": 3,
        "deliverable": "Dashboard live with initial data loaded; team trained",
    },
    "day_2_to_3": {
        "phase": "Daily Support & Monitoring",
        "founder_tasks": [
            "Daily 15-min standup with client",
            "Monitor: Are they using the system?",
            "Log: # of prospects added, # of follow-ups sent, # of approvals given",
        ],
        "hours": 2,
        "deliverable": "Proof events logged (user activities, system actions)",
    },
    "day_4_to_7": {
        "phase": "Early Results & Quick Wins",
        "founder_tasks": [
            "Weekly sync (30 min) — show metrics: prospects tracked, follow-ups automated",
            "Identify early win (1 deal advanced, 1 follow-up successful)",
            "Adjust dashboard based on feedback",
        ],
        "hours": 3,
        "deliverable": "First proof events + testimonial quote",
    },
    "day_8_to_11": {
        "phase": "Proof Accumulation",
        "founder_tasks": [
            "Twice-weekly checkins (2×20 min each)",
            "Verify: prospect pipeline growing, follow-ups consistent",
            "Collect: before/after metrics on their sales process",
        ],
        "hours": 3,
        "deliverable": "5-10 proof events with quantified impact",
    },
    "day_12_to_14": {
        "phase": "Final Push & Case Study Prep",
        "founder_tasks": [
            "Final deep-dive call (45 min)",
            "Assemble proof pack: 5 screenshots + quote + metrics",
            "Ask renewal question: 'Want to continue at 3,999 SAR/mo?'",
        ],
        "hours": 4,
        "deliverable": "Proof Pack ready + renewal decision",
    },
}


def generate_pilot_contract(
    customer_name: str,
    company_name: str,
    start_date: str,
    price_sar: int = 499,
) -> dict[str, str]:
    """Generate pilot contract terms (for Moyasar payment + founder approval)."""
    end_date = datetime.fromisoformat(start_date) + timedelta(days=14)

    return {
        "contract_id": f"PILOT_{customer_name.replace(' ', '_')}_{start_date}",
        "customer_name": customer_name,
        "company_name": company_name,
        "service": "Dealix Sales Pipeline Pilot — 14-day proof sprint",
        "price_sar": price_sar,
        "currency": "SAR",
        "duration_days": 14,
        "start_date": start_date,
        "end_date": end_date.isoformat()[:10],
        "includes": [
            "Data import (up to 500 prospects)",
            "Dashboard setup & team training",
            "Daily founder support & approvals",
            "Proof event logging",
            "Final proof pack assembly",
        ],
        "excludes": [
            "Custom integrations (API)",
            "Dedicated delivery manager",
            "Advanced reporting",
        ],
        "renewal_option": "3,999 SAR/month (same customer, annual contract)",
        "payment_terms": "Upfront via Moyasar (test mode)",
        "cancellation": "No refunds; can cancel anytime after day 7",
        "status": "draft",
        "created_at": datetime.now().isoformat(),
    }


def initialize_pilot_project(
    customer_name: str,
    company_name: str,
    sector: str,
    pain_angle: str,
) -> dict[str, Any]:
    """Initialize a pilot project tracking record."""
    pilot_id = f"pilot_{customer_name.replace(' ', '_')}_{datetime.now().timestamp()}"
    pilot_dir = PILOTS_DIR / pilot_id
    pilot_dir.mkdir(parents=True, exist_ok=True)

    pilot = {
        "pilot_id": pilot_id,
        "customer_name": customer_name,
        "company_name": company_name,
        "sector": sector,
        "pain_angle": pain_angle,
        "status": "initialized",
        "start_date": datetime.now().isoformat()[:10],
        "day_started": 1,
        "day_current": 1,
        "end_date": (datetime.now() + timedelta(days=14)).isoformat()[:10],
        "proof_events": [],
        "metrics": {
            "prospects_added": 0,
            "followups_sent": 0,
            "deals_advanced": 0,
            "founder_hours_spent": 0,
        },
        "renewal_decision": None,  # "yes", "no", or null
        "proof_pack_status": "pending",
    }

    # Save pilot metadata
    pilot_meta_path = pilot_dir / "metadata.json"
    with open(pilot_meta_path, 'w', encoding='utf-8') as f:
        json.dump(pilot, f, ensure_ascii=False, indent=2)

    return pilot


def log_proof_event(
    pilot_id: str,
    event_type: str,
    description: str,
    metric_name: str = None,
    metric_value: Any = None,
) -> dict[str, Any]:
    """Log a proof event during pilot delivery.

    Event types:
    - prospect_added: Customer added X prospects to pipeline
    - followup_sent: Customer sent follow-up via Dealix
    - deal_advanced: Customer advanced a deal (cold → warm)
    - timeline_improvement: Customer closed deal faster
    - efficiency_gain: Customer saved time with automation
    - customer_quote: Customer testimonial/quote
    """
    event = {
        "event_id": f"event_{datetime.now().timestamp()}",
        "pilot_id": pilot_id,
        "event_type": event_type,
        "description": description,
        "timestamp": datetime.now().isoformat(),
        "metric_name": metric_name,
        "metric_value": metric_value,
    }

    # Append to pilot's events log
    pilot_dir = PILOTS_DIR / pilot_id
    events_path = pilot_dir / "proof_events.jsonl"

    try:
        with open(events_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + '\n')
    except (IOError, OSError):
        pass

    return event


def generate_daily_checklist(pilot_id: str, day: int) -> dict[str, Any]:
    """Generate founder's daily checklist for pilot delivery."""
    phase_key = f"day_{day}" if day <= 3 else f"day_{(day-1)//4 + 2}_to_{(day-1)//4 * 4 + 3}"
    phase = DELIVERY_SCHEDULE.get(phase_key, DELIVERY_SCHEDULE["day_1"])

    return {
        "pilot_id": pilot_id,
        "day": day,
        "phase": phase["phase"],
        "tasks": phase["founder_tasks"],
        "estimated_hours": phase["hours"] / 5,  # Assuming 5-day sprint weeks
        "deliverable": phase["deliverable"],
        "completed": False,
        "notes": "",
    }


def generate_proof_pack_template(pilot_id: str) -> dict[str, Any]:
    """Generate proof pack template for final delivery."""
    return {
        "pilot_id": pilot_id,
        "status": "in_progress",
        "components": {
            "title": "Case Study: Before/After Sales Results",
            "executive_summary": "Company increased sales productivity by X% in 14 days",
            "section_1_overview": {
                "title": "The Challenge",
                "content": "[Customer's original problem — copy from intake call notes]",
            },
            "section_2_solution": {
                "title": "Dealix Solution",
                "content": "[How Dealix solved it — what features they used]",
            },
            "section_3_results": {
                "title": "Results (14 days)",
                "metrics": [
                    {"name": "Prospects Tracked", "before": 0, "after": 0, "change": 0},
                    {"name": "Follow-ups/Day", "before": 0, "after": 0, "change": 0},
                    {"name": "Close Rate", "before": "0%", "after": "0%", "change": "0%"},
                    {"name": "Sales Cycle", "before": "0 days", "after": "0 days", "change": "0%"},
                ],
            },
            "section_4_testimonial": {
                "title": "Customer Quote",
                "quote": "[Get from final call]",
                "name": "[Customer name]",
                "company": "[Company]",
                "role": "[Role]",
            },
            "section_5_next_steps": {
                "title": "Moving Forward",
                "content": "[Renewal offer: 3,999 SAR/month ongoing support]",
            },
        },
        "pdf_sections": [
            "Title page",
            "Executive summary (1 page)",
            "Case study narrative (2 pages)",
            "Before/after metrics (1 page)",
            "Customer testimonial (1 page)",
        ],
        "created_date": datetime.now().isoformat(),
        "completion_target": "Day 14 EOD",
    }


def main() -> int:
    """Initialize and demonstrate pilot delivery orchestration."""
    print("🚀 Pilot Delivery Orchestrator")
    print("=" * 50)

    # Example: Initialize first pilot
    customer = "محمد"
    company = "عقارات الحمد"
    sector = "Real Estate"
    pain = "20 طلب عقاري شهرياً، لكن 30% بتضيع"

    print(f"\n📋 Initializing pilot for {customer} ({company})")

    # Generate contract
    start_date = datetime.now().isoformat()[:10]
    contract = generate_pilot_contract(customer, company, start_date)
    print(f"✅ Contract generated: {contract['contract_id']}")

    # Initialize project
    pilot = initialize_pilot_project(customer, company, sector, pain)
    pilot_id = pilot["pilot_id"]
    print(f"✅ Pilot initialized: {pilot_id}")

    # Generate Day 1 checklist
    day1_checklist = generate_daily_checklist(pilot_id, 1)
    print(f"✅ Day 1 checklist generated: {len(day1_checklist['tasks'])} tasks")

    # Log sample proof event
    event = log_proof_event(
        pilot_id,
        "prospect_added",
        "Customer added 50 prospects from Google Sheets",
        "prospects_added",
        50,
    )
    print(f"✅ Sample proof event logged: {event['event_type']}")

    # Generate proof pack template
    proof_pack = generate_proof_pack_template(pilot_id)
    print(f"✅ Proof pack template generated: {len(proof_pack['components'])} sections")

    # Save all to pilot directory
    pilot_dir = PILOTS_DIR / pilot_id
    with open(pilot_dir / "contract.json", 'w', encoding='utf-8') as f:
        json.dump(contract, f, ensure_ascii=False, indent=2)
    with open(pilot_dir / "day1_checklist.json", 'w', encoding='utf-8') as f:
        json.dump(day1_checklist, f, ensure_ascii=False, indent=2)
    with open(pilot_dir / "proof_pack_template.json", 'w', encoding='utf-8') as f:
        json.dump(proof_pack, f, ensure_ascii=False, indent=2)

    print(f"\n💾 All pilot files saved to: {pilot_dir}")
    print("\n✅ Pilot delivery orchestrator ready")
    print(f"Next: Founder sends contract to customer for Moyasar payment")

    return 0


if __name__ == '__main__':
    exit(main())
