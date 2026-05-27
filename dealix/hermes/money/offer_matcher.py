"""Match an opportunity to an offer in the Product offer library."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.schemas import Opportunity


@dataclass(frozen=True)
class OfferMatch:
    offer_id: str
    confidence: float
    rationale: str


class OfferMatcher:
    def __init__(self, offer_library: dict[str, dict] | None = None) -> None:
        # offer_library is a thin dict view of the Products module's library
        # to keep this module decoupled from products at import time.
        self._offers = offer_library or {}

    def upsert_offer(self, offer_id: str, manifest: dict) -> None:
        self._offers[offer_id] = manifest

    def match(self, opp: Opportunity) -> OfferMatch | None:
        if not self._offers:
            return None
        best: OfferMatch | None = None
        for offer_id, manifest in self._offers.items():
            domain_match = manifest.get("domain") == opp.domain
            buyer_overlap = set(manifest.get("buyer_tags", [])) & set(opp.tags)
            price_fit = manifest.get("min_value_sar", 0) <= opp.estimated_value_sar
            score = (
                0.5 * (1.0 if domain_match else 0.0)
                + 0.3 * (1.0 if buyer_overlap else 0.0)
                + 0.2 * (1.0 if price_fit else 0.0)
            )
            if score > 0 and (best is None or score > best.confidence):
                best = OfferMatch(
                    offer_id=offer_id,
                    confidence=score,
                    rationale=f"domain={domain_match}, buyer_overlap={bool(buyer_overlap)}, price_fit={price_fit}",
                )
        return best


__all__ = ["OfferMatch", "OfferMatcher"]
