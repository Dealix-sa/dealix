"""
Audit Sink — append-only storage for AuditEntry.

Phase 0–1: InMemorySink + structured-log mirror.
Phase 2: PostgresSink with append-only table + monthly partition.

Wave 1 extends this module with:
  * AuditEvent / AuditLog — Hermes-shaped audit records
  * HermesAuditAdapter — bridges hermes EventBus → AuditSink
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from dealix.contracts.audit_log import AuditAction, AuditEntry

if TYPE_CHECKING:  # pragma: no cover - import-time only
    from dealix.hermes.events import Event, EventBus


def _utcnow() -> datetime:
    from datetime import UTC

    return datetime.now(UTC)


class AuditSink(ABC):
    """Abstract append-only audit sink."""

    @abstractmethod
    def append(self, entry: AuditEntry) -> None: ...

    @abstractmethod
    def recent(self, limit: int = 100) -> list[AuditEntry]: ...


class InMemoryAuditSink(AuditSink):
    """In-memory circular buffer — dev/test only."""

    def __init__(self, max_entries: int = 10_000) -> None:
        self._entries: list[AuditEntry] = []
        self._max = max_entries

    def append(self, entry: AuditEntry) -> None:
        self._entries.append(entry)
        if len(self._entries) > self._max:
            self._entries = self._entries[-self._max :]

    def recent(self, limit: int = 100) -> list[AuditEntry]:
        return self._entries[-limit:]

    def filter(
        self,
        *,
        entity_id: str | None = None,
        decision_id: str | None = None,
        action_contains: str | None = None,
    ) -> list[AuditEntry]:
        result = []
        for e in self._entries:
            if entity_id and e.entity_id != entity_id:
                continue
            if decision_id and e.decision_id != decision_id:
                continue
            if action_contains and action_contains not in e.action.value:
                continue
            result.append(e)
        return result


# ─────────────────────────────────────────────────────────────
# Hermes-shaped audit log (Wave 1)
# ─────────────────────────────────────────────────────────────


def _new_audit_event_id() -> str:
    return f"hau_{uuid4().hex}"


class AuditEvent(BaseModel):
    """Audit-side mirror of a Hermes event.

    Distinct from the legacy AuditEntry — those are tied to DecisionOutput
    and the older policy lane. This is the lightweight Hermes audit shape
    requested by the Wave 1 spec.
    """

    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(default_factory=_new_audit_event_id)
    actor: str = Field(..., min_length=1, max_length=128)
    action: str = Field(..., min_length=1, max_length=128)
    entity_ref: str = Field(..., min_length=1, max_length=200)
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None
    sovereignty_level: str = Field(default="s0_autonomous", min_length=1, max_length=64)
    created_at: datetime = Field(default_factory=_utcnow)


class AuditLog:
    """In-memory audit log with filterable query."""

    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def record(self, event: AuditEvent) -> AuditEvent:
        self._events.append(event)
        return event

    def query(
        self,
        *,
        actor: str | None = None,
        action_contains: str | None = None,
        entity_ref: str | None = None,
        min_sovereignty: str | None = None,
    ) -> list[AuditEvent]:
        result: list[AuditEvent] = []
        for e in self._events:
            if actor and e.actor != actor:
                continue
            if action_contains and action_contains not in e.action:
                continue
            if entity_ref and e.entity_ref != entity_ref:
                continue
            if min_sovereignty and e.sovereignty_level < min_sovereignty:
                continue
            result.append(e)
        return result

    def all(self) -> list[AuditEvent]:
        return list(self._events)


# ─────────────────────────────────────────────────────────────
# Bridge: Hermes EventBus → AuditSink
# ─────────────────────────────────────────────────────────────


# Map hermes EventType.value strings → legacy AuditAction
_HERMES_TO_AUDIT_ACTION: dict[str, AuditAction] = {
    "signal.captured": AuditAction.WORKFLOW_STARTED,
    "opportunity.created": AuditAction.WORKFLOW_STARTED,
    "opportunity.scored": AuditAction.WORKFLOW_STARTED,
    "decision.created": AuditAction.DECISION_EMITTED,
    "execution.planned": AuditAction.WORKFLOW_STARTED,
    "trust.checked": AuditAction.POLICY_EVALUATED,
    "approval.requested": AuditAction.APPROVAL_REQUESTED,
    "approval.approved": AuditAction.APPROVAL_GRANTED,
    "approval.denied": AuditAction.APPROVAL_REJECTED,
    "execution.completed": AuditAction.WORKFLOW_COMPLETED,
    "outcome.logged": AuditAction.WORKFLOW_COMPLETED,
    "asset.created": AuditAction.WORKFLOW_COMPLETED,
    "scale.recommended": AuditAction.WORKFLOW_COMPLETED,
    "kill.recommended": AuditAction.WORKFLOW_COMPLETED,
    "tool.blocked": AuditAction.TOOL_BLOCKED,
    "agent.blocked": AuditAction.ACCESS_DENIED,
    "risk.detected": AuditAction.POLICY_EVALUATED,
}


class HermesAuditAdapter:
    """Subscribes to a Hermes EventBus and mirrors events into AuditSink + AuditLog."""

    def __init__(
        self,
        sink: AuditSink,
        audit_log: AuditLog | None = None,
    ) -> None:
        self._sink = sink
        self._log = audit_log or AuditLog()

    @property
    def log(self) -> AuditLog:
        return self._log

    def attach(self, bus: EventBus) -> None:
        bus.subscribe_all(self.handle)

    def handle(self, event: Event) -> None:
        # 1. Mirror into the lightweight AuditLog
        self._log.record(
            AuditEvent(
                actor=event.actor,
                action=event.event_type.value,
                entity_ref=f"{event.entity_type}:{event.entity_id}",
                sovereignty_level=event.sovereignty_level,
                after=event.payload,
            )
        )
        # 2. Mirror into the legacy AuditSink as an AuditEntry
        legacy_action = _HERMES_TO_AUDIT_ACTION.get(
            event.event_type.value, AuditAction.WORKFLOW_STARTED
        )
        entry = AuditEntry(
            action=legacy_action,
            actor_type="agent" if event.actor != "system" else "system",
            actor_id=event.actor,
            entity_id=event.entity_id,
            event_id=event.event_id,
            outcome="ok",
            details={
                "event_type": event.event_type.value,
                "sovereignty_level": event.sovereignty_level,
                "risk_level": event.risk_level.value,
                "payload": event.payload,
            },
        )
        self._sink.append(entry)


__all__ = [
    "AuditEvent",
    "AuditLog",
    "AuditSink",
    "HermesAuditAdapter",
    "InMemoryAuditSink",
]
