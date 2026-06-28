#!/usr/bin/env python3
"""Source & validate commercial leads (requires source_url to be send-ready)."""
from __future__ import annotations

from _common import DATA_DIR, dump, load_json

from app.commercial import lead_sourcing


def main() -> int:
    records = load_json(DATA_DIR / "accounts.sample.json", key="accounts")
    accounts = lead_sourcing.load_accounts(records)
    out = []
    for a in accounts:
        d = a.to_dict()
        d["send_ready"] = lead_sourcing.is_send_ready(a)
        out.append(d)
    dump({"accounts": out, "count": len(out)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
