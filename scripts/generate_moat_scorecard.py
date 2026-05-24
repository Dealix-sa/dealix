#!/usr/bin/env python3
"""Generate Moat Scorecard."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Moat Scorecard").parse_args()
    ws = workspace_root()
    metrics = read_csv_rows(ws / "metrics" / "hypergrowth_metrics.csv")
    body = (
        "# Moat Scorecard\n\n"
        "## Strength signals\n"
        + md_table(["metric", "value", "freshness_iso"], [[r.get("metric",""), r.get("value",""), r.get("freshness_iso","")] for r in metrics])
        + "\n## Moat lenses\n"
        "- Data moat — how much sector signal we accumulate\n"
        "- Proof moat — how many approved customer outcomes\n"
        "- Partner moat — channel + co-sell concentration\n"
        "- Sector knowledge moat — depth of objection + playbook library\n"
    )
    out = write_doc("docs/moat/MOAT_SCORECARD.md", body, [ws / "metrics" / "hypergrowth_metrics.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
