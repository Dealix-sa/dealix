"""Approval Center — workflow for any S2/S3 / requires_approval call.

Approval is a first-class object so it can be queried, audited, and
expired. The center never sends external messages; it queues drafts.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any


class ApprovalState(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass
class ApprovalRequest:
    id: str
    requested_by: str
    action: str
    payload: dict[str, Any]
    state: ApprovalState = ApprovalState.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime | None = None
    decided_by: str | None = None
    decided_at: datetime | None = None
    decision_note: str = ""


@dataclass
class ApprovalCenter:
    default_ttl: timedelta = timedelta(hours=48)
    sovereign_approver: str = "sami"
    _requests: dict[str, ApprovalRequest] = field(default_factory=dict)

    def request(
        self,
        *,
        requested_by: str,
        action: str,
        payload: dict[str, Any] | None = None,
        ttl: timedelta | None = None,
    ) -> ApprovalRequest:
        req = ApprovalRequest(
            id=f"apv_{uuid.uuid4().hex[:10]}",
            requested_by=requested_by,
            action=action,
            payload=payload or {},
            expires_at=datetime.now(timezone.utc) + (ttl or self.default_ttl),
        )
        self._requests[req.id] = req
        return req

    def approve(self, request_id: str, *, by: str | None = None, note: str = "") -> ApprovalRequest:
        approver = by or self.sovereign_approver
        if approver != self.sovereign_approver:
            raise PermissionError(f"Only '{self.sovereign_approver}' may approve.")
        req = self._requests[request_id]
        self._check_alive(req)
        req.state = ApprovalState.APPROVED
        req.decided_by = approver
        req.decided_at = datetime.now(timezone.utc)
        req.decision_note = note
        return req

    def reject(self, request_id: str, *, by: str | None = None, note: str = "") -> ApprovalRequest:
        approver = by or self.sovereign_approver
        if approver != self.sovereign_approver:
            raise PermissionError(f"Only '{self.sovereign_approver}' may reject.")
        req = self._requests[request_id]
        self._check_alive(req)
        req.state = ApprovalState.REJECTED
        req.decided_by = approver
        req.decided_at = datetime.now(timezone.utc)
        req.decision_note = note
        return req

    def expire_due(self) -> list[ApprovalRequest]:
        now = datetime.now(timezone.utc)
        expired: list[ApprovalRequest] = []
        for req in self._requests.values():
            if req.state == ApprovalState.PENDING and req.expires_at and req.expires_at <= now:
                req.state = ApprovalState.EXPIRED
                expired.append(req)
        return expired

    def pending(self) -> list[ApprovalRequest]:
        return [r for r in self._requests.values() if r.state == ApprovalState.PENDING]

    def get(self, request_id: str) -> ApprovalRequest:
        return self._requests[request_id]

    def all(self) -> list[ApprovalRequest]:
        return list(self._requests.values())

    def _check_alive(self, req: ApprovalRequest) -> None:
        if req.state != ApprovalState.PENDING:
            raise ValueError(f"Approval {req.id} is already {req.state.value}.")
        if req.expires_at and req.expires_at <= datetime.now(timezone.utc):
            req.state = ApprovalState.EXPIRED
            raise ValueError(f"Approval {req.id} has expired.")


__all__ = ["ApprovalCenter", "ApprovalRequest", "ApprovalState"]
