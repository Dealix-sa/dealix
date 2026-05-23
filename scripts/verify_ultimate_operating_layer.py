#!/usr/bin/env python3
"""Dealix Ultimate Operating Layer — master verifier.

Runs every sub-verifier and checks that every expected artefact exists.
Exit non-zero on any failure. This is the single command that proves the
operating layer is wired end to end.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "CLAUDE.md",
    "policies/dealix_control_policy.yaml",
    "registries/agent_registry.yaml",
    "evals/gates/dealix_agent_eval_gate.yaml",
    "api/internal/__init__.py",
    "api/internal/auth.py",
    "api/internal/runtime_reader.py",
    "api/internal/policy_adapter.py",
    "api/internal/agent_registry_reader.py",
    "api/routers/internal/founder_console.py",
    "scripts/bootstrap_private_ops_runtime.py",
    "scripts/generate_operating_scorecard.py",
    "scripts/verify_policy_as_code.py",
    "scripts/verify_agent_registry.py",
    "scripts/verify_eval_gate.py",
    "scripts/verify_prompt_output_quality.py",
    "scripts/smoke_internal_api.py",
    "apps/web/lib/dealix-runtime.ts",
    "apps/web/lib/dealix-actions.ts",
    "apps/web/components/founder/founder-shell.tsx",
    "apps/web/app/ceo/page.tsx",
    "apps/web/app/sales-cockpit/page.tsx",
    "apps/web/app/approvals/page.tsx",
    "apps/web/app/workers/page.tsx",
    "apps/web/app/trust/page.tsx",
    "apps/web/app/finance/page.tsx",
    "apps/web/app/distribution/page.tsx",
    "apps/web/app/delivery/page.tsx",
    "apps/web/app/retention/page.tsx",
    "apps/web/app/proof/page.tsx",
    "apps/web/app/control-plane/page.tsx",
    "apps/web/app/audit/page.tsx",
    "apps/web/app/evals/page.tsx",
    "apps/web/app/product/page.tsx",
    "apps/web/app/security/page.tsx",
    ".github/workflows/dealix-ultimate-operating-layer.yml",
]

SUB_VERIFIERS = [
    "scripts/verify_policy_as_code.py",
    "scripts/verify_agent_registry.py",
    "scripts/verify_eval_gate.py",
    "scripts/verify_prompt_output_quality.py",
]


def check_files() -> list[str]:
    missing: list[str] = []
    for rel in REQUIRED_FILES:
        if not (REPO / rel).exists():
            missing.append(rel)
    return missing


def run_sub(script: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(REPO / script)],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main() -> int:
    print("== Dealix Ultimate Operating Layer — master verifier ==\n")
    missing = check_files()
    if missing:
        print("FAIL: missing required files:")
        for path in missing:
            print(f"  - {path}")
        return 1
    print(f"OK: all {len(REQUIRED_FILES)} required files present\n")

    failures: list[tuple[str, str]] = []
    for script in SUB_VERIFIERS:
        print(f"-- running {script}")
        code, output = run_sub(script)
        if code != 0:
            failures.append((script, output))
            print(output)
            print(f"FAIL ({script})\n")
        else:
            tail = output.strip().splitlines()
            if tail:
                print(tail[-1])
            print(f"OK ({script})\n")

    # Quick smoke: importing internal modules must not error.
    sys.path.insert(0, str(REPO))
    print("-- importing api.internal.* modules")
    try:
        from api.internal import (  # noqa: F401
            agent_registry_reader,
            auth,
            policy_adapter,
            runtime_reader,
        )
        from api.routers.internal import founder_console  # noqa: F401
        print("OK: imports succeeded\n")
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: import error: {exc}")
        return 1

    if failures:
        print("\n== SUMMARY: FAIL ==")
        for script, _ in failures:
            print(f"  - {script}")
        return 1

    print("== SUMMARY: ALL CHECKS PASSED ==")
    return 0


if __name__ == "__main__":
    sys.exit(main())
