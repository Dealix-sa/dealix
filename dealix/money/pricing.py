"""خادم المال — PricingEngine + DiscountAdvisory (spec §38/§43).

`quote(offer, opportunity)` returns a deterministic price within the
offer's price band — biased toward the midpoint, nudged up when the
opportunity is high-urgency/high-fit, nudged down when urgency is low.

`discount_advisory(...)` inspects a proposed discount against the
spec §38 critical-pricing triggers and decides whether Sami approval
is required, or whether the discount exceeds the hard floor.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.opportunities import Opportunity
from dealix.hermes.core.schemas import Money
from dealix.hermes.sovereignty import SovereigntyLevel
from dealix.money.offer_matcher import Offer


# ─────────────────────────────────────────────────────────────
# Thresholds — kept inline so tests can pin behaviour
# ─────────────────────────────────────────────────────────────


_DISCOUNT_APPROVAL_THRESHOLD: Decimal = Decimal("0.10")  # 10 %
_DISCOUNT_HARD_FLOOR: Decimal = Decimal("0.30")  # 30 %
_HIGH_VALUE_AMOUNT_SAR: Decimal = Decimal("25000")


class DiscountVerdict(StrEnum):
    NO_DISCOUNT = "no_discount"
    AUTONOMOUS = "autonomous"
    REQUIRES_APPROVAL = "requires_approval"
    EXCEEDS_LIMIT = "exceeds_limit"


class DiscountAdvisory(BaseModel):
    """Result of inspecting a quoted price + discount."""

    model_config = ConfigDict(extra="forbid")

    base_amount: Money
    quoted_amount: Money
    discount_pct: float = Field(..., ge=0.0, le=1.0)
    verdict: DiscountVerdict
    reasons: list[str] = Field(default_factory=list, max_length=10)
    requires_sami_approval: bool = False
    suggested_sovereignty: SovereigntyLevel = SovereigntyLevel.S0_AUTONOMOUS


# ─────────────────────────────────────────────────────────────
# Engine
# ─────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class _Bias:
    """Internal scoring of where in the band to land the quote."""

    urgency: int
    fit_score: int


class PricingEngine:
    """Deterministic pricing within an Offer's price band."""

    def quote(self, offer: Offer, opportunity: Opportunity) -> Money:
        low, high = offer.price_band
        midpoint = (low.amount + high.amount) / Decimal("2")
        span = (high.amount - low.amount)
        bias = _Bias(urgency=opportunity.urgency, fit_score=opportunity.fit_score)
        # Each combined point above 6 (mid baseline) pulls 5% of the span up.
        delta = Decimal(str((bias.urgency + bias.fit_score) - 6)) * span * Decimal("0.05")
        amount = midpoint + delta
        # Clamp to band.
        amount = max(low.amount, min(high.amount, amount))
        # Quantize to nearest 50 SAR for clean numbers.
        rounded = (amount / Decimal("50")).to_integral_value() * Decimal("50")
        rounded = max(low.amount, min(high.amount, rounded))
        return Money(amount=rounded, currency=low.currency)

    def discount_advisory(
        self,
        base_amount: Money,
        quoted_amount: Money,
        *,
        sovereignty_level: SovereigntyLevel = SovereigntyLevel.S0_AUTONOMOUS,
    ) -> DiscountAdvisory:
        if base_amount.currency != quoted_amount.currency:
            raise ValueError("base_amount and quoted_amount currencies must match")
        if quoted_amount.amount > base_amount.amount:
            # Markups don't need a discount advisory.
            return DiscountAdvisory(
                base_amount=base_amount,
                quoted_amount=quoted_amount,
                discount_pct=0.0,
                verdict=DiscountVerdict.NO_DISCOUNT,
                reasons=["quoted_amount >= base_amount; no discount applied"],
                requires_sami_approval=False,
                suggested_sovereignty=sovereignty_level,
            )

        if base_amount.amount == 0:
            return DiscountAdvisory(
                base_amount=base_amount,
                quoted_amount=quoted_amount,
                discount_pct=0.0,
                verdict=DiscountVerdict.NO_DISCOUNT,
                reasons=["base amount is zero — no discount to evaluate"],
            )

        discount_amount = base_amount.amount - quoted_amount.amount
        discount_pct = discount_amount / base_amount.amount

        reasons: list[str] = []
        verdict = DiscountVerdict.AUTONOMOUS
        requires_approval = False
        suggested = sovereignty_level

        if discount_pct == 0:
            verdict = DiscountVerdict.NO_DISCOUNT
            reasons.append("price unchanged")
        elif discount_pct >= _DISCOUNT_HARD_FLOOR:
            verdict = DiscountVerdict.EXCEEDS_LIMIT
            requires_approval = True
            suggested = SovereigntyLevel.S3_SAMI_ONLY
            reasons.append(
                f"discount {discount_pct:.0%} >= hard floor "
                f"{_DISCOUNT_HARD_FLOOR:.0%} → Sami-only"
            )
        elif discount_pct >= _DISCOUNT_APPROVAL_THRESHOLD:
            verdict = DiscountVerdict.REQUIRES_APPROVAL
            requires_approval = True
            suggested = SovereigntyLevel.S2_SAMI_APPROVAL
            reasons.append(
                f"discount {discount_pct:.0%} >= approval threshold "
                f"{_DISCOUNT_APPROVAL_THRESHOLD:.0%} → S2 approval"
            )
        else:
            reasons.append(
                f"discount {discount_pct:.0%} within autonomous range"
            )

        # §39 critical-trigger overlay: high-value deals always need a
        # second pair of eyes.
        if base_amount.amount >= _HIGH_VALUE_AMOUNT_SAR and verdict != DiscountVerdict.NO_DISCOUNT:
            requires_approval = True
            if suggested.numeric < SovereigntyLevel.S2_SAMI_APPROVAL.numeric:
                suggested = SovereigntyLevel.S2_SAMI_APPROVAL
            reasons.append(
                f"base amount {base_amount.amount} SAR is enterprise-tier"
            )

        return DiscountAdvisory(
            base_amount=base_amount,
            quoted_amount=quoted_amount,
            discount_pct=float(round(discount_pct, 4)),
            verdict=verdict,
            reasons=reasons,
            requires_sami_approval=requires_approval,
            suggested_sovereignty=suggested,
        )


__all__ = [
    "DiscountAdvisory",
    "DiscountVerdict",
    "PricingEngine",
]
