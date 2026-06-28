#!/usr/bin/env python3
"""Generate proposal briefs (approval-required, no final price)."""
from __future__ import annotations

from _common import DATA_DIR, dump, load_json

from app.commercial import growth_cards, lead_sourcing, proposal_factory


def main() -> int:
    records = load_json(DATA_DIR / "accounts.sample.json", key="accounts")
    pricing = load_json(DATA_DIR / "pricing_guardrails.sample.json")
    accounts = lead_sourcing.load_accounts(records)
    cards = growth_cards.build_cards_for_accounts(accounts)
    briefs = proposal_factory.build_proposal_briefs(cards, pricing, limit=5)
    dump({"proposal_briefs": [b.to_dict() for b in briefs], "count": len(briefs)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
