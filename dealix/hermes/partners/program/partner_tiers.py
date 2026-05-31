"""PartnerTier — referral, white-label, implementation, strategic."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PartnerTier(StrEnum):
    REFERRAL = "referral"
    WHITE_LABEL = "white_label"
    IMPLEMENTATION = "implementation"
    STRATEGIC = "strategic"


@dataclass(frozen=True)
class PartnerTierSpec:
    tier: PartnerTier
    description: str
    revenue_share_pct: float
    minimum_verified_revenue_sar: float
    requires_certification: bool


PARTNER_TIERS: dict[PartnerTier, PartnerTierSpec] = {
    PartnerTier.REFERRAL: PartnerTierSpec(
        tier=PartnerTier.REFERRAL,
        description="Refers customers; Dealix delivers.",
        revenue_share_pct=0.10,
        minimum_verified_revenue_sar=0.0,
        requires_certification=False,
    ),
    PartnerTier.WHITE_LABEL: PartnerTierSpec(
        tier=PartnerTier.WHITE_LABEL,
        description="Sells Dealix offers under partner brand.",
        revenue_share_pct=0.30,
        minimum_verified_revenue_sar=25_000.0,
        requires_certification=True,
    ),
    PartnerTier.IMPLEMENTATION: PartnerTierSpec(
        tier=PartnerTier.IMPLEMENTATION,
        description="Delivers Dealix engagements with quality and governance.",
        revenue_share_pct=0.20,
        minimum_verified_revenue_sar=50_000.0,
        requires_certification=True,
    ),
    PartnerTier.STRATEGIC: PartnerTierSpec(
        tier=PartnerTier.STRATEGIC,
        description="Co-builds products and brings strategic distribution.",
        revenue_share_pct=0.40,
        minimum_verified_revenue_sar=200_000.0,
        requires_certification=True,
    ),
}
