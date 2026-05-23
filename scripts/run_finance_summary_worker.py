#!/usr/bin/env python3
"""Finance summary — cash collected, AI unit economics."""
from __future__ import annotations

import csv
import os
import sys
from pathlib import Path


def _runtime_dir() -> Path:
    return Path(os.getenv("PRIVATE_OPS") or os.getenv("DEALIX_PRIVATE_OPS_DIR") or "/opt/dealix-ops-private").expanduser()


def _sum(path: Path, col: str) -> float:
    if not path.exists():
        return 0.0
    total = 0.0
    with path.open("r", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            try:
                total += float(r.get(col, "0") or 0)
            except ValueError:
                continue
    return total


def main() -> int:
    base = _runtime_dir()
    cash = _sum(base / "finance" / "cash_collected.csv", "amount_sar")
    ai_cost = _sum(base / "finance" / "ai_unit_economics.csv", "ai_cost_usd")
    print(f"[finance_summary] cash_sar={cash:.0f} ai_cost_usd={ai_cost:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
