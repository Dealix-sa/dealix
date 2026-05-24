#!/usr/bin/env python3
"""Verify Capital Allocation: doc + generator present and doc covers the
required budget pools (people, infra, sales, R&D, runway buffer)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "Capital Allocation"
DOC = "docs/company/DEALIX_CAPITAL_ALLOCATION.md"


def main() -> None:
    reasons = must_exist(DOC, "scripts/generate_capital_allocation_report.py")
    reasons += file_contains(DOC, "people", "infra", "sales", "R&D", "runway")
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
