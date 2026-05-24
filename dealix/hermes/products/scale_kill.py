"""Offer-level scale/kill recommendations.

Wraps `hermes.core.scale` to operate at the *offer* granularity, joining
the offer library with the outcome log.
"""

from __future__ import annotations

from collections import defaultdict

from dealix.hermes.core.outcomes import OutcomeLog
from dealix.hermes.core.scale import ScaleEngine
from dealix.hermes.core.schemas import ScaleDecision
from dealix.hermes.products.offer_builder import OfferLibrary


def evaluate_library(
    *,
    library: OfferLibrary,
    outcomes: OutcomeLog,
    opportunity_to_offer: dict[str, str],
    engine: ScaleEngine | None = None,
) -> list[ScaleDecision]:
    """Returns one ScaleDecision per offer in the library."""
    engine = engine or ScaleEngine()
    by_offer: dict[str, list] = defaultdict(list)
    for o in outcomes.all():
        offer_id = opportunity_to_offer.get(o.opportunity_id)
        if offer_id is None:
            continue
        by_offer[offer_id].append(o)

    out: list[ScaleDecision] = []
    for offer in library.all():
        out.append(engine.evaluate_offer(offer_id=offer.offer_id, outcomes=by_offer.get(offer.offer_id, [])))
    return out


__all__ = ["evaluate_library"]
