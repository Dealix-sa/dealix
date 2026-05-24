#!/usr/bin/env python3
"""Verify Company Memory: registers package + doc covering decision log,
value ledger, proof packs, capital assets."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "Company Memory"
DOC = "docs/company/DEALIX_COMPANY_MEMORY.md"


def main() -> None:
    reasons = must_exist(
        DOC,
        "dealix/registers/__init__.py",
        "dealix/registers/90_day_execution.yaml",
    )
    reasons += file_contains(
        DOC,
        "decision log",
        "value ledger",
        "proof pack",
        "capital asset",
    )
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
