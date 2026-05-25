"""
Approval Gate — يحوّل الأفعال الحساسة إلى approval ticket ويُعلِّق التنفيذ
لحين قرار بشري. يلتزم بـ default-deny: لو ما في قرار صريح خلال TTL، يتحوّل
الطلب إلى `EXPIRED` (لا يُنفّذ تلقائيًا).

يخزّن في الذاكرة بشكل افتراضي. يُستبدل لاحقًا بـ Postgres-backed store
(يربط بجدول `hermes_approvals` في migration 002).
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from typing import Any, Protocol

from ..contracts import ContextPacket, SovereigntyLevel


PENDING_TTL = timedelta(hours=24)


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass
class ApprovalTicket:
    ticket_id: str
    request_id: str
    intent: str
    sovereignty_level: SovereigntyLevel
    approver_role: str  # "founder" | "legal" | "board"
    summary: dict[str, Any]
    status: ApprovalStatus = ApprovalStatus.PENDING
    decided_by: str | None = None
    decided_at: datetime | None = None
    decision_note: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc) + PENDING_TTL
    )

    def is_expired(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return self.status == ApprovalStatus.PENDING and now >= self.expires_at


class ApprovalStore(Protocol):
    def save(self, ticket: ApprovalTicket) -> None: ...
    def get(self, ticket_id: str) -> ApprovalTicket | None: ...
    def list_pending(self) -> list[ApprovalTicket]: ...


class InMemoryApprovalStore:
    def __init__(self) -> None:
        self._tickets: dict[str, ApprovalTicket] = {}
        self._lock = threading.Lock()

    def save(self, ticket: ApprovalTicket) -> None:
        with self._lock:
            self._tickets[ticket.ticket_id] = ticket

    def get(self, ticket_id: str) -> ApprovalTicket | None:
        with self._lock:
            return self._tickets.get(ticket_id)

    def list_pending(self) -> list[ApprovalTicket]:
        with self._lock:
            return [t for t in self._tickets.values() if not t.is_expired() and t.status == ApprovalStatus.PENDING]


_APPROVER_BY_LEVEL: dict[SovereigntyLevel, str] = {
    SovereigntyLevel.S2_SAMI_APPROVAL: "founder",
    SovereigntyLevel.S3_LEGAL_APPROVAL: "legal",
    SovereigntyLevel.S4_BOARD_APPROVAL: "board",
}


class ApprovalGate:
    STAGE = "gate.approval"

    def __init__(self, store: ApprovalStore | None = None) -> None:
        self._store: ApprovalStore = store or InMemoryApprovalStore()

    def open_ticket(
        self,
        *,
        context: ContextPacket,
        intent: str,
        sovereignty_level: SovereigntyLevel,
        summary: dict[str, Any],
    ) -> ApprovalTicket:
        approver = _APPROVER_BY_LEVEL.get(sovereignty_level, "founder")
        ticket = ApprovalTicket(
            ticket_id=f"apr_{uuid.uuid4().hex[:16]}",
            request_id=context.request_id,
            intent=intent,
            sovereignty_level=sovereignty_level,
            approver_role=approver,
            summary=summary,
        )
        self._store.save(ticket)
        return ticket

    def decide(
        self,
        ticket_id: str,
        *,
        decided_by: str,
        approve: bool,
        note: str | None = None,
    ) -> ApprovalTicket:
        ticket = self._store.get(ticket_id)
        if ticket is None:
            raise KeyError(ticket_id)
        if ticket.is_expired():
            ticket.status = ApprovalStatus.EXPIRED
            self._store.save(ticket)
            return ticket
        if ticket.status != ApprovalStatus.PENDING:
            return ticket
        ticket.status = ApprovalStatus.APPROVED if approve else ApprovalStatus.REJECTED
        ticket.decided_by = decided_by
        ticket.decided_at = datetime.now(timezone.utc)
        ticket.decision_note = note
        self._store.save(ticket)
        return ticket

    def get(self, ticket_id: str) -> ApprovalTicket | None:
        ticket = self._store.get(ticket_id)
        if ticket and ticket.is_expired():
            ticket.status = ApprovalStatus.EXPIRED
            self._store.save(ticket)
        return ticket

    def list_pending(self) -> list[ApprovalTicket]:
        return self._store.list_pending()


__all__ = [
    "ApprovalGate",
    "ApprovalStatus",
    "ApprovalStore",
    "ApprovalTicket",
    "InMemoryApprovalStore",
    "PENDING_TTL",
]
