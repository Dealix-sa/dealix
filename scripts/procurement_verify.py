#!/usr/bin/env python3
"""Verify the Procurement & Contracting OS (V9). Static, read-only."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402

REQUIRED_FILES = [
    "docs/procurement-os/00_PROCUREMENT_OS.md",
    "docs/procurement-os/01_VENDOR_REGISTRATION_PACKET.md",
    "docs/procurement-os/02_PURCHASE_ORDER_PROCESS.md",
    "docs/procurement-os/03_CONTRACT_NEGOTIATION_RULES.md",
    "docs/procurement-os/04_PAYMENT_TERMS_POLICY.md",
    "docs/procurement-os/05_SOW_ACCEPTANCE_CRITERIA.md",
    "docs/procurement-os/06_CHANGE_REQUEST_PROCESS.md",
    "docs/procurement-os/99_PROCUREMENT_OS_REPORT.md",
]


def verify() -> dict:
    return v9_lib.run_system_check("procurement", REQUIRED_FILES)


def main() -> int:
    return v9_lib.print_and_exit(verify())


if __name__ == "__main__":
    raise SystemExit(main())
