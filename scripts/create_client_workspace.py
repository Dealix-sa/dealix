#!/usr/bin/env python3
"""Create a client workspace from a won deal.

Usage:
    python3 scripts/create_client_workspace.py --account-id demo-001 --offer "Revenue OS" --demo
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.workspace_store import find, load, next_id, save


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--client-name", default="")
    parser.add_argument("--offer", required=True)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    data = load()
    if find(data["workspaces"], args.account_id):
        print(f"workspace already exists for {args.account_id}")
        return 0
    ws = {
        "id": next_id("ws", data["workspaces"]),
        "clientId": args.account_id,
        "clientName": args.client_name or args.account_id,
        "offer": args.offer,
        "status": "active",
        "startDate": _dt.date.today().isoformat(),
        "nextReview": (_dt.date.today() + _dt.timedelta(days=7)).isoformat(),
        "deliverables": [],
        "approvals": [],
        "risks": [],
        "proofItems": [],
        "demo": args.demo,
    }
    data["workspaces"].append(ws)
    save(data)
    print(f"created workspace {ws['id']} for {args.account_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
