"""Revenue quality score — weighted across verification, margin, retainer."""

from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from dealix.growth_os.revenue_assurance.checks import run_all_checks
from dealix.growth_os.revenue_assurance.verification import verify_record
from dealix.growth_os.revenue_proof.proof_rules import is_real_revenue
from dealix.growth_os.revenue_proof.revenue_record import RevenueRecord

# Weights sum to 1.0. See section 39 of the spec.
QUALITY_WEIGHTS: Final[dict[str, float]] = {
    "verification": 0.35,
    "margin": 0.20,
    "retainer_potential": 0.20,
    "attribution_clarity": 0.10,
    "stage_consistency": 0.10,
    "delivery_efficiency": 0.05,
}


class RevenueQualityScore(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record_id: str
    score: float = Field(..., ge=0.0, le=1.0)
    components: dict[str, float]
    is_real_revenue: bool
    band: str  # gold | silver | bronze | reject


def _band_for(score: float, real: bool) -> str:
    if not real:
        return "reject"
    if score >= 0.8:
        return "gold"
    if score >= 0.6:
        return "silver"
    return "bronze"


def revenue_quality_score(record: RevenueRecord) -> RevenueQualityScore:
    """Compute the weighted quality score for a RevenueRecord.

    A record that is not ``is_real_revenue`` scores 0.0 with band 'reject'.
    """
    real = is_real_revenue(record)
    if not real:
        return RevenueQualityScore(
            record_id=record.record_id,
            score=0.0,
            components=dict.fromkeys(QUALITY_WEIGHTS, 0.0),
            is_real_revenue=False,
            band="reject",
        )

    bundle = verify_record(record)
    checks = run_all_checks(record)

    verification_component = 1.0  # already real
    margin_component = 1.0 if checks.margin.is_healthy else max(
        0.0, record.margin_pct / max(checks.margin.threshold, 1e-9)
    )
    retainer_component = checks.retainer.signal_strength
    attribution_component = 1.0 if bundle.attribution.has_any_attribution else 0.0
    stage_component = 1.0 if bundle.deal_stage.stage_consistent else 0.0
    delivery_component = 1.0 if checks.delivery.is_efficient else max(
        0.0, checks.delivery.usd_per_hour / max(checks.delivery.threshold_usd_per_hour, 1e-9)
    )

    components = {
        "verification": verification_component,
        "margin": margin_component,
        "retainer_potential": retainer_component,
        "attribution_clarity": attribution_component,
        "stage_consistency": stage_component,
        "delivery_efficiency": min(delivery_component, 1.0),
    }

    score = sum(components[k] * QUALITY_WEIGHTS[k] for k in QUALITY_WEIGHTS)
    score = max(0.0, min(score, 1.0))

    return RevenueQualityScore(
        record_id=record.record_id,
        score=round(score, 4),
        components={k: round(v, 4) for k, v in components.items()},
        is_real_revenue=True,
        band=_band_for(score, real),
    )


__all__ = ["QUALITY_WEIGHTS", "RevenueQualityScore", "revenue_quality_score"]
