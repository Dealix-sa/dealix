#!/usr/bin/env python3
"""Print a quote for human review."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.quote_engine import load_quotes  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quote-id", help="Specific quote id; default: latest")
    parser.add_argument("--latest", action="store_true")
    args = parser.parse_args()

    quotes = load_quotes()["quotes"]
    if not quotes:
        print("No quotes registered.")
        return 0

    q = None
    if args.quote_id:
        q = next((x for x in quotes if x["id"] == args.quote_id), None)
        if not q:
            print(f"ERROR: quote {args.quote_id} not found.", file=sys.stderr)
            return 1
    else:
        q = quotes[-1]

    print(json.dumps(q, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
