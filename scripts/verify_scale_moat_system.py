#!/usr/bin/env python3
"""Verify scale + moat docs (defensibility, expansion, gates)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = (
    "docs/moat/MOAT_SCORE.md",
    "docs/moat/COMPETITIVE_STRATEGY.md",
    "docs/moat/MOAT_OPERATING_ROUTINE.md",
    "docs/moat/GOVERNANCE_TO_MOAT_LOOP.md",
    "docs/moat/MOAT_DASHBOARD.md",
    "docs/scale/SCALE_MODEL.md",
    "docs/scale/SCALE_GATES.md",
    "docs/scale/ENTERPRISE_SALES_PATH.md",
    "docs/scale/REGIONAL_EXPANSION.md",
)


def main() -> int:
    missing = [p for p in REQUIRED if not (REPO / p).is_file()]
    for m in missing:
        print(f"missing_scale_moat_doc:{m}", file=sys.stderr)
    ok = not missing
    print(f"SCALE_MOAT_SYSTEM_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
