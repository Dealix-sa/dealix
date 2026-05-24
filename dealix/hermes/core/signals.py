"""Signal Intake — the door through which raw inputs enter Hermes.

Intake validates the signal envelope, enforces a value-output guess, and
hands it to the opportunity stage. It does *not* execute anything.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from dealix.hermes.core.schemas import Signal, SignalSource


class SignalIntake:
    """In-memory signal store. Replace `_store` with a durable backend in
    Phase 2 (Postgres event table or Kafka topic).
    """

    def __init__(self) -> None:
        self._store: dict[str, Signal] = {}

    def capture(
        self,
        *,
        source: SignalSource | str,
        title: str,
        summary: str,
        captured_by: str,
        raw_payload: dict[str, Any] | None = None,
        tags: Iterable[str] | None = None,
    ) -> Signal:
        signal = Signal(
            source=SignalSource(source) if isinstance(source, str) else source,
            title=title,
            summary=summary,
            captured_by=captured_by,
            raw_payload=dict(raw_payload or {}),
            tags=list(tags or []),
        )
        self._store[signal.signal_id] = signal
        return signal

    def get(self, signal_id: str) -> Signal | None:
        return self._store.get(signal_id)

    def list_by_source(self, source: SignalSource) -> list[Signal]:
        return [s for s in self._store.values() if s.source is source]

    def all(self) -> list[Signal]:
        return list(self._store.values())

    def __len__(self) -> int:
        return len(self._store)


__all__ = ["SignalIntake"]
