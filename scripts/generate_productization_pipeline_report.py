#!/usr/bin/env python3
"""Generate Productization Pipeline report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Productization Pipeline report").parse_args()
    ws = workspace_root()
    cands = read_csv_rows(ws / "product" / "productization_candidates.csv")
    pipe = read_csv_rows(ws / "product" / "productization_pipeline.csv")
    body = (
        "# Productization Pipeline\n\n"
        "## Candidates\n"
        + md_table(["candidate", "evidence", "decision"], [[r.get("candidate",""), r.get("evidence",""), r.get("decision","")] for r in cands])
        + "\n## Pipeline\n"
        + md_table(["candidate", "stage", "next_step"], [[r.get("candidate",""), r.get("stage",""), r.get("next_step","")] for r in pipe])
    )
    out = write_doc("docs/product/PRODUCTIZATION_PIPELINE.md", body, [ws / "product" / "productization_pipeline.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
