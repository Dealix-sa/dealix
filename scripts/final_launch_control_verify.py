#!/usr/bin/env python3
"""Aggregate verifier: final launch control across all V9 systems.

Rolls up every V9 verifier into a single launch-control verdict.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _v9_aggregate as agg  # noqa: E402

KEYS = list(agg.V9_MODULES.keys())


def verify() -> dict:
    return agg.aggregate("final_launch_control", KEYS, "final_launch_control")


def main() -> int:
    return agg.print_aggregate(verify())


if __name__ == "__main__":
    raise SystemExit(main())
