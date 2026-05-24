#!/usr/bin/env python3
"""Generate Weekly Growth Review."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Weekly Growth Review").parse_args()
    ws = workspace_root()
    msg = read_csv_rows(ws / "growth" / "message_performance.csv")
    seg = read_csv_rows(ws / "growth" / "target_segments.csv")
    body = (
        "# Weekly Growth Review\n\n"
        "## Message performance\n"
        + md_table(["angle", "reply_rate", "convert_rate"], [[r.get("angle",""), r.get("reply_rate",""), r.get("convert_rate","")] for r in msg])
        + "\n## Segments\n"
        + md_table(["segment", "score", "decision"], [[r.get("segment",""), r.get("score",""), r.get("decision","")] for r in seg])
    )
    out = write_doc("docs/growth/WEEKLY_GROWTH_REVIEW.md", body, [ws / "growth" / "message_performance.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
