"""
Revenue quality score.

Inputs:
- margin (0-1)
- repeatability (0-1 — how easily can this deal be cloned)
- retainer_potential (0-1)
- data_moat (0-1 — does the work produce reusable proprietary signal)
- partner_potential (0-1)
- low_delivery_burden (0-1, higher is better)
- risk (0-1, higher is worse)
- founder_time_dependency (0-1, higher is worse)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RevenueQualityScore:
    score: float        # 0-100
    band: str           # "kill" | "caution" | "good" | "great" | "exceptional"
    breakdown: dict[str, float]
    notes: list[str]


def _band(score: float) -> str:
    if score < 30:
        return "kill"
    if score < 50:
        return "caution"
    if score < 70:
        return "good"
    if score < 85:
        return "great"
    return "exceptional"


def score_revenue_quality(
    *,
    margin: float,
    repeatability: float,
    retainer_potential: float,
    data_moat: float,
    partner_potential: float,
    low_delivery_burden: float,
    risk: float,
    founder_time_dependency: float,
    notes: list[str] | None = None,
) -> RevenueQualityScore:
    for name, value in [
        ("margin", margin),
        ("repeatability", repeatability),
        ("retainer_potential", retainer_potential),
        ("data_moat", data_moat),
        ("partner_potential", partner_potential),
        ("low_delivery_burden", low_delivery_burden),
        ("risk", risk),
        ("founder_time_dependency", founder_time_dependency),
    ]:
        if not 0 <= value <= 1:
            raise ValueError(f"{name} must be in [0,1], got {value}")

    breakdown = {
        "margin": margin * 25,
        "repeatability": repeatability * 15,
        "retainer_potential": retainer_potential * 20,
        "data_moat": data_moat * 10,
        "partner_potential": partner_potential * 10,
        "low_delivery_burden": low_delivery_burden * 10,
        "risk_penalty": -risk * 15,
        "founder_time_penalty": -founder_time_dependency * 15,
    }
    raw = sum(breakdown.values())
    score = max(0.0, min(100.0, round(raw, 2)))
    return RevenueQualityScore(
        score=score,
        band=_band(score),
        breakdown={k: round(v, 2) for k, v in breakdown.items()},
        notes=list(notes or []),
    )
