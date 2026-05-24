#!/usr/bin/env python3
"""Generate Monthly Advisor Update (draft for founder approval)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Monthly Advisor Update").parse_args()
    ws = workspace_root()
    cash = read_csv_rows(ws / "finance" / "cash_collected.csv")
    decisions = read_csv_rows(ws / "founder" / "decision_log.csv")
    learnings = read_csv_rows(ws / "graph" / "learnings.csv")
    cash_total = sum(float(r.get("amount_sar", 0) or 0) for r in cash)
    body = (
        "# Monthly Advisor / Board Update — DRAFT\n\n"
        "> Founder approves before sending. No guaranteed revenue claims.\n\n"
        f"- recorded cash this month: {cash_total:.0f} SAR\n"
        f"- decisions logged: {len(decisions)}\n"
        f"- learnings recorded: {len(learnings)}\n\n"
        "## Highlights\n"
        + md_table(["decided_at", "decision", "owner"], [[r.get("decided_at",""), r.get("decision",""), r.get("owner","")] for r in decisions[-10:]])
        + "\n## What we learned\n"
        + md_table(["learning_id", "summary"], [[r.get("learning_id",""), r.get("summary","")] for r in learnings[-10:]])
    )
    out = write_doc("docs/founder/MONTHLY_ADVISOR_UPDATE.md", body, [ws / "finance" / "cash_collected.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
