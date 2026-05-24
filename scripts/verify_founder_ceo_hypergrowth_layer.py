#!/usr/bin/env python3
"""
verify_founder_ceo_hypergrowth_layer.py — confirm the Founder Console
surface is wired end-to-end:

  - 6 Founder pages exist (ceo, capital-allocation, market-attack,
    ai-governance, trust, audit).
  - Internal API modules exist (api/internal/auth.py, runtime_reader.py,
    policy_adapter.py + api/routers/internal/founder_console.py).
  - 5 CEO report generators exist in scripts/.
  - apps/web/lib runtime/actions/brand-tokens modules exist.

This is a static existence check — no claims are made about runtime
correctness here.

Exit: 0 PASS / 1 FAIL.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAGES = [
    "apps/web/app/ceo/page.tsx",
    "apps/web/app/capital-allocation/page.tsx",
    "apps/web/app/market-attack/page.tsx",
    "apps/web/app/ai-governance/page.tsx",
    "apps/web/app/trust/page.tsx",
    "apps/web/app/audit/page.tsx",
]
LIB = [
    "apps/web/lib/brand-tokens.ts",
    "apps/web/lib/dealix-runtime.ts",
    "apps/web/lib/dealix-actions.ts",
    "apps/web/components/founder-shell.tsx",
]
INTERNAL_API = [
    "api/internal/__init__.py",
    "api/internal/auth.py",
    "api/internal/runtime_reader.py",
    "api/internal/policy_adapter.py",
    "api/routers/internal/__init__.py",
    "api/routers/internal/founder_console.py",
]
GENERATORS = [
    "scripts/generate_ceo_daily_brief.py",
    "scripts/generate_ceo_weekly_review.py",
    "scripts/generate_capital_allocation_report.py",
    "scripts/generate_strategy_scorecard.py",
    "scripts/generate_revenue_forecast.py",
    "scripts/smoke_internal_api.py",
]


def _check(group: str, rel_paths: list[str], failures: list[str]) -> int:
    present = 0
    for rel in rel_paths:
        if (ROOT / rel).exists():
            present += 1
        else:
            failures.append(f"{group}: missing {rel}")
    return present


def main() -> int:
    failures: list[str] = []
    n_pages = _check("pages", PAGES, failures)
    n_lib = _check("lib", LIB, failures)
    n_api = _check("internal_api", INTERNAL_API, failures)
    n_gen = _check("generators", GENERATORS, failures)

    verdict = "PASS" if not failures else "FAIL"
    print(f"FOUNDER_CEO_HYPERGROWTH_LAYER={verdict.lower()}")
    print(f"FCH_LAYER_PAGES_PRESENT={n_pages}/{len(PAGES)}")
    print(f"FCH_LAYER_LIB_PRESENT={n_lib}/{len(LIB)}")
    print(f"FCH_LAYER_INTERNAL_API_PRESENT={n_api}/{len(INTERNAL_API)}")
    print(f"FCH_LAYER_GENERATORS_PRESENT={n_gen}/{len(GENERATORS)}")
    print(f"FCH_LAYER_FAILS={len(failures)}")
    if failures:
        print("\n## Founder-CEO Hypergrowth Layer FAILURES")
        for f in failures[:30]:
            print(f"  - {f}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
