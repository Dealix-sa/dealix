#!/usr/bin/env python3
"""
Composite verifier for the Brand & Growth Operating Layer.

Runs:
- verify_brand_system.py
- verify_growth_system.py
- verify_marketing_system.py
- verify_product_distribution.py

Also verifies:
- AI agent docs exist (brand_guardian, growth_strategist, distribution_operator,
  content_strategist, offer_architect, performance_analyst, trust_guardian, eval_red_team).
- Positioning + category docs exist.
- Performance OS docs exist.
- The internal API router file exists.
- The new founder console pages exist.

Exits non-zero if anything fails. This is the gate for the
`brand-growth-operating-layer` Makefile target and the matching GitHub Action.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHILD_VERIFIERS = [
    "scripts/verify_brand_system.py",
    "scripts/verify_growth_system.py",
    "scripts/verify_marketing_system.py",
    "scripts/verify_product_distribution.py",
]

REQUIRED_FILES = [
    # Positioning
    "docs/positioning/CATEGORY_CREATION_OS.md",
    "docs/positioning/DEALIX_POSITIONING.md",
    "docs/positioning/COMPETITIVE_NARRATIVE.md",
    "docs/positioning/WHY_DEALIX_NOW.md",
    "docs/positioning/MESSAGING_HIERARCHY.md",
    # AI agents
    "docs/ai/BRAND_GUARDIAN_AGENT.md",
    "docs/ai/GROWTH_STRATEGIST_AGENT.md",
    "docs/ai/DISTRIBUTION_OPERATOR_AGENT.md",
    "docs/ai/CONTENT_STRATEGIST_AGENT.md",
    "docs/ai/OFFER_ARCHITECT_AGENT.md",
    "docs/ai/PERFORMANCE_ANALYST_AGENT.md",
    "docs/ai/TRUST_GUARDIAN_AGENT.md",
    "docs/ai/EVAL_RED_TEAM_SYSTEM.md",
    # Performance
    "docs/performance/PERFORMANCE_IMPROVEMENT_OS.md",
    "docs/performance/REVENUE_KPI_TREE.md",
    "docs/performance/CONVERSION_DIAGNOSTICS.md",
    "docs/performance/EXPERIMENT_BACKLOG.md",
    "docs/performance/LEARNING_LOOP.md",
    # API router
    "api/routers/brand_growth_internal.py",
    # Founder console pages
    "apps/web/app/ceo/page.tsx",
    "apps/web/app/sales-cockpit/page.tsx",
    "apps/web/app/distribution/page.tsx",
    "apps/web/app/trust/page.tsx",
    "apps/web/app/finance/page.tsx",
    "apps/web/app/delivery/page.tsx",
    "apps/web/app/retention/page.tsx",
    "apps/web/app/proof/page.tsx",
    "apps/web/app/audit/page.tsx",
    "apps/web/app/evals/page.tsx",
    "apps/web/app/product/page.tsx",
    "apps/web/app/marketing/page.tsx",
    "apps/web/app/growth/page.tsx",
    "apps/web/app/workers/page.tsx",
    "apps/web/app/security/page.tsx",
    "apps/web/app/sovereign/page.tsx",
]


def run_child(script: str) -> int:
    print(f"\n=== {script} ===")
    result = subprocess.run(
        [sys.executable, str(ROOT / script)],
        capture_output=True,
        text=True,
        check=False,
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode


def main() -> int:
    failures: list[str] = []
    passes: list[str] = []

    for script in CHILD_VERIFIERS:
        code = run_child(script)
        if code != 0:
            failures.append(f"{script} returned {code}")
        else:
            passes.append(f"{script} OK")

    print("\n=== File existence sweep ===")
    for path in REQUIRED_FILES:
        if (ROOT / path).exists():
            passes.append(f"file exists: {path}")
        else:
            failures.append(f"MISSING file: {path}")

    print(f"\nComposite PASSED: {len(passes)}")
    print(f"Composite FAILED: {len(failures)}")
    for f in failures:
        print(f"  - {f}")

    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
