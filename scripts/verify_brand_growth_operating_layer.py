#!/usr/bin/env python3
"""
Master verifier for the Dealix brand-growth operating layer.

Runs the four sub-verifiers in sequence and prints a single roll-up
verdict. Exits 0 only if every sub-verifier exits 0.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SUB = [
    ("brand", REPO_ROOT / "scripts" / "verify_brand_system.py"),
    ("growth", REPO_ROOT / "scripts" / "verify_growth_system.py"),
    ("marketing", REPO_ROOT / "scripts" / "verify_marketing_system.py"),
    ("product-distribution", REPO_ROOT / "scripts" / "verify_product_distribution.py"),
]


def main() -> int:
    results: list[tuple[str, int]] = []
    for label, path in SUB:
        print(f"\n----- {label}: {path.name} -----")
        proc = subprocess.run([sys.executable, str(path)], cwd=REPO_ROOT)
        results.append((label, proc.returncode))

    print("\n=== Dealix Brand-Growth Operating Layer Verdict ===")
    fail = False
    for label, rc in results:
        verdict = "PASS" if rc == 0 else "FAIL"
        print(f"  {label:24s} → {verdict}")
        if rc != 0:
            fail = True
    print("\nOVERALL:", "FAIL" if fail else "PASS")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
