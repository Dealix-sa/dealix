#!/usr/bin/env python3
"""Verify GitHub Actions: new dealix-everything + dealix-company-os workflows
exist and reference make targets."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "GitHub Actions"


def main() -> None:
    reasons = must_exist(
        ".github/workflows/dealix-everything.yml",
        ".github/workflows/dealix-company-os.yml",
    )
    reasons += file_contains(
        ".github/workflows/dealix-everything.yml",
        "make everything",
        "schedule",
    )
    reasons += file_contains(
        ".github/workflows/dealix-company-os.yml",
        "make company-os",
    )
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
