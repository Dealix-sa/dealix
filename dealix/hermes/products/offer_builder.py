"""OfferBuilder — assembles an Offer with all readiness fields populated."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class OfferLifecycleStatus(str, Enum):
    DRAFT = "draft"
    INTERNAL_REVIEW = "internal_review"
    TRUST_REVIEW = "trust_review"
    PILOT_READY = "pilot_ready"
    ACTIVE = "active"
    PRODUCTIZED = "productized"
    SCALED = "scaled"
    PAUSED = "paused"
    RETIRED = "retired"


@dataclass
class Offer:
    id: str
    buyer: str
    pain: str
    promise: str
    deliverables: list[str]
    price_sar: float
    timeline_weeks: int
    metric: str
    upsell: str
    trust_risks: list[str]
    domain: str = "money"
    status: OfferLifecycleStatus = OfferLifecycleStatus.DRAFT
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class OfferBuilder:
    _by_id: dict[str, Offer] = field(default_factory=dict)

    def draft(
        self,
        *,
        buyer: str,
        pain: str,
        promise: str,
        deliverables: list[str],
        price_sar: float,
        timeline_weeks: int,
        metric: str,
        upsell: str,
        trust_risks: list[str],
        domain: str = "money",
    ) -> Offer:
        # Section 117 readiness check: every offer needs all the fields.
        missing = [
            k
            for k, v in {
                "buyer": buyer,
                "pain": pain,
                "promise": promise,
                "deliverables": deliverables,
                "price_sar": price_sar,
                "timeline_weeks": timeline_weeks,
                "metric": metric,
                "upsell": upsell,
                "trust_risks": trust_risks,
            }.items()
            if not v
        ]
        if missing:
            raise ValueError(f"Offer not ready; missing: {', '.join(missing)}")
        if price_sar <= 0:
            raise ValueError("Offer price must be > 0.")
        offer = Offer(
            id=f"off_{uuid.uuid4().hex[:10]}",
            buyer=buyer,
            pain=pain,
            promise=promise,
            deliverables=list(deliverables),
            price_sar=float(price_sar),
            timeline_weeks=int(timeline_weeks),
            metric=metric,
            upsell=upsell,
            trust_risks=list(trust_risks),
            domain=domain,
        )
        self._by_id[offer.id] = offer
        return offer

    def transition(self, offer_id: str, status: OfferLifecycleStatus) -> Offer:
        offer = self._by_id[offer_id]
        offer.status = status
        return offer

    def get(self, offer_id: str) -> Offer:
        return self._by_id[offer_id]

    def all(self) -> list[Offer]:
        return list(self._by_id.values())


__all__ = ["Offer", "OfferBuilder", "OfferLifecycleStatus"]
