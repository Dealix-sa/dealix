#!/usr/bin/env python3
"""
Dealix Proposal Generator
Generates a commercial proposal document from offer templates.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OFFERS_DIR = REPO / "business" / "offers"

def load_offer(offer_name: str) -> str:
    fname = offer_name.replace(" ", "_").upper() + "_OFFER.md"
    path = OFFERS_DIR / fname
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"# {offer_name}\n\n(Offer template not yet written. Please create {path})\n"

def generate_proposal(account_id: str, offer_name: str, lang: str, timeline: str, mode: str) -> dict:
    offer_md = load_offer(offer_name)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    proposal = {
        "meta": {
            "account_id": account_id,
            "offer": offer_name,
            "language": lang,
            "timeline": timeline,
            "mode": mode,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "review_status": "pending_review",
        },
        "executive_summary": f"Proposal for {account_id} to implement {offer_name} over {timeline}.",
        "client_situation_hypothesis": "Client operates with scattered tools and manual follow-up. Revenue leakage is likely.",
        "scope": [
            "Discovery and diagnostic",
            "System design and configuration",
            "Pilot delivery",
            "Proof-of-value reporting",
            "Handover and training",
        ],
        "deliverables": [
            "Operating system configuration",
            "Dashboard and reporting layer",
            "Governance and review gates",
            "Documentation and SOPs",
        ],
        "implementation_timeline": timeline,
        "governance": "Weekly review calls. Human approval required for all client-facing sends.",
        "proof_plan": "L0-L5 evidence ladder. Pilot metrics tracked weekly.",
        "client_responsibilities": [
            "Provide CRM access and data exports",
            "Assign a point of contact",
            "Review drafts within 48 hours",
        ],
        "exclusions": [
            "Third-party advertising spend",
            "Platform subscription fees (billed separately)",
            "Custom development outside agreed scope",
        ],
        "pricing": {
            "currency": "SAR",
            "setup": "TBD",
            "monthly": "TBD",
            "note": "Pricing placeholders. Fill after discovery call."
        },
        "next_step": "Schedule discovery call to confirm scope and pricing.",
        "signature_placeholder": "____________________\nClient Name & Title\nDate",
        "offer_reference": offer_md[:500],
    }
    return proposal

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--offer", default="Revenue OS")
    parser.add_argument("--lang", default="both")
    parser.add_argument("--timeline", default="21 days")
    parser.add_argument("--mode", choices=["demo", "production"], default="demo")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    langs = ["ar", "en"] if args.lang == "both" else [args.lang]
    out_dir = Path(args.output) if args.output else REPO / "business" / "proposals" / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)

    for lang in langs:
        prop = generate_proposal(args.account_id, args.offer, lang, args.timeline, args.mode)
        fname = f"proposal-{args.account_id}-{args.offer.replace(' ','_')}-{lang}-{datetime.utcnow().strftime('%Y-%m-%d')}.json"
        path = out_dir / fname
        path.write_text(json.dumps(prop, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[PASS] Proposal written: {path}")

if __name__ == "__main__":
    main()
