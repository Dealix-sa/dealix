#!/usr/bin/env python3
"""Generate Growth Cards for sourced accounts (draft-only)."""
from __future__ import annotations

from _common import DATA_DIR, dump, load_json

from app.commercial import growth_cards, icp_scoring, lead_sourcing


def main() -> int:
    records = load_json(DATA_DIR / "accounts.sample.json", key="accounts")
    icp = load_json(DATA_DIR / "icp_rules.sample.json")
    accounts = lead_sourcing.load_accounts(records)
    for a in accounts:
        icp_scoring.apply_score(a, icp)
    cards = growth_cards.build_cards_for_accounts(accounts)
    dump({"cards": [c.to_dict() for c in cards], "count": len(cards)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
