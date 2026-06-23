#!/usr/bin/env python3
"""Mark a deliverable as done."""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.workspace_store import find, load, save


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--deliverable-id", required=True)
    args = parser.parse_args()

    data = load()
    w = find(data["workspaces"], args.client_id)
    if not w:
        print("ERROR: workspace not found.", file=sys.stderr)
        return 1
    if args.deliverable_id == "latest":
        d = w["deliverables"][-1] if w["deliverables"] else None
    else:
        d = next((x for x in w["deliverables"] if x["id"] == args.deliverable_id), None)
    if not d:
        print("ERROR: deliverable not found.", file=sys.stderr)
        return 1
    d["status"] = "done"
    d["completedAt"] = _dt.date.today().isoformat()
    save(data)
    print(f"marked done: {d['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
