#!/usr/bin/env python3
"""Generate Expansion report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Expansion report").parse_args()
    ws = workspace_root()
    opp = read_csv_rows(ws / "customer_success" / "expansion_opportunities.csv")
    risk = read_csv_rows(ws / "customer_success" / "renewal_risk.csv")
    body = (
        "# Expansion Report\n\n"
        "## Opportunities\n"
        + md_table(["customer", "opportunity", "approval_state"], [[r.get("customer",""), r.get("opportunity",""), r.get("approval_state","")] for r in opp])
        + "\n## Renewal risk\n"
        + md_table(["customer", "risk_level", "next_action"], [[r.get("customer",""), r.get("risk_level",""), r.get("next_action","")] for r in risk])
    )
    out = write_doc("docs/customer_success/EXPANSION_REPORT.md", body, [ws / "customer_success" / "expansion_opportunities.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
