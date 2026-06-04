#!/usr/bin/env python3
"""Verify the Trust Center OS (V9). Static, read-only, artifact-only."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402

REQUIRED_FILES = [
    "docs/trust-center-os/00_TRUST_CENTER_OS.md",
    "docs/trust-center-os/01_PUBLIC_TRUST_PAGE_SPEC.md",
    "docs/trust-center-os/02_SECURITY_OVERVIEW.md",
    "docs/trust-center-os/03_PRIVACY_OVERVIEW.md",
    "docs/trust-center-os/04_HUMAN_APPROVAL_POLICY.md",
    "docs/trust-center-os/05_NO_BLIND_AUTOMATION_POLICY.md",
    "docs/trust-center-os/06_DATA_MINIMIZATION_POLICY.md",
    "docs/trust-center-os/07_INCIDENT_DISCLOSURE_PROCESS.md",
    "docs/trust-center-os/08_CUSTOMER_SECURITY_FAQ.md",
    "docs/trust-center-os/99_TRUST_CENTER_REPORT.md",
]


def verify() -> dict:
    return v9_lib.run_system_check("trust_center", REQUIRED_FILES)


def main() -> int:
    return v9_lib.print_and_exit(verify())


if __name__ == "__main__":
    raise SystemExit(main())
