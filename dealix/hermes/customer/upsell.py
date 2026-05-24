"""Upsell Suggester — picks the next-best offer for an existing customer."""

from __future__ import annotations

from dealix.hermes.customer.health_score import CustomerHealth
from dealix.hermes.products.offer_library import default_offers


class UpsellSuggester:
    def suggest(self, health: CustomerHealth) -> dict | None:
        if health.renewal_risk == "high":
            return None
        catalog = default_offers()
        # Bias toward the AI Trust Kit for medium-risk; managed retainer for low-risk.
        if health.renewal_risk == "medium":
            return next((o for o in catalog if "Trust" in o["offer"]), catalog[0])
        return next((o for o in catalog if "White-label" in o["offer"]), catalog[0])
