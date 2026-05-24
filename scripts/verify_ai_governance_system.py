#!/usr/bin/env python3
"""Verify the AI governance system layer."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, must_exist, print_and_exit  # noqa: E402

REQUIRED = [
    "policies/dealix_control_policy.yaml",
    "registries/agent_registry.yaml",
    "registries/machine_registry.yaml",
    "evals/gates/dealix_agent_eval_gate.yaml",
    "apps/web/app/ai-governance/page.tsx",
    "apps/web/app/trust/page.tsx",
    "scripts/generate_ai_governance_board_pack.py",
]


def main() -> int:
    result = VerifyResult(name="AI Governance", passed=True)
    must_exist(REQUIRED, result)
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
