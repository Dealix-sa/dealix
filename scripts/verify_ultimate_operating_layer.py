#!/usr/bin/env python3
"""Verify the Ultimate Operating Layer documents are present."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = [
    "docs/ops/DEALIX_FINAL_OPERATING_SYSTEM.md",
    "docs/ops/DEALIX_MARKET_ENTRY_OPERATING_STACK.md",
    "docs/ops/CLAUDE_CODE_EXECUTION_REPORT.md",
    "docs/trust/POLICY_AS_CODE_V1.md",
    "docs/trust/ULTIMATE_TRUST_PLANE.md",
    "docs/trust/AUDIT_EVENT_MODEL.md",
    "docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md",
    "docs/runtime/WORKER_ORCHESTRATOR_V1.md",
    "docs/runtime/ULTIMATE_WORKER_MESH.md",
    "docs/data/POSTGRES_PRIMARY_MODE.md",
    "docs/data/ULTIMATE_DATA_PLATFORM.md",
    "docs/engineering/ULTIMATE_OBSERVABILITY_DORA.md",
    "docs/engineering/DEPLOYMENT_AND_ROLLBACK_SYSTEM.md",
    "docs/ai/AGENT_REGISTRY_SYSTEM.md",
    "docs/evals/EVAL_GATE_V1.md",
    "docs/evals/PROMPT_OUTPUT_EVAL_MATRIX.md",
    "policies/dealix_control_policy.yaml",
    "registries/agent_registry.yaml",
    "evals/gates/dealix_agent_eval_gate.yaml",
]


def main() -> int:
    missing = [f for f in REQUIRED if not (REPO / f).exists()]
    print("[ultimate-operating-layer]")
    print(f"  missing: {len(missing)}")
    for m in missing:
        print(f"    - {m}")
    print("RESULT:", "FAIL" if missing else "PASS")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
