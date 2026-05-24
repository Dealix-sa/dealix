#!/usr/bin/env python3
"""Verify Strategy Metrics: scorecard generator + doc present, doc defines
north-star + input metrics + tracking cadence."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "Strategy Metrics"
DOC = "docs/company/DEALIX_STRATEGY_METRICS.md"


def main() -> None:
    reasons = must_exist(DOC, "scripts/generate_strategy_scorecard.py")
    reasons += file_contains(
        DOC,
        "north-star",
        "input metric",
        "cadence",
        "Estimated value is not Verified value",
    )
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
