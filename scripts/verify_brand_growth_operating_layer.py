#!/usr/bin/env python3
"""Composite verifier for the brand + growth + marketing + product layer."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

VERIFIERS = [
    "verify_brand_system.py",
    "verify_growth_system.py",
    "verify_marketing_system.py",
    "verify_product_distribution.py",
]


def main() -> int:
    failures = 0
    for v in VERIFIERS:
        print(f"\n=== running {v} ===")
        rc = subprocess.run([sys.executable, str(ROOT / v)]).returncode
        if rc != 0:
            failures += 1
    print(f"\n[brand-growth-operating-layer] {len(VERIFIERS) - failures} pass / {failures} fail")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
