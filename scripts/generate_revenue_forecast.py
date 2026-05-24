#!/usr/bin/env python3
"""Generate the Revenue Forecast doc."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Revenue Forecast").parse_args()
    ws = workspace_root()
    cash = read_csv_rows(ws / "finance" / "cash_collected.csv")
    unit = read_csv_rows(ws / "finance" / "ai_unit_economics.csv")
    pipeline = read_csv_rows(ws / "growth" / "sector_targets.csv")
    total = sum(float(r.get("amount_sar", 0) or 0) for r in cash)
    body = (
        "# Revenue Forecast\n\n"
        f"## Cash collected (recorded)\n\n- total: {total:.0f} SAR\n\n"
        "## Pipeline (sector targets)\n"
        + md_table(["sector", "score", "decision"], [[r.get("sector",""), r.get("score",""), r.get("decision","")] for r in pipeline])
        + "\n## Unit economics\n"
        + md_table(["unit", "cost_sar", "revenue_sar", "margin"], [[r.get("unit",""), r.get("cost_sar",""), r.get("revenue_sar",""), r.get("margin","")] for r in unit])
        + "\n_No guaranteed revenue claims — values are recorded, not projected with certainty._\n"
    )
    out = write_doc("docs/revenue/REVENUE_FORECAST.md", body, [ws / "finance" / "cash_collected.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
