"""
RevenueAttribution — top-level attribution facade.

Defers to the multi-touch model by default; first/last/asset/agent/partner
strategies live in ``growth.attribution`` and can be combined.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dealix.hermes.growth.attribution import (
    asset_influenced,
    first_touch,
    last_touch,
    multi_touch,
    partner_influenced,
    revenue_weighting,
)


@dataclass
class DealAttribution:
    deal_id: str
    verified_revenue_sar: float
    first_touch: str | None
    last_touch: str | None
    assets: tuple[str, ...] = field(default_factory=tuple)
    agents: tuple[str, ...] = field(default_factory=tuple)
    partner: str | None = None
    confidence: float = 0.0
    weights: dict[str, float] = field(default_factory=dict)


def attribute(
    *,
    deal_id: str,
    verified_revenue_sar: float,
    touches: list[dict[str, Any]],
    assets: tuple[str, ...] = (),
    agents: tuple[str, ...] = (),
    partner: str | None = None,
) -> DealAttribution:
    ft = first_touch.attribute(touches)
    lt = last_touch.attribute(touches)
    weights = multi_touch.weights(touches)
    weights = asset_influenced.apply(weights, assets)
    weights = partner_influenced.apply(weights, partner)
    weights = revenue_weighting.normalize(weights)
    confidence = round(min(1.0, len(touches) / 5.0), 4) if touches else 0.0
    return DealAttribution(
        deal_id=deal_id,
        verified_revenue_sar=verified_revenue_sar,
        first_touch=ft,
        last_touch=lt,
        assets=assets,
        agents=agents,
        partner=partner,
        confidence=confidence,
        weights=weights,
    )
