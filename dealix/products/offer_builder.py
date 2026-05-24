"""خادم المنتج — OfferBuilder.

Validates and instantiates new `Offer` records before they enter the
catalog. Runs `NoOverclaimGuardrail` on the name + pain so we don't
ship marketing claims we can't substantiate.
"""

from __future__ import annotations

from decimal import Decimal

from dealix.hermes.core.opportunities import OpportunityType
from dealix.hermes.core.schemas import Money
from dealix.money.offer_matcher import Offer
from dealix.trust.guardrails import NoOverclaimGuardrail


class OfferBuilderError(ValueError):
    """Raised when an offer fails validation or a guardrail check."""


class OfferBuilder:
    """Construct + validate new Offer records."""

    def __init__(self, overclaim_guardrail: NoOverclaimGuardrail | None = None) -> None:
        self._guard = overclaim_guardrail or NoOverclaimGuardrail()

    def build(
        self,
        name: str,
        buyer: str,
        pain: str,
        deliverable: str,
        price_band: tuple[Money, Money],
        success_metric: str = "Closed pilot within 30 days",
        keywords: tuple[str, ...] = (),
        opportunity_types: tuple[OpportunityType, ...] = (
            OpportunityType.REVENUE,
        ),
    ) -> Offer:
        if not name.strip():
            raise OfferBuilderError("offer name must not be empty")
        if not buyer.strip():
            raise OfferBuilderError("offer buyer must not be empty")
        low, high = price_band
        if low.amount > high.amount:
            raise OfferBuilderError(
                f"price band low {low.amount} > high {high.amount}"
            )
        if low.amount < Decimal("0"):
            raise OfferBuilderError("price band low must be >= 0")
        if low.currency != high.currency:
            raise OfferBuilderError("price band currencies must match")

        payload = {
            "title": name,
            "body": pain,
            "summary": deliverable,
        }
        result = self._guard.check(payload)
        if not result.passed:
            raise OfferBuilderError(
                f"overclaim guardrail blocked offer name/pain: {result.findings}"
            )
        try:
            return Offer(
                name=name.strip(),
                buyer=buyer.strip(),
                pain=pain.strip(),
                deliverable=deliverable.strip(),
                price_band=price_band,
                success_metric=success_metric.strip(),
                keywords=keywords,
                opportunity_types=opportunity_types,
            )
        except ValueError as exc:
            raise OfferBuilderError(str(exc)) from exc


__all__ = ["OfferBuilder", "OfferBuilderError"]
