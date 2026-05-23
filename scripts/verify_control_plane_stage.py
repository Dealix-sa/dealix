#!/usr/bin/env python3
"""Verify that the control plane stage files exist and load."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED = [
    "policies/dealix_control_policy.yaml",
    "registries/agent_registry.yaml",
    "evals/gates/dealix_agent_eval_gate.yaml",
    "api/internal/auth.py",
    "api/internal/runtime_reader.py",
    "api/internal/policy_adapter.py",
    "api/routers/internal/founder_console.py",
    "apps/web/components/founder-shell.tsx",
    "apps/web/lib/dealix-runtime.ts",
    "apps/web/lib/dealix-actions.ts",
    "apps/web/app/control-plane/page.tsx",
    "apps/web/app/ceo/page.tsx",
]


def main() -> int:
    missing = [p for p in REQUIRED if not (REPO_ROOT / p).exists()]
    if missing:
        for m in missing:
            print(f"[verify_control_plane_stage] FAIL: missing {m}")
        return 1
    print(f"[verify_control_plane_stage] PASS  required={len(REQUIRED)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
