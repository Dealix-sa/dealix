"""Packages a set of offers into a bundle (e.g. AI Trust Kit)."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass
class OfferPackage:
    id: str
    name: str
    offer_ids: list[str]
    price_sar: float
    promise: str


@dataclass
class OfferPackager:
    _by_id: dict[str, OfferPackage] = field(default_factory=dict)

    def bundle(self, *, name: str, offer_ids: list[str], price_sar: float, promise: str) -> OfferPackage:
        if not offer_ids:
            raise ValueError("Cannot bundle zero offers.")
        if price_sar <= 0:
            raise ValueError("Bundle price must be > 0.")
        pkg = OfferPackage(
            id=f"pkg_{uuid.uuid4().hex[:10]}",
            name=name,
            offer_ids=list(offer_ids),
            price_sar=float(price_sar),
            promise=promise,
        )
        self._by_id[pkg.id] = pkg
        return pkg

    def all(self) -> list[OfferPackage]:
        return list(self._by_id.values())


__all__ = ["OfferPackage", "OfferPackager"]
