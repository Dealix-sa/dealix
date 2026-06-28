#!/usr/bin/env python3
"""Generate delivery handoff stubs (pending approval)."""
from __future__ import annotations

from _common import DATA_DIR, dump, load_json

from app.commercial import delivery_handoff, growth_cards, lead_sourcing, proposal_factory


def main() -> int:
    records = load_json(DATA_DIR / "accounts.sample.json", key="accounts")
    pricing = load_json(DATA_DIR / "pricing_guardrails.sample.json")
    accounts = lead_sourcing.load_accounts(records)
    cards = growth_cards.build_cards_for_accounts(accounts)
    briefs = proposal_factory.build_proposal_briefs(cards, pricing, limit=5)
    card_to_account = {c.card_id: c.account_id for c in cards}
    handoffs = delivery_handoff.build_delivery_handoffs(briefs, card_to_account)
    dump({"delivery_handoffs": [h.to_dict() for h in handoffs], "count": len(handoffs)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
