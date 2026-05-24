#!/usr/bin/env python3
"""Generate Strategic Account List."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Strategic Account List").parse_args()
    ws = workspace_root()
    rows = read_csv_rows(ws / "market_attack" / "strategic_accounts.csv")
    body = (
        "# Strategic Account List\n\n"
        + md_table(["account", "priority", "rationale"], [[r.get("account",""), r.get("priority",""), r.get("rationale","")] for r in rows])
        + "\n_Outreach to these accounts is queued, never auto-sent._\n"
    )
    out = write_doc("docs/market_attack/STRATEGIC_ACCOUNTS.md", body, [ws / "market_attack" / "strategic_accounts.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
