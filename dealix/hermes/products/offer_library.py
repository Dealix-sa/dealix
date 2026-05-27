"""Searchable library of active offers."""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.products.offer_builder import Offer, OfferLifecycleStatus


@dataclass
class OfferLibrary:
    _by_id: dict[str, Offer] = field(default_factory=dict)

    def register(self, offer: Offer) -> None:
        self._by_id[offer.id] = offer

    def active(self) -> list[Offer]:
        return [
            o
            for o in self._by_id.values()
            if o.status in {OfferLifecycleStatus.ACTIVE, OfferLifecycleStatus.PRODUCTIZED, OfferLifecycleStatus.SCALED}
        ]

    def by_buyer(self, buyer: str) -> list[Offer]:
        return [o for o in self._by_id.values() if buyer.lower() in o.buyer.lower()]

    def all(self) -> list[Offer]:
        return list(self._by_id.values())

    def as_manifest_dict(self) -> dict[str, dict]:
        """Manifest view consumed by money.OfferMatcher."""
        return {
            o.id: {
                "domain": o.domain,
                "buyer_tags": [o.buyer],
                "min_value_sar": o.price_sar * 0.5,
                "price_sar": o.price_sar,
            }
            for o in self.active()
        }


__all__ = ["OfferLibrary"]
