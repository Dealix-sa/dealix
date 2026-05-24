#!/usr/bin/env python3
"""Generate Objection Intelligence Report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Objection Intelligence Report").parse_args()
    ws = workspace_root()
    rows = read_csv_rows(ws / "market_attack" / "objection_library.csv")
    body = (
        "# Objection Intelligence\n\n"
        + md_table(
            ["objection", "response", "approved"],
            [[r.get("objection",""), r.get("response",""), r.get("approved","")] for r in rows],
        )
    )
    out = write_doc("docs/intelligence/OBJECTION_INTELLIGENCE.md", body, [ws / "market_attack" / "objection_library.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
