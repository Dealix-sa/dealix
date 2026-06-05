#!/usr/bin/env python3
"""Aggregate verifier: execution intelligence across V9 systems.

Rolls up the systems that turn execution into intelligence: demo OS,
customer lifecycle, strategic moat, and deployment static verification.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _v9_aggregate as agg  # noqa: E402

KEYS = ["demo_os", "customer_lifecycle", "strategic_moat", "deployment_static"]


def verify() -> dict:
    return agg.aggregate("execution_intelligence", KEYS, "execution_intelligence")


def main() -> int:
    return agg.print_aggregate(verify())


if __name__ == "__main__":
    raise SystemExit(main())
