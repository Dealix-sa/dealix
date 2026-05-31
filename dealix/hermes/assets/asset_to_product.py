"""
asset_to_product — turns an Asset that meets the productization criteria
into an entry in the productization queue.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.products.from_asset import is_productization_candidate


@dataclass
class AssetUsageEvent:
    asset_id: str
    times_used: int
    influenced_revenue_sar: float
    reusable: bool
    low_risk: bool


@dataclass
class PromotionDecision:
    asset_id: str
    promoted: bool
    rationale: list[str]


def promote_asset(usage: AssetUsageEvent) -> PromotionDecision:
    candidate = is_productization_candidate(
        asset_id=usage.asset_id,
        times_used=usage.times_used,
        influenced_revenue_sar=usage.influenced_revenue_sar,
        reusable=usage.reusable,
        low_risk=usage.low_risk,
    )
    return PromotionDecision(
        asset_id=usage.asset_id,
        promoted=candidate.is_candidate,
        rationale=candidate.rationale or ["meets all productization criteria"],
    )
