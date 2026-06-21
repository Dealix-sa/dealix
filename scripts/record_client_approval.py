#!/usr/bin/env python3
"""Record a client approval decision."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.workspace_store import load, save, find, now_iso  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--approval-id", required=True)
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--status", choices=["approved", "rejected"], default="approved")
    args = parser.parse_args()

    data = load()
    w = find(data["workspaces"], args.client_id)
    if not w:
        print("ERROR: workspace not found.", file=sys.stderr)
        return 1
    if args.approval_id == "latest":
        a = w["approvals"][-1] if w["approvals"] else None
    else:
        a = next((x for x in w["approvals"] if x["id"] == args.approval_id), None)
    if not a:
        print("ERROR: approval not found.", file=sys.stderr)
        return 1
    a["status"] = args.status
    a["reviewer"] = args.reviewer
    a["decidedAt"] = now_iso()
    save(data)
    print(f"{args.status}: {a['id']} by {args.reviewer}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
