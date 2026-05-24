#!/usr/bin/env python3
"""Composite verifier for the ultimate operating layer.

Brand+growth+marketing+product, plus policy-as-code, agent registry,
eval gate, and the founder-console UI surface.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from _verify_common import ROOT as REPO_ROOT, Verifier

ROOT = Path(__file__).resolve().parent

CHILD_VERIFIERS = [
    "verify_brand_system.py",
    "verify_growth_system.py",
    "verify_marketing_system.py",
    "verify_product_distribution.py",
    "verify_policy_as_code.py",
    "verify_agent_registry.py",
    "verify_eval_gate.py",
    "verify_prompt_output_quality.py",
]

CONSOLE_PAGES = [
    "apps/web/app/page.tsx",
    "apps/web/app/ceo/page.tsx",
    "apps/web/app/sales-cockpit/page.tsx",
    "apps/web/app/approvals/page.tsx",
    "apps/web/app/workers/page.tsx",
    "apps/web/app/trust/page.tsx",
    "apps/web/app/finance/page.tsx",
    "apps/web/app/distribution/page.tsx",
    "apps/web/app/delivery/page.tsx",
    "apps/web/app/retention/page.tsx",
    "apps/web/app/proof/page.tsx",
    "apps/web/app/control-plane/page.tsx",
    "apps/web/app/audit/page.tsx",
    "apps/web/app/evals/page.tsx",
    "apps/web/app/product/page.tsx",
    "apps/web/app/security/page.tsx",
    "apps/web/app/sovereign/page.tsx",
    "apps/web/app/growth/page.tsx",
    "apps/web/app/marketing/page.tsx",
    "apps/web/app/agents/page.tsx",
]

INTERNAL_API_FILES = [
    "api/internal/auth.py",
    "api/internal/runtime_reader.py",
    "api/internal/policy_adapter.py",
    "api/routers/internal/founder_console.py",
]


def main() -> int:
    failures = 0

    v = Verifier("founder-console + internal-api scaffolding")
    v.check_files(CONSOLE_PAGES)
    v.check_files(INTERNAL_API_FILES)
    if v.report() != 0:
        failures += 1

    for child in CHILD_VERIFIERS:
        print(f"\n=== running {child} ===")
        rc = subprocess.run([sys.executable, str(ROOT / child)]).returncode
        if rc != 0:
            failures += 1

    print(f"\n[ultimate-operating-layer] failures: {failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
