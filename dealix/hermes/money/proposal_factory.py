"""Proposal Factory — drafts a structured proposal (no external send)."""

from __future__ import annotations

from typing import Any

from dealix.hermes.core.schemas import Opportunity
from dealix.hermes.money.pricing import PricingIntelligence


class ProposalFactory:
    def __init__(self) -> None:
        self._pricing = PricingIntelligence()

    def draft(self, opp: Opportunity, *, offer: dict[str, Any]) -> dict[str, Any]:
        price = self._pricing.recommend(opp)
        return {
            "title": f"{offer.get('offer', 'Custom Offer')} — {opp.title}",
            "buyer": offer.get("buyer", "Decision maker"),
            "pain": offer.get("pain", opp.description[:160]),
            "promise": offer.get("promise", opp.recommended_action),
            "deliverables": offer.get("deliverables", []),
            "price": {
                "floor_sar": price.floor_sar,
                "target_sar": price.target_sar,
                "ceiling_sar": price.ceiling_sar,
            },
            "metric": offer.get("outcome_metric", "Outcome to be agreed"),
            "delivery_time": offer.get("delivery_time", "TBD"),
            "upsell": offer.get("upsell", ""),
            "draft_only": True,
            "external_send": False,
        }
