"""
Signal Graph — كل إشارة (lead, intent, mention, signal_event) تُحفظ مع روابطها
إلى الفرص (`opportunity_id`). يجاوب أسئلة مثل: "ما الإشارات التي رفعت
opportunity X؟" و "أي قناة جلبت إشارات حُولت لفرص؟"
"""

from __future__ import annotations

import threading
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Signal:
    signal_id: str
    source: str  # channel id
    payload: dict[str, Any]
    captured_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    opportunity_id: str | None = None
    tags: list[str] = field(default_factory=list)


class SignalGraph:
    def __init__(self) -> None:
        self._signals: dict[str, Signal] = {}
        self._by_opportunity: dict[str, list[str]] = defaultdict(list)
        self._lock = threading.Lock()

    def add(self, signal: Signal) -> Signal:
        with self._lock:
            self._signals[signal.signal_id] = signal
            if signal.opportunity_id:
                self._by_opportunity[signal.opportunity_id].append(signal.signal_id)
            return signal

    def link_to_opportunity(self, signal_id: str, opportunity_id: str) -> None:
        with self._lock:
            sig = self._signals.get(signal_id)
            if sig is None:
                raise KeyError(signal_id)
            sig.opportunity_id = opportunity_id
            self._by_opportunity[opportunity_id].append(signal_id)

    def signals_for_opportunity(self, opportunity_id: str) -> list[Signal]:
        with self._lock:
            return [self._signals[sid] for sid in self._by_opportunity.get(opportunity_id, [])]

    def signals_by_source(self) -> dict[str, int]:
        with self._lock:
            counts: dict[str, int] = defaultdict(int)
            for s in self._signals.values():
                counts[s.source] += 1
            return dict(counts)


__all__ = ["Signal", "SignalGraph"]
