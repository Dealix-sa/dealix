#!/usr/bin/env python3
"""Generate the Beachhead Sector Scorecard."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Beachhead Sector Scorecard").parse_args()
    ws = workspace_root()
    rows = read_csv_rows(ws / "market_attack" / "beachhead_sector_scorecard.csv")
    rows_sorted = sorted(rows, key=lambda r: float(r.get("score", 0) or 0), reverse=True)
    body = (
        "# Beachhead Sector Scorecard\n\n"
        + md_table(["sector", "score", "rationale"], [[r.get("sector",""), r.get("score",""), r.get("rationale","")] for r in rows_sorted])
    )
    out = write_doc("docs/market_attack/BEACHHEAD_SCORECARD.md", body, [ws / "market_attack" / "beachhead_sector_scorecard.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
