#!/usr/bin/env python3
"""Generate Buyer Objection Graph."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Buyer Objection Graph").parse_args()
    ws = workspace_root()
    rows = read_csv_rows(ws / "graph" / "objections.csv")
    body = (
        "# Buyer Objection Graph\n\n"
        + md_table(
            ["objection_id", "account_id", "objection"],
            [[r.get("objection_id",""), r.get("account_id",""), r.get("objection","")] for r in rows],
        )
    )
    out = write_doc("docs/intelligence/BUYER_OBJECTION_GRAPH.md", body, [ws / "graph" / "objections.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
