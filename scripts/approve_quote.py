#!/usr/bin/env python3
"""Approve a quote (founder gate). Demo-safe.

Usage:
    python3 scripts/approve_quote.py --quote-id Q-2026-06-11-001 --reviewer Sami
    python3 scripts/approve_quote.py --quote-id latest --reviewer Sami
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.quote_engine import load_quotes, now, save_quotes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quote-id", required=True)
    parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()

    data = load_quotes()
    quotes = data["quotes"]
    if args.quote_id == "latest":
        if not quotes:
            print("ERROR: no quotes to approve.", file=sys.stderr)
            return 1
        q = quotes[-1]
    else:
        q = next((x for x in quotes if x["id"] == args.quote_id), None)
        if not q:
            print(f"ERROR: quote {args.quote_id} not found.", file=sys.stderr)
            return 1
    if q["status"] not in ("pending_review", "draft"):
        print(f"WARN: quote is in status {q['status']}; approving anyway.")
    q["status"] = "approved"
    q["reviewer"] = args.reviewer
    q["reviewedAt"] = now()
    save_quotes(data)
    print(f"approved: {q['id']} by {args.reviewer}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
