#!/usr/bin/env python3
"""Verify Enterprise Sales: doc lists deal stages, AI governance review SOW,
security questionnaire response pack, MSAs."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "Enterprise Sales"
DOC = "docs/company/DEALIX_ENTERPRISE_SALES.md"


def main() -> None:
    reasons = must_exist(DOC)
    reasons += file_contains(DOC, "deal stage", "governance review",
                              "security questionnaire", "MSA")
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
