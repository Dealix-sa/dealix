"""خادم الثقة — approval queue for Hermes (S2+).

Wraps an in-memory queue around the Hermes sovereignty model. Tickets
carry the sovereignty level, evidence-pack reference, expiry, and a
state machine: PENDING → APPROVED | DENIED | EXPIRED.

This module is intentionally decoupled from the older
`dealix.trust.approval.ApprovalCenter` (which is bound to DecisionOutput
in `dealix/contracts/decision.py`). We reuse the ApprovalStatus enum
where convenient so callers can interoperate.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from enum import StrEnum
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from dealix.hermes.core.schemas import utcnow
from dealix.hermes.sovereignty import SovereigntyLevel
from dealix.trust._jsonl_store import JsonlStore
from dealix.trust.approval import ApprovalStatus as LegacyApprovalStatus


class TicketStatus(StrEnum):
    """Distinct from legacy ApprovalStatus to keep Hermes self-contained."""

    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"
    WITHDRAWN = "withdrawn"

    @classmethod
    def from_legacy(cls, legacy: LegacyApprovalStatus) -> TicketStatus:
        mapping = {
            LegacyApprovalStatus.PENDING: cls.PENDING,
            LegacyApprovalStatus.GRANTED: cls.APPROVED,
            LegacyApprovalStatus.REJECTED: cls.DENIED,
            LegacyApprovalStatus.TIMED_OUT: cls.EXPIRED,
            LegacyApprovalStatus.WITHDRAWN: cls.WITHDRAWN,
        }
        return mapping[legacy]


def _new_ticket_id() -> str:
    return f"tkt_{uuid4().hex}"


class ApprovalTicket(BaseModel):
    """An approval ticket sitting in the queue."""

    model_config = ConfigDict(extra="forbid")

    ticket_id: str = Field(default_factory=_new_ticket_id)
    decision_id: str = Field(..., min_length=1)
    plan_id: str | None = None
    summary: str = Field(..., min_length=1, max_length=600)
    sovereignty_level: SovereigntyLevel
    evidence_pack_ref: str | None = None
    status: TicketStatus = TicketStatus.PENDING
    requested_by: str = "hermes"
    decided_by: str | None = None
    decision_note: str | None = None
    created_at: datetime = Field(default_factory=utcnow)
    expires_at: datetime = Field(
        default_factory=lambda: utcnow() + timedelta(hours=48)
    )
    decided_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("expires_at")
    @classmethod
    def _expires_in_future(cls, value: datetime) -> datetime:
        if value < utcnow() - timedelta(seconds=5):
            raise ValueError("expires_at must be in the future")
        return value

    @property
    def is_terminal(self) -> bool:
        return self.status != TicketStatus.PENDING

    def is_expired(self, now: datetime | None = None) -> bool:
        return (now or utcnow()) > self.expires_at


# ─────────────────────────────────────────────────────────────
# Queue
# ─────────────────────────────────────────────────────────────


class ApprovalQueue:
    """In-memory approval queue (optionally JSONL-backed).

    Behaviour with `persist_path=None` is unchanged. With a path supplied,
    every mutation appends to that file and `__init__` rehydrates from it.
    If the directory cannot be created (e.g. read-only filesystem) the
    queue silently falls back to pure in-memory state.
    """

    def __init__(self, persist_path: Path | str | None = None) -> None:
        self._tickets: dict[str, ApprovalTicket] = {}
        self._store: JsonlStore | None = None
        if persist_path is not None:
            store = JsonlStore(persist_path)
            if store.ensure_parent():
                self._store = store
                self._rehydrate()

    def _rehydrate(self) -> None:
        if self._store is None:
            return
        for record in self._store.load_all():
            try:
                ticket = ApprovalTicket.model_validate(record)
            except Exception:
                # Corrupt record — skip silently; never block boot.
                continue
            self._tickets[ticket.ticket_id] = ticket

    def _flush(self) -> None:
        if self._store is None:
            return
        records = [t.model_dump(mode="json") for t in self._tickets.values()]
        try:
            self._store.replace_all(records)
        except OSError:
            # FS went read-only mid-flight — degrade to in-memory only.
            self._store = None

    def submit(self, ticket: ApprovalTicket) -> str:
        if ticket.ticket_id in self._tickets:
            raise ValueError(f"duplicate ticket_id: {ticket.ticket_id}")
        self._tickets[ticket.ticket_id] = ticket
        if self._store is not None:
            try:
                self._store.append(ticket.model_dump(mode="json"))
            except OSError:
                self._store = None
        return ticket.ticket_id

    def get(self, ticket_id: str) -> ApprovalTicket:
        try:
            return self._tickets[ticket_id]
        except KeyError as exc:
            raise KeyError(f"unknown ticket: {ticket_id}") from exc

    def pending(self) -> list[ApprovalTicket]:
        swept = self._sweep_expired()
        if swept:
            self._flush()
        return [t for t in self._tickets.values() if t.status == TicketStatus.PENDING]

    def approve(self, ticket_id: str, by: str, note: str | None = None) -> ApprovalTicket:
        ticket = self.get(ticket_id)
        if ticket.is_terminal:
            return ticket
        if ticket.is_expired():
            ticket.status = TicketStatus.EXPIRED
            ticket.decided_at = utcnow()
            self._flush()
            return ticket
        ticket.status = TicketStatus.APPROVED
        ticket.decided_by = by
        ticket.decision_note = note
        ticket.decided_at = utcnow()
        self._tickets[ticket_id] = ticket
        self._flush()
        return ticket

    def deny(self, ticket_id: str, by: str, reason: str) -> ApprovalTicket:
        ticket = self.get(ticket_id)
        if ticket.is_terminal:
            return ticket
        ticket.status = TicketStatus.DENIED
        ticket.decided_by = by
        ticket.decision_note = reason
        ticket.decided_at = utcnow()
        self._tickets[ticket_id] = ticket
        self._flush()
        return ticket

    def withdraw(self, ticket_id: str) -> ApprovalTicket:
        ticket = self.get(ticket_id)
        if ticket.is_terminal:
            return ticket
        ticket.status = TicketStatus.WITHDRAWN
        ticket.decided_at = utcnow()
        self._flush()
        return ticket

    def _sweep_expired(self) -> bool:
        now = utcnow()
        swept = False
        for ticket in self._tickets.values():
            if ticket.status == TicketStatus.PENDING and ticket.is_expired(now):
                ticket.status = TicketStatus.EXPIRED
                ticket.decided_at = now
                swept = True
        return swept


__all__ = [
    "ApprovalQueue",
    "ApprovalTicket",
    "TicketStatus",
]
