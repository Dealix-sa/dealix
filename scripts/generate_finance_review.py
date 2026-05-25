import argparse
import sys
from pathlib import Path
from datetime import date

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops_runtime.finance_calculator import calculate_finance  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    root = Path(args.private_ops)
    finance = calculate_finance(str(root))
    content = f"""# Monthly Finance Review

## Date
{date.today().isoformat()}

## Cash
- Cash collected: {finance['cash_collected']} SAR
- Pipeline value: {finance['pipeline_value']} SAR
- Weighted pipeline: {finance['weighted_pipeline']} SAR

## Recurring
- MRR: {finance['mrr']} SAR

## Expenses
- Monthly recurring expenses: {finance['monthly_expenses']} SAR
- Net burn: {finance['net_burn']} SAR

## CEO Finance Decision
-

## Next Action
-
"""
    out_dir = root / "finance"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "monthly_finance_review.md"
    out.write_text(content, encoding="utf-8")
    print(f"PASS: wrote finance review to {out}")


if __name__ == "__main__":
    main()
