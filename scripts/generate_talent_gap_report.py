#!/usr/bin/env python3
"""Generate Talent Gap report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Talent Gap report").parse_args()
    ws = workspace_root()
    gap = read_csv_rows(ws / "people" / "talent_gap.csv")
    hiring = read_csv_rows(ws / "people" / "hiring_triggers.csv")
    contractors = read_csv_rows(ws / "people" / "contractor_bench.csv")
    body = (
        "# Talent Gap\n\n"
        "## Gaps\n"
        + md_table(["gap", "severity", "next_step"], [[r.get("gap",""), r.get("severity",""), r.get("next_step","")] for r in gap])
        + "\n## Hiring triggers\n"
        + md_table(["role", "trigger_metric", "threshold"], [[r.get("role",""), r.get("trigger_metric",""), r.get("threshold","")] for r in hiring])
        + "\n## Contractor bench\n"
        + md_table(["contractor", "skill", "availability"], [[r.get("contractor",""), r.get("skill",""), r.get("availability","")] for r in contractors])
    )
    out = write_doc("docs/people/TALENT_GAP.md", body, [ws / "people" / "talent_gap.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
