"""Vertical Launcher — the Vertical Test Template made executable.

A vertical cannot be launched without filling every slot. The score
function turns the filled template into a recommendation:
    SCALE if score ≥ 0.7 and risk ≤ 0.4
    HOLD  if 0.4 ≤ score < 0.7
    KILL  otherwise
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4

from dealix.hermes.core.scoring import clip01, weighted_score
from dealix.hermes.core.schemas import ScaleVerdict


@dataclass(slots=True)
class VerticalTest:
    test_id: str
    sector: str
    buyer: str
    pain: str
    offer: str
    price_sar: float
    first_targets_count: int
    partner_angle: str
    trust_requirements: str
    pilot_metric: str
    fit_score: float
    risk_score: float
    notes: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


_WEIGHTS = {
    "first_targets_norm": 0.3,
    "fit_score": 0.4,
    "partner_strength": 0.3,
}


def evaluate(test: VerticalTest, *, partner_strength: float) -> tuple[float, ScaleVerdict]:
    first_targets_norm = clip01(test.first_targets_count / 50.0)
    score = weighted_score(
        _WEIGHTS,
        {
            "first_targets_norm": first_targets_norm,
            "fit_score": test.fit_score,
            "partner_strength": clip01(partner_strength),
        },
    )
    risk = clip01(test.risk_score)
    if score >= 0.7 and risk <= 0.4:
        verdict = ScaleVerdict.SCALE
    elif score >= 0.4:
        verdict = ScaleVerdict.HOLD
    else:
        verdict = ScaleVerdict.KILL
    return round(score, 3), verdict


def make(
    *,
    sector: str,
    buyer: str,
    pain: str,
    offer: str,
    price_sar: float,
    first_targets_count: int,
    partner_angle: str,
    trust_requirements: str,
    pilot_metric: str,
    fit_score: float,
    risk_score: float,
    notes: str = "",
) -> VerticalTest:
    return VerticalTest(
        test_id=str(uuid4()),
        sector=sector,
        buyer=buyer,
        pain=pain,
        offer=offer,
        price_sar=price_sar,
        first_targets_count=first_targets_count,
        partner_angle=partner_angle,
        trust_requirements=trust_requirements,
        pilot_metric=pilot_metric,
        fit_score=clip01(fit_score),
        risk_score=clip01(risk_score),
        notes=notes,
    )


__all__ = ["VerticalTest", "make", "evaluate"]
