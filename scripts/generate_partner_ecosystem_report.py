#!/usr/bin/env python3
"""Generate Partner Ecosystem report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Partner Ecosystem report").parse_args()
    ws = workspace_root()
    eco = read_csv_rows(ws / "partners" / "partner_ecosystem.csv")
    pri = read_csv_rows(ws / "partners" / "partner_priority.csv")
    body = (
        "# Partner Ecosystem\n\n"
        "## Ecosystem\n"
        + md_table(["partner_id", "category", "state"], [[r.get("partner_id",""), r.get("category",""), r.get("state","")] for r in eco])
        + "\n## Priority\n"
        + md_table(["partner_id", "priority", "rationale"], [[r.get("partner_id",""), r.get("priority",""), r.get("rationale","")] for r in pri])
    )
    out = write_doc("docs/partners/PARTNER_ECOSYSTEM.md", body, [ws / "partners" / "partner_ecosystem.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
