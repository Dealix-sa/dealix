"""Offer Builder — the canonical Offer Card.

An OfferCard is the only shape an external "thing we sell" can take.
Anything missing required fields is rejected at construction time, so a
half-formed offer cannot leak to a customer-facing surface.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field, NonNegativeFloat, field_validator

from dealix.hermes.sovereignty import SovereigntyLevel


class OfferKind(StrEnum):
    PILOT = "pilot"
    PACKAGE = "package"
    RETAINER = "retainer"
    LICENSE = "license"
    WHITE_LABEL = "white_label"
    TRAINING = "training"
    REPORT = "report"
    SAAS = "saas"
    API = "api"


class OfferCard(BaseModel):
    offer_id: str = Field(default_factory=lambda: str(uuid4()))
    offer_name: str = Field(min_length=3, max_length=80)
    kind: OfferKind
    buyer: str = Field(min_length=3)
    pain: str = Field(min_length=10)
    promise: str = Field(min_length=10)
    deliverables: list[str] = Field(min_length=1)
    floor_price_sar: NonNegativeFloat
    ceiling_price_sar: NonNegativeFloat
    delivery_days: int = Field(ge=1, le=180)
    proof_required: bool = True
    upsell: str | None = None
    sovereignty_level: SovereigntyLevel = SovereigntyLevel.S2_SAMI_APPROVAL
    sales_channels: list[str] = Field(min_length=1)
    outcome_metric: str = Field(min_length=3)
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("ceiling_price_sar")
    @classmethod
    def _ceiling_ge_floor(cls, v: float, info) -> float:  # type: ignore[no-untyped-def]
        floor = info.data.get("floor_price_sar", 0.0)
        if v < floor:
            raise ValueError("ceiling_price_sar must be >= floor_price_sar")
        return v


class OfferLibrary:
    def __init__(self) -> None:
        self._offers: dict[str, OfferCard] = {}

    def register(self, offer: OfferCard) -> OfferCard:
        if offer.offer_id in self._offers:
            raise ValueError(f"offer already registered: {offer.offer_id}")
        self._offers[offer.offer_id] = offer
        return offer

    def upsert(self, offer: OfferCard) -> OfferCard:
        self._offers[offer.offer_id] = offer
        return offer

    def get(self, offer_id: str) -> OfferCard | None:
        return self._offers.get(offer_id)

    def by_name(self, offer_name: str) -> OfferCard | None:
        for o in self._offers.values():
            if o.offer_name == offer_name:
                return o
        return None

    def active(self) -> list[OfferCard]:
        return [o for o in self._offers.values() if o.active]

    def all(self) -> list[OfferCard]:
        return list(self._offers.values())

    def deactivate(self, offer_id: str) -> OfferCard:
        o = self._offers[offer_id]
        o = o.model_copy(update={"active": False})
        self._offers[offer_id] = o
        return o


__all__ = ["OfferCard", "OfferKind", "OfferLibrary"]
