"""خادم Hermes — event bus.

Spec §27 enumerates 16 kernel events. The EventBus is an in-process,
asyncio-safe pub/sub used by the orchestrator + downstream observers
(audit log, friction log, dashboards).

Synchronous handlers are supported via `publish(event)`; async handlers
are dispatched serially via `apublish(event)`. Subscribers can register
for a single EventType or for all events.
"""

from __future__ import annotations

import asyncio
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.schemas import RiskLevel, utcnow


class EventType(StrEnum):
    """Spec §27 — the 16 canonical kernel events."""

    SIGNAL_CAPTURED = "signal.captured"
    OPPORTUNITY_CREATED = "opportunity.created"
    OPPORTUNITY_SCORED = "opportunity.scored"
    DECISION_CREATED = "decision.created"
    EXECUTION_PLANNED = "execution.planned"
    TRUST_CHECKED = "trust.checked"
    APPROVAL_REQUESTED = "approval.requested"
    APPROVAL_APPROVED = "approval.approved"
    APPROVAL_DENIED = "approval.denied"
    EXECUTION_COMPLETED = "execution.completed"
    OUTCOME_LOGGED = "outcome.logged"
    ASSET_CREATED = "asset.created"
    SCALE_RECOMMENDED = "scale.recommended"
    KILL_RECOMMENDED = "kill.recommended"
    TOOL_BLOCKED = "tool.blocked"
    AGENT_BLOCKED = "agent.blocked"
    RISK_DETECTED = "risk.detected"


def _new_event_id() -> str:
    return f"evt_{uuid4().hex}"


class Event(BaseModel):
    """The canonical kernel event envelope (spec §27 shape)."""

    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(default_factory=_new_event_id)
    event_type: EventType
    actor: str = Field(..., min_length=1, max_length=128)
    entity_type: str = Field(..., min_length=1, max_length=64)
    entity_id: str = Field(..., min_length=1, max_length=128)
    payload: dict[str, Any] = Field(default_factory=dict)
    risk_level: RiskLevel = RiskLevel.LOW
    sovereignty_level: str = Field(default="s0_autonomous", min_length=1, max_length=64)
    created_at: datetime = Field(default_factory=utcnow)


SyncHandler = Callable[[Event], None]
AsyncHandler = Callable[[Event], Awaitable[None]]
Handler = SyncHandler | AsyncHandler


# ─────────────────────────────────────────────────────────────
# EventBus
# ─────────────────────────────────────────────────────────────


class EventBus:
    """In-process pub/sub with a bounded recent-events buffer.

    Thread-safety: this bus is async-safe via an asyncio.Lock around
    publish/subscribe state mutations. Synchronous publish() is fine for
    fully sync callers because the lock is only entered inside async
    paths; the underlying lists are guarded by the GIL for the simple
    append/get patterns used here.
    """

    def __init__(self, recent_capacity: int = 1024) -> None:
        self._subscribers: dict[EventType, list[Handler]] = defaultdict(list)
        self._wildcard: list[Handler] = []
        self._recent: deque[Event] = deque(maxlen=recent_capacity)
        self._lock = asyncio.Lock()

    # ── subscription ───────────────────────────────────────────
    def subscribe(self, event_type: EventType, handler: Handler) -> None:
        if not callable(handler):
            raise TypeError("handler must be callable")
        self._subscribers[event_type].append(handler)

    def subscribe_all(self, handler: Handler) -> None:
        if not callable(handler):
            raise TypeError("handler must be callable")
        self._wildcard.append(handler)

    def unsubscribe(self, event_type: EventType, handler: Handler) -> bool:
        try:
            self._subscribers[event_type].remove(handler)
            return True
        except ValueError:
            return False

    # ── inspection ─────────────────────────────────────────────
    def recent(self, limit: int = 100) -> list[Event]:
        if limit <= 0:
            return []
        events = list(self._recent)
        return events[-limit:]

    def clear(self) -> None:
        self._recent.clear()

    # ── publish (sync) ─────────────────────────────────────────
    def publish(self, event: Event) -> None:
        """Synchronously fan-out to handlers. Async handlers are scheduled."""
        self._recent.append(event)
        for handler in list(self._subscribers.get(event.event_type, [])) + list(self._wildcard):
            self._dispatch(handler, event)

    async def apublish(self, event: Event) -> None:
        """Async fan-out with the lock held for ordering guarantees."""
        async with self._lock:
            self._recent.append(event)
            handlers = list(self._subscribers.get(event.event_type, [])) + list(self._wildcard)
        for handler in handlers:
            await self._adispatch(handler, event)

    @staticmethod
    def _dispatch(handler: Handler, event: Event) -> None:
        result = handler(event)
        if asyncio.iscoroutine(result):
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(result)
                else:
                    loop.run_until_complete(result)
            except RuntimeError:
                # No loop available — run a private one for one-shot dispatch.
                asyncio.run(result)

    @staticmethod
    async def _adispatch(handler: Handler, event: Event) -> None:
        result = handler(event)
        if asyncio.iscoroutine(result):
            await result


__all__ = [
    "Event",
    "EventBus",
    "EventType",
]
