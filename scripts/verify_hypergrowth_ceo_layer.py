#!/usr/bin/env python3
"""Verify CEO / hypergrowth layer artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = (
    "docs/company/CEO_OPERATING_SYSTEM.md",
    "docs/company/DEALIX_CAPITAL_MODEL.md",
    "docs/company/DEALIX_CEO_CTO_MASTER_STRATEGY_V3.md",
    "docs/company/BOARD_PACK.md",
    "docs/strategy/CEO_OPERATING_CADENCE_AR.md",
    "docs/strategy/CEO_STRATEGY.md",
    "docs/strategy/12_MONTH_ROADMAP.md",
)


def main() -> int:
    missing = [p for p in REQUIRED if not (REPO / p).is_file()]
    for m in missing:
        print(f"missing_ceo_artifact:{m}", file=sys.stderr)
    ok = not missing
    print(f"HYPERGROWTH_CEO_LAYER_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
