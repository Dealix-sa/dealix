"""Landing Page Builder — produces a static landing-page blob for an offer."""

from __future__ import annotations

from typing import Any


class LandingPageBuilder:
    def build(self, offer: dict[str, Any]) -> dict[str, Any]:
        return {
            "headline": offer.get("promise", ""),
            "subhead": offer.get("pain", ""),
            "deliverables": offer.get("deliverables", []),
            "price": offer.get("price_range_sar", "On request"),
            "cta": f"Request {offer.get('offer', 'this offer')}",
            "metric": offer.get("outcome_metric", ""),
            "draft_only": True,
            "external_publish": False,
        }
