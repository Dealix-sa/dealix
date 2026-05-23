#!/usr/bin/env python3
"""Verify the Control Plane stage is wired (frontend + API + governance)."""

from __future__ import annotations

import sys
from pathlib import Path

REQUIRED = [
    "apps/web/app/control-plane/page.tsx",
    "apps/web/lib/dealix-runtime.ts",
    "apps/web/lib/dealix-actions.ts",
    "api/routers/internal/founder_console.py",
    "api/internal/auth.py",
    "api/internal/runtime_reader.py",
    "api/internal/policy_adapter.py",
    "policies/dealix_control_policy.yaml",
    "registries/agent_registry.yaml",
    "evals/gates/dealix_agent_eval_gate.yaml",
]


def main() -> int:
    missing = [p for p in REQUIRED if not Path(p).exists()]
    if missing:
        for p in missing:
            print(f"[FAIL] control plane stage missing: {p}", file=sys.stderr)
        return 1
    print(f"[PASS] control plane stage: {len(REQUIRED)} required files present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
