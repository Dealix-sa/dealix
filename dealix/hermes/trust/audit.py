"""Append-only audit log of every Trust Gateway decision."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class AuditEvent:
    timestamp: datetime
    actor: str
    action: str
    target: str
    verdict: str            # allow|deny|approve|reject|...
    detail: dict[str, Any]


@dataclass
class AuditLog:
    _events: list[AuditEvent] = field(default_factory=list)

    def record(
        self,
        *,
        actor: str,
        action: str,
        target: str,
        verdict: str,
        detail: dict[str, Any] | None = None,
    ) -> AuditEvent:
        event = AuditEvent(
            timestamp=datetime.now(timezone.utc),
            actor=actor,
            action=action,
            target=target,
            verdict=verdict,
            detail=detail or {},
        )
        self._events.append(event)
        return event

    def all(self) -> list[AuditEvent]:
        return list(self._events)

    def latest(self, n: int = 100) -> list[AuditEvent]:
        return list(self._events[-n:])

    def by_actor(self, actor: str) -> list[AuditEvent]:
        return [e for e in self._events if e.actor == actor]

    def denials(self) -> list[AuditEvent]:
        return [e for e in self._events if e.verdict in {"deny", "reject", "blocked"}]


__all__ = ["AuditEvent", "AuditLog"]
