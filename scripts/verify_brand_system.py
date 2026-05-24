#!/usr/bin/env python3
"""Verify Dealix brand system assets exist (CSS, logos, components)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = (
    "frontend/src/styles/dealix-brand.css",
    "frontend/public/brand/logo.svg",
    "frontend/public/brand/logo-mark.svg",
    "frontend/public/brand/og-dealix.svg",
    "frontend/src/components/brand/BrandLogo.tsx",
    "frontend/src/components/brand/PublicLaunchShell.tsx",
)


def main() -> int:
    missing = [p for p in REQUIRED if not (REPO / p).is_file()]
    for m in missing:
        print(f"missing_brand_asset:{m}", file=sys.stderr)
    ok = not missing
    print(f"BRAND_SYSTEM_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
