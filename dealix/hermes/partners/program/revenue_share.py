from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.partners.program.tiers import PartnerTier


_TIER_SHARES: dict[PartnerTier, float] = {
    PartnerTier.APPLICANT: 0.0,
    PartnerTier.REGISTERED: 0.10,
    PartnerTier.AUTHORIZED: 0.15,
    PartnerTier.CERTIFIED: 0.20,
    PartnerTier.STRATEGIC: 0.25,
}


@dataclass
class RevenueShareSplit:
    partner_id: str
    tier: PartnerTier
    deal_sar: float
    partner_share_sar: float
    dealix_share_sar: float


def compute_revenue_share(
    *,
    partner_id: str,
    tier: PartnerTier,
    deal_sar: float,
    sourced_by_partner: bool,
    delivered_by_partner: bool,
) -> RevenueShareSplit:
    if deal_sar < 0:
        raise ValueError("deal_sar must be >= 0")
    base = _TIER_SHARES[tier]
    multiplier = 0.5
    if sourced_by_partner:
        multiplier += 0.5
    if delivered_by_partner:
        multiplier += 0.5
    share = min(base * multiplier, 0.5)  # hard cap at 50%
    partner_amount = round(deal_sar * share, 2)
    return RevenueShareSplit(
        partner_id=partner_id,
        tier=tier,
        deal_sar=round(deal_sar, 2),
        partner_share_sar=partner_amount,
        dealix_share_sar=round(deal_sar - partner_amount, 2),
    )
