"""Offer library — every offer with readiness gating."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field


class Offer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    offer_id: str
    name: str
    buyer: str
    pain: str
    promise: str
    deliverables: list[str] = Field(default_factory=list)
    price_sar: float = 0.0
    timeline_days: int = 0
    metric: str = ""
    upsell: str = ""
    trust_risks: list[str] = Field(default_factory=list)
    cta: str = ""


@dataclass(frozen=True)
class OfferReadiness:
    ready: bool
    missing_fields: tuple[str, ...]


def check_readiness(offer: Offer) -> OfferReadiness:
    missing: list[str] = []
    for required in ("buyer", "pain", "promise", "metric", "cta"):
        if not getattr(offer, required):
            missing.append(required)
    if not offer.deliverables:
        missing.append("deliverables")
    if offer.price_sar <= 0:
        missing.append("price_sar")
    if offer.timeline_days <= 0:
        missing.append("timeline_days")
    return OfferReadiness(ready=not missing, missing_fields=tuple(missing))


DEFAULT_OFFERS: tuple[Offer, ...] = (
    Offer(
        offer_id="revenue_hunter_pilot",
        name="Revenue Hunter Pilot",
        buyer="founder / head of sales",
        pain="warm leads going cold without proposals",
        promise="3 board-grade proposals shipped in 14 days",
        deliverables=["3 proposals", "1 follow-up plan", "1 weekly review"],
        price_sar=4999,
        timeline_days=14,
        metric="proposals_accepted",
        upsell="managed_ops",
        cta="book_pilot",
    ),
    Offer(
        offer_id="ai_trust_kit",
        name="AI Trust Kit",
        buyer="head of compliance / CTO",
        pain="agents and tools used without governance",
        promise="agent registry, MCP review, evidence packs in 30 days",
        deliverables=["agent registry", "MCP review", "evidence pack template"],
        price_sar=24999,
        timeline_days=30,
        metric="controls_active",
        upsell="managed_ops",
        cta="book_review",
    ),
    Offer(
        offer_id="agency_white_label_kit",
        name="Agency White-label Kit",
        buyer="agency owner",
        pain="clients asking for AI services the agency cannot deliver",
        promise="white-label revenue stream within 60 days",
        deliverables=["white-label landing pack", "deal-room template", "training kit"],
        price_sar=49999,
        timeline_days=60,
        metric="partner_signed_deals",
        upsell="custom_ai",
        cta="book_partner_call",
    ),
)


@dataclass
class OfferLibrary:
    _offers: dict[str, Offer] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for offer in DEFAULT_OFFERS:
            self._offers[offer.offer_id] = offer

    def upsert(self, offer: Offer) -> Offer:
        self._offers[offer.offer_id] = offer
        return offer

    def get(self, offer_id: str) -> Offer:
        return self._offers[offer_id]

    def exists(self, offer_id: str) -> bool:
        return offer_id in self._offers

    def list(self) -> list[Offer]:
        return list(self._offers.values())

    def ready_offers(self) -> list[Offer]:
        return [o for o in self._offers.values() if check_readiness(o).ready]
