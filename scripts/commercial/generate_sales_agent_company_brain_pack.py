#!/usr/bin/env python3
"""Generate a review-first Sales Agent + Company Brain pack."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from app.commercial.sales_agent import build_sales_agent_pack

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "reports" / "commercial" / "sales_agent_company_brain"


def markdown(pack: dict) -> str:
    questions = "\n".join(f"- {item}" for item in pack["discovery_questions"])
    notes = "\n".join(f"- {item}" for item in pack["negotiation_notes"])
    return f"""# Sales Agent + Company Brain Pack

## Target

- Company: {pack['company_name']}
- Sector: {pack['sector']}
- City: {pack['city']}
- Source: {pack['source_url']}
- Buyer persona: {pack['buyer_persona']}

## Pain hypothesis

{pack['pain_hypothesis']}

## Recommended offer

{pack['recommended_offer']}

## Review-only draft

{pack['draft_message_ar']}

## Discovery questions

{questions}

## Negotiation notes

{notes}

## Company Brain decision

{pack['company_brain_decision']}

## Next action

{pack['next_action']}

## Safety state

- Communication mode: {pack['communication_mode']}
- Owner decision required: {pack['owner_decision_required']}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", required=True)
    parser.add_argument("--sector", default="b2b_services")
    parser.add_argument("--city", default="Riyadh")
    parser.add_argument("--source-url", default="manual_review_required")
    args = parser.parse_args()

    pack = build_sales_agent_pack(
        company_name=args.company,
        sector=args.sector,
        city=args.city,
        source_url=args.source_url,
    ).to_dict()

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pack": pack,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(ch.lower() if ch.isalnum() else "_" for ch in args.company).strip("_") or "company"
    (OUT_DIR / f"{safe_name}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT_DIR / f"{safe_name}.md").write_text(markdown(pack), encoding="utf-8")
    print(f"SALES_AGENT_COMPANY_BRAIN_PACK={OUT_DIR / f'{safe_name}.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
