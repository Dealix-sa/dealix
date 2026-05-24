"""Renders an offer into a landing page descriptor (markdown blocks)."""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from dealix.hermes.products.offer_builder import Offer


@dataclass(frozen=True)
class LandingPage:
    id: str
    slug: str
    headline: str
    promise: str
    bullets: list[str]
    cta: str
    price_block: str
    risk_disclaimer: str


class LandingPageBuilder:
    def render(self, offer: Offer, *, slug: str | None = None, cta: str = "Book a 15-min call") -> LandingPage:
        return LandingPage(
            id=f"lnd_{uuid.uuid4().hex[:10]}",
            slug=slug or f"offer-{offer.id}",
            headline=offer.promise,
            promise=offer.promise,
            bullets=offer.deliverables,
            cta=cta,
            price_block=f"{offer.price_sar:,.0f} SAR / {offer.timeline_weeks} weeks",
            risk_disclaimer="Draft offer — terms confirmed in proposal.",
        )


__all__ = ["LandingPage", "LandingPageBuilder"]
