"""
Section 67 — Offer System.

An Offer is the atomic commercial unit. No Offer leaves `internal_review`
unless it holds: buyer, pain, promise, deliverables, price, metric,
upsell, and trust risks. Metrics drive the Scale/Kill Board.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class OfferState(StrEnum):
    DRAFT = "draft"
    INTERNAL_REVIEW = "internal_review"
    PILOT_READY = "pilot_ready"
    ACTIVE = "active"
    PRODUCTIZED = "productized"
    SCALED = "scaled"
    PAUSED = "paused"
    RETIRED = "retired"


@dataclass
class OfferMetrics:
    views: int = 0
    messages_sent: int = 0
    replies: int = 0
    calls: int = 0
    proposals: int = 0
    wins: int = 0
    losses: int = 0
    revenue_sar: float = 0.0
    delivery_time_days: float = 0.0
    margin_pct: float = 0.0
    assets_created: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "views": self.views,
            "messages_sent": self.messages_sent,
            "replies": self.replies,
            "calls": self.calls,
            "proposals": self.proposals,
            "wins": self.wins,
            "losses": self.losses,
            "revenue_sar": self.revenue_sar,
            "delivery_time_days": self.delivery_time_days,
            "margin_pct": self.margin_pct,
            "assets_created": self.assets_created,
        }


@dataclass
class Offer:
    offer_id: str
    name: str
    buyer: str
    pain: str
    promise: str
    deliverables: list[str]
    price_sar: float
    metric: str
    upsell: str
    trust_risks: list[str]
    state: OfferState = OfferState.DRAFT
    metrics: OfferMetrics = field(default_factory=OfferMetrics)
    workspace_id: str = "internal_dealix_workspace"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    last_updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def is_ready_for_review(self) -> bool:
        return bool(
            self.buyer
            and self.pain
            and self.promise
            and self.deliverables
            and self.price_sar > 0
            and self.metric
            and self.upsell
            and self.trust_risks
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "offer_id": self.offer_id,
            "name": self.name,
            "buyer": self.buyer,
            "pain": self.pain,
            "promise": self.promise,
            "deliverables": list(self.deliverables),
            "price_sar": self.price_sar,
            "metric": self.metric,
            "upsell": self.upsell,
            "trust_risks": list(self.trust_risks),
            "state": self.state.value,
            "metrics": self.metrics.to_dict(),
            "workspace_id": self.workspace_id,
            "created_at": self.created_at.isoformat(),
            "last_updated_at": self.last_updated_at.isoformat(),
        }


_VALID_TRANSITIONS: dict[OfferState, set[OfferState]] = {
    OfferState.DRAFT: {OfferState.INTERNAL_REVIEW, OfferState.RETIRED},
    OfferState.INTERNAL_REVIEW: {OfferState.PILOT_READY, OfferState.DRAFT, OfferState.RETIRED},
    OfferState.PILOT_READY: {OfferState.ACTIVE, OfferState.PAUSED, OfferState.RETIRED},
    OfferState.ACTIVE: {
        OfferState.PRODUCTIZED,
        OfferState.PAUSED,
        OfferState.RETIRED,
        OfferState.SCALED,
    },
    OfferState.PRODUCTIZED: {OfferState.SCALED, OfferState.PAUSED, OfferState.RETIRED},
    OfferState.SCALED: {OfferState.PAUSED, OfferState.RETIRED},
    OfferState.PAUSED: {OfferState.ACTIVE, OfferState.RETIRED},
    OfferState.RETIRED: set(),
}


class OfferSystem:
    def __init__(self) -> None:
        self._offers: dict[str, Offer] = {}

    def draft(
        self,
        *,
        name: str,
        buyer: str = "",
        pain: str = "",
        promise: str = "",
        deliverables: Iterable[str] = (),
        price_sar: float = 0.0,
        metric: str = "",
        upsell: str = "",
        trust_risks: Iterable[str] = (),
        workspace_id: str = "internal_dealix_workspace",
    ) -> Offer:
        offer = Offer(
            offer_id=f"of_{uuid.uuid4().hex[:12]}",
            name=name,
            buyer=buyer,
            pain=pain,
            promise=promise,
            deliverables=list(deliverables),
            price_sar=price_sar,
            metric=metric,
            upsell=upsell,
            trust_risks=list(trust_risks),
            workspace_id=workspace_id,
        )
        self._offers[offer.offer_id] = offer
        return offer

    def transition(self, offer_id: str, *, target: OfferState) -> Offer:
        offer = self.get(offer_id)
        if offer.state is target:
            return offer
        if target not in _VALID_TRANSITIONS[offer.state]:
            raise ValueError(
                f"invalid offer transition: {offer.state.value} → {target.value}"
            )
        if target in (
            OfferState.INTERNAL_REVIEW,
            OfferState.PILOT_READY,
            OfferState.ACTIVE,
        ) and not offer.is_ready_for_review():
            raise ValueError(
                f"offer {offer_id} missing required fields — cannot enter {target.value}"
            )
        offer.state = target
        offer.last_updated_at = datetime.now(UTC)
        return offer

    def record_metric_event(self, offer_id: str, *, field: str, delta: float = 1.0) -> Offer:
        offer = self.get(offer_id)
        if not hasattr(offer.metrics, field):
            raise ValueError(f"unknown metric field: {field}")
        setattr(offer.metrics, field, getattr(offer.metrics, field) + delta)
        offer.last_updated_at = datetime.now(UTC)
        return offer

    def get(self, offer_id: str) -> Offer:
        try:
            return self._offers[offer_id]
        except KeyError as exc:
            raise KeyError(f"unknown offer: {offer_id}") from exc

    def all(self) -> list[Offer]:
        return list(self._offers.values())

    def by_state(self, state: OfferState) -> list[Offer]:
        return [o for o in self._offers.values() if o.state is state]
