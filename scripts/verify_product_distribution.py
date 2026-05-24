#!/usr/bin/env python3
"""Verify Dealix product distribution: offer ladder + productized services."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = (
    "docs/company/BUSINESS_MODEL.md",
    "docs/services/ai_ops_diagnostic",
    "docs/services/ai_quick_win_sprint",
    "docs/services/lead_intelligence_sprint",
    "docs/services/ai_support_desk_sprint",
    "docs/services/company_brain_sprint",
    "docs/services/ai_governance_program",
    "docs/services/data_readiness_assessment",
    "docs/services/client_ai_policy_pack",
)


def _exists(p: Path) -> bool:
    return p.is_file() or p.is_dir()


def main() -> int:
    missing = [p for p in REQUIRED if not _exists(REPO / p)]
    for m in missing:
        print(f"missing_product_path:{m}", file=sys.stderr)
    ok = not missing
    print(f"PRODUCT_DISTRIBUTION_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
