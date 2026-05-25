"""
RevenueQuality — not all revenue is equal. The formula::

    quality = margin + repeatability + retainer_potential + data_moat
            + partner_potential - delivery_burden - risk

Outputs map onto a scale / optimize / reprice / kill decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RevenueQualityVerdict(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGATIVE = "negative"


@dataclass
class RevenueQualityScore:
    deal_id: str
    score: float
    verdict: RevenueQualityVerdict
    recommendation: str


def score_revenue_quality(
    *,
    deal_id: str,
    margin: float,
    repeatability: float,
    retainer_potential: float,
    data_moat: float,
    partner_potential: float,
    delivery_burden: float,
    risk: float,
) -> RevenueQualityScore:
    raw = margin + repeatability + retainer_potential + data_moat + partner_potential - delivery_burden - risk
    score = round(raw, 4)
    if score >= 2.5:
        verdict = RevenueQualityVerdict.HIGH
        rec = "Scale; productize and lock in retainer."
    elif score >= 1.0:
        verdict = RevenueQualityVerdict.MEDIUM
        rec = "Optimize delivery and look for retainer conversion."
    elif score >= 0:
        verdict = RevenueQualityVerdict.LOW
        rec = "Reprice, bundle, or pause."
    else:
        verdict = RevenueQualityVerdict.NEGATIVE
        rec = "Kill — refuse similar deals."
    return RevenueQualityScore(deal_id=deal_id, score=score, verdict=verdict, recommendation=rec)
