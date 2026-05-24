#!/usr/bin/env python3
"""
generate_capital_allocation_report.py — assemble a capital-allocation
report from $PRIVATE_OPS/finance/capital_allocation.csv.

Writes: $PRIVATE_OPS/founder/capital_allocation.md
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--private-ops", default=os.environ.get("PRIVATE_OPS", "/opt/dealix"))
    args = p.parse_args()
    root = Path(args.private_ops).expanduser().resolve()
    if not root.exists():
        print(f"CAPITAL_ALLOCATION=fail reason=private_ops_missing path={root}")
        return 2

    src = root / "finance" / "capital_allocation.csv"
    rows: list[dict[str, str]] = []
    if src.exists():
        try:
            with src.open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
        except (OSError, UnicodeDecodeError, csv.Error):
            rows = []

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [f"# Capital Allocation — {now}", ""]
    if not rows:
        lines.append("_no_data_ — populate `finance/capital_allocation.csv`.")
    else:
        total = 0.0
        for r in rows:
            try:
                total += float(r.get("monthly_sar", "0") or 0)
            except ValueError:
                pass
        lines.extend([
            f"Total monthly: **{total:.2f} SAR** (sum of rows; per-row source required for any external citation).",
            "",
            "| category | subcategory | monthly_sar | roi_note | owner | review_date |",
            "|---|---|---|---|---|---|",
        ])
        for r in rows:
            lines.append(
                "| {category} | {subcategory} | {monthly_sar} | {roi_note} | {owner} | {review_date} |".format(
                    category=r.get("category", ""),
                    subcategory=r.get("subcategory", ""),
                    monthly_sar=r.get("monthly_sar", ""),
                    roi_note=r.get("roi_note", ""),
                    owner=r.get("owner", ""),
                    review_date=r.get("review_date", ""),
                )
            )
    out = root / "founder" / "capital_allocation.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"CAPITAL_ALLOCATION=pass output={out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
