#!/usr/bin/env python3
"""Aggregate verifier: company utilization view across V9 systems.

Rolls up the systems that measure how fully the company's assets are used:
strategic moat, customer lifecycle, QMS, and cost control.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _v9_aggregate as agg  # noqa: E402

KEYS = ["strategic_moat", "customer_lifecycle", "qms", "cost_control"]


def verify() -> dict:
    return agg.aggregate("company_utilization", KEYS, "company_utilization")


def main() -> int:
    return agg.print_aggregate(verify())


if __name__ == "__main__":
    raise SystemExit(main())
