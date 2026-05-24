"""Founder Console read-only aggregator.

Surfaces the founder-facing 26-layer status as JSON, ready for the
Next.js Founder Console (`apps/web/app/<page>/page.tsx`).

Doctrine:
  * Read-only. No external action. No outbound sends.
  * No PII in payloads (callers must not pass customer data here).
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/internal/founder-console", tags=["internal-founder-console"])

REPO_ROOT = Path(__file__).resolve().parents[3]


def _file_exists(rel: str) -> bool:
    return (REPO_ROOT / rel).exists()


@router.get("/status")
def get_status() -> dict[str, Any]:
    """Return high-level 26-layer status. Source=fallback when not wired."""
    layers = [
        ("brand_os", "docs/brand/DEALIX_BRAND_OS.md"),
        ("founder_console", "apps/web/app/page.tsx"),
        ("ceo_os", "docs/company/DEALIX_CEO_OS.md"),
        ("capital_allocation", "docs/company/DEALIX_CAPITAL_ALLOCATION.md"),
        ("strategy_metrics", "docs/company/DEALIX_STRATEGY_METRICS.md"),
        ("revenue_factory", "docs/company/DEALIX_REVENUE_FACTORY.md"),
        ("launch_layer", "docs/company/DEALIX_LAUNCH_LAYER.md"),
        ("market_attack", "docs/company/DEALIX_MARKET_ATTACK.md"),
        ("scale_moat", "docs/company/DEALIX_SCALE_MOAT.md"),
        ("hypergrowth_ceo", "docs/company/DEALIX_HYPERGROWTH_CEO.md"),
        ("ai_governance", "docs/company/DEALIX_AI_GOVERNANCE.md"),
        ("policy_as_code", "policies/dealix_control_policy.yaml"),
        ("agent_registry", "registries/agent_registry.yaml"),
        ("machine_registry", "registries/machine_registry.yaml"),
        ("eval_gate", "evals/gates/dealix_agent_eval_gate.yaml"),
        ("worker_orchestrator", "docs/company/DEALIX_WORKER_ORCHESTRATOR.md"),
        ("customer_success", "docs/company/DEALIX_CUSTOMER_SUCCESS.md"),
        ("enterprise_sales", "docs/company/DEALIX_ENTERPRISE_SALES.md"),
        ("legal_trust_security", "docs/company/DEALIX_LEGAL_TRUST_SECURITY.md"),
        ("company_memory", "docs/company/DEALIX_COMPANY_MEMORY.md"),
        ("private_ops_runtime", "scripts/bootstrap_private_ops_runtime.py"),
    ]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "files",  # not yet wired to live DB
        "governance_decision": "auto_approved",
        "layers": [
            {"key": key, "doc_rel": rel, "present": _file_exists(rel)}
            for key, rel in layers
        ],
    }


@router.get("/layers/{key}")
def get_layer(key: str) -> dict[str, Any]:
    """Read-only single-layer summary."""
    all_status = get_status()
    for layer in all_status["layers"]:
        if layer["key"] == key:
            return {
                "key": key,
                "present": layer["present"],
                "doc_rel": layer["doc_rel"],
                "source": "files",
                "governance_decision": "auto_approved",
                "generated_at": all_status["generated_at"],
            }
    return {
        "key": key,
        "present": False,
        "source": "fallback",
        "governance_decision": "auto_approved",
        "generated_at": all_status["generated_at"],
    }
