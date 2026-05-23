#!/usr/bin/env python3
"""Top-level verifier for the Dealix Brand-Led Autonomous Growth OS.

Runs each sub-verifier and aggregates the result. Designed to be the
single command CI runs to validate the brand+growth+marketing+product+
AI+performance operating layer.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

SUB_VERIFIERS = [
    "scripts/verify_brand_system.py",
    "scripts/verify_growth_system.py",
    "scripts/verify_marketing_system.py",
    "scripts/verify_product_distribution.py",
    "scripts/verify_advanced_ai_agents.py",
    "scripts/verify_performance_system.py",
]

REQUIRED_AGENT_DOCS = [
    "docs/ai/BRAND_GUARDIAN_AGENT.md",
    "docs/ai/GROWTH_STRATEGIST_AGENT.md",
    "docs/ai/DISTRIBUTION_OPERATOR_AGENT.md",
    "docs/ai/CONTENT_STRATEGIST_AGENT.md",
    "docs/ai/OFFER_ARCHITECT_AGENT.md",
    "docs/ai/PERFORMANCE_ANALYST_AGENT.md",
]


def run(cmd: list[str]) -> int:
    print(f"\n>>> {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=ROOT)
    return proc.returncode


def main() -> int:
    rc_total = 0
    for rel in SUB_VERIFIERS:
        path = ROOT / rel
        if not path.exists():
            print(f"[WARN] missing sub-verifier: {rel}")
            rc_total = 1
            continue
        rc = run([PY, rel])
        if rc != 0:
            rc_total = 1

    # quick spot check of agent docs (defence in depth)
    for rel in REQUIRED_AGENT_DOCS:
        if not (ROOT / rel).exists():
            print(f"[FAIL] missing required agent doc: {rel}")
            rc_total = 1

    print("\n" + "=" * 60)
    if rc_total == 0:
        print("[PASS] Dealix Brand-Led Autonomous Growth OS verified")
    else:
        print("[FAIL] one or more sub-verifiers failed")
    print("=" * 60)
    return rc_total


if __name__ == "__main__":
    sys.exit(main())
