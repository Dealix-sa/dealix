"""Generate a bilingual proposal (JSON) for a given account + offer.

Writes to ``business/proposals/generated/proposal-<account_id>-<offer>-<lang>-<date>.json``
with the schema that ``review_proposal_quality.py`` consumes.

Usage:
    python3 scripts/generate_proposal.py --account-id demo-acc-003 --offer "Revenue OS" --lang en --timeline "21 days" --mode demo
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEADS_PATH = REPO_ROOT / "business" / "_data" / "leads.json"
INDEX_PATH = REPO_ROOT / "business" / "_data" / "proposals.index.json"
EXPORT_DIR = REPO_ROOT / "business" / "proposals" / "generated"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


OFFER_SETUP = {
    "Revenue OS": 18000,
    "Command Center": 35000,
    "Delivery OS": 25000,
    "Review & Reputation": 12000,
    "Custom Enterprise": 80000,
    "Managed Retainer": 0,
}
OFFER_MONTHLY = {
    "Revenue OS": 5000,
    "Command Center": 9000,
    "Delivery OS": 6000,
    "Review & Reputation": 3500,
    "Custom Enterprise": 18000,
    "Managed Retainer": 8000,
}

OFFER_REFERENCES = {
    "Revenue OS": (
        "# Revenue OS Offer\n\n"
        "## Purpose\nTurn scattered sales, follow-up, and pipeline into a governed revenue operating system.\n\n"
        "## Scope\n- Lead intake and scoring\n- Outreach draft generation (human-reviewed)\n"
        "- Follow-up queue and reminders\n- Pipeline dashboard\n- Weekly revenue brief\n\n"
        "## Deliverables\n- Configured Revenue OS instance\n- Outreach template library (AR/EN)\n"
        "- Pipeline dashboard\n- SOP manual\n\n## Timeline\n21 days\n\n"
        "## Pricing\nSetup: 15,000 – 30,000 SAR\nMonthly: 3,000 – 7,000 SAR\n\n"
        "## Governance\n- Human approval required for all client-facing sends\n- Weekly review"
    ),
    "Command Center": (
        "# Command Center Offer\n\n## Purpose\nUnified operating dashboard for multi-branch or multi-team operations.\n\n"
        "## Scope\n- KPI selection\n- Dashboard configuration\n- Governance cadence"
    ),
    "Delivery OS": (
        "# Delivery OS Offer\n\n## Purpose\nProductize delivery, track SLAs, and report proof-of-value weekly."
    ),
    "Review & Reputation": (
        "# Review & Reputation Offer\n\n## Purpose\nHuman-approved reply system for public reviews + monthly report."
    ),
    "Custom Enterprise": "# Custom Enterprise Offer\n\n## Purpose\nCustom scope, governed delivery, enterprise SLAs.",
    "Managed Retainer": "# Managed Retainer Offer\n\n## Purpose\nOngoing operations as a service.",
}

DEMO_ACCOUNT = {
    "id": "demo-test",
    "name": "Demo Test Account",
    "segment": "B2B Services",
    "city": "Riyadh",
    "visibleSignal": "Manual follow-up, scattered tools",
    "weaknessHypothesis": "Revenue leakage from slow response",
}


def load_account(account_id: str, mode: str) -> dict | None:
    if LEADS_PATH.exists():
        data = json.loads(LEADS_PATH.read_text(encoding="utf-8"))
        match = next((a for a in data.get("accounts", []) if a["id"] == account_id), None)
        if match:
            return match
    if mode == "demo":
        return {**DEMO_ACCOUNT, "id": account_id}
    return None


def build_proposal(account: dict, offer: str, lang: str, timeline: str, mode: str) -> dict:
    setup = OFFER_SETUP.get(offer, 0)
    monthly = OFFER_MONTHLY.get(offer, 0)
    return {
        "meta": {
            "account_id": account["id"],
            "offer": offer,
            "language": lang,
            "timeline": timeline,
            "mode": mode,
            "generated_at": dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z"),
            "review_status": "pending_review",
        },
        "executive_summary": (
            f"Proposal for {account['id']} to implement {offer} over {timeline}."
        ),
        "client_situation_hypothesis": (
            f"Client operates with scattered tools and manual follow-up. "
            f"Visible signal: {account.get('visibleSignal', '')}. "
            f"Hypothesized weakness: {account.get('weaknessHypothesis', '')}."
        ),
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
            "setup": str(setup) if setup else "TBD",
            "monthly": str(monthly) if monthly else "TBD",
            "note": "Pricing placeholders. Fill after discovery call." if mode == "demo" else "Confirmed pricing.",
        },
        "next_step": "Schedule discovery call to confirm scope and pricing.",
        "signature_placeholder": "____________________\nClient Name & Title\nDate",
        "offer_reference": OFFER_REFERENCES.get(offer, ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--offer", required=True)
    parser.add_argument("--lang", choices=["ar", "en", "both"], default="both")
    parser.add_argument("--timeline", default="21 days")
    parser.add_argument("--mode", choices=["demo", "live"], default="demo")
    args = parser.parse_args()

    account = load_account(args.account_id, args.mode)
    if not account:
        print(f"account not found: {args.account_id}")
        return 1

    languages = ["ar", "en"] if args.lang == "both" else [args.lang]
    today = dt.date.today().isoformat()
    offer_slug = args.offer.replace(" ", "_")
    written: list[Path] = []

    for lang in languages:
        proposal = build_proposal(account, args.offer, lang, args.timeline, args.mode)
        out_file = EXPORT_DIR / f"proposal-{account['id']}-{offer_slug}-{lang}-{today}.json"
        out_file.write_text(
            json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        written.append(out_file)

        index: dict = {"proposals": [], "version": "1.0"}
        if INDEX_PATH.exists():
            try:
                index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        index.setdefault("proposals", []).append(
            {
                "id": f"prop-{account['id']}-{today}-{lang}",
                "accountId": account["id"],
                "offer": args.offer,
                "lang": lang,
                "timeline": args.timeline,
                "setupPrice": OFFER_SETUP.get(args.offer, 0),
                "monthlyPrice": OFFER_MONTHLY.get(args.offer, 0),
                "status": "draft",
                "createdAt": today,
                "path": str(out_file.relative_to(REPO_ROOT)),
            }
        )
        INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    for f in written:
        print(f"wrote {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
