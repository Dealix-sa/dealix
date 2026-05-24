"""Layer 9 — Executive intelligence: composite read across health, growth,
proof, friction. Never invents metrics. Reads only what is in the context.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.ai_layers.schemas import LayerContext, LayerResult


def _grade(score: int) -> str:
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 55:
        return "C"
    if score >= 40:
        return "D"
    return "E"


def run(ctx: LayerContext) -> LayerResult:
    """Compose an exec read.

    Expected payload keys (all optional, derived from prior layers):
        customer_health_composite: int 0..100
        proof_artifact_count_sourced: int
        growth_signal_acceptance_pct: int 0..100
        compliance_overall: str
        partnership_active_count: int
    """
    health = int(ctx.payload.get("customer_health_composite", 0) or 0)
    proofs = int(ctx.payload.get("proof_artifact_count_sourced", 0) or 0)
    growth_pct = int(ctx.payload.get("growth_signal_acceptance_pct", 0) or 0)
    compliance = str(ctx.payload.get("compliance_overall", "ALLOW"))
    partnerships = int(ctx.payload.get("partnership_active_count", 0) or 0)

    proof_bucket = min(100, proofs * 20)  # 5 sourced proofs ≈ 100
    partner_bucket = min(100, partnerships * 25)
    compliance_score = {
        "ALLOW": 100,
        "ALLOW_WITH_REVIEW": 85,
        "DRAFT_ONLY": 70,
        "REQUIRE_APPROVAL": 60,
        "REDACT": 40,
        "BLOCK": 0,
        "ESCALATE": 30,
    }.get(compliance, 50)

    composite = round(
        0.30 * health
        + 0.20 * proof_bucket
        + 0.15 * growth_pct
        + 0.25 * compliance_score
        + 0.10 * partner_bucket
    )
    composite = max(0, min(100, composite))
    grade = _grade(composite)

    headlines: list[str] = []
    if health < 50:
        headlines.append("customer health below threshold")
    if proofs < 1:
        headlines.append("no sourced proof artifacts yet")
    if compliance != "ALLOW":
        headlines.append(f"compliance posture={compliance}")
    if partnerships == 0:
        headlines.append("no active partnerships")
    if not headlines:
        headlines.append("on track")

    return LayerResult(
        layer="executive_intelligence",
        customer_id=ctx.customer_id,
        ok=True,
        governance_decision="ALLOW",
        output={
            "composite": composite,
            "grade": grade,
            "headlines": headlines,
            "components": {
                "customer_health": health,
                "proof_bucket": proof_bucket,
                "growth_pct": growth_pct,
                "compliance_score": compliance_score,
                "partner_bucket": partner_bucket,
            },
        },
        notes=(f"grade={grade}", f"composite={composite}"),
    )
