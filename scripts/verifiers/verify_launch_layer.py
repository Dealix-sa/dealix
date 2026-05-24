#!/usr/bin/env python3
"""Verify Launch Layer: doc + existing launch verifier present."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "Launch Layer"
DOC = "docs/company/DEALIX_LAUNCH_LAYER.md"


def main() -> None:
    reasons = must_exist(
        DOC,
        "scripts/verify_commercial_launch_ready.py",
        "scripts/official_launch_verify.sh",
    )
    reasons += file_contains(DOC, "launch gate", "soft launch", "rollback")
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
