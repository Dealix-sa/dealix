#!/usr/bin/env python3
"""Verify product distribution surface."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, must_exist, print_and_exit  # noqa: E402


REQUIRED = [
    "apps/web/app/productization/page.tsx",
    "apps/web/app/distribution/page.tsx",
    "scripts/generate_productization_pipeline_report.py",
]


def main() -> int:
    result = VerifyResult(name="Product Distribution", passed=True)
    must_exist(REQUIRED, result)
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
