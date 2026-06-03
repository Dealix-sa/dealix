#!/usr/bin/env python3
"""Verify the Productization & Engineering OS artifacts are in place."""
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED = [
    "docs/product/PRODUCTIZATION_ENGINEERING_OS.md",
    "docs/product/PRODUCTIZATION_DECISION_SYSTEM.md",
    "docs/product/SAAS_ARCHITECTURE_GATE.md",
    "docs/engineering/ENGINEERING_ARCHITECTURE.md",
    "docs/automation/AUTOMATION_PERMISSION_MATRIX.md",
    "docs/agents/AGENT_READINESS_SYSTEM.md",
    "ops_runtime/productization_scorer.py",
    "scripts/generate_productization_review.py",
]


def main() -> int:
    failures: list[str] = []
    for rel in REQUIRED:
        p = Path(rel)
        if not p.exists():
            failures.append(f"Missing: {rel}")
        elif p.stat().st_size < 30:
            failures.append(f"Too short: {rel}")
    if failures:
        print("Productization/Engineering OS verification FAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: Productization/Engineering OS is in place.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
