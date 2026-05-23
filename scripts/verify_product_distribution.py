#!/usr/bin/env python3
"""Verify the Dealix product distribution documentation surface.

Checks for the presence of:
- docs/product/PRODUCT_DISTRIBUTION_OS.md
- docs/product/DEALIX_PRODUCT_LADDER.md

Exit 0 on success, 1 on failure.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED = [
    REPO_ROOT / "docs" / "product" / "PRODUCT_DISTRIBUTION_OS.md",
    REPO_ROOT / "docs" / "product" / "DEALIX_PRODUCT_LADDER.md",
]


def main() -> int:
    results: List[Tuple[str, bool]] = []
    for path in REQUIRED:
        results.append((str(path), path.exists()))
    passed = sum(1 for _, ok in results if ok)
    print("Dealix product-distribution verification")
    print("-" * 40)
    for label, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {label}")
    print("-" * 40)
    print(f"summary: {passed}/{len(results)} checks passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
