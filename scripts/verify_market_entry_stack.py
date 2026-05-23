#!/usr/bin/env python3
"""Runs every Dealix Section-A verifier and prints a final scorecard."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

COMPONENTS: List[Tuple[str, Path]] = [
    ("brand-system", SCRIPT_DIR / "verify_brand_system.py"),
    ("growth-system", SCRIPT_DIR / "verify_growth_system.py"),
    ("marketing-system", SCRIPT_DIR / "verify_marketing_system.py"),
    ("product-distribution", SCRIPT_DIR / "verify_product_distribution.py"),
    ("policy-as-code", SCRIPT_DIR / "verify_policy_as_code.py"),
    ("agent-registry", SCRIPT_DIR / "verify_agent_registry.py"),
    ("eval-gate", SCRIPT_DIR / "verify_eval_gate.py"),
    ("prompt-output-quality", SCRIPT_DIR / "verify_prompt_output_quality.py"),
]

SECURITY_GATE = REPO_ROOT / "docs" / "security" / "PRODUCTION_SECURITY_GATE.md"


def main() -> int:
    results: List[Tuple[str, int]] = []
    for name, path in COMPONENTS:
        print()
        print(f"## {name}")
        rc = subprocess.run([sys.executable, str(path)], check=False).returncode
        results.append((name, rc))
    print()
    print("## production-security-gate")
    if SECURITY_GATE.exists() and SECURITY_GATE.stat().st_size > 200:
        print(f"  [PASS] {SECURITY_GATE}")
        results.append(("production-security-gate", 0))
    else:
        print(f"  [FAIL] missing or undersized {SECURITY_GATE}")
        results.append(("production-security-gate", 1))

    print()
    print("Dealix market-entry stack scorecard")
    print("-" * 50)
    failed = [name for name, rc in results if rc != 0]
    for name, rc in results:
        mark = "PASS" if rc == 0 else "FAIL"
        print(f"  [{mark}] {name}")
    print("-" * 50)
    print(f"  components run : {len(results)}")
    print(f"  failures       : {len(failed)}")
    if failed:
        print(f"  failed         : {', '.join(failed)}")
        return 1
    print("summary: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
