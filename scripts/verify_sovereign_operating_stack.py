#!/usr/bin/env python3
"""Verify the sovereign / Saudi-ready operating stack documentation."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = [
    "docs/security/ULTIMATE_SECURITY_GOVERNANCE.md",
    "docs/security/PRODUCTION_SECURITY_GATE.md",
    "docs/security/INTERNAL_API_AUTH_GATE.md",
    "docs/security/BRANCH_PROTECTION_REQUIRED_CHECKS.md",
    "docs/security/INCIDENT_RESPONSE_OS.md",
    "docs/security/BACKUP_AND_RESTORE_OS.md",
    "docs/security/ACCESS_CONTROL_MODEL.md",
    "docs/data/POSTGRES_PRIMARY_MODE.md",
    "docs/trust/ULTIMATE_TRUST_PLANE.md",
    "docs/trust/AUDIT_EVENT_MODEL.md",
]


def main() -> int:
    missing = [f for f in REQUIRED if not (REPO / f).exists()]
    print("[sovereign-operating-stack]")
    print(f"  missing: {len(missing)}")
    for m in missing:
        print(f"    - {m}")
    print("RESULT:", "FAIL" if missing else "PASS")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
