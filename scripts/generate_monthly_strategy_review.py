"""Generate the Monthly Strategy Review."""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops_runtime.business_audit import calculate_business_score  # noqa: E402
from ops_runtime.finance_calculator import calculate_finance  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    root.mkdir(parents=True, exist_ok=True)
    (root / "founder").mkdir(parents=True, exist_ok=True)

    score = calculate_business_score(str(root))
    finance = calculate_finance(str(root))

    content = f"""# Monthly Strategy Review
## Date
{date.today().isoformat()}
## CEO Business Score
{score['total_score']} / 100
## Status
{score['status']}
## Finance
- Cash collected: {finance['cash_collected']} SAR
- Pipeline value: {finance['pipeline_value']} SAR
- Weighted pipeline: {finance['weighted_pipeline']} SAR
- MRR: {finance['mrr']} SAR
- Monthly expenses: {finance['monthly_expenses']} SAR
- Net burn: {finance['net_burn']} SAR
## Strategic Decision
Build / Fix / Kill / Defer / Continue
## Biggest Bottleneck
-
## Best Market Signal
-
## Worst Distraction
-
## Next Month Focus
-
## Kill / Defer
-
## Productization Signal
-
"""
    out = root / "founder/monthly_strategy_review.md"
    out.write_text(content, encoding="utf-8")
    print(f"PASS: monthly strategy review generated: {out}")


if __name__ == "__main__":
    main()
