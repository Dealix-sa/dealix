"""
Offer registry — §99.

Every offer must declare a real buyer, a real pain, a clear promise,
deliverables, a price, the metric of success, the planned upsell, and
the trust risks. Anything less is rejected at the gate.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from typing import Any

from dealix.sovereign_control_plane.types import OFFER_STATE_ORDER, OfferState


class OfferGateError(ValueError):
    """Raised when an offer fails the §99 completeness gate."""


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
    metrics: dict[str, Any] = field(default_factory=dict)

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
            "metrics": dict(self.metrics),
        }


def _new_id() -> str:
    return f"off_{uuid.uuid4().hex[:12]}"


_REQUIRED_FIELDS = (
    "buyer", "pain", "promise", "deliverables",
    "price_sar", "metric", "upsell", "trust_risks",
)


class OfferRegistry:
    def __init__(self) -> None:
        self._items: dict[str, Offer] = {}
        self._lock = threading.Lock()

    def register(self, offer: Offer) -> Offer:
        self._validate(offer)
        with self._lock:
            if not offer.offer_id:
                offer.offer_id = _new_id()
            self._items[offer.offer_id] = offer
            return offer

    def get(self, offer_id: str) -> Offer | None:
        return self._items.get(offer_id)

    def list(self) -> list[Offer]:
        return list(self._items.values())

    def transition(self, offer_id: str, new_state: OfferState) -> Offer:
        with self._lock:
            offer = self._items.get(offer_id)
            if offer is None:
                raise KeyError(offer_id)
            self._validate_transition(offer.state, new_state)
            offer.state = new_state
            return offer

    @staticmethod
    def _validate(offer: Offer) -> None:
        missing: list[str] = []
        for field_name in _REQUIRED_FIELDS:
            value = getattr(offer, field_name)
            if value is None or (isinstance(value, (str, list)) and not value):
                missing.append(field_name)
            elif field_name == "price_sar" and value <= 0:
                missing.append(field_name)
        if missing:
            raise OfferGateError(f"offer missing/empty fields: {missing}")

    @staticmethod
    def _validate_transition(current: OfferState, target: OfferState) -> None:
        terminal = {OfferState.PAUSED, OfferState.RETIRED}
        if target in terminal:
            return
        if current in terminal and target not in terminal:
            return
        try:
            cur_idx = OFFER_STATE_ORDER.index(current)
            tgt_idx = OFFER_STATE_ORDER.index(target)
        except ValueError:
            raise OfferGateError(f"unknown state {current}/{target}")
        if tgt_idx != cur_idx + 1:
            raise OfferGateError(
                f"cannot skip states: {current.value} → {target.value}"
            )
