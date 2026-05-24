"""Approval queue for Hermes.

This wraps a lightweight in-memory queue suitable for tests and the
standalone Hermes API. In production, plug `dealix.governance.approvals`
(Redis-backed) in as the `external_queue` callback so that the existing
admin approval flow continues to drive Hermes too.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any
from uuid import uuid4

from dealix.hermes.sovereignty import Action, GateDecision, SovereigntyLevel


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    GRANTED = "granted"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass(slots=True)
class ApprovalRequest:
    request_id: str
    action: Action
    decision: GateDecision
    status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    decided_at: datetime | None = None
    approver: str | None = None
    note: str = ""
    expires_at: datetime = field(
        default_factory=lambda: datetime.now(UTC) + timedelta(hours=24)
    )


class ApprovalCenter:
    def __init__(
        self,
        *,
        external_queue: Callable[[ApprovalRequest], None] | None = None,
    ) -> None:
        self._requests: dict[str, ApprovalRequest] = {}
        self._external = external_queue

    def enqueue(self, action: Action, decision: GateDecision) -> ApprovalRequest:
        req = ApprovalRequest(
            request_id=str(uuid4()),
            action=action,
            decision=decision,
        )
        self._requests[req.request_id] = req
        if self._external is not None:
            self._external(req)
        return req

    def decide(
        self,
        request_id: str,
        *,
        granted: bool,
        approver: str,
        note: str = "",
    ) -> ApprovalRequest:
        req = self._requests.get(request_id)
        if req is None:
            raise KeyError(request_id)
        if req.status is not ApprovalStatus.PENDING:
            return req
        if datetime.now(UTC) >= req.expires_at:
            req.status = ApprovalStatus.EXPIRED
            return req
        req.status = ApprovalStatus.GRANTED if granted else ApprovalStatus.REJECTED
        req.approver = approver
        req.note = note
        req.decided_at = datetime.now(UTC)
        return req

    def sweep_expired(self) -> int:
        now = datetime.now(UTC)
        expired = 0
        for req in self._requests.values():
            if req.status is ApprovalStatus.PENDING and now >= req.expires_at:
                req.status = ApprovalStatus.EXPIRED
                expired += 1
        return expired

    def pending(self) -> list[ApprovalRequest]:
        self.sweep_expired()
        return [
            r for r in self._requests.values() if r.status is ApprovalStatus.PENDING
        ]

    def get(self, request_id: str) -> ApprovalRequest | None:
        return self._requests.get(request_id)

    def all(self) -> list[ApprovalRequest]:
        return list(self._requests.values())


__all__ = ["ApprovalCenter", "ApprovalRequest", "ApprovalStatus"]
