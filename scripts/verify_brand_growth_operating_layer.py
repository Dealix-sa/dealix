#!/usr/bin/env python3
"""Composite verifier: brand + growth + marketing + product distribution + positioning."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

POSITIONING_DOCS = [
    "docs/positioning/CATEGORY_CREATION_OS.md",
    "docs/positioning/DEALIX_POSITIONING.md",
    "docs/positioning/COMPETITIVE_NARRATIVE.md",
    "docs/positioning/WHY_DEALIX_NOW.md",
    "docs/positioning/MESSAGING_HIERARCHY.md",
    "docs/positioning/OBJECTION_HANDLING.md",
    "docs/positioning/SAUDI_B2B_NARRATIVE.md",
    "docs/positioning/COMPETITOR_COMPARISON_MATRIX.md",
    "docs/positioning/SALES_NARRATIVE.md",
]


def run(name: str, script: str) -> int:
    print(f"--- {name} ---")
    res = subprocess.run([sys.executable, str(REPO / "scripts" / script)], cwd=str(REPO))
    return res.returncode


def main() -> int:
    rc = 0
    rc |= run("brand", "verify_brand_system.py")
    rc |= run("growth", "verify_growth_system.py")
    rc |= run("marketing", "verify_marketing_system.py")
    rc |= run("product", "verify_product_distribution.py")
    missing = [f for f in POSITIONING_DOCS if not (REPO / f).exists()]
    print("[positioning]")
    print(f"  missing: {missing}")
    if missing:
        rc |= 1
    print("RESULT:", "FAIL" if rc else "PASS")
    return rc


if __name__ == "__main__":
    sys.exit(main())
