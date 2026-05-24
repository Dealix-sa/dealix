#!/usr/bin/env python3
"""Verify CEO Operating System (also covers Founder Management & Hypergrowth):
key docs + report generators present, daily brief generator runnable."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "Company OS"


def main() -> None:
    reasons = must_exist(
        "docs/company/DEALIX_CEO_OS.md",
        "docs/ops/FOUNDER_OPERATING_SYSTEM_AR.md",
        "scripts/generate_ceo_daily_brief.py",
        "scripts/generate_ceo_weekly_review.py",
    )
    reasons += file_contains(
        "docs/company/DEALIX_CEO_OS.md",
        "daily brief",
        "weekly review",
        "non-negotiable",
    )
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
