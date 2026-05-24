#!/usr/bin/env python3
"""Verify Brand OS: brand doc exists, lists positioning + voice + visual rules,
ends with bilingual disclaimer."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO_ROOT, report, file_contains  # noqa: E402

LAYER = "Brand OS"
DOC = "docs/brand/DEALIX_BRAND_OS.md"


def main() -> None:
    reasons = file_contains(
        DOC,
        "Positioning",
        "Voice",
        "Visual",
        "non-negotiable",
        "القيمة التقديرية ليست قيمة مُتحقَّقة",
    )
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
