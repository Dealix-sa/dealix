#!/usr/bin/env python3
"""
generate_strategy_scorecard.py — assemble a strategy scorecard from
$PRIVATE_OPS/founder/strategic_assumptions.csv + market_attack rollups.

Writes: $PRIVATE_OPS/founder/strategy_scorecard.md
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def _read(p: Path) -> list[dict[str, str]]:
    if not p.exists():
        return []
    try:
        with p.open(encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    except (OSError, UnicodeDecodeError, csv.Error):
        return []


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--private-ops", default=os.environ.get("PRIVATE_OPS", "/opt/dealix"))
    args = p.parse_args()
    root = Path(args.private_ops).expanduser().resolve()
    if not root.exists():
        print(f"STRATEGY_SCORECARD=fail reason=private_ops_missing path={root}")
        return 2

    assumptions = _read(root / "founder" / "strategic_assumptions.csv")
    beachhead = _read(root / "market_attack" / "beachhead_sector_scorecard.csv")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_lines = [f"# Strategy Scorecard — {now}", ""]
    out_lines.append("## Strategic Assumptions")
    if assumptions:
        out_lines += ["", "| id | statement | owner | test_method | review_date | status |", "|---|---|---|---|---|---|"]
        for r in assumptions:
            out_lines.append(
                f"| {r.get('assumption_id', '')} | {r.get('statement_en', '')} | {r.get('owner', '')} | "
                f"{r.get('test_method', '')} | {r.get('review_date', '')} | {r.get('status', '')} |"
            )
    else:
        out_lines.append("_no_data_")

    out_lines += ["", "## Beachhead Scorecard"]
    if beachhead:
        out_lines += ["", "| sector | fit_score | evidence_count | active_conversations | paid_pilots | review_date |", "|---|---|---|---|---|---|"]
        for r in beachhead:
            out_lines.append(
                f"| {r.get('sector', '')} | {r.get('fit_score', '')} | "
                f"{r.get('evidence_count', '')} | {r.get('active_conversations', '')} | "
                f"{r.get('paid_pilots', '')} | {r.get('review_date', '')} |"
            )
    else:
        out_lines.append("_no_data_")

    out = root / "founder" / "strategy_scorecard.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"STRATEGY_SCORECARD=pass output={out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
