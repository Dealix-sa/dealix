"""Offer-level scale/kill verdicts."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.outcomes import get_outcome_store
from dealix.hermes.core.schemas import OutcomeStatus


@dataclass
class OfferVerdict:
    offer: str
    paid_count: int
    revenue_sar: float
    verdict: str
    reason: str


class OfferScaleKill:
    def evaluate(self, offer_name: str, *, paying_threshold: int = 2) -> OfferVerdict:
        outs = get_outcome_store().list()
        paid = [o for o in outs if o.status == OutcomeStatus.PAID.value]
        revenue = sum(o.revenue_sar for o in paid)
        if len(paid) >= paying_threshold:
            return OfferVerdict(offer_name, len(paid), revenue, "scale", "Paying threshold met.")
        if len(paid) == 0 and len(outs) > 20:
            return OfferVerdict(offer_name, 0, revenue, "kill", "No paid outcomes after wide exposure.")
        return OfferVerdict(offer_name, len(paid), revenue, "hold", "Keep observing.")
