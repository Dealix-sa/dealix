#!/usr/bin/env python3
"""Verify launch readiness pages + workflows."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, must_exist, print_and_exit  # noqa: E402

REQUIRED = [
    "apps/web/app/launch/page.tsx",
    "apps/web/app/approvals/page.tsx",
    ".github/workflows/dealix-execution-launch-layer.yml",
]


def main() -> int:
    result = VerifyResult(name="Launch Readiness", passed=True)
    must_exist(REQUIRED, result)
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
