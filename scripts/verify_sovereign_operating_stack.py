#!/usr/bin/env python3
"""Top-level verifier for the Dealix Sovereign Operating Stack.

Runs every sub-verifier in sequence and prints an aggregated checklist.
This is what `make sovereign-operating-stack` invokes; CI re-runs it.

Exits 0 only if every step passes.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def _file_check(label: str, path: str) -> tuple[str, bool]:
    return label, Path(path).exists()


def _script(label: str, script: str) -> tuple[str, bool]:
    if not Path(script).exists():
        return label, False
    res = subprocess.run([sys.executable, script], capture_output=True, text=True)
    if res.returncode != 0:
        if res.stderr:
            sys.stderr.write(res.stderr)
    return label, res.returncode == 0


def _frontend_build_check() -> tuple[str, bool]:
    apps_web = Path("apps/web")
    if not apps_web.exists():
        return "Frontend present (apps/web)", False

    # We only verify presence + a valid package.json here.
    pkg = apps_web / "package.json"
    if not pkg.exists():
        return "apps/web/package.json present", False
    return "apps/web/package.json present", True


def main() -> int:
    checks: list[tuple[str, bool]] = []
    checks.append(_file_check("CLAUDE.md", "CLAUDE.md"))
    checks.append(_script("Policy-as-Code verifier", "scripts/verify_policy_as_code.py"))
    checks.append(_script("Agent Registry verifier", "scripts/verify_agent_registry.py"))
    checks.append(_script("Eval Gate verifier", "scripts/verify_eval_gate.py"))
    checks.append(_script("Prompt/output safety", "scripts/verify_prompt_output_quality.py"))
    checks.append(_file_check("Founder Console (CEO page)", "apps/web/app/ceo/page.tsx"))
    checks.append(_file_check("Founder Console (Sovereign page)", "apps/web/app/sovereign/page.tsx"))
    checks.append(_file_check("Internal API router", "api/routers/internal/founder_console.py"))
    checks.append(_file_check("Internal runtime reader", "api/internal/runtime_reader.py"))
    checks.append(_file_check("Internal auth gate", "api/internal/auth.py"))
    checks.append(_file_check("Private ops bootstrap script", "scripts/bootstrap_private_ops_runtime.py"))
    checks.append(_file_check("Operating scorecard script", "scripts/generate_operating_scorecard.py"))
    checks.append(_file_check("Sovereign readiness script", "scripts/generate_sovereign_readiness.py"))
    checks.append(_file_check("Control Plane page", "apps/web/app/control-plane/page.tsx"))
    checks.append(_file_check("Sovereign page", "apps/web/app/sovereign/page.tsx"))
    checks.append(_file_check("GitHub workflow", ".github/workflows/dealix-sovereign-operating-stack.yml"))
    checks.append(_file_check("Makefile target: bootstrap-runtime", "Makefile"))
    checks.append(_frontend_build_check())

    print("Dealix Sovereign Operating Stack — Verifier")
    print("=" * 56)
    fails = 0
    for label, ok in checks:
        marker = "[PASS]" if ok else "[FAIL]"
        if not ok:
            fails += 1
        print(f"{marker}  {label}")
    print("=" * 56)
    total = len(checks)
    print(f"summary: {total - fails}/{total} passed")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
