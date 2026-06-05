#!/usr/bin/env python3
"""Aggregate verifier: startup OS readiness across V9 systems.

Rolls up the systems that make Dealix operate as a company: enterprise
readiness, trust center, procurement, and data room.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _v9_aggregate as agg  # noqa: E402

KEYS = ["enterprise_readiness", "trust_center", "procurement", "data_room"]


def verify() -> dict:
    return agg.aggregate("startup_os", KEYS, "startup_os")


def main() -> int:
    return agg.print_aggregate(verify())


if __name__ == "__main__":
    raise SystemExit(main())
