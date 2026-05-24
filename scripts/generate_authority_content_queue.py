#!/usr/bin/env python3
"""Generate Authority Content Queue."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Authority Content Queue").parse_args()
    ws = workspace_root()
    rows = read_csv_rows(ws / "campaigns" / "campaign_assets.csv")
    body = (
        "# Authority Content Queue\n\n"
        + md_table(
            ["asset_id", "campaign_id", "kind", "approval_state"],
            [[r.get("asset_id",""), r.get("campaign_id",""), r.get("kind",""), r.get("approval_state","")] for r in rows],
        )
        + "\n_Drafts only — founder approves before publish._\n"
    )
    out = write_doc("docs/marketing/AUTHORITY_CONTENT_QUEUE.md", body, [ws / "campaigns" / "campaign_assets.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
