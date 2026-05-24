"""خادم العميل — UpsellRecommender."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.money.offer_matcher import Offer


class UpsellSuggestion(BaseModel):
    """A suggested next purchase for an existing customer."""

    model_config = ConfigDict(extra="forbid")

    offer_name: str = Field(..., min_length=1, max_length=120)
    rationale: str = Field(..., min_length=1, max_length=400)
    score: float = Field(..., ge=0.0, le=5.0)
    requires_approval: bool = True


class UpsellRecommender:
    """Score catalog offers against a customer's current footprint."""

    def recommend(
        self,
        customer: dict[str, Any],
        current_offers: list[str],
        catalog: list[Offer],
        limit: int = 3,
    ) -> list[UpsellSuggestion]:
        current = {name.lower() for name in current_offers}
        candidates: list[UpsellSuggestion] = []
        for offer in catalog:
            if offer.name.lower() in current:
                continue
            score = self._score(customer, offer)
            if score <= 0:
                continue
            rationale = self._rationale(customer, offer, score)
            candidates.append(
                UpsellSuggestion(
                    offer_name=offer.name,
                    rationale=rationale,
                    score=round(score, 3),
                    requires_approval=True,
                )
            )
        candidates.sort(key=lambda s: (-s.score, s.offer_name))
        return candidates[: max(0, limit)]

    @staticmethod
    def _score(customer: dict[str, Any], offer: Offer) -> float:
        score = 0.5  # baseline
        sector = str(customer.get("sector", "")).lower()
        buyer_role = str(customer.get("buyer_role", "")).lower()
        if buyer_role and buyer_role in offer.buyer.lower():
            score += 1.0
        bag = " ".join(
            [
                sector,
                str(customer.get("notes", "")),
                str(customer.get("interests", "")),
            ]
        ).lower()
        hits = sum(1 for kw in offer.keywords if kw in bag)
        score += 0.5 * hits
        # Sensitive customers favour AI Trust Kit.
        if customer.get("regulated") and "trust" in offer.name.lower():
            score += 1.0
        # Repeat-purchase customers favour Renewal pack.
        if customer.get("retainer") and "renewal" in offer.name.lower():
            score += 1.0
        return min(5.0, score)

    @staticmethod
    def _rationale(customer: dict[str, Any], offer: Offer, score: float) -> str:
        return (
            f"Matches buyer profile + sector signals (score={score:.2f}); "
            f"offer success metric: {offer.success_metric}"
        )


__all__ = ["UpsellRecommender", "UpsellSuggestion"]
