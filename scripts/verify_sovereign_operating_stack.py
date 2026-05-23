#!/usr/bin/env python3
"""Verify the 18-layer sovereign operating stack.

Each layer has a minimum set of artifacts. If any required artifact is missing,
this verifier fails. Use --json to emit a machine-readable readiness map.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _verify_common import ROOT

LAYERS: list[tuple[str, list[str]]] = [
    (
        "01 Brand Authority",
        [
            "docs/brand/brand-tokens.json",
            "apps/web/lib/brand-tokens.ts",
            "apps/web/styles/brand.css",
            "assets/brand/wordmark/dealix-wordmark.svg",
            "apps/web/components/brand/DealixLogo.tsx",
        ],
    ),
    (
        "02 Category & Positioning",
        [
            "docs/positioning/CATEGORY_CREATION_OS.md",
            "docs/positioning/DEALIX_POSITIONING.md",
            "docs/positioning/MESSAGING_HIERARCHY.md",
        ],
    ),
    (
        "03 Market Intelligence",
        [
            "docs/intelligence/MARKET_DOMINATION_INTELLIGENCE.md",
            "docs/intelligence/SECTOR_RANKING_SYSTEM.md",
        ],
    ),
    (
        "04 ICP & Account Scoring",
        [
            "docs/intelligence/ICP_SEGMENTATION_SYSTEM.md",
            "docs/intelligence/ACCOUNT_SCORING_MODEL.md",
        ],
    ),
    (
        "05 Distribution War Machine",
        [
            "docs/growth/DISTRIBUTION_WAR_MACHINE.md",
            "docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md",
            "docs/growth/OUTBOUND_DRAFT_MACHINE.md",
            "docs/growth/FOLLOW_UP_MACHINE.md",
        ],
    ),
    (
        "06 Revenue Factory",
        [
            "docs/revenue/REVENUE_FACTORY_OS.md",
            "docs/revenue/SAMPLE_FACTORY.md",
            "docs/revenue/PROPOSAL_FACTORY.md",
        ],
    ),
    (
        "07 Product Marketing OS",
        [
            "docs/product/DEALIX_PRODUCT_LADDER.md",
            "docs/product/PRICING_GUARDRAILS.md",
            "docs/marketing/DEALIX_MARKETING_OS.md",
        ],
    ),
    (
        "08 Founder Console",
        [
            "apps/web/components/shell/ConsoleShell.tsx",
            "apps/web/app/ceo/page.tsx",
            "apps/web/app/sales-cockpit/page.tsx",
            "apps/web/app/sovereign/page.tsx",
        ],
    ),
    (
        "09 Control Plane",
        [
            "docs/control_plane/DEALIX_CONTROL_PLANE.md",
            "docs/api/CONTROL_PLANE_API.md",
            "api/routers/internal/founder_console.py",
        ],
    ),
    (
        "10 AI Agent OS",
        [
            "registries/agent_registry.yaml",
            "docs/ai/AGENT_REGISTRY_SYSTEM.md",
            "docs/ai/CEO_COPILOT_SYSTEM.md",
        ],
    ),
    (
        "11 Policy-as-Code",
        [
            "policies/dealix_control_policy.yaml",
            "api/internal/policy_adapter.py",
        ],
    ),
    (
        "12 Eval / Red Team Gate",
        [
            "evals/gates/dealix_agent_eval_gate.yaml",
            "docs/evals/EVAL_GATE_V1.md",
            "scripts/verify_eval_gate.py",
        ],
    ),
    (
        "13 Trust + Audit Layer",
        [
            "docs/security/INTERNAL_API_AUTH_GATE.md",
            "api/internal/auth.py",
        ],
    ),
    (
        "14 Worker Orchestrator",
        [
            "docs/runtime/WORKER_ORCHESTRATOR_V1.md",
            "scripts/update_worker_state.py",
            "scripts/run_ceo_summary_worker.py",
        ],
    ),
    (
        "15 Data Platform",
        [
            "docs/data/POSTGRES_PRIMARY_MODE.md",
            "docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md",
            "scripts/bootstrap_private_ops_runtime.py",
        ],
    ),
    (
        "16 Delivery + Retention OS",
        [
            "docs/delivery/ULTIMATE_DELIVERY_OS.md",
            "docs/client_success/RETENTION_REFERRAL_OS.md",
            "docs/proof/PROOF_APPROVAL_OS.md",
        ],
    ),
    (
        "17 Finance + Unit Economics",
        [
            "docs/finance/ULTIMATE_FINANCE_OS.md",
            "docs/finance/AI_UNIT_ECONOMICS_SYSTEM.md",
        ],
    ),
    (
        "18 Observability + Security + Production Gates",
        [
            "docs/engineering/ULTIMATE_OBSERVABILITY_DORA.md",
            "docs/security/ULTIMATE_SECURITY_GOVERNANCE.md",
            "docs/security/PRODUCTION_SECURITY_GATE.md",
            "docs/security/BRANCH_PROTECTION_REQUIRED_CHECKS.md",
        ],
    ),
]


def evaluate() -> tuple[list[dict], int]:
    out: list[dict] = []
    failures = 0
    for name, paths in LAYERS:
        missing = [p for p in paths if not (ROOT / p).exists()]
        passed = not missing
        out.append({"layer": name, "passed": passed, "missing": missing})
        if not passed:
            failures += 1
    return out, failures


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    results, failures = evaluate()
    if args.json:
        json.dump({"failures": failures, "layers": results}, sys.stdout, indent=2)
        print()
    else:
        for r in results:
            status = "PASS" if r["passed"] else "FAIL"
            print(f"{status}  {r['layer']}")
            for m in r["missing"]:
                print(f"      missing: {m}")
        print(f"\n[sovereign-operating-stack] {len(LAYERS) - failures} pass / {failures} fail")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
