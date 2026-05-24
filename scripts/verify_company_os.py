#!/usr/bin/env python3
"""Verify layer-level existence of Dealix Company OS.

Each "layer" is a small, fixed list of artifacts that anchor the layer.
This script answers: "does each layer have at least its anchor files?"
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

LAYERS: dict[str, tuple[str, ...]] = {
    "Brand OS": (
        "frontend/src/styles/dealix-brand.css",
        "frontend/public/brand/logo.svg",
        "docs/company/BRAND_VOICE.md",
    ),
    "Founder Console": (
        "docs/company/FOUNDER_COMMAND_CENTER.md",
        "docs/company/FOUNDER_KPIS_AR.md",
    ),
    "CEO OS": (
        "docs/company/CEO_OPERATING_SYSTEM.md",
        "docs/strategy/CEO_STRATEGY.md",
    ),
    "Capital Allocation": (
        "docs/company/DEALIX_CAPITAL_MODEL.md",
        "docs/operating_finance",
    ),
    "Revenue Factory": (
        "dealix/business_now",
        "auto_client_acquisition/revenue_os",
        "docs/revenue",
    ),
    "Market Attack": (
        "docs/strategy/CATEGORY_DESIGN.md",
        "docs/strategy/COMPETITIVE_POSITIONING.md",
        "dealix/config/icp_primary.yaml",
    ),
    "Launch Layer": (
        "docs/launch/DEALIX_LAUNCH_NOW_BUNDLE.md",
        ".github/workflows/official-launch-verify.yml",
        ".github/workflows/daily-revenue-machine.yml",
    ),
    "Scale / Moat": (
        "docs/moat/MOAT_SCORE.md",
        "docs/scale/SCALE_MODEL.md",
    ),
    "Hypergrowth": (
        "docs/strategy/12_MONTH_ROADMAP.md",
        "docs/company/DEALIX_CEO_CTO_MASTER_STRATEGY_V3.md",
    ),
    "AI Governance": (
        "policies/dealix_control_policy.yaml",
        "registries/agent_registry.yaml",
        "registries/machine_registry.yaml",
        "evals/gates/dealix_agent_eval_gate.yaml",
        "auto_client_acquisition/governance_os/draft_gate.py",
    ),
    "Policy-as-Code": (
        "policies/dealix_control_policy.yaml",
        "dealix/config/approval_policy.yaml",
        "dealix/config/claim_policy.yaml",
    ),
    "Agent Registry": (
        "registries/agent_registry.yaml",
        "auto_client_acquisition/agent_governance/agent_registry.py",
    ),
    "Machine Registry": (
        "registries/machine_registry.yaml",
    ),
    "Eval Gate": (
        "evals/gates/dealix_agent_eval_gate.yaml",
        "evals/governance_eval.yaml",
        "evals/outreach_quality_eval.yaml",
    ),
    "Data Platform": (
        "dealix/analytics",
        "db",
    ),
    "Worker Orchestrator": (
        "dealix/execution_assurance",
        "dealix/reliability",
    ),
    "Customer Success": (
        "auto_client_acquisition/customer_success_os" if (REPO / "auto_client_acquisition/customer_success_os").is_dir() else "api/routers/customer_success.py",
        "docs/delivery/DELIVERY_STANDARD.md",
    ),
    "Trust / Legal / Security": (
        "docs/governance/APPROVAL_POLICY.md",
        "SECURITY.md",
        "dealix/registers/compliance_saudi.yaml",
    ),
    "Company Memory": (
        "docs/memory",
        "dealix/observability" if (REPO / "dealix/observability").is_dir() else "dealix",
    ),
}


def _exists(p: Path) -> bool:
    return p.is_file() or p.is_dir()


def main() -> int:
    overall_ok = True
    per_layer: dict[str, list[str]] = {}
    for layer, paths in LAYERS.items():
        missing = [p for p in paths if not _exists(REPO / p)]
        per_layer[layer] = missing
        layer_ok = not missing
        if not layer_ok:
            overall_ok = False
        slug = layer.replace(" ", "_").replace("/", "_").upper()
        print(f"COMPANY_OS_LAYER_{slug}={'PASS' if layer_ok else 'FAIL'}")
        for m in missing:
            print(f"missing_layer_artifact:{layer}:{m}", file=sys.stderr)

    print(f"COMPANY_OS_PASS={'true' if overall_ok else 'false'}")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
