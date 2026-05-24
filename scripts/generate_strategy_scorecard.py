#!/usr/bin/env python3
"""Generate the Strategy Scorecard."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Strategy Scorecard").parse_args()
    ws = workspace_root()
    assumptions = read_csv_rows(ws / "founder" / "strategic_assumptions.csv")
    body = (
        "# Strategy Scorecard\n\n"
        "## Strategic assumptions\n"
        + md_table(
            ["assumption", "validation_state", "evidence"],
            [[r.get("assumption",""), r.get("validation_state",""), r.get("evidence","")] for r in assumptions],
        )
    )
    out = write_doc("docs/strategy/STRATEGY_SCORECARD.md", body, [ws / "founder" / "strategic_assumptions.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
