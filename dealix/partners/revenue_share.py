"""خادم الشركاء — RevenueShareCalculator (spec §43 partner tiers).

Tiers:

    STANDARD   → 20 % of deal amount
    PREFERRED  → 30 %
    STRATEGIC  → 40 %
"""

from __future__ import annotations

from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.schemas import Money


class PartnerTier(StrEnum):
    STANDARD = "standard"
    PREFERRED = "preferred"
    STRATEGIC = "strategic"


_TIER_RATES: dict[PartnerTier, Decimal] = {
    PartnerTier.STANDARD: Decimal("0.20"),
    PartnerTier.PREFERRED: Decimal("0.30"),
    PartnerTier.STRATEGIC: Decimal("0.40"),
}


class RevenueShareSplit(BaseModel):
    """How a deal amount splits between Dealix and the partner."""

    model_config = ConfigDict(extra="forbid")

    partner_tier: PartnerTier
    deal_amount: Money
    partner_share: Money
    dealix_share: Money
    rate: float = Field(..., ge=0.0, le=1.0)


class RevenueShareCalculator:
    """Split a deal amount per partner tier."""

    def calc(self, deal_amount: Money, partner_tier: PartnerTier | str) -> RevenueShareSplit:
        tier = PartnerTier(partner_tier) if isinstance(partner_tier, str) else partner_tier
        rate = _TIER_RATES[tier]
        partner_amount = deal_amount.amount * rate
        # Round to 2 decimal places for currency-safe arithmetic.
        partner_amount_q = partner_amount.quantize(Decimal("0.01"))
        dealix_amount_q = (deal_amount.amount - partner_amount_q).quantize(Decimal("0.01"))
        return RevenueShareSplit(
            partner_tier=tier,
            deal_amount=deal_amount,
            partner_share=Money(amount=partner_amount_q, currency=deal_amount.currency),
            dealix_share=Money(amount=dealix_amount_q, currency=deal_amount.currency),
            rate=float(rate),
        )

    @staticmethod
    def rate_for(tier: PartnerTier | str) -> float:
        tier_enum = PartnerTier(tier) if isinstance(tier, str) else tier
        return float(_TIER_RATES[tier_enum])


__all__ = [
    "PartnerTier",
    "RevenueShareCalculator",
    "RevenueShareSplit",
]
