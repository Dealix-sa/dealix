#!/usr/bin/env python3
"""Generate the CEO Weekly Review."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate CEO Weekly Review").parse_args()
    ws = workspace_root()
    cash = read_csv_rows(ws / "finance" / "cash_collected.csv")
    capital = read_csv_rows(ws / "finance" / "capital_allocation.csv")
    decisions = read_csv_rows(ws / "founder" / "decision_log.csv")
    body = (
        "# CEO Weekly Review\n\n"
        "## Cash\n"
        + md_table(["received_at", "customer", "amount_sar"], [[r.get("received_at",""), r.get("customer",""), r.get("amount_sar","")] for r in cash[-10:]])
        + "\n## Capital allocation\n"
        + md_table(["category", "decision", "rationale"], [[r.get("category",""), r.get("decision",""), r.get("rationale","")] for r in capital])
        + "\n## Decisions this week\n"
        + md_table(["decided_at", "decision", "owner"], [[r.get("decided_at",""), r.get("decision",""), r.get("owner","")] for r in decisions[-15:]])
    )
    out = write_doc("docs/founder/CEO_WEEKLY_REVIEW.md", body, [ws / "finance" / "cash_collected.csv", ws / "founder" / "decision_log.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
