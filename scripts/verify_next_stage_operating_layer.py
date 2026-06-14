"""Verify that Dealix Operating Layer v1 docs and policies are in place.

Run via:  make next-stage
       or python scripts/verify_next_stage_operating_layer.py

Exits non-zero with a list of missing or too-small artifacts.
"""

from __future__ import annotations

from pathlib import Path

REQUIRED: list[str] = [
    "docs/ops/DEALIX_OPERATING_LAYER_V1.md",
    "docs/ai/CEO_COPILOT_SYSTEM.md",
    "docs/ai/REVENUE_AGENT_SWARM.md",
    "docs/ai/TRUST_GUARDIAN_AGENT.md",
    "docs/ai/EVAL_RED_TEAM_SYSTEM.md",
    "docs/finance/AI_UNIT_ECONOMICS_SYSTEM.md",
    "docs/architecture/AI_NATIVE_COMPANY_ARCHITECTURE.md",
    "docs/data/POSTGRES_PRIMARY_MODE.md",
    "docs/runtime/WORKER_ORCHESTRATOR_V1.md",
    "docs/trust/POLICY_AS_CODE_SYSTEM.md",
    "policies/founder_console_policy.yaml",
]

MIN_BYTES = 80


def main() -> int:
    failures: list[str] = []
    for item in REQUIRED:
        path = Path(item)
        if not path.exists():
            failures.append(f"Missing: {item}")
            continue
        if path.stat().st_size < MIN_BYTES:
            failures.append(f"Too small (< {MIN_BYTES} bytes): {item}")

    if failures:
        print("Next stage operating layer verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: Next-stage operating layer exists.")
    print(f"      {len(REQUIRED)} artifacts present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
