#!/usr/bin/env python3
"""Verify Customer Success: doc lists onboarding flow, health score,
escalation path, NPS cadence."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "Customer Success"
DOC = "docs/company/DEALIX_CUSTOMER_SUCCESS.md"


def main() -> None:
    reasons = must_exist(DOC, "dealix/commercial_ops")
    reasons += file_contains(DOC, "onboarding", "health score", "escalation", "NPS")
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
