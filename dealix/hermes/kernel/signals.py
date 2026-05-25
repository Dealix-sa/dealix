"""Phase 1: Signal capture and classification. No Signal is ever lost."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from dealix.hermes.kernel.schemas import (
    LifecycleEvent,
    Signal,
    SignalSensitivity,
    SignalSource,
    SignalType,
)


@dataclass
class SignalStore:
    """In-memory store. Production replaces with hermes_signals table."""

    _signals: dict[str, Signal] = field(default_factory=dict)
    _events: list[LifecycleEvent] = field(default_factory=list)

    def capture(self, signal: Signal) -> LifecycleEvent:
        if signal.signal_id in self._signals:
            raise ValueError(f"signal {signal.signal_id} already captured")
        self._signals[signal.signal_id] = signal
        event = LifecycleEvent(
            event_type="signal.captured",
            entity_id=signal.signal_id,
            workspace_id=signal.workspace_id,
            actor=signal.owner,
            payload={"signal_type": signal.signal_type.value, "source": signal.source.value},
        )
        self._events.append(event)
        return event

    def classify(self, signal_id: str, signal_type: SignalType, sensitivity: SignalSensitivity) -> Signal:
        s = self._signals[signal_id]
        updated = s.model_copy(update={
            "signal_type": signal_type,
            "sensitivity": sensitivity,
            "classified": True,
        })
        self._signals[signal_id] = updated
        self._events.append(LifecycleEvent(
            event_type="signal.classified",
            entity_id=signal_id,
            workspace_id=updated.workspace_id,
            payload={"signal_type": signal_type.value, "sensitivity": sensitivity.value},
        ))
        return updated

    def archive(self, signal_id: str, reason: str = "") -> Signal:
        s = self._signals[signal_id]
        from datetime import UTC, datetime
        updated = s.model_copy(update={"archived_at": datetime.now(UTC).isoformat()})
        self._signals[signal_id] = updated
        return updated

    def get(self, signal_id: str) -> Signal:
        return self._signals[signal_id]

    def list(self) -> Iterable[Signal]:
        return list(self._signals.values())

    def events(self) -> list[LifecycleEvent]:
        return list(self._events)


def capture_signal(
    *,
    store: SignalStore,
    source: SignalSource,
    signal_type: SignalType,
    title: str,
    content: str,
    confidence: float = 0.5,
    sensitivity: SignalSensitivity = SignalSensitivity.internal,
    workspace_id: str = "dealix_internal",
    owner: str = "Sami",
    tags: list[str] | None = None,
    raw: dict | None = None,
) -> Signal:
    """Convenience function: build + capture in one step."""
    signal = Signal(
        source=source,
        signal_type=signal_type,
        title=title,
        content=content,
        confidence=confidence,
        sensitivity=sensitivity,
        workspace_id=workspace_id,
        owner=owner,
        tags=tags or [],
        raw=raw or {},
    )
    store.capture(signal)
    return signal
