#!/usr/bin/env python3
"""Request a client approval (queues it; does NOT auto-notify)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.workspace_store import find, load, next_id, now_iso, save


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--item", required=True)
    args = parser.parse_args()

    data = load()
    w = find(data["workspaces"], args.client_id)
    if not w:
        print("ERROR: workspace not found.", file=sys.stderr)
        return 1
    a = {"id": next_id("a", w["approvals"]), "item": args.item, "status": "pending", "requestedAt": now_iso()}
    w["approvals"].append(a)
    save(data)
    print(f"queued approval {a['id']} for {w['clientId']}: '{args.item}'")
    print("Send the approval request manually via the customer's preferred channel.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
