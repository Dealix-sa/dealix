#!/usr/bin/env python3
"""Aggregate AI governance gate.

Runs the five child verifiers as subprocesses and reports overall PASS/FAIL.
Mirrors the _run_script pattern from scripts/verify_dealix_ready.py.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

CHILDREN = (
    "verify_policy_as_code.py",
    "verify_agent_registry.py",
    "verify_machine_registry.py",
    "verify_eval_gate.py",
    "verify_prompt_output_quality.py",
)


def _run(name: str) -> bool:
    proc = subprocess.run(  # noqa: S603
        [sys.executable, str(REPO / "scripts" / name)],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        # Surface child stderr for diagnostics.
        sys.stderr.write(proc.stderr)
    return proc.returncode == 0


def main() -> int:
    results = {name: _run(name) for name in CHILDREN}
    for name, ok in results.items():
        print(f"AI_GOV_CHILD_{name}={'true' if ok else 'false'}")
    overall = all(results.values())
    print(f"AI_GOVERNANCE_SYSTEM_PASS={'true' if overall else 'false'}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
