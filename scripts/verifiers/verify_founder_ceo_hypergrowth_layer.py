#!/usr/bin/env python3
"""Verify Hypergrowth CEO Layer: doc lists weekly hypergrowth loop, founder
leverage focus areas, automation budget per week."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "Hypergrowth CEO Layer"
DOC = "docs/company/DEALIX_HYPERGROWTH_CEO.md"


def main() -> None:
    reasons = must_exist(DOC)
    reasons += file_contains(DOC, "leverage", "weekly loop", "automation budget")
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
