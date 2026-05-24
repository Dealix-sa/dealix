"""
Event bus — §93.

Synchronous in-memory pub/sub. Sufficient for this stage; replaceable
later by an async broker. Handler exceptions are recorded as incidents
of type ``agent_behavior_anomaly``.
"""

from __future__ import annotations

import threading
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class Event:
    event_id: str
    event_type: str
    source: str
    workspace_id: str | None
    sensitivity: str
    payload: dict[str, Any]
    created_at: str
    correlation_id: str | None = None
    sovereignty_level: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "source": self.source,
            "workspace_id": self.workspace_id,
            "sensitivity": self.sensitivity,
            "payload": dict(self.payload),
            "created_at": self.created_at,
            "correlation_id": self.correlation_id,
            "sovereignty_level": self.sovereignty_level,
        }


Handler = Callable[[Event], None]


class EventBus:
    def __init__(self) -> None:
        self._log: list[Event] = []
        self._subs: dict[str, list[Handler]] = {}
        self._wildcard: list[Handler] = []
        self._lock = threading.Lock()
        self._incident_sink: Callable[[str, str], None] | None = None

    def set_incident_sink(self, sink: Callable[[str, str], None]) -> None:
        """Wire an incident creator — used when a handler raises."""
        self._incident_sink = sink

    def publish(self, event: Event) -> None:
        with self._lock:
            self._log.append(event)
            handlers = list(self._subs.get(event.event_type, [])) + list(self._wildcard)
        for h in handlers:
            try:
                h(event)
            except Exception as exc:  # noqa: BLE001
                if self._incident_sink is not None:
                    self._incident_sink(
                        "agent_behavior_anomaly",
                        f"handler {h.__name__} raised on {event.event_type}: {exc!r}",
                    )

    def subscribe(self, event_type: str, handler: Handler) -> None:
        with self._lock:
            if event_type == "*":
                self._wildcard.append(handler)
            else:
                self._subs.setdefault(event_type, []).append(handler)

    def tail(self, n: int = 100) -> list[Event]:
        return list(self._log[-n:])

    def replay(self, event_type: str | None = None) -> list[Event]:
        if event_type is None:
            return list(self._log)
        return [e for e in self._log if e.event_type == event_type]


def make_event(
    event_type: str,
    source: str,
    payload: dict[str, Any],
    *,
    workspace_id: str | None = None,
    sensitivity: str = "INTERNAL",
    correlation_id: str | None = None,
    sovereignty_level: str | None = None,
) -> Event:
    return Event(
        event_id=f"evt_{uuid.uuid4().hex[:12]}",
        event_type=event_type,
        source=source,
        workspace_id=workspace_id,
        sensitivity=sensitivity,
        payload=dict(payload),
        created_at=datetime.now(UTC).isoformat(),
        correlation_id=correlation_id,
        sovereignty_level=sovereignty_level,
    )
