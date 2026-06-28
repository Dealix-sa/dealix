#!/usr/bin/env python3
"""Generate D1/D3/D7 follow-up tasks (opt-out respected)."""
from __future__ import annotations

from _common import DATA_DIR, dump, load_json

from app.commercial import followup_engine, growth_cards, lead_sourcing


def main() -> int:
    records = load_json(DATA_DIR / "accounts.sample.json", key="accounts")
    accounts = lead_sourcing.load_accounts(records)
    cards = growth_cards.build_cards_for_accounts(accounts)
    by_id = {a.account_id: a for a in accounts}
    tasks = followup_engine.build_followups_for_cards(cards, by_id)
    dump({"followup_tasks": [t.to_dict() for t in tasks], "count": len(tasks)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
