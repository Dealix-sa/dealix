"""Offer Matcher — picks the canonical offer for an opportunity."""

from __future__ import annotations

from dealix.hermes.core.schemas import Opportunity, OpportunityType
from dealix.hermes.products.offer_library import default_offers


class OfferMatcher:
    def match(self, opp: Opportunity) -> dict | None:
        catalog = default_offers()
        otype = opp.opportunity_type
        if otype == OpportunityType.PARTNER.value:
            return next((o for o in catalog if "white_label" in o["offer"].lower()), None)
        if otype == OpportunityType.GOVERNANCE.value:
            return next((o for o in catalog if "trust" in o["offer"].lower()), None)
        if otype == OpportunityType.TRAINING.value:
            return next((o for o in catalog if "training" in o["offer"].lower() or "workshop" in o["offer"].lower()), None)
        return next(iter(catalog), None)
