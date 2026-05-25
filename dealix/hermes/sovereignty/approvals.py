"""Approval Center — Sami's queue of pending sovereign decisions."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.sovereignty.levels import SovereigntyLevel, is_never_autonomous


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _aid() -> str:
    return f"appr_{uuid.uuid4().hex[:16]}"


class ApprovalState(StrEnum):
    pending = "pending"
    approved = "approved"
    denied = "denied"
    expired = "expired"


class ApprovalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    approval_id: str = Field(default_factory=_aid)
    subject_id: str  # decision_id or execution_id
    subject_type: str  # "decision" | "execution"
    title: str
    summary: str
    sovereignty_level: SovereigntyLevel
    required_approvers: int = 1
    state: ApprovalState = ApprovalState.pending
    requested_by: str = "system"
    approved_by: list[str] = Field(default_factory=list)
    denied_by: str | None = None
    deny_reason: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=_now)
    decided_at: str | None = None


@dataclass
class ApprovalCenter:
    """In-memory approval queue; production swaps for hermes_approvals."""

    _requests: dict[str, ApprovalRequest] = field(default_factory=dict)

    def open(
        self,
        *,
        subject_id: str,
        subject_type: str,
        title: str,
        summary: str,
        sovereignty_level: SovereigntyLevel,
        requested_by: str = "system",
        payload: dict | None = None,
    ) -> ApprovalRequest:
        required = 2 if is_never_autonomous(sovereignty_level) else 1
        req = ApprovalRequest(
            subject_id=subject_id,
            subject_type=subject_type,
            title=title,
            summary=summary,
            sovereignty_level=sovereignty_level,
            required_approvers=required,
            requested_by=requested_by,
            payload=payload or {},
        )
        self._requests[req.approval_id] = req
        return req

    def approve(self, approval_id: str, approver: str = "Sami") -> ApprovalRequest:
        req = self._requests[approval_id]
        if req.state != ApprovalState.pending:
            return req
        approvers = [*req.approved_by, approver] if approver not in req.approved_by else req.approved_by
        state = ApprovalState.approved if len(approvers) >= req.required_approvers else ApprovalState.pending
        updated = req.model_copy(update={
            "approved_by": approvers,
            "state": state,
            "decided_at": _now() if state == ApprovalState.approved else None,
        })
        self._requests[approval_id] = updated
        return updated

    def deny(self, approval_id: str, denier: str = "Sami", reason: str = "") -> ApprovalRequest:
        req = self._requests[approval_id]
        updated = req.model_copy(update={
            "state": ApprovalState.denied,
            "denied_by": denier,
            "deny_reason": reason,
            "decided_at": _now(),
        })
        self._requests[approval_id] = updated
        return updated

    def get(self, approval_id: str) -> ApprovalRequest:
        return self._requests[approval_id]

    def pending(self) -> list[ApprovalRequest]:
        return [r for r in self._requests.values() if r.state == ApprovalState.pending]

    def list(self) -> list[ApprovalRequest]:
        return list(self._requests.values())
