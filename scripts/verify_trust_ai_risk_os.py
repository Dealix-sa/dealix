#!/usr/bin/env python3
"""Verify the Trust, Compliance, AI Risk OS artifacts are in place."""
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED = [
    "docs/trust/TRUST_COMPLIANCE_AI_RISK_OS.md",
    "docs/trust/APPROVAL_MATRIX_V2.md",
    "docs/trust/CLAIM_GOVERNANCE_SYSTEM.md",
    "docs/data/DATA_MINIMIZATION_RETENTION.md",
    "docs/data/REDACTION_SYSTEM.md",
    "docs/ai_management/AI_RISK_REGISTER.md",
    "docs/ai_management/PROMPT_INJECTION_DEFENSE.md",
    "scripts/generate_trust_review.py",
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
        print("Trust/AI Risk OS verification FAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: Trust/Compliance/AI Risk OS is in place.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
