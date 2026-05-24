#!/usr/bin/env python3
"""Generate Revenue Intelligence Graph Report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Revenue Intelligence Graph Report").parse_args()
    ws = workspace_root()
    accounts = read_csv_rows(ws / "graph" / "accounts.csv")
    contacts = read_csv_rows(ws / "graph" / "contacts.csv")
    messages = read_csv_rows(ws / "graph" / "messages.csv")
    learnings = read_csv_rows(ws / "graph" / "learnings.csv")
    body = (
        "# Revenue Intelligence Graph Report\n\n"
        f"- accounts: {len(accounts)}\n"
        f"- contacts: {len(contacts)}\n"
        f"- messages: {len(messages)}\n"
        f"- learnings: {len(learnings)}\n\n"
        "## Recent learnings\n"
        + md_table(["learning_id", "summary", "ts"], [[r.get("learning_id",""), r.get("summary",""), r.get("ts","")] for r in learnings[-10:]])
    )
    out = write_doc("docs/intelligence/REVENUE_INTELLIGENCE_GRAPH.md", body, [ws / "graph" / "accounts.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
