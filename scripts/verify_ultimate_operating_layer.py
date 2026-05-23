#!/usr/bin/env python3
"""Master verifier for the Dealix Ultimate Operating Layer.

Runs the per-layer verifiers and reports pass/fail per layer. Returns
non-zero on any failure. Does NOT build the frontend (the GitHub
workflow does that) — it only checks that the frontend files exist.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


CHECKS = [
    ("policy",   [sys.executable, "scripts/verify_policy_as_code.py"]),
    ("agents",   [sys.executable, "scripts/verify_agent_registry.py"]),
    ("evals",    [sys.executable, "scripts/verify_eval_gate.py"]),
    ("quality",  [sys.executable, "scripts/verify_prompt_output_quality.py"]),
    ("stage",    [sys.executable, "scripts/verify_control_plane_stage.py"]),
]

FRONTEND_FILES = [
    "apps/web/components/founder-shell.tsx",
    "apps/web/lib/dealix-runtime.ts",
    "apps/web/lib/dealix-actions.ts",
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
]


def run(cmd: list[str]) -> int:
    proc = subprocess.run(cmd, cwd=REPO_ROOT)
    return proc.returncode


def main() -> int:
    fail = 0
    for name, cmd in CHECKS:
        rc = run(cmd)
        print(f"[ultimate_operating_layer] {name}: {'PASS' if rc == 0 else 'FAIL'}")
        if rc != 0:
            fail += 1
    missing = [f for f in FRONTEND_FILES if not (REPO_ROOT / f).exists()]
    if missing:
        for m in missing:
            print(f"[ultimate_operating_layer] frontend missing: {m}")
        fail += 1
    else:
        print(f"[ultimate_operating_layer] frontend files: PASS ({len(FRONTEND_FILES)})")
    if fail:
        print(f"[ultimate_operating_layer] OVERALL: FAIL ({fail} layer(s))")
        return 1
    print("[ultimate_operating_layer] OVERALL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
