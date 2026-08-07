#!/usr/bin/env python3
"""Conservative company launch readiness gate for Dealix test matrix.

This gate validates that the repository can run in review-only / draft-only mode.
It does not enable sending, mutate production, or require live provider credentials.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    if truthy("SMS_SEND_ENABLED"):
        failures.append("SMS_SEND_ENABLED=true is not allowed in baseline launch readiness.")

    if truthy("EXTERNAL_SEND_ENABLED"):
        mode = os.getenv("OUTBOUND_MODE", "")
        if mode != "controlled_live":
            failures.append("EXTERNAL_SEND_ENABLED=true requires OUTBOUND_MODE=controlled_live.")

    required = [
        "Makefile",
        "pyproject.toml",
        "scripts/security_smoke.py",
        "scripts/check_env_contract.py",
        "scripts/ops/run_full_repo_test_matrix.sh",
    ]

    for rel in required:
        if not (ROOT / rel).exists():
            failures.append(f"Missing required launch file: {rel}")

    optional = [
        "apps/web/package.json",
        "docs/ops/FULL_REPO_TEST_MATRIX.md",
        "docs/ops/TESTSPRITE_MCP_SETUP.md",
    ]

    for rel in optional:
        if not (ROOT / rel).exists():
            warnings.append(f"Missing optional launch file: {rel}")

    if failures:
        print("COMPANY_LAUNCH_READY=BLOCKED")
        for item in failures:
            print(f"FAIL: {item}")
        for item in warnings:
            print(f"WARN: {item}")
        return 1

    print("COMPANY_LAUNCH_READY=READY_FOR_MANUAL_OUTREACH")
    print("Mode: safe review-only / draft-only unless controlled-live gates are explicitly enabled.")
    for item in warnings:
        print(f"WARN: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
