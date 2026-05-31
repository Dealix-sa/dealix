"""Partner fit scoring."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PartnerFit:
    score: int
    components: dict[str, int]


def score_partner_fit(
    *,
    client_base_score: int,
    sales_capability: int,
    delivery_capability: int,
    trust_level: int,
    sector_fit: int,
    risk_level: int,
) -> PartnerFit:
    weighted = (
        client_base_score * 2
        + sales_capability * 2
        + delivery_capability * 2
        + trust_level * 2
        + sector_fit
        - risk_level * 2
    )
    return PartnerFit(
        score=max(0, weighted),
        components={
            "client_base_score": client_base_score,
            "sales_capability": sales_capability,
            "delivery_capability": delivery_capability,
            "trust_level": trust_level,
            "sector_fit": sector_fit,
            "risk_level": risk_level,
        },
    )
