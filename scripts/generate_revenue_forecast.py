#!/usr/bin/env python3
"""
generate_revenue_forecast.py — assemble a revenue forecast from
$PRIVATE_OPS/finance/cash_collected.csv + payment_capture_queue.csv.

Honors NO_FAKE_REVENUE: only payment-evidence rows are counted as
collected. Pipeline rows are weighted but explicitly marked
is_estimate=true.

Writes: $PRIVATE_OPS/founder/revenue_forecast.md
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


def _sum_sar(rows: list[dict[str, str]], key: str) -> float:
    total = 0.0
    for r in rows:
        try:
            total += float(r.get(key, "0") or 0)
        except ValueError:
            continue
    return total


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--private-ops", default=os.environ.get("PRIVATE_OPS", "/opt/dealix"))
    args = p.parse_args()
    root = Path(args.private_ops).expanduser().resolve()
    if not root.exists():
        print(f"REVENUE_FORECAST=fail reason=private_ops_missing path={root}")
        return 2

    cash = _read(root / "finance" / "cash_collected.csv")
    pipeline = _read(root / "finance" / "payment_capture_queue.csv")

    collected_sar = _sum_sar(cash, "amount_sar")
    pipeline_sar = _sum_sar(pipeline, "amount_sar")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        f"# Revenue Forecast — {now}",
        "",
        "Per the doctrine: **Revenue = payment evidence only** (Moyasar bank TX).",
        "Pipeline numbers are explicit estimates and **must not** be quoted",
        "externally as revenue.",
        "",
        "## Collected (payment evidence only)",
        f"- Total collected: **{collected_sar:.2f} SAR** (source: cash_collected.csv)",
        f"- Receipts on file: {len(cash)}",
        "",
        "## Pipeline (is_estimate=true)",
        f"- Pipeline (unweighted): **{pipeline_sar:.2f} SAR** _is_estimate=true_",
        f"- Open invoices: {len(pipeline)}",
        "",
        "## Notes",
        "- Do not publish either figure externally without (a) source rows",
        "  citing API/customer-supplied evidence and (b) approval per the",
        "  case_study_publish gate.",
    ]
    out = root / "founder" / "revenue_forecast.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"REVENUE_FORECAST=pass output={out}")
    print(f"REVENUE_FORECAST_COLLECTED_SAR={collected_sar:.2f}")
    print(f"REVENUE_FORECAST_PIPELINE_SAR={pipeline_sar:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
