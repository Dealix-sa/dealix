#!/usr/bin/env python3
"""C2 — Verify the private-ops directory layout.

Ensures `$PRIVATE_OPS` exists, sits OUTSIDE the repository, and contains
the canonical subtree: founder/, intelligence/, outreach/, sales/,
finance/, runtime/, logs/. Skipped under CI.
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

REQUIRED_SUBTREE = (
    "founder",
    "intelligence",
    "outreach",
    "sales",
    "finance",
    "runtime",
    "logs",
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

    print("# C2 — Private Ops Contracts")

    if os.environ.get("CI") == "true":
        warn("CI mode: skipping private-ops layout checks")
        ok_status = not FAILURES
        print(f"VERIFY_PRIVATE_OPS_CONTRACTS_READY={'true' if ok_status else 'false'}")
        return 0 if ok_status else 1

    private_ops = args.private_ops
    if not private_ops.exists():
        fail(f"private ops dir does not exist: {private_ops}")
        print("VERIFY_PRIVATE_OPS_CONTRACTS_READY=false")
        return 1

    try:
        resolved = private_ops.resolve()
    except OSError as e:
        fail(f"cannot resolve private ops path: {e}")
        print("VERIFY_PRIVATE_OPS_CONTRACTS_READY=false")
        return 1

    if str(resolved).startswith(str(REPO)):
        fail(f"private ops must NOT be inside the repo: {resolved} is under {REPO}")
    else:
        ok(f"private ops is outside the repo: {resolved}")

    for sub in REQUIRED_SUBTREE:
        path = private_ops / sub
        if path.is_dir():
            ok(f"subdir present: {sub}/")
        else:
            fail(f"missing subdir: {sub}/")

    ok_status = not FAILURES
    print(f"\nWARNINGS={len(WARNINGS)} FAILURES={len(FAILURES)}")
    print(f"VERIFY_PRIVATE_OPS_CONTRACTS_READY={'true' if ok_status else 'false'}")
    return 0 if ok_status else 1


if __name__ == "__main__":
    raise SystemExit(main())
