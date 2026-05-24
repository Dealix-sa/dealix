#!/usr/bin/env python3
"""Generate the CEO Daily Brief from private ops CSVs."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate CEO Daily Brief").parse_args()
    ws = workspace_root()
    flags = read_csv_rows(ws / "trust" / "trust_flags.csv")
    workers = read_csv_rows(ws / "runtime" / "worker_state.csv")
    cash = read_csv_rows(ws / "finance" / "cash_collected.csv")
    decisions = read_csv_rows(ws / "founder" / "decision_log.csv")

    cash_today = sum(float(r.get("amount_sar", 0) or 0) for r in cash)
    stale_workers = [w for w in workers if w.get("status", "").lower() != "healthy"]
    body = (
        "# CEO Daily Brief\n\n"
        "## Top CEO action\n"
        "Approve A-priority outreach drafts and clear any pending payment captures.\n"
        "Open /ceo and /approvals.\n\n"
        "## Revenue\n"
        f"- cash collected (today, recorded): {cash_today:.0f} SAR\n\n"
        "## Trust\n"
        f"- trust flags open: {len(flags)}\n\n"
        "## Workers\n"
        f"- stale workers: {len(stale_workers)}\n"
        + md_table(["worker_id", "status"], [[w.get("worker_id", ""), w.get("status", "")] for w in stale_workers])
        + "\n## Decisions logged\n"
        + md_table(["decided_at", "decision"], [[d.get("decided_at", ""), d.get("decision", "")] for d in decisions[-5:]])
    )
    out = write_doc("docs/founder/CEO_DAILY_BRIEF.md", body, [ws / "trust" / "trust_flags.csv", ws / "runtime" / "worker_state.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
