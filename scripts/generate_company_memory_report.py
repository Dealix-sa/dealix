#!/usr/bin/env python3
"""Generate Company Memory report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Company Memory report").parse_args()
    ws = workspace_root()
    memory = read_csv_rows(ws / "learning" / "company_memory.csv")
    market = read_csv_rows(ws / "learning" / "market_learning.csv")
    message = read_csv_rows(ws / "learning" / "message_learning.csv")
    offer = read_csv_rows(ws / "learning" / "offer_learning.csv")
    body = (
        "# Company Memory\n\n"
        "## Lessons\n"
        + md_table(["recorded_at", "lesson", "owner"], [[r.get("recorded_at",""), r.get("lesson",""), r.get("owner","")] for r in memory[-20:]])
        + "\n## Market learning\n"
        + md_table(["recorded_at", "sector", "lesson"], [[r.get("recorded_at",""), r.get("sector",""), r.get("lesson","")] for r in market[-10:]])
        + "\n## Message learning\n"
        + md_table(["recorded_at", "angle", "lesson"], [[r.get("recorded_at",""), r.get("angle",""), r.get("lesson","")] for r in message[-10:]])
        + "\n## Offer learning\n"
        + md_table(["recorded_at", "offer", "lesson"], [[r.get("recorded_at",""), r.get("offer",""), r.get("lesson","")] for r in offer[-10:]])
    )
    out = write_doc("docs/learning/COMPANY_MEMORY.md", body, [ws / "learning" / "company_memory.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
