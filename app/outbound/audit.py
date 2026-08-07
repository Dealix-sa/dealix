"""Audit log for outbound safety decisions.

Records every policy-gate evaluation, approval action, suppression change,
and provider stub invocation. The log is in-memory and bounded; production
deployments should ship this to a durable store (Postgres/S3/OTLP), but the
interface (``record`` / ``query`` / ``recent``) stays the same.

Audit entries are append-only; ``clear_audit`` exists only for tests.
"""

from __future__ import annotations

import time
import uuid
from collections import deque
from threading import Lock
from typing import Any, Mapping

_LOCK = Lock()
_MAX_ENTRIES = 10_000
_LOG: "deque[dict[str, Any]]" = deque(maxlen=_MAX_ENTRIES)


def record(
    event_type: str,
    channel: str | None = None,
    identifier: str | None = None,
    allowed: bool | None = None,
    reason: str | None = None,
    extra: Mapping[str, Any] | None = None,
) -> str:
    """Record an audit entry. Returns the entry id."""
    entry_id = uuid.uuid4().hex
    entry: dict[str, Any] = {
        "id": entry_id,
        "ts": time.time(),
        "event_type": event_type,
        "channel": channel,
        "identifier": identifier,
        "allowed": allowed,
        "reason": reason,
        "extra": dict(extra) if extra else {},
    }
    with _LOCK:
        _LOG.append(entry)
    return entry_id


def record_evaluation(evaluation: Mapping[str, Any]) -> str:
    """Record a SendEvaluation.to_dict() result."""
    return record(
        event_type="policy_evaluation",
        channel=evaluation.get("channel"),
        identifier=_identifier_from_contact(evaluation.get("contact", {}), evaluation.get("channel")),
        allowed=evaluation.get("allowed"),
        reason=evaluation.get("reason"),
        extra={
            "safe_to_send": evaluation.get("safe_to_send"),
            "mode": evaluation.get("mode"),
            "reasons": evaluation.get("reasons", []),
        },
    )


def _identifier_from_contact(contact: Mapping[str, Any], channel: str | None) -> str | None:
    if not channel or not contact:
        return None
    if channel == "email":
        return str(contact.get("email", "")).lower() or None
    if channel == "whatsapp":
        return str(contact.get("whatsapp", "")).lower() or None
    if channel == "sms":
        return str(contact.get("phone", "")).lower() or None
    return None


def recent(limit: int = 100) -> list[dict[str, Any]]:
    """Return the most recent audit entries (oldest first within the slice)."""
    with _LOCK:
        items = list(_LOG)
    return items[-limit:]


def query(
    event_type: str | None = None,
    channel: str | None = None,
    identifier: str | None = None,
    allowed: bool | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Query audit entries by filter. Returns matching entries (newest first)."""
    with _LOCK:
        items = list(_LOG)
    results: list[dict[str, Any]] = []
    for entry in reversed(items):
        if event_type is not None and entry.get("event_type") != event_type:
            continue
        if channel is not None and entry.get("channel") != channel:
            continue
        if identifier is not None and entry.get("identifier") != identifier.lower():
            continue
        if allowed is not None and entry.get("allowed") != allowed:
            continue
        results.append(entry)
        if len(results) >= limit:
            break
    return results


def clear_audit() -> None:
    """Clear all audit entries (used by tests)."""
    with _LOCK:
        _LOG.clear()


def count() -> int:
    """Return the total number of audit entries."""
    with _LOCK:
        return len(_LOG)