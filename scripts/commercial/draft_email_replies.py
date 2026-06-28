#!/usr/bin/env python3
"""Draft threaded email replies for sample inbox threads (with unsubscribe)."""
from __future__ import annotations

from _common import DATA_DIR, dump, load_json

from app.commercial import email_desk
from app.commercial.lead_sourcing import load_accounts


def main() -> int:
    records = load_json(DATA_DIR / "accounts.sample.json", key="accounts")
    by_id = {a.account_id: a for a in load_accounts(records)}
    threads = load_json(DATA_DIR / "email_threads.sample.json", key="threads")
    out = []
    for t in threads:
        acct = by_id.get(t["account_id"])
        if acct is None:
            continue
        thread = email_desk.ingest_thread(t["account_id"], t.get("subject", ""), t.get("messages", []))
        reply = email_desk.draft_reply(thread, acct)
        out.append({"thread_id": thread.thread_id, "subject": reply.subject,
                    "has_unsubscribe": "List-Unsubscribe" in reply.headers,
                    "send_status": reply.send_status, "payload": reply.to_dict()})
    dump({"email_drafts": out, "count": len(out)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
