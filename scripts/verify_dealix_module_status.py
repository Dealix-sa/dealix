#!/usr/bin/env python3
"""Wave 5/6 gate — Dealix module status verification.

Confirms the canonical operating modules referenced by the Company OS exist in
the repo. These are the spine the agents and the commercial chain depend on.
Prints a per-module status table and an overall PASS/FAIL.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Canonical modules (directory must exist). Mirrors the doctrine module layout.
CORE_MODULES = (
    "auto_client_acquisition/data_os",
    "auto_client_acquisition/governance_os",
    "auto_client_acquisition/proof_os",
    "auto_client_acquisition/value_os",
    "auto_client_acquisition/capital_os",
    "auto_client_acquisition/adoption_os",
    "auto_client_acquisition/friction_log",
    "auto_client_acquisition/client_os",
    "auto_client_acquisition/sales_os",
    "auto_client_acquisition/approval_center",
    "auto_client_acquisition/delivery_os",
)

# Commercial business logic (Wave 5/6).
COMMERCIAL = (
    "dealix/commercial",
    "dealix/payments",
    "api/routers",
)


def check(rel: str) -> bool:
    return (REPO / rel).is_dir()


def main() -> int:
    print("== Dealix Module Status Verification ==")
    failures: list[str] = []

    print("\n[core operating modules]")
    for rel in CORE_MODULES:
        ok = check(rel)
        print(f"  {'ok ' if ok else 'MISS'}  {rel}")
        if not ok:
            failures.append(rel)

    print("\n[commercial spine]")
    for rel in COMMERCIAL:
        ok = check(rel)
        print(f"  {'ok ' if ok else 'MISS'}  {rel}")
        if not ok:
            failures.append(rel)

    total = len(CORE_MODULES) + len(COMMERCIAL)
    present = total - len(failures)
    print(f"\nModules present: {present}/{total}")

    if failures:
        print("RESULT: FAIL")
        for f in failures:
            print(f"  - missing {f}")
        return 1

    print("RESULT: PASS — all canonical modules present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
