#!/usr/bin/env python3
"""Verify the Dealix brand system is present."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, must_exist, print_and_exit  # noqa: E402


REQUIRED = [
    "apps/web/lib/brand-tokens.ts",
    "apps/web/styles/brand.css",
    "apps/web/components/brand/dealix-logo.tsx",
    "apps/web/components/brand/brand-card.tsx",
    "apps/web/components/brand/metric-card.tsx",
    "apps/web/components/brand/status-badge.tsx",
    "apps/web/components/brand/section-heading.tsx",
    "apps/web/components/brand/cta-button.tsx",
    "apps/web/components/brand/trust-badge.tsx",
    "apps/web/components/brand/growth-arrow.tsx",
    "apps/web/components/brand/proof-card.tsx",
    "apps/web/components/brand/offer-card.tsx",
    "apps/web/components/brand/founder-page.tsx",
    "apps/web/components/founder-shell.tsx",
]


def main() -> int:
    result = VerifyResult(name="Brand OS", passed=True)
    must_exist(REQUIRED, result)
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
