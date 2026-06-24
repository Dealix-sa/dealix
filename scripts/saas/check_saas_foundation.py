#!/usr/bin/env python3
"""Check that the Dealix SaaS foundation files exist."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    "docs/saas/SAAS_FOUNDATION_PLAN.md",
    "docs/saas/MULTI_TENANT_ARCHITECTURE.md",
    "docs/saas/TENANT_SECURITY_MODEL.md",
    "docs/saas/COMMERCIAL_LAUNCH_PLAYBOOK_AR.md",
    "sales/SAAS_BETA_OFFER_AR.md",
    "api/tenant_context.py",
    "app/saas/access_policy.py",
    "app/saas/tenant_guard.py",
    "app/billing/moyasar_stub.py",
]


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        print("SAAS_FOUNDATION_CHECK=FAIL")
        for path in missing:
            print(f"MISSING: {path}")
        return 1
    print("SAAS_FOUNDATION_CHECK=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
