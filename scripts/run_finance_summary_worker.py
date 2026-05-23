#!/usr/bin/env python3
"""Finance summary worker — read-only.

Reads finance/cash_collected.csv, finance/payment_capture_queue.csv, and
finance/ai_unit_economics.csv. Prints a snapshot to stdout. Never sends
anything externally.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import Counter
from pathlib import Path
from typing import List, Tuple

DEFAULT_ROOT = os.environ.get("PRIVATE_OPS", "/opt/dealix-ops-private")


def sum_amounts(path: Path, amount_column: str, currency_column: str) -> Counter:
    totals: Counter = Counter()
    if not path.exists():
        return totals
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            currency = (row.get(currency_column) or "").strip() or "(unknown)"
            try:
                amount = float(row.get(amount_column) or 0)
            except (TypeError, ValueError):
                amount = 0.0
            totals[currency] += amount
    return totals


def latest_unit_econ(path: Path) -> Tuple[str, str, float] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return None
    last = rows[-1]
    try:
        margin = float(last.get("margin_pct") or 0)
    except (TypeError, ValueError):
        margin = 0.0
    return (last.get("period", ""), last.get("model", ""), margin)


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=DEFAULT_ROOT)
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    collected = sum_amounts(root / "finance/cash_collected.csv", "amount", "currency")
    pending = sum_amounts(
        root / "finance/payment_capture_queue.csv", "amount", "currency"
    )
    last_econ = latest_unit_econ(root / "finance/ai_unit_economics.csv")

    print("Dealix finance snapshot")
    print("-" * 40)
    print("cash collected by currency:")
    for currency, total in sorted(collected.items()):
        print(f"  {currency:<8} {total:,.2f}")
    print("payment capture queue by currency:")
    for currency, total in sorted(pending.items()):
        print(f"  {currency:<8} {total:,.2f}")
    if last_econ is None:
        print("ai unit economics: (no data)")
    else:
        period, model, margin = last_econ
        print(f"ai unit economics: latest period={period} model={model} margin={margin:.1f}%")
    print(f"source root: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
