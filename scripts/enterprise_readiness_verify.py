#!/usr/bin/env python3
"""Verify the Enterprise Readiness OS (V9). Static, read-only, artifact-only."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402

REQUIRED_FILES = [
    "docs/enterprise-readiness-os/00_ENTERPRISE_READINESS_OS.md",
    "docs/enterprise-readiness-os/01_ENTERPRISE_BUYER_MAP.md",
    "docs/enterprise-readiness-os/02_PROCUREMENT_READINESS.md",
    "docs/enterprise-readiness-os/03_VENDOR_ONBOARDING_ANSWERS.md",
    "docs/enterprise-readiness-os/04_SECURITY_QUESTIONNAIRE_ANSWERS.md",
    "docs/enterprise-readiness-os/05_DATA_PROCESSING_ANSWERS.md",
    "docs/enterprise-readiness-os/06_IMPLEMENTATION_GOVERNANCE.md",
    "docs/enterprise-readiness-os/07_ENTERPRISE_PILOT_STRUCTURE.md",
    "docs/enterprise-readiness-os/08_ENTERPRISE_PRICING_GUARDRAILS.md",
    "docs/enterprise-readiness-os/99_ENTERPRISE_READINESS_REPORT.md",
]


def verify() -> dict:
    return v9_lib.run_system_check("enterprise_readiness", REQUIRED_FILES)


def main() -> int:
    return v9_lib.print_and_exit(verify())


if __name__ == "__main__":
    raise SystemExit(main())
