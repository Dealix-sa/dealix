#!/usr/bin/env python3
"""verify_learning_os.py — Learning OS docs + loop completeness."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "docs/learning/EXPERIMENT_LOG.md",
    "docs/learning/WIN_LOSS_REVIEW.md",
    "docs/learning/MESSAGE_PERFORMANCE.md",
    "docs/learning/SECTOR_PERFORMANCE.md",
    "docs/learning/PRICING_LEARNING.md",
    "docs/learning/AGENT_EVALS.md",
    "docs/learning/MONTHLY_STRATEGY_UPDATE.md",
]

# Monthly Strategy Update must explicitly aggregate the other learning sources.
MONTHLY_AGGREGATIONS = [
    "EXPERIMENT_LOG",
    "WIN_LOSS_REVIEW",
    "SECTOR_PERFORMANCE",
    "MESSAGE_PERFORMANCE",
    "PRICING_LEARNING",
    "AGENT_EVALS",
]


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if not (REPO_ROOT / rel).exists():
            failures.append(f"missing file: {rel}")

    monthly = REPO_ROOT / "docs/learning/MONTHLY_STRATEGY_UPDATE.md"
    if monthly.exists():
        text = monthly.read_text(encoding="utf-8")
        for keyword in MONTHLY_AGGREGATIONS:
            if keyword not in text:
                failures.append(
                    f"MONTHLY_STRATEGY_UPDATE.md: missing reference to {keyword}"
                )

    if failures:
        print("Learning OS verification FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"Learning OS verification OK ({len(REQUIRED_FILES)} files, "
          f"{len(MONTHLY_AGGREGATIONS)} aggregation references checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
