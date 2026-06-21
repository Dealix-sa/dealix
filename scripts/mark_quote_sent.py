#!/usr/bin/env python3
"""Mark an APPROVED quote as sent (via the customer's own channel).

Dealix does NOT auto-send. This script just records that the founder sent
the quote out-of-band so the deal ledger reflects reality.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.quote_engine import load_quotes, save_quotes, now  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quote-id", required=True)
    parser.add_argument("--channel", default="email", choices=["email", "whatsapp", "in-person", "other"])
    args = parser.parse_args()

    data = load_quotes()
    quotes = data["quotes"]
    if args.quote_id == "latest":
        q = quotes[-1] if quotes else None
    else:
        q = next((x for x in quotes if x["id"] == args.quote_id), None)
    if not q:
        print(f"ERROR: quote {args.quote_id} not found.", file=sys.stderr)
        return 1
    if q["status"] != "approved":
        print(f"ERROR: quote {q['id']} not approved (status={q['status']}). Approve first.", file=sys.stderr)
        return 2
    q["status"] = "sent"
    q["sentAt"] = now()
    q["sentChannel"] = args.channel
    save_quotes(data)
    print(f"marked sent: {q['id']} via {args.channel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
