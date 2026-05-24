"""Tiny synchronous event bus.

Every cross-module hop goes through this bus. The bus is intentionally
in-memory and synchronous so the kernel stays deterministic and easy to
test; a Redis / NATS adapter can replace it later.

Event names follow ``<module>.<verb>_<noun>`` from section 125:

    market.signal_detected
    opportunity.created
    product.offer_suggested
    money.proposal_requested
    trust.check_required
    approval.requested
    execution.completed
    outcome.logged
    asset.created
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable


class EventKind(str):
    """String alias kept loose so domains can mint their own names."""


Handler = Callable[["Event"], None]


@dataclass(frozen=True)
class Event:
    name: str
    payload: dict[str, Any]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = defaultdict(list)
        self._history: list[Event] = []

    def on(self, name: str, handler: Handler) -> None:
        self._handlers[name].append(handler)

    def emit(self, name: str, **payload: Any) -> Event:
        event = Event(name=name, payload=payload)
        self._history.append(event)
        for h in list(self._handlers.get(name, ())):
            h(event)
        return event

    def history(self) -> list[Event]:
        return list(self._history)

    def by_name(self, name: str) -> list[Event]:
        return [e for e in self._history if e.name == name]


__all__ = ["Event", "EventBus", "EventKind", "Handler"]
