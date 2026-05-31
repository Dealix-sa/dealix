"""RevenueShareRule — calculate the partner share on a verified deal."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.partners.program.partner_tiers import PARTNER_TIERS, PartnerTier


@dataclass
class RevenueShareRule:
    tier: PartnerTier
    minimum_verified_revenue_sar: float
    share_pct: float


def calculate_share(*, tier: PartnerTier, verified_revenue_sar: float) -> float:
    spec = PARTNER_TIERS[tier]
    if verified_revenue_sar < spec.minimum_verified_revenue_sar:
        return 0.0
    return round(verified_revenue_sar * spec.revenue_share_pct, 2)
