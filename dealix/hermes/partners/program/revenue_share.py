"""Revenue share percentages per partner tier."""

from __future__ import annotations

from dataclasses import dataclass

_TIER_SHARE: dict[str, float] = {
    "referral": 0.10,
    "white_label": 0.30,
    "implementation": 0.25,
    "strategic": 0.20,
}


@dataclass(frozen=True)
class PartnerPayout:
    partner_id: str
    tier: str
    revenue_sar: float
    share_pct: float
    payout_sar: float


def share_pct(tier: str) -> float:
    """Return the revenue share percentage for a partner tier (0 if unknown)."""
    return _TIER_SHARE.get(tier, 0.0)


def compute(partner_id: str, tier: str, revenue_sar: float) -> PartnerPayout:
    """Compute the revenue-share payout for a partner on a given deal amount."""
    pct = share_pct(tier)
    return PartnerPayout(
        partner_id=partner_id,
        tier=tier,
        revenue_sar=round(float(revenue_sar), 2),
        share_pct=pct,
        payout_sar=round(revenue_sar * pct, 2),
    )
