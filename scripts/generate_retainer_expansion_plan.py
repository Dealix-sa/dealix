#!/usr/bin/env python3
"""Generate a retainer expansion plan from healthy customer workspaces."""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.workspace_store import load  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "reports" / "customer_success"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", help="Specific client; omit for all healthy")
    args = parser.parse_args()

    data = load()
    workspaces = [w for w in data["workspaces"] if w["status"] == "active" and len(w.get("proofItems", [])) >= 1]
    if args.client_id:
        workspaces = [w for w in workspaces if w["clientId"] == args.client_id]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    date = _dt.date.today().isoformat()
    lines = [f"# Retainer expansion plan — {date}", "", f"Eligible workspaces: {len(workspaces)}", ""]
    for w in workspaces:
        lines.extend([
            f"## {w['clientName']} ({w['clientId']})",
            f"- Current offer: {w['offer']}",
            f"- Proof items so far: {len(w.get('proofItems', []))}",
            f"- Suggested next step: scope adjacent OS module + propose at next weekly review",
            "",
        ])
    out = OUT_DIR / f"retainer-expansion-{date}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
