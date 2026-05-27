"""Upsell suggester based on health + offer library."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.customer.health_score import CustomerHealth


@dataclass(frozen=True)
class UpsellSuggestion:
    customer_id: str
    suggested_offer_id: str
    confidence: float
    rationale: str


class UpsellSuggester:
    def suggest(
        self,
        *,
        customer_id: str,
        health: CustomerHealth,
        catalog: list[tuple[str, str]],   # [(offer_id, tier_label)]
    ) -> UpsellSuggestion | None:
        if health.upsell_potential == "low" or not catalog:
            return None
        offer_id, tier = catalog[-1]      # crude: suggest the largest offer
        return UpsellSuggestion(
            customer_id=customer_id,
            suggested_offer_id=offer_id,
            confidence=health.score,
            rationale=f"Health {health.score:.2f}, upsell_potential={health.upsell_potential} → recommend {tier}.",
        )


__all__ = ["UpsellSuggester", "UpsellSuggestion"]
