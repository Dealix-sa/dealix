"""Partner fit scoring."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.scoring import clip01, weighted_score


@dataclass(slots=True)
class PartnerSignals:
    client_base: float  # depth + relevance of their book of business
    sales_capability: float
    delivery_capability: float
    trust_score: float
    sector_fit: float
    risk_score: float  # higher = worse

    def __post_init__(self) -> None:
        for name in (
            "client_base",
            "sales_capability",
            "delivery_capability",
            "trust_score",
            "sector_fit",
            "risk_score",
        ):
            setattr(self, name, clip01(getattr(self, name)))


_WEIGHTS = {
    "client_base": 0.25,
    "sales_capability": 0.2,
    "delivery_capability": 0.2,
    "trust_score": 0.15,
    "sector_fit": 0.2,
}


def score(signals: PartnerSignals) -> float:
    values = {
        "client_base": signals.client_base,
        "sales_capability": signals.sales_capability,
        "delivery_capability": signals.delivery_capability,
        "trust_score": signals.trust_score,
        "sector_fit": signals.sector_fit,
    }
    upside = weighted_score(_WEIGHTS, values)
    risk_penalty = 0.6 * signals.risk_score
    return clip01(upside - risk_penalty)


__all__ = ["PartnerSignals", "score"]
