#!/usr/bin/env python3
"""Verify the full Dealix Company OS surface (pages + APIs + workflows)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, must_exist, print_and_exit  # noqa: E402

REQUIRED = [
    # Founder shell
    "apps/web/components/founder-shell.tsx",
    "apps/web/components/brand/founder-page.tsx",
    # Internal API
    "api/internal/auth.py",
    "api/internal/runtime_reader.py",
    "api/internal/policy_adapter.py",
    "api/routers/internal/founder_console.py",
    # Bootstrap + smoke
    "scripts/bootstrap_private_ops_runtime.py",
    "scripts/smoke_internal_api.py",
    # GitHub
    ".github/workflows/dealix-company-os.yml",
    ".github/workflows/dealix-everything.yml",
]


def main() -> int:
    result = VerifyResult(name="Company OS", passed=True)
    must_exist(REQUIRED, result)
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
