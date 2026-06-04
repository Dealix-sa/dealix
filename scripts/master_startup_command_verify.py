#!/usr/bin/env python3
"""Aggregate verifier: master startup command center across V9 systems.

Rolls up the founder command-center systems: agent governance, agent registry,
delegation (via agent governance), cost control, and docs governance.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _v9_aggregate as agg  # noqa: E402

KEYS = ["agent_governance", "agent_registry", "cost_control", "docs_governance"]


def verify() -> dict:
    return agg.aggregate("master_startup_command", KEYS, "master_startup_command")


def main() -> int:
    return agg.print_aggregate(verify())


if __name__ == "__main__":
    raise SystemExit(main())
