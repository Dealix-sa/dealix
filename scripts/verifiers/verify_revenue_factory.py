#!/usr/bin/env python3
"""Verify Revenue Factory: forecast generator + doc present + autopilot pkg."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "Revenue Factory"
DOC = "docs/company/DEALIX_REVENUE_FACTORY.md"


def main() -> None:
    reasons = must_exist(
        DOC,
        "scripts/generate_revenue_forecast.py",
        "dealix/revenue_ops_autopilot",
    )
    reasons += file_contains(DOC, "rung", "Sprint", "Retainer", "Diagnostic")
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
