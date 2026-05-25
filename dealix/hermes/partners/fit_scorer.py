"""
Partner Fit Scorer — يقيّم candidate partner على محاور deterministic ويعطي
score ∈ [0..100] + توصية صريحة.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PartnerFitInputs:
    partner_id: str
    sector_overlap_pct: float  # 0..1 with our ICPs
    distribution_size_companies: int  # how many SMBs the partner can reach
    track_record_years: int
    pdpl_aware: bool
    has_dedicated_owner: bool
    is_existing_customer: bool = False
    requires_payment_facilitation: bool = False


@dataclass
class PartnerFitResult:
    partner_id: str
    score: int
    tier_recommendation: str  # "reject" | "trial" | "activate" | "scale"
    rationale: list[str] = field(default_factory=list)


class PartnerFitScorer:
    def score(self, inputs: PartnerFitInputs) -> PartnerFitResult:
        score = 0
        rationale: list[str] = []

        sector = int(inputs.sector_overlap_pct * 30)
        score += sector
        rationale.append(f"sector overlap +{sector}")

        if inputs.distribution_size_companies >= 200:
            score += 25
            rationale.append("distribution >= 200 (+25)")
        elif inputs.distribution_size_companies >= 50:
            score += 15
            rationale.append("distribution >= 50 (+15)")
        else:
            rationale.append("distribution < 50 (+0)")

        if inputs.track_record_years >= 3:
            score += 15
            rationale.append("track_record >= 3 years (+15)")
        elif inputs.track_record_years >= 1:
            score += 8
            rationale.append("track_record >= 1 year (+8)")

        if inputs.pdpl_aware:
            score += 10
            rationale.append("PDPL aware (+10)")

        if inputs.has_dedicated_owner:
            score += 10
            rationale.append("dedicated owner (+10)")

        if inputs.is_existing_customer:
            score += 10
            rationale.append("existing customer (+10)")

        if inputs.requires_payment_facilitation:
            score -= 15
            rationale.append("requires payment facilitation (-15)")

        score = max(0, min(100, score))
        tier = self._tier(score)
        return PartnerFitResult(
            partner_id=inputs.partner_id,
            score=score,
            tier_recommendation=tier,
            rationale=rationale,
        )

    @staticmethod
    def _tier(score: int) -> str:
        if score >= 80:
            return "scale"
        if score >= 60:
            return "activate"
        if score >= 40:
            return "trial"
        return "reject"


__all__ = ["PartnerFitInputs", "PartnerFitResult", "PartnerFitScorer"]
