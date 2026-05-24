"""Layer 7 — Customer health from observed signals only.

Composes a health score from adoption signals, usage cadence, friction events,
and renewal posture. Never invents signals; missing signals lower confidence.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.ai_layers.schemas import LayerContext, LayerResult


def _bucket(score: int) -> str:
    if score >= 80:
        return "healthy"
    if score >= 60:
        return "watch"
    if score >= 40:
        return "at_risk"
    return "critical"


def run(ctx: LayerContext) -> LayerResult:
    """Compute customer health.

    Expected payload keys:
        adoption_pct: int 0..100 (from adoption_os.compute).
        usage_last_7d: int — number of meaningful interactions.
        friction_high_severity_14d: int — count of HIGH severity friction events.
        renewal_due_in_days: int | None.
        last_value_event_tier: 'estimated' | 'observed' | 'verified' | 'client_confirmed'.
    """
    adoption = int(ctx.payload.get("adoption_pct", 0) or 0)
    usage = int(ctx.payload.get("usage_last_7d", 0) or 0)
    frictions = int(ctx.payload.get("friction_high_severity_14d", 0) or 0)
    renewal_days = ctx.payload.get("renewal_due_in_days")
    tier = str(ctx.payload.get("last_value_event_tier", "estimated"))

    # Base: 40% adoption, 25% usage cap, 25% friction penalty inversion, 10% tier
    usage_score = min(100, usage * 10)
    friction_score = max(0, 100 - frictions * 25)
    tier_score = {
        "estimated": 25,
        "observed": 60,
        "verified": 85,
        "client_confirmed": 100,
    }.get(tier, 25)

    composite = round(
        0.4 * adoption + 0.25 * usage_score + 0.25 * friction_score + 0.1 * tier_score
    )
    composite = max(0, min(100, composite))
    bucket = _bucket(composite)

    notes: list[str] = [f"bucket={bucket}", f"composite={composite}"]
    if isinstance(renewal_days, int) and 0 <= renewal_days <= 30:
        notes.append(f"renewal_due_in_{renewal_days}d")

    # Risk surfacing
    risk_flags: list[str] = []
    if adoption < 50:
        risk_flags.append("low_adoption")
    if frictions >= 3:
        risk_flags.append("repeated_friction")
    if tier == "estimated":
        risk_flags.append("no_observed_value_yet")

    return LayerResult(
        layer="customer_health",
        customer_id=ctx.customer_id,
        ok=True,
        governance_decision="ALLOW",
        output={
            "composite": composite,
            "bucket": bucket,
            "components": {
                "adoption_pct": adoption,
                "usage_score": usage_score,
                "friction_score": friction_score,
                "tier_score": tier_score,
            },
            "risk_flags": risk_flags,
            "renewal_due_in_days": renewal_days,
        },
        notes=tuple(notes),
    )
