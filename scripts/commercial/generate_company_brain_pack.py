#!/usr/bin/env python3
"""Generate the Company Brain launch pack.

Local-only generator. It creates product, pain, proposal, and negotiation notes
for founder review.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "reports" / "commercial"

SERVICES = [
    {
        "service": "Company Brain OS",
        "buyer": "CEO / Founder / GM",
        "pain": "unclear daily priorities across revenue, ops, and risk",
        "first_offer": "7-Day Operating Diagnostic",
        "deliverable": "daily CEO decision, risk radar, 30-day execution plan",
    },
    {
        "service": "Revenue Command Room OS",
        "buyer": "Sales Director / Founder",
        "pain": "pipeline and follow-up not visible enough",
        "first_offer": "7-Day Revenue Command Room Sprint",
        "deliverable": "hot opportunities, overdue follow-ups, proposal status",
    },
    {
        "service": "Follow-up Recovery OS",
        "buyer": "Sales / Operations Manager",
        "pain": "inquiries and conversations are not converted into clear actions",
        "first_offer": "Follow-up Recovery Sprint",
        "deliverable": "reply queue, escalation rules, lost-opportunity log",
    },
    {
        "service": "Proposal Co-Pilot",
        "buyer": "Founder / Sales Manager",
        "pain": "discounting starts before scope is protected",
        "first_offer": "Proposal and Negotiation Sprint",
        "deliverable": "objection map, price-floor rules, scope tradeables",
    },
    {
        "service": "Client Delivery OS",
        "buyer": "Operations / Account Manager",
        "pain": "delivery quality depends on people, not a repeatable system",
        "first_offer": "Delivery OS Setup",
        "deliverable": "intake, scope card, acceptance criteria, proof pack",
    },
    {
        "service": "AI Trust OS",
        "buyer": "CEO / Compliance / IT",
        "pain": "AI is used without clear policy or approval gates",
        "first_offer": "AI Trust Setup Sprint",
        "deliverable": "policy, data rules, approval map, audit log",
    },
]

SECTOR_ANGLES = {
    "clinics": "recover bookings and patient follow-ups",
    "real_estate": "stop lead leakage after first inquiry",
    "logistics": "track proposals and B2B account follow-up",
    "training": "convert inquiries into registrations",
    "marketing_agencies": "standardize delivery and client reporting",
    "b2b_services": "turn proposals and follow-ups into a daily command room",
}


def build_markdown() -> str:
    today = date.today().isoformat()
    lines = [
        f"# Dealix Company Brain Launch Pack — {today}",
        "",
        "## Executive positioning",
        "",
        "Dealix should be sold as a company operating layer: brain, revenue command, follow-up recovery, proposal discipline, delivery proof, and AI trust.",
        "",
        "## Service matrix",
        "",
        "| Service | Buyer | Pain | First offer | Deliverable |",
        "|---|---|---|---|---|",
    ]
    for item in SERVICES:
        lines.append(
            f"| {item['service']} | {item['buyer']} | {item['pain']} | {item['first_offer']} | {item['deliverable']} |"
        )
    lines += [
        "",
        "## Sector persuasion angles",
        "",
        "| Sector | Angle |",
        "|---|---|",
    ]
    for sector, angle in SECTOR_ANGLES.items():
        lines.append(f"| {sector} | {angle} |")
    lines += [
        "",
        "## Dealix pitch formula",
        "",
        "1. Identify visible pain.",
        "2. Ask one diagnostic question.",
        "3. Offer a 7-day proof sprint.",
        "4. Show command-room output before proposing a large build.",
        "5. Convert proof into monthly operating retainer.",
        "",
        "## Negotiation rule",
        "",
        "Protect scope first, then price. If the client wants a lower entry price, reduce integrations or dashboard depth, not the proof pack.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "services": SERVICES,
        "sector_angles": SECTOR_ANGLES,
        "status": "ready_for_founder_review",
    }
    (OUT_DIR / "company_brain_launch_pack.md").write_text(build_markdown(), encoding="utf-8")
    (OUT_DIR / "company_brain_launch_pack.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("COMPANY_BRAIN_PACK_GENERATED=reports/commercial/company_brain_launch_pack.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
