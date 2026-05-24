#!/usr/bin/env python3
"""Verify Scale / Moat System: doc lists data moat, governance moat,
distribution moat, switching cost mechanics."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "Scale Moat System"
DOC = "docs/company/DEALIX_SCALE_MOAT.md"


def main() -> None:
    reasons = must_exist(DOC)
    reasons += file_contains(DOC, "data moat", "governance moat",
                              "distribution moat", "switching cost")
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
