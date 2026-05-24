"""خادم المنتج — OfferLibrary.

In-memory registry of paid offers, seeded with the five canonical
offers from spec §43 (via `dealix.money.offer_matcher.SEED_OFFERS`).
"""

from __future__ import annotations

from dealix.money.offer_matcher import SEED_OFFERS, Offer


class OfferLibrary:
    """In-memory offer registry with lookup helpers."""

    def __init__(self, offers: list[Offer] | None = None) -> None:
        self._offers: dict[str, Offer] = {}
        seed = offers if offers is not None else list(SEED_OFFERS)
        for offer in seed:
            self.register(offer)

    def register(self, offer: Offer) -> Offer:
        if offer.name in self._offers:
            raise ValueError(f"offer already registered: {offer.name}")
        self._offers[offer.name] = offer
        return offer

    def get(self, name: str) -> Offer:
        try:
            return self._offers[name]
        except KeyError as exc:
            raise KeyError(f"unknown offer: {name}") from exc

    def all(self) -> list[Offer]:
        return list(self._offers.values())

    def list_for_buyer(self, buyer: str) -> list[Offer]:
        needle = buyer.lower().strip()
        if not needle:
            return self.all()
        return [
            o for o in self._offers.values() if needle in o.buyer.lower()
        ]

    def list_for_keyword(self, keyword: str) -> list[Offer]:
        needle = keyword.lower().strip()
        if not needle:
            return []
        out: list[Offer] = []
        for offer in self._offers.values():
            text = " ".join(
                [
                    offer.name,
                    offer.buyer,
                    offer.pain,
                    offer.deliverable,
                    *offer.keywords,
                ]
            ).lower()
            if needle in text:
                out.append(offer)
        return out


__all__ = ["OfferLibrary"]
