"""
Sovereign Approval Center — §88.

Wraps every approval-bearing action (external_message, proposal,
pricing, tool_activation, mcp_server, sensitive_workflow, public_api,
marketplace_listing, enterprise_deal). Every state change is recorded
on the event bus.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dealix.sovereign_control_plane.events import EventBus, make_event
from dealix.sovereign_control_plane.types import (
    ApprovalDecision,
    RiskLevel,
    SovereigntyLevel,
)


_ALLOWED_ACTION_TYPES: frozenset[str] = frozenset({
    "external_message", "proposal", "pricing", "tool_activation",
    "mcp_server", "sensitive_workflow", "public_api",
    "marketplace_listing", "enterprise_deal",
})


@dataclass
class ApprovalRequest:
    approval_id: str
    requested_by: str
    workspace_id: str
    action_type: str
    sovereignty_level: SovereigntyLevel
    risk_level: RiskLevel
    summary: str
    payload_preview: dict[str, Any]
    trust_check: dict[str, Any]
    evidence_pack_id: str | None
    decision: ApprovalDecision
    created_at: str
    resolved_at: str | None = None
    notes: str | None = None
    approver_id: str | None = None
    audit_trail: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "approval_id": self.approval_id,
            "requested_by": self.requested_by,
            "workspace_id": self.workspace_id,
            "action_type": self.action_type,
            "sovereignty_level": self.sovereignty_level.value,
            "risk_level": self.risk_level.value,
            "summary": self.summary,
            "payload_preview": dict(self.payload_preview),
            "trust_check": dict(self.trust_check),
            "evidence_pack_id": self.evidence_pack_id,
            "decision": self.decision.value,
            "created_at": self.created_at,
            "resolved_at": self.resolved_at,
            "notes": self.notes,
            "approver_id": self.approver_id,
            "audit_trail": list(self.audit_trail),
        }


class SovereignApprovalCenter:
    def __init__(self, event_bus: EventBus) -> None:
        self._items: dict[str, ApprovalRequest] = {}
        self._lock = threading.Lock()
        self._bus = event_bus

    def submit(
        self,
        *,
        requested_by: str,
        workspace_id: str,
        action_type: str,
        sovereignty_level: SovereigntyLevel,
        risk_level: RiskLevel,
        summary: str,
        payload_preview: dict[str, Any] | None = None,
        trust_check: dict[str, Any] | None = None,
        evidence_pack_id: str | None = None,
    ) -> ApprovalRequest:
        if action_type not in _ALLOWED_ACTION_TYPES:
            raise ValueError(f"action_type '{action_type}' not allowed")
        req = ApprovalRequest(
            approval_id=f"apr_{uuid.uuid4().hex[:12]}",
            requested_by=requested_by,
            workspace_id=workspace_id,
            action_type=action_type,
            sovereignty_level=sovereignty_level,
            risk_level=risk_level,
            summary=summary,
            payload_preview=dict(payload_preview or {}),
            trust_check=dict(trust_check or {}),
            evidence_pack_id=evidence_pack_id,
            decision=ApprovalDecision.PENDING,
            created_at=datetime.now(UTC).isoformat(),
        )
        with self._lock:
            self._items[req.approval_id] = req
            self._audit(req, "submitted", requested_by)
        self._emit("approval.submitted", req)
        return req

    def approve(self, approval_id: str, approver_id: str) -> ApprovalRequest:
        req = self._transition(approval_id, ApprovalDecision.APPROVED, approver_id)
        self._emit("approval.approved", req)
        return req

    def deny(self, approval_id: str, approver_id: str, reason: str) -> ApprovalRequest:
        req = self._transition(
            approval_id, ApprovalDecision.DENIED, approver_id, notes=reason
        )
        self._emit("approval.denied", req)
        return req

    def request_changes(
        self, approval_id: str, approver_id: str, notes: str
    ) -> ApprovalRequest:
        req = self._transition(
            approval_id, ApprovalDecision.CHANGES_REQUESTED, approver_id, notes=notes
        )
        self._emit("approval.changes_requested", req)
        return req

    def escalate(self, approval_id: str, memo: str) -> ApprovalRequest:
        req = self._transition(
            approval_id, ApprovalDecision.ESCALATED, approver_id="system", notes=memo
        )
        self._emit("approval.escalated", req)
        return req

    def kill(self, approval_id: str) -> ApprovalRequest:
        req = self._transition(approval_id, ApprovalDecision.KILLED, approver_id="system")
        self._emit("approval.killed", req)
        return req

    def list_pending(self, workspace_id: str | None = None) -> list[ApprovalRequest]:
        items = [r for r in self._items.values() if r.decision == ApprovalDecision.PENDING]
        if workspace_id is not None:
            items = [r for r in items if r.workspace_id == workspace_id]
        return items

    def get(self, approval_id: str) -> ApprovalRequest | None:
        return self._items.get(approval_id)

    def _transition(
        self,
        approval_id: str,
        decision: ApprovalDecision,
        approver_id: str,
        notes: str | None = None,
    ) -> ApprovalRequest:
        with self._lock:
            req = self._items.get(approval_id)
            if req is None:
                raise KeyError(approval_id)
            if req.decision != ApprovalDecision.PENDING and decision != ApprovalDecision.KILLED:
                raise ValueError(f"approval {approval_id} already {req.decision.value}")
            req.decision = decision
            req.approver_id = approver_id
            req.notes = notes
            req.resolved_at = datetime.now(UTC).isoformat()
            self._audit(req, decision.value, approver_id, notes)
            return req

    @staticmethod
    def _audit(
        req: ApprovalRequest,
        action: str,
        actor_id: str,
        notes: str | None = None,
    ) -> None:
        req.audit_trail.append({
            "action": action,
            "actor_id": actor_id,
            "at": datetime.now(UTC).isoformat(),
            "notes": notes,
        })

    def _emit(self, event_type: str, req: ApprovalRequest) -> None:
        self._bus.publish(make_event(
            event_type=event_type,
            source="approval_center",
            payload=req.to_dict(),
            workspace_id=req.workspace_id,
            sensitivity="CONFIDENTIAL",
            sovereignty_level=req.sovereignty_level.value,
        ))
