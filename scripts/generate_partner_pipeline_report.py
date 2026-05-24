#!/usr/bin/env python3
"""Generate Partner Pipeline Report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Partner Pipeline Report").parse_args()
    ws = workspace_root()
    rows = read_csv_rows(ws / "partners" / "partner_pipeline.csv")
    body = (
        "# Partner Pipeline\n\n"
        + md_table(["partner_id", "stage", "next_step"], [[r.get("partner_id",""), r.get("stage",""), r.get("next_step","")] for r in rows])
    )
    out = write_doc("docs/partners/PARTNER_PIPELINE.md", body, [ws / "partners" / "partner_pipeline.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
