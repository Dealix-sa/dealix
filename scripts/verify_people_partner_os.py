#!/usr/bin/env python3
"""Verify the People, Delegation, Partner OS artifacts are in place."""
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED = [
    "docs/people/PEOPLE_DELEGATION_PARTNER_OS.md",
    "docs/people/FOUNDER_BOTTLENECK_SYSTEM.md",
    "docs/people/DELEGATION_LADDER.md",
    "docs/people/ROLE_ARCHITECTURE.md",
    "docs/people/HIRING_TRIGGER_SYSTEM.md",
    "docs/people/CONTRACTOR_ONBOARDING_SYSTEM.md",
    "docs/people/ACCESS_CONTROL_SYSTEM.md",
    "docs/partners/PARTNER_OPERATING_SYSTEM.md",
    "docs/partners/REFERRAL_TERMS_SYSTEM.md",
    "docs/partners/WHITE_LABEL_GUARDRAILS.md",
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
        print("People/Partner OS verification FAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: People/Delegation/Partner OS is in place.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
