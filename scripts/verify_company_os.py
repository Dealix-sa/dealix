#!/usr/bin/env python3
"""Composite verifier: every Dealix Operating System pillar at once."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

PIPELINE = [
    ("brand", "verify_brand_system.py"),
    ("growth", "verify_growth_system.py"),
    ("marketing", "verify_marketing_system.py"),
    ("product", "verify_product_distribution.py"),
    ("policy", "verify_policy_as_code.py"),
    ("agents", "verify_agent_registry.py"),
    ("evals", "verify_eval_gate.py"),
    ("prompt_quality", "verify_prompt_output_quality.py"),
    ("ultimate_layer", "verify_ultimate_operating_layer.py"),
    ("brand_growth_layer", "verify_brand_growth_operating_layer.py"),
    ("sovereign", "verify_sovereign_operating_stack.py"),
    ("market_entry", "verify_market_entry_stack.py"),
]


def main() -> int:
    failures: list[tuple[str, int]] = []
    for name, script in PIPELINE:
        print(f"=== company-os :: {name} ===", flush=True)
        rc = subprocess.call(
            [sys.executable, str(REPO / "scripts" / script)],
            cwd=str(REPO),
        )
        if rc != 0:
            failures.append((name, rc))
            print(f"  >>> step '{name}' returned non-zero rc={rc}", flush=True)
    print(flush=True)
    print("===== Dealix Company OS Verifier =====", flush=True)
    if failures:
        print(f"  failed steps: {failures}", flush=True)
    else:
        print("  failed steps: []", flush=True)
    print("RESULT:", "FAIL" if failures else "PASS", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
