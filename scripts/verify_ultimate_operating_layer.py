#!/usr/bin/env python3
"""Composite verifier: brand + growth + marketing + policy + agents + evals."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
COMPONENTS: List[Tuple[str, Path]] = [
    ("brand-system", SCRIPT_DIR / "verify_brand_system.py"),
    ("growth-system", SCRIPT_DIR / "verify_growth_system.py"),
    ("marketing-system", SCRIPT_DIR / "verify_marketing_system.py"),
    ("policy-as-code", SCRIPT_DIR / "verify_policy_as_code.py"),
    ("agent-registry", SCRIPT_DIR / "verify_agent_registry.py"),
    ("eval-gate", SCRIPT_DIR / "verify_eval_gate.py"),
]


def main() -> int:
    failures: List[str] = []
    for name, path in COMPONENTS:
        print()
        print(f"## {name}")
        rc = subprocess.run([sys.executable, str(path)], check=False).returncode
        if rc != 0:
            failures.append(name)
    print()
    print("Dealix ultimate operating layer summary")
    print("-" * 40)
    print(f"  components run : {len(COMPONENTS)}")
    print(f"  failures       : {len(failures)}")
    if failures:
        print(f"  failed         : {', '.join(failures)}")
        return 1
    print("summary: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
