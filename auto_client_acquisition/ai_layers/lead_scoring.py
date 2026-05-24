"""Layer 1 — Lead scoring on founder-supplied data only.

Honors:
    - No scraping (data must come from founder-supplied source_refs).
    - No PII in score output (only signal tags).
    - Output carries governance_decision.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.ai_layers.schemas import LayerContext, LayerResult

# Reuse the canonical weights baked into config/lead_scoring.yaml. We embed the
# defaults here so this layer remains self-contained when the YAML is absent.
_POSITIVE = {
    "title_founder_exec": 4,
    "b2b_company": 3,
    "crm_or_pipeline": 3,
    "uses_or_plans_ai": 3,
    "saudi_or_gcc": 2,
    "urgent_within_30d": 2,
    "budget_5k_plus_sar": 2,
    "partner_or_referral_potential": 2,
}
_NEGATIVE = {
    "no_company": -4,
    "student_or_job_seeker": -3,
    "vague_ai_curiosity": -3,
    "no_clear_workflow_pain": -2,
}
_THRESHOLDS = {"qualified_a_min": 15, "qualified_b_min": 10, "nurture_min": 6}


def _route(score: int) -> str:
    if score >= _THRESHOLDS["qualified_a_min"]:
        return "qualified_a"
    if score >= _THRESHOLDS["qualified_b_min"]:
        return "qualified_b"
    if score >= _THRESHOLDS["nurture_min"]:
        return "nurture"
    return "archive"


def run(ctx: LayerContext) -> LayerResult:
    """Score a single lead.

    Expected payload keys (all optional booleans):
        title_founder_exec, b2b_company, crm_or_pipeline, uses_or_plans_ai,
        saudi_or_gcc, urgent_within_30d, budget_5k_plus_sar,
        partner_or_referral_potential, no_company, student_or_job_seeker,
        vague_ai_curiosity, no_clear_workflow_pain.
    """
    signals: dict[str, bool] = {
        k: bool(ctx.payload.get(k, False))
        for k in (*_POSITIVE.keys(), *_NEGATIVE.keys())
    }

    if not ctx.source_refs:
        return LayerResult(
            layer="lead_scoring",
            customer_id=ctx.customer_id,
            ok=False,
            governance_decision="BLOCK",
            output={"reason": "no_source_ref", "signals": signals},
            notes=("Source reference required (no scraping)",),
        )

    pos = sum(w for k, w in _POSITIVE.items() if signals.get(k))
    neg = sum(w for k, w in _NEGATIVE.items() if signals.get(k))
    score = pos + neg
    route = _route(score)

    return LayerResult(
        layer="lead_scoring",
        customer_id=ctx.customer_id,
        ok=True,
        governance_decision="ALLOW",
        output={
            "score": score,
            "route": route,
            "positive_signals": [k for k in _POSITIVE if signals.get(k)],
            "negative_signals": [k for k in _NEGATIVE if signals.get(k)],
            "source_refs": list(ctx.source_refs),
        },
        notes=(f"Routed to {route}",),
    )
