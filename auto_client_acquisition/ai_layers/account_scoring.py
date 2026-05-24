"""Layer 2 — Account scoring on Trust-Plane sourced data only.

Wraps deterministic heuristics for ICP fit + readiness + opportunity size,
returning a transparent reason chain. Refuses to score if no source_ref is
present (no scraping).
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.ai_layers.schemas import LayerContext, LayerResult

_ICP_WEIGHTS = {
    "saudi_b2b": 5,
    "size_50_500_emp": 4,
    "has_data_owner": 3,
    "uses_crm": 3,
    "has_ai_budget": 3,
    "regulated_industry_bonus": 2,
}

_READINESS_WEIGHTS = {
    "data_available": 4,
    "owner_present": 3,
    "accepts_governance": 3,
    "workflow_pain_clear": 3,
}


def _scale(score: int, max_score: int) -> int:
    if max_score <= 0:
        return 0
    return max(0, min(100, round(100 * score / max_score)))


def run(ctx: LayerContext) -> LayerResult:
    """Score an account.

    Expected payload keys: account_name (str), icp_signals (dict[str, bool]),
    readiness_signals (dict[str, bool]), estimated_acv_sar (int).
    """
    if not ctx.source_refs:
        return LayerResult(
            layer="account_scoring",
            customer_id=ctx.customer_id,
            ok=False,
            governance_decision="BLOCK",
            output={"reason": "no_source_ref"},
            notes=("Account scoring needs founder-supplied source_ref",),
        )

    account_name: str = str(ctx.payload.get("account_name", ""))
    icp = ctx.payload.get("icp_signals", {}) or {}
    readiness = ctx.payload.get("readiness_signals", {}) or {}
    acv = int(ctx.payload.get("estimated_acv_sar", 0) or 0)

    icp_max = sum(_ICP_WEIGHTS.values())
    icp_score = sum(w for k, w in _ICP_WEIGHTS.items() if bool(icp.get(k)))
    readiness_max = sum(_READINESS_WEIGHTS.values())
    readiness_score = sum(
        w for k, w in _READINESS_WEIGHTS.items() if bool(readiness.get(k))
    )

    icp_pct = _scale(icp_score, icp_max)
    readiness_pct = _scale(readiness_score, readiness_max)
    # Composite: 50% ICP, 40% readiness, 10% deal-size bucket
    deal_bucket = 0
    if acv >= 25_000:
        deal_bucket = 100
    elif acv >= 5_000:
        deal_bucket = 70
    elif acv >= 499:
        deal_bucket = 40

    composite = round(
        0.5 * icp_pct + 0.4 * readiness_pct + 0.1 * deal_bucket
    )

    if composite >= 75:
        tier = "A"
    elif composite >= 55:
        tier = "B"
    elif composite >= 35:
        tier = "C"
    else:
        tier = "D"

    return LayerResult(
        layer="account_scoring",
        customer_id=ctx.customer_id,
        ok=True,
        governance_decision="ALLOW",
        output={
            "account_name": account_name,
            "tier": tier,
            "composite": composite,
            "icp_pct": icp_pct,
            "readiness_pct": readiness_pct,
            "deal_bucket": deal_bucket,
            "reasons": {
                "icp_hit": [k for k in _ICP_WEIGHTS if bool(icp.get(k))],
                "readiness_hit": [
                    k for k in _READINESS_WEIGHTS if bool(readiness.get(k))
                ],
            },
            "source_refs": list(ctx.source_refs),
        },
        notes=(f"Tier {tier} (composite {composite})",),
        capital_asset_candidates=("scoring_rule",) if tier in ("A", "B") else (),
    )
