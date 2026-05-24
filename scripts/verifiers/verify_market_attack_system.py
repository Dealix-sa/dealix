#!/usr/bin/env python3
"""Verify Market Attack System: doc present, lists ICP wedge, beachhead,
landing motion, qualification triggers."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "Market Attack System"
DOC = "docs/company/DEALIX_MARKET_ATTACK.md"


def main() -> None:
    reasons = must_exist(DOC)
    reasons += file_contains(DOC, "ICP", "beachhead", "wedge", "qualification")
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
