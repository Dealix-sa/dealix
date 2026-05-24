#!/usr/bin/env python3
"""Generate Campaign Command Report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Campaign Command Report").parse_args()
    ws = workspace_root()
    reg = read_csv_rows(ws / "campaigns" / "campaign_registry.csv")
    results = read_csv_rows(ws / "campaigns" / "campaign_results.csv")
    body = (
        "# Campaign Command Report\n\n"
        "## Registry\n"
        + md_table(["campaign_id", "name", "owner", "state"], [[r.get("campaign_id",""), r.get("name",""), r.get("owner",""), r.get("state","")] for r in reg])
        + "\n## Results\n"
        + md_table(["campaign_id", "metric", "value"], [[r.get("campaign_id",""), r.get("metric",""), r.get("value","")] for r in results])
    )
    out = write_doc("docs/marketing/CAMPAIGN_COMMAND.md", body, [ws / "campaigns" / "campaign_registry.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
