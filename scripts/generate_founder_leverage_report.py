#!/usr/bin/env python3
"""Generate the Founder Leverage report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Founder Leverage report").parse_args()
    ws = workspace_root()
    audit = read_csv_rows(ws / "founder" / "founder_time_audit.csv")
    queue = read_csv_rows(ws / "founder" / "delegation_queue.csv")
    body = (
        "# Founder Leverage\n\n"
        "## Time audit\n"
        + md_table(["date", "category", "roi_estimate"], [[r.get("date",""), r.get("category",""), r.get("roi_estimate","")] for r in audit])
        + "\n## Delegation queue\n"
        + md_table(["task", "to", "due_date", "state"], [[r.get("task",""), r.get("to",""), r.get("due_date",""), r.get("state","")] for r in queue])
    )
    out = write_doc("docs/founder/FOUNDER_LEVERAGE.md", body, [ws / "founder" / "founder_time_audit.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
