#!/usr/bin/env python3
"""Generate a case study DRAFT from workspace proof items.

Demo only by default. Marks demo prominently. NEVER auto-publishes.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.workspace_store import load, find  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "business" / "cases" / "drafts"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--demo", action="store_true", default=True)
    args = parser.parse_args()

    data = load()
    w = find(data["workspaces"], args.client_id)
    if not w:
        print("ERROR: workspace not found.", file=sys.stderr)
        return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    date = _dt.date.today().isoformat()
    label = "DEMO CASE STUDY DRAFT — not for distribution" if args.demo else "DRAFT — needs customer written consent before any external use"
    out = OUT_DIR / f"case-{w['clientId']}-{date}.md"
    out.write_text(
        f"# {label}\n\n"
        f"## {w['clientName']} — {w['offer']}\n\n"
        "### Challenge (placeholder)\n[Describe the friction we found in the workflow review.]\n\n"
        "### What we did\n"
        + "\n".join(f"- {d['title']}" for d in w["deliverables"])
        + "\n\n### Proof (must cite source)\n"
        + "\n".join(f"- {p['title']} — source: {p['evidence']} ({p['date']})" for p in w["proofItems"])
        + "\n\n### Customer quote\n[Pending written consent. Do NOT publish until customer approves verbatim.]\n",
        encoding="utf-8",
    )
    print(f"wrote {out}")
    print("Reminder: case study draft requires explicit customer consent before any external publication.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
