#!/usr/bin/env python3
"""Generate booking options (no calendar write by default)."""
from __future__ import annotations

from _common import DATA_DIR, dump, load_json

from app.commercial import booking_desk, growth_cards, lead_sourcing


def main() -> int:
    records = load_json(DATA_DIR / "accounts.sample.json", key="accounts")
    accounts = lead_sourcing.load_accounts(records)
    cards = growth_cards.build_cards_for_accounts(accounts)
    options = booking_desk.build_booking_options(cards)
    dump({"booking_options": [o.to_dict() for o in options], "count": len(options)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
