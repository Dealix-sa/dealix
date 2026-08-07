#!/usr/bin/env python3
"""Add a deliverable to a client workspace."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.workspace_store import find, load, next_id, save


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--due", help="YYYY-MM-DD")
    args = parser.parse_args()

    data = load()
    w = find(data["workspaces"], args.client_id)
    if not w:
        print(f"ERROR: workspace not found for {args.client_id}", file=sys.stderr)
        return 1
    d = {"id": next_id("d", w["deliverables"]), "title": args.title, "status": "queued"}
    if args.due:
        d["due"] = args.due
    w["deliverables"].append(d)
    save(data)
    print(f"added deliverable {d['id']} to {w['clientId']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
