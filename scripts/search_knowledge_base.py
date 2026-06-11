#!/usr/bin/env python3
"""Substring search the knowledge index."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / "business" / "_data" / "knowledge_index.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    if not IDX.exists():
        print("ERROR: knowledge index missing. Run scripts/index_knowledge_sources.py --demo first.", file=sys.stderr)
        return 1
    data = json.loads(IDX.read_text(encoding="utf-8"))
    q = args.query.lower()
    hits = []
    for e in data["entries"]:
        score = e["title"].lower().count(q) * 5 + e["preview"].lower().count(q)
        if score > 0:
            hits.append((score, e))
    hits.sort(key=lambda x: -x[0])
    if not hits:
        print(f"No hits for '{args.query}'.")
        return 0
    for score, e in hits[: args.limit]:
        print(f"  [{score}]  {e['path']}  — {e['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
