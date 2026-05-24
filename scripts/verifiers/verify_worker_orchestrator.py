#!/usr/bin/env python3
"""Verify Worker Orchestrator: doc + autopilot pkg + machine registry entries
for the daily/evening loops."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "Worker Orchestrator"


def main() -> None:
    reasons = must_exist(
        "docs/company/DEALIX_WORKER_ORCHESTRATOR.md",
        "dealix/revenue_ops_autopilot",
        "scripts/run_founder_commercial_day.sh",
        "scripts/founder_evening_evidence.py",
        "registries/machine_registry.yaml",
    )
    reasons += file_contains(
        "registries/machine_registry.yaml",
        "founder-commercial-day",
        "ops-autopilot-evening",
    )
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
