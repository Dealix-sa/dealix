"""Outbound events — a lightweight in-process event bus for outbound lifecycle.

Events are emitted by the policy gate, approval queue, suppression list, and
provider stubs. Subscribers (audit, observability, future notification
handlers) register via ``subscribe`` and receive a dict per event.

This is deliberately synchronous and in-process. For cross-process delivery,
production deployments should bridge to a durable message bus (Redis Streams
/ SQS / Kafka), but the interface (``emit`` / ``subscribe``) stays the same.
"""

from __future__ import annotations

import time
import uuid
from threading import Lock
from typing import Any, Callable, Mapping

_LOCK = Lock()
_SUBSCRIBERS: "list[Callable[[dict[str, Any]], None]]" = []

# Well-known event type names.
EVENT_EVALUATION = "outbound.evaluation"
EVENT_APPROVAL_SUBMITTED = "outbound.approval.submitted"
EVENT_APPROVAL_APPROVED = "outbound.approval.approved"
EVENT_APPROVAL_REJECTED = "outbound.approval.rejected"
EVENT_SUPPRESSION_ADDED = "outbound.suppression.added"
EVENT_SUPPRESSION_REMOVED = "outbound.suppression.removed"
EVENT_PROVIDER_STUB_CALLED = "outbound.provider.stub_called"
EVENT_SEND_BLOCKED = "outbound.send.blocked"
EVENT_SEND_QUEUED = "outbound.send.queued"


def subscribe(handler: Callable[[dict[str, Any]], None]) -> Callable[[], None]:
    """Register a subscriber. Returns an unsubscribe function."""
    with _LOCK:
        _SUBSCRIBERS.append(handler)

    def _unsubscribe() -> None:
        with _LOCK:
            if handler in _SUBSCRIBERS:
                _SUBSCRIBERS.remove(handler)

    return _unsubscribe


def emit(event_type: str, payload: Mapping[str, Any] | None = None) -> str:
    """Emit an event to all subscribers. Returns the event id."""
    event_id = uuid.uuid4().hex
    event = {
        "id": event_id,
        "ts": time.time(),
        "type": event_type,
        "payload": dict(payload) if payload else {},
    }
    # Snapshot subscribers under the lock, then invoke outside the lock to
    # avoid re-entrancy/deadlock if a handler emits another event.
    with _LOCK:
        subs = list(_SUBSCRIBERS)
    for handler in subs:
        try:
            handler(event)
        except Exception:  # noqa: BLE001 — a misbehaving subscriber must not kill the bus
            pass
    return event_id


def clear_subscribers() -> None:
    """Remove all subscribers (used by tests)."""
    with _LOCK:
        _SUBSCRIBERS.clear()


def subscriber_count() -> int:
    """Return the number of registered subscribers."""
    with _LOCK:
        return len(_SUBSCRIBERS)