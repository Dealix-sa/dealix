#!/usr/bin/env python3
"""Generate Data Moat report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Data Moat report").parse_args()
    ws = workspace_root()
    base = read_csv_rows(ws / "intelligence" / "lead_intelligence_base.csv")
    accounts = read_csv_rows(ws / "graph" / "accounts.csv")
    signals = read_csv_rows(ws / "graph" / "signals.csv")
    learnings = read_csv_rows(ws / "graph" / "learnings.csv")
    body = (
        "# Data Moat\n\n"
        f"- intelligence base rows: {len(base)}\n"
        f"- graph accounts: {len(accounts)}\n"
        f"- graph signals: {len(signals)}\n"
        f"- learnings recorded: {len(learnings)}\n\n"
        "## Recent learnings\n"
        + md_table(["learning_id", "summary"], [[r.get("learning_id",""), r.get("summary","")] for r in learnings[-15:]])
    )
    out = write_doc("docs/data/DATA_MOAT.md", body, [ws / "intelligence" / "lead_intelligence_base.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
