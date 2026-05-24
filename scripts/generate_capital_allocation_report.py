#!/usr/bin/env python3
"""Generate the Capital Allocation report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Capital Allocation report").parse_args()
    ws = workspace_root()
    cap = read_csv_rows(ws / "finance" / "capital_allocation.csv")
    roi = read_csv_rows(ws / "finance" / "roi_priority_matrix.csv")
    res = read_csv_rows(ws / "finance" / "resource_allocation.csv")
    body = (
        "# Capital Allocation\n\n"
        "## Decisions\n"
        + md_table(["category", "decision", "rationale"], [[r.get("category",""), r.get("decision",""), r.get("rationale","")] for r in cap])
        + "\n## ROI priority matrix\n"
        + md_table(["item", "roi_score", "decision"], [[r.get("item",""), r.get("roi_score",""), r.get("decision","")] for r in roi])
        + "\n## Resource allocation\n"
        + md_table(["resource", "allocation_pct", "rationale"], [[r.get("resource",""), r.get("allocation_pct",""), r.get("rationale","")] for r in res])
    )
    out = write_doc("docs/finance/CAPITAL_ALLOCATION.md", body, [ws / "finance" / "capital_allocation.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
