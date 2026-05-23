#!/usr/bin/env python3
"""Generate a monthly finance review markdown from private ops CSV ledgers.

Usage:
    python scripts/generate_finance_review.py --private-ops /home/user/dealix-ops-private
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from dealix.finance.calculator import calculate_finance  # noqa: E402


def render_review(finance: dict[str, float], today: str) -> str:
    return f"""# Monthly Finance Review

## Date
{today}

## Cash
- Cash collected: {finance['cash_collected']:.2f} SAR
- Pipeline value: {finance['pipeline_value']:.2f} SAR
- Weighted pipeline: {finance['weighted_pipeline']:.2f} SAR

## Recurring
- MRR: {finance['mrr']:.2f} SAR

## Expenses
- Monthly recurring expenses: {finance['monthly_expenses']:.2f} SAR
- Net burn: {finance['net_burn']:.2f} SAR

## CEO Finance Decision
-

## Next Action
-
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--private-ops",
        required=True,
        help="Path to dealix-ops-private/ root.",
    )
    args = parser.parse_args()

    root = Path(args.private_ops).expanduser().resolve()
    if not root.exists():
        print(f"FAIL: private ops not found at {root}", file=sys.stderr)
        return 1

    finance = calculate_finance(str(root))
    content = render_review(finance, date.today().isoformat())

    out = root / "finance" / "monthly_finance_review.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    print(f"PASS: wrote finance review to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
