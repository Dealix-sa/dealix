#!/usr/bin/env python3
"""Score commercial accounts against the ICP rules."""
from __future__ import annotations

from _common import DATA_DIR, dump, load_json

from app.commercial import icp_scoring, lead_sourcing


def main() -> int:
    records = load_json(DATA_DIR / "accounts.sample.json", key="accounts")
    icp = load_json(DATA_DIR / "icp_rules.sample.json")
    accounts = lead_sourcing.load_accounts(records)
    out = []
    for a in accounts:
        res = icp_scoring.score_account(a, icp)
        out.append({"account_id": a.account_id, **res})
    dump({"scores": out})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
