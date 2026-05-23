"""Render the finance review as a markdown brief."""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops_runtime.finance_calculator import calculate_finance  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    (root / "finance").mkdir(parents=True, exist_ok=True)
    finance = calculate_finance(str(root))

    content = f"""# Finance Review
## Date
{date.today().isoformat()}
## Headline
| Field | Value (SAR) |
|---|---:|
| Cash collected | {finance['cash_collected']} |
| Pipeline value | {finance['pipeline_value']} |
| Weighted pipeline | {finance['weighted_pipeline']} |
| MRR | {finance['mrr']} |
| Monthly expenses | {finance['monthly_expenses']} |
| Net burn | {finance['net_burn']} |
## Rules
- Cash collected before pipeline narrative.
- Pricing decisions require gross margin evidence.
- Net burn must be reconciled monthly.
"""
    out = root / "finance/finance_review.md"
    out.write_text(content, encoding="utf-8")
    print(f"PASS: finance review written: {out}")


if __name__ == "__main__":
    main()
