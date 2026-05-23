#!/usr/bin/env python3
"""Composite verifier: brand + growth + marketing.

Runs verify_brand_system, verify_growth_system, verify_marketing_system and
returns the aggregated exit code.
"""

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
]


def run_component(name: str, path: Path) -> int:
    print()
    print(f"## {name}")
    result = subprocess.run([sys.executable, str(path)], check=False)
    return result.returncode


def main() -> int:
    failures: List[str] = []
    for name, path in COMPONENTS:
        rc = run_component(name, path)
        if rc != 0:
            failures.append(name)
    print()
    print("Dealix brand-growth operating layer summary")
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
