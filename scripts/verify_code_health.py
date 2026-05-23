#!/usr/bin/env python3
"""C1 — Verify code health of the acceptance system files.

Runs ruff (hard gate), black --check (warn), and mypy (warn) against the
scripts and docs newly introduced by the certification system. Does not
run them against the whole repo to avoid unrelated noise.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

FAILURES: list[str] = []
WARNINGS: list[str] = []

TARGETS = [
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
]


def ok(msg: str) -> None:
    print(f"  ok: {msg}")


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  FAIL: {msg}")


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"  warn: {msg}")


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)  # noqa: S603


def check_ruff(paths: list[str]) -> None:
    if shutil.which("ruff") is None:
        warn("ruff not installed; skipping")
        return
    result = _run(["ruff", "check", *paths])
    if result.returncode == 0:
        ok("ruff clean on certification scripts")
    else:
        fail(f"ruff errors:\n{result.stdout}\n{result.stderr}")


def check_black(paths: list[str]) -> None:
    if shutil.which("black") is None:
        warn("black not installed; skipping")
        return
    result = _run(["black", "--check", "--quiet", *paths])
    if result.returncode == 0:
        ok("black --check clean on certification scripts")
    else:
        warn(f"black would reformat (non-fatal):\n{result.stdout}")


def check_mypy(paths: list[str]) -> None:
    if shutil.which("mypy") is None:
        warn("mypy not installed; skipping")
        return
    result = _run(["mypy", "--ignore-missing-imports", "--no-error-summary", *paths])
    if result.returncode == 0:
        ok("mypy clean on certification scripts")
    else:
        warn(f"mypy reported issues (non-fatal):\n{result.stdout}")


def check_syntax(paths: list[str]) -> None:
    for p in paths:
        path = REPO / p
        if not path.is_file():
            fail(f"missing target: {p}")
            continue
        result = _run([sys.executable, "-m", "py_compile", str(path)])
        if result.returncode == 0:
            ok(f"compiles: {p}")
        else:
            fail(f"syntax error in {p}: {result.stderr.strip()}")


def main() -> int:
    ensure_stdout_utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-ops", required=True, type=Path)
    parser.parse_args()

    print("# C1 — Code Health")
    existing = [p for p in TARGETS if (REPO / p).is_file()]
    if not existing:
        fail("no certification scripts found yet")
    else:
        check_syntax(existing)
        check_ruff(existing)
        check_black(existing)
        check_mypy(existing)

    ok_status = not FAILURES
    print(f"\nWARNINGS={len(WARNINGS)} FAILURES={len(FAILURES)}")
    print(f"VERIFY_CODE_HEALTH_READY={'true' if ok_status else 'false'}")
    return 0 if ok_status else 1


if __name__ == "__main__":
    raise SystemExit(main())
