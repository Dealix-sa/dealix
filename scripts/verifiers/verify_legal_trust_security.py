#!/usr/bin/env python3
"""Verify Legal / Trust / Security: SECURITY_RUNBOOK + DPA + PDPL artifact +
trust module present."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "Legal Trust Security"


def main() -> None:
    reasons = must_exist(
        "docs/SECURITY_RUNBOOK.md",
        "docs/company/DEALIX_LEGAL_TRUST_SECURITY.md",
        "dealix/trust",
    )
    reasons += file_contains(
        "docs/company/DEALIX_LEGAL_TRUST_SECURITY.md",
        "PDPL", "DPA", "incident response", "data retention",
    )
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
