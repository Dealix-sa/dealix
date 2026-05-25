#!/usr/bin/env python3
"""C1 — Verify Dealix repository structure for the acceptance system.

Checks that the folders, files, and acceptance docs required by the
certification system are present in the repo. Skips private-ops-only
assertions under CI.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

FAILURES: list[str] = []
WARNINGS: list[str] = []

REQUIRED_DIRS = (
    "dealix",
    "scripts",
    "tests",
    "docs/certification",
    "evals",
    "dealix/contracts/schemas",
)

REQUIRED_FILES = (
    "Makefile",
    "pyproject.toml",
    "requirements.txt",
    "docs/certification/DEALIX_OS_ACCEPTANCE.md",
    "docs/certification/SERVER_ACCEPTANCE_TEST.md",
    "docs/certification/REVENUE_FACTORY_ACCEPTANCE_TEST.md",
    "docs/certification/AGENT_OUTPUT_CONTRACT.md",
    "dealix/contracts/schemas/agent_output_contract.schema.json",
    "evals/golden/prompt_output_golden_tests.yaml",
)

REQUIRED_SCRIPTS = (
    "scripts/certify_dealix_os.py",
    "scripts/verify_repository_structure.py",
    "scripts/verify_code_health.py",
    "scripts/verify_private_ops_contracts.py",
    "scripts/verify_revenue_runtime.py",
    "scripts/verify_prompt_output_quality.py",
    "scripts/verify_trust_security_runtime.py",
    "scripts/verify_server_runtime.py",
    "scripts/verify_business_evidence.py",
    "scripts/run_prompt_golden_tests.py",
    "scripts/verify_agent_outputs.py",
    "scripts/generate_ceo_verification_brief.py",
)


def ok(msg: str) -> None:
    print(f"  ok: {msg}")


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  FAIL: {msg}")


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"  warn: {msg}")


def main() -> int:
    ensure_stdout_utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-ops", required=True, type=Path)
    args = parser.parse_args()

    print("# C1 — Repository Structure")

    for d in REQUIRED_DIRS:
        path = REPO / d
        if path.is_dir():
            ok(f"dir present: {d}")
        else:
            fail(f"missing directory: {d}")

    for f in REQUIRED_FILES:
        path = REPO / f
        if path.is_file():
            ok(f"file present: {f}")
        else:
            fail(f"missing file: {f}")

    for s in REQUIRED_SCRIPTS:
        path = REPO / s
        if path.is_file():
            ok(f"script present: {s}")
        else:
            fail(f"missing script: {s}")

    # Private-ops cross-check only outside CI.
    if os.environ.get("CI") != "true":
        if not args.private_ops.exists():
            warn(f"private ops dir does not exist yet: {args.private_ops}")
        else:
            ok(f"private ops dir reachable: {args.private_ops}")

    ok_status = not FAILURES
    print(f"\nWARNINGS={len(WARNINGS)} FAILURES={len(FAILURES)}")
    print(f"VERIFY_REPOSITORY_STRUCTURE_READY={'true' if ok_status else 'false'}")
    return 0 if ok_status else 1


if __name__ == "__main__":
    raise SystemExit(main())
