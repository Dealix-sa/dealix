"""
ApprovalGate — pauses execution until a sovereign actor (Sami) authorizes
the proposed action.

Approvals are stored in an in-memory queue here; in production this is
backed by the existing ``dealix.governance.approvals`` durable store.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from dealix.hermes.control_plane.request_context import RequestContext
from dealix.hermes.control_plane.sovereignty_gate import (
    SovereigntyDecision,
    SovereigntyLevel,
)


class ApprovalStatus(StrEnum):
    NOT_REQUIRED = "not_required"
    PENDING = "pending"
    GRANTED = "granted"
    REJECTED = "rejected"


@dataclass
class ApprovalTicket:
    ticket_id: str
    request_id: str
    capability: str
    sovereignty: SovereigntyLevel
    reason: str
    status: ApprovalStatus
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    resolved_at: datetime | None = None
    resolved_by: str | None = None
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "ticket_id": self.ticket_id,
            "request_id": self.request_id,
            "capability": self.capability,
            "sovereignty": self.sovereignty.value,
            "reason": self.reason,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "resolved_by": self.resolved_by,
            "notes": self.notes,
        }


class ApprovalCenter:
    def __init__(self) -> None:
        self._tickets: dict[str, ApprovalTicket] = {}

    def open(
        self,
        context: RequestContext,
        sovereignty: SovereigntyDecision,
    ) -> ApprovalTicket:
        ticket = ApprovalTicket(
            ticket_id=f"appr_{uuid.uuid4().hex[:10]}",
            request_id=context.request_id,
            capability=context.capability,
            sovereignty=sovereignty.level,
            reason=sovereignty.reason,
            status=ApprovalStatus.PENDING,
        )
        self._tickets[ticket.ticket_id] = ticket
        return ticket

    def grant(self, ticket_id: str, by: str, notes: str = "") -> ApprovalTicket:
        ticket = self._tickets[ticket_id]
        ticket.status = ApprovalStatus.GRANTED
        ticket.resolved_at = datetime.now(UTC)
        ticket.resolved_by = by
        ticket.notes = notes
        return ticket

    def reject(self, ticket_id: str, by: str, notes: str = "") -> ApprovalTicket:
        ticket = self._tickets[ticket_id]
        ticket.status = ApprovalStatus.REJECTED
        ticket.resolved_at = datetime.now(UTC)
        ticket.resolved_by = by
        ticket.notes = notes
        return ticket

    def pending(self) -> list[ApprovalTicket]:
        return [t for t in self._tickets.values() if t.status == ApprovalStatus.PENDING]

    def get(self, ticket_id: str) -> ApprovalTicket | None:
        return self._tickets.get(ticket_id)


CENTER = ApprovalCenter()


def evaluate(
    context: RequestContext, sovereignty: SovereigntyDecision
) -> tuple[ApprovalStatus, ApprovalTicket | None]:
    if not sovereignty.requires_sami:
        return ApprovalStatus.NOT_REQUIRED, None
    ticket = CENTER.open(context, sovereignty)
    return ApprovalStatus.PENDING, ticket
