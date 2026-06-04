#!/usr/bin/env python3
"""Verify the Strategic Moat OS (V9). Static, read-only, artifact-only."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402

REQUIRED_FILES = [
    "docs/strategic-moat-os/00_STRATEGIC_MOAT_OS.md",
    "docs/strategic-moat-os/01_MOAT_THESIS.md",
    "docs/strategic-moat-os/02_COMPOUNDING_ADVANTAGES.md",
    "docs/strategic-moat-os/03_DATA_ASSET_STRATEGY.md",
    "docs/strategic-moat-os/04_WORKFLOW_IP_STRATEGY.md",
    "docs/strategic-moat-os/05_TRUST_MOAT.md",
    "docs/strategic-moat-os/06_DISTRIBUTION_MOAT.md",
    "docs/strategic-moat-os/07_DELIVERY_MOAT.md",
    "docs/strategic-moat-os/08_CATEGORY_MOAT.md",
    "docs/strategic-moat-os/99_STRATEGIC_MOAT_REPORT.md",
]


def verify() -> dict:
    return v9_lib.run_system_check("strategic_moat", REQUIRED_FILES)


def main() -> int:
    return v9_lib.print_and_exit(verify())


if __name__ == "__main__":
    raise SystemExit(main())
