#!/usr/bin/env python3
"""Verify market-attack system: beachhead, sector, offer-market-fit docs."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = (
    "docs/market",
    "docs/market_power",
    "docs/strategy/CATEGORY_DESIGN.md",
    "docs/strategy/COMPETITIVE_POSITIONING.md",
    "docs/strategy/CATEGORY_DESIGN.md",
    "docs/strategy/90_DAY_PLAN.md",
    "dealix/config/icp_primary.yaml",
    "dealix/config/icp_segments.yaml",
    "dealix/config/gtm_abm_wave1.yaml",
)


def _exists(p: Path) -> bool:
    return p.is_file() or p.is_dir()


def main() -> int:
    missing = [p for p in REQUIRED if not _exists(REPO / p)]
    for m in missing:
        print(f"missing_market_attack_path:{m}", file=sys.stderr)
    ok = not missing
    print(f"MARKET_ATTACK_SYSTEM_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
