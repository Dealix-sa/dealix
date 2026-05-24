"""Signal Intake — entry point for every input the system observes."""

from __future__ import annotations

from threading import RLock
from typing import Any

from dealix.hermes.core.schemas import Sensitivity, Signal, SignalType


class SignalStore:
    """In-memory signal inbox. Thread-safe; swappable to a DB-backed store."""

    def __init__(self) -> None:
        self._items: dict[str, Signal] = {}
        self._lock = RLock()

    def ingest(
        self,
        *,
        source: str,
        signal_type: SignalType | str,
        title: str,
        content: str = "",
        confidence: float = 0.5,
        sensitivity: Sensitivity | str = Sensitivity.INTERNAL,
        raw_payload: dict[str, Any] | None = None,
        owner: str = "Sami",
    ) -> Signal:
        sig = Signal(
            source=source,
            signal_type=SignalType(signal_type),
            title=title,
            content=content,
            confidence=confidence,
            sensitivity=Sensitivity(sensitivity),
            raw_payload=raw_payload or {},
            owner=owner,
        )
        with self._lock:
            self._items[sig.id] = sig
        return sig

    def get(self, signal_id: str) -> Signal | None:
        with self._lock:
            return self._items.get(signal_id)

    def mark_processed(self, signal_id: str) -> None:
        with self._lock:
            sig = self._items.get(signal_id)
            if sig is not None:
                self._items[signal_id] = sig.model_copy(update={"processed": True})

    def list(self, *, only_unprocessed: bool = False) -> list[Signal]:
        with self._lock:
            items = list(self._items.values())
        if only_unprocessed:
            items = [s for s in items if not s.processed]
        return sorted(items, key=lambda s: s.created_at, reverse=True)

    def clear(self) -> None:
        with self._lock:
            self._items.clear()


_default_store: SignalStore | None = None


def get_signal_store() -> SignalStore:
    global _default_store
    if _default_store is None:
        _default_store = SignalStore()
    return _default_store
