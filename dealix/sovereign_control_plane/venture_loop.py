"""
Venture Value Loop — §104.

No vertical product is scaled before: real replies, a clear pain map,
an understood offer, a leads list, and recorded outcomes. The
``recommend_action`` rule enforces this gate.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class Venture:
    venture_id: str
    sector: str
    pain_map: dict[str, str]
    offer_id: str | None
    targets_count: int
    outcomes_count: int
    status: str = "scouting"
    signals: list[dict[str, Any]] = field(default_factory=list)
    pilots: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "venture_id": self.venture_id,
            "sector": self.sector,
            "pain_map": dict(self.pain_map),
            "offer_id": self.offer_id,
            "targets_count": self.targets_count,
            "outcomes_count": self.outcomes_count,
            "status": self.status,
            "signals": list(self.signals),
            "pilots": list(self.pilots),
            "created_at": self.created_at,
        }


class VentureValueLoop:
    def __init__(self) -> None:
        self._items: dict[str, Venture] = {}
        self._lock = threading.Lock()

    def create(self, sector: str) -> Venture:
        with self._lock:
            v = Venture(
                venture_id=f"ven_{uuid.uuid4().hex[:12]}",
                sector=sector, pain_map={}, offer_id=None,
                targets_count=0, outcomes_count=0, status="scouting",
                created_at=datetime.now(UTC).isoformat(),
            )
            self._items[v.venture_id] = v
            return v

    def get(self, venture_id: str) -> Venture | None:
        return self._items.get(venture_id)

    def add_signal(
        self, venture_id: str, source: str, body: str, replied: bool
    ) -> dict[str, Any]:
        v = self._items[venture_id]
        rec = {"source": source, "body": body, "replied": replied,
               "at": datetime.now(UTC).isoformat()}
        v.signals.append(rec)
        return rec

    def define_pain(self, venture_id: str, pain_map: dict[str, str]) -> Venture:
        v = self._items[venture_id]
        v.pain_map = dict(pain_map)
        v.status = "pain_defined"
        return v

    def attach_offer(self, venture_id: str, offer_id: str) -> Venture:
        v = self._items[venture_id]
        v.offer_id = offer_id
        v.status = "offer_attached"
        return v

    def add_targets(self, venture_id: str, count: int) -> Venture:
        v = self._items[venture_id]
        v.targets_count += int(count)
        return v

    def record_pilot(
        self, venture_id: str, customer: str, outcome_recorded: bool
    ) -> dict[str, Any]:
        v = self._items[venture_id]
        rec = {"customer": customer, "outcome_recorded": outcome_recorded,
               "at": datetime.now(UTC).isoformat()}
        v.pilots.append(rec)
        if outcome_recorded:
            v.outcomes_count += 1
        return rec

    def recommend_action(self, venture_id: str) -> str:
        v = self._items[venture_id]
        real_replies = any(s["replied"] for s in v.signals)
        if not real_replies:
            return "hold:no_real_replies"
        if not v.pain_map:
            return "hold:no_pain_map"
        if v.offer_id is None:
            return "hold:no_offer"
        if v.targets_count < 10:
            return "hold:no_leads_list"
        if v.outcomes_count == 0:
            return "hold:no_outcomes"
        return "scale"
