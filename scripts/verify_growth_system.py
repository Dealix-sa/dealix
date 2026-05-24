#!/usr/bin/env python3
"""Verify Dealix growth-system docs (beachhead, accounts, scoring) exist."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = (
    "docs/growth",
    "docs/company/ICP.md",
    "dealix/config/icp_primary.yaml",
    "dealix/config/icp_segments.yaml",
    "dealix/config/lead_scoring.yaml",
    "dealix/config/gtm_abm_wave1.yaml",
    "dealix/config/gtm_blitz_90d.yaml",
)


def _exists(p: Path) -> bool:
    return p.is_file() or p.is_dir()


def main() -> int:
    missing = [p for p in REQUIRED if not _exists(REPO / p)]
    for m in missing:
        print(f"missing_growth_path:{m}", file=sys.stderr)
    ok = not missing
    print(f"GROWTH_SYSTEM_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
