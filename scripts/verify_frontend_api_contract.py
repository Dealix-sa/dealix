"""Verify the Dealix Founder Frontend P0 contract files exist and are non-trivial.

Enforces:
  - P0 founder routes exist under apps/web/app/
  - Canonical docs exist (route inventory, API contract, must-have pages,
    CEO implementation, machine priority map, certification system)
  - Each required file is non-empty (>= 50 bytes)

This is the F2/F3 gate of the Frontend Certification System.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_ROUTES = [
    "apps/web/app/ceo/page.tsx",
    "apps/web/app/sales-cockpit/page.tsx",
    "apps/web/app/approvals/page.tsx",
    "apps/web/app/distribution/page.tsx",
    "apps/web/app/workers/page.tsx",
    "apps/web/app/trust/page.tsx",
    "apps/web/app/finance/page.tsx",
]

REQUIRED_DOCS = [
    "docs/api/FRONTEND_API_CONTRACT.md",
    "docs/frontend/FRONTEND_MUST_HAVE_PAGES.md",
    "docs/frontend/FRONTEND_ROUTE_INVENTORY.md",
    "docs/frontend/FRONTEND_CERTIFICATION_SYSTEM.md",
    "docs/product/CEO_COMMAND_CENTER_IMPLEMENTATION.md",
    "docs/runtime/FOUNDER_MACHINE_PRIORITY_MAP.md",
]

REQUIRED_LIB = [
    "apps/web/lib/api.ts",
    "apps/web/lib/types.ts",
]


def main() -> int:
    failures: list[str] = []
    for rel in REQUIRED_ROUTES + REQUIRED_DOCS + REQUIRED_LIB:
        path = REPO_ROOT / rel
        if not path.exists():
            failures.append(f"missing: {rel}")
        elif path.stat().st_size < 50:
            failures.append(f"too short (<50 bytes): {rel}")

    if failures:
        print("FAIL: Frontend API contract verification failed:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS: {len(REQUIRED_ROUTES)} routes + {len(REQUIRED_DOCS)} docs + {len(REQUIRED_LIB)} libs present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
