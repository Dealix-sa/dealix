"""Compute pipeline quality from ICP fit, deal age, stage, and proof attached."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PipelineDeal:
    deal_id: str
    icp_fit: float
    stage: str
    age_days: int
    has_proof_pack: bool
    amount_sar: float


@dataclass(frozen=True)
class PipelineQuality:
    total_value_sar: float
    quality_weighted_value_sar: float
    quality_ratio: float
    grade: str


_STAGE_WEIGHTS: dict[str, float] = {
    "prospect": 0.1,
    "qualified": 0.3,
    "proposal": 0.55,
    "negotiation": 0.75,
    "closed_won": 1.0,
}


def _grade(ratio: float) -> str:
    if ratio >= 0.6:
        return "A"
    if ratio >= 0.4:
        return "B"
    if ratio >= 0.25:
        return "C"
    return "D"


def assess(deals: list[PipelineDeal]) -> PipelineQuality:
    """Return PipelineQuality from a list of PipelineDeals weighted by stage, fit, age, proof."""
    total = sum(d.amount_sar for d in deals)
    weighted = 0.0
    for d in deals:
        stage_w = _STAGE_WEIGHTS.get(d.stage, 0.1)
        age_penalty = max(0.0, 1.0 - (d.age_days / 180.0))
        proof_bonus = 0.15 if d.has_proof_pack else 0.0
        weighted += d.amount_sar * min(1.0, stage_w * d.icp_fit * age_penalty + proof_bonus)
    ratio = round(weighted / total, 4) if total else 0.0
    return PipelineQuality(
        total_value_sar=round(total, 2),
        quality_weighted_value_sar=round(weighted, 2),
        quality_ratio=ratio,
        grade=_grade(ratio),
    )
