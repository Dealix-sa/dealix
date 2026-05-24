#!/usr/bin/env python3
"""Generate Sector Playbook."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Sector Playbook").parse_args()
    ws = workspace_root()
    sectors = read_csv_rows(ws / "growth" / "sector_targets.csv")
    lessons = read_csv_rows(ws / "learning" / "sector_learning.csv")
    body = (
        "# Sector Playbook\n\n"
        "## Sectors\n"
        + md_table(["sector", "score", "decision"], [[r.get("sector",""), r.get("score",""), r.get("decision","")] for r in sectors])
        + "\n## Sector lessons\n"
        + md_table(["recorded_at", "sector", "lesson"], [[r.get("recorded_at",""), r.get("sector",""), r.get("lesson","")] for r in lessons])
    )
    out = write_doc("docs/playbooks/SECTOR_PLAYBOOK.md", body, [ws / "growth" / "sector_targets.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
