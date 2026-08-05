"""
Section 59 — Approval Center.

The Approval Center is the safety valve. Every escalated policy result
materialises as an `ApprovalCard` here. The only legal way for an
external action to execute is via an approved card from a Sami-tier
identity (or an explicit delegate).
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from dealix.control_plane.identity_access import Identity, Permission
from dealix.control_plane.sovereignty import SovereigntyTier


class SovereigntyLevel(StrEnum):
    """The escalation rung an approval requires."""

    S0_AUTO = "S0_AUTO"
    S1_INTERNAL = "S1_INTERNAL"
    S2_SAMI_APPROVAL = "S2_SAMI_APPROVAL"
    S3_SOVEREIGN_MEMO = "S3_SOVEREIGN_MEMO"
    S4_LAUNCH_GATE = "S4_LAUNCH_GATE"


class ApprovalDecision(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    REQUEST_CHANGES = "request_changes"
    ESCALATED = "escalated_to_sovereign_memo"
    KILLED = "killed"


@dataclass
class ApprovalCard:
    approval_id: str
    requested_by: str
    action_type: str
    sovereignty_level: SovereigntyLevel
    risk_level: str
    summary: str
    payload_preview: dict[str, Any]
    trust_check: dict[str, Any] = field(default_factory=dict)
    evidence_pack_id: str | None = None
    decision: ApprovalDecision = ApprovalDecision.PENDING
    decided_by: str | None = None
    decided_at: datetime | None = None
    decision_note: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "approval_id": self.approval_id,
            "requested_by": self.requested_by,
            "action_type": self.action_type,
            "sovereignty_level": self.sovereignty_level.value,
            "risk_level": self.risk_level,
            "summary": self.summary,
            "payload_preview": dict(self.payload_preview),
            "trust_check": dict(self.trust_check),
            "evidence_pack_id": self.evidence_pack_id,
            "decision": self.decision.value,
            "decided_by": self.decided_by,
            "decided_at": self.decided_at.isoformat() if self.decided_at else None,
            "decision_note": self.decision_note,
            "created_at": self.created_at.isoformat(),
        }


_REQUIRED_TIER: dict[SovereigntyLevel, SovereigntyTier] = {
    SovereigntyLevel.S0_AUTO: SovereigntyTier.AGENT,
    SovereigntyLevel.S1_INTERNAL: SovereigntyTier.INTERNAL,
    SovereigntyLevel.S2_SAMI_APPROVAL: SovereigntyTier.SAMI,
    SovereigntyLevel.S3_SOVEREIGN_MEMO: SovereigntyTier.SAMI,
    SovereigntyLevel.S4_LAUNCH_GATE: SovereigntyTier.SAMI,
}


class ApprovalCenter:
    def __init__(self) -> None:
        self._cards: dict[str, ApprovalCard] = {}

    def request(
        self,
        *,
        requested_by: str,
        action_type: str,
        sovereignty_level: SovereigntyLevel,
        risk_level: str,
        summary: str,
        payload_preview: dict[str, Any] | None = None,
        trust_check: dict[str, Any] | None = None,
        evidence_pack_id: str | None = None,
    ) -> ApprovalCard:
        card = ApprovalCard(
            approval_id=f"appr_{uuid.uuid4().hex[:12]}",
            requested_by=requested_by,
            action_type=action_type,
            sovereignty_level=sovereignty_level,
            risk_level=risk_level,
            summary=summary,
            payload_preview=dict(payload_preview or {}),
            trust_check=dict(trust_check or {}),
            evidence_pack_id=evidence_pack_id,
        )
        self._cards[card.approval_id] = card
        return card

    def get(self, approval_id: str) -> ApprovalCard:
        try:
            return self._cards[approval_id]
        except KeyError as exc:
            raise KeyError(f"unknown approval: {approval_id}") from exc

    def pending(self) -> list[ApprovalCard]:
        return [c for c in self._cards.values() if c.decision is ApprovalDecision.PENDING]

    def all(self) -> list[ApprovalCard]:
        return list(self._cards.values())

    def decide(
        self,
        *,
        approval_id: str,
        actor: Identity,
        decision: ApprovalDecision,
        note: str | None = None,
    ) -> ApprovalCard:
        card = self.get(approval_id)
        if card.decision is not ApprovalDecision.PENDING:
            raise ValueError(f"approval {approval_id} already decided")
        if decision is ApprovalDecision.PENDING:
            raise ValueError("cannot decide as PENDING")

        required_tier = _REQUIRED_TIER[card.sovereignty_level]
        if not actor.tier.at_least(required_tier):
            raise PermissionError(
                f"actor {actor.identity_id} (tier {actor.tier.value}) cannot "
                f"decide approval at level {card.sovereignty_level.value}"
            )
        if card.sovereignty_level in (
            SovereigntyLevel.S2_SAMI_APPROVAL,
            SovereigntyLevel.S3_SOVEREIGN_MEMO,
            SovereigntyLevel.S4_LAUNCH_GATE,
        ):
            actor.require(Permission.APPROVE_EXTERNAL_ACTION)

        card.decision = decision
        card.decided_by = actor.identity_id
        card.decided_at = datetime.now(UTC)
        card.decision_note = note
        return card

    def approve(self, *, approval_id: str, actor: Identity, note: str | None = None) -> ApprovalCard:
        return self.decide(
            approval_id=approval_id, actor=actor, decision=ApprovalDecision.APPROVED, note=note
        )

    def deny(self, *, approval_id: str, actor: Identity, note: str | None = None) -> ApprovalCard:
        return self.decide(
            approval_id=approval_id, actor=actor, decision=ApprovalDecision.DENIED, note=note
        )

    def request_changes(
        self, *, approval_id: str, actor: Identity, note: str | None = None
    ) -> ApprovalCard:
        return self.decide(
            approval_id=approval_id,
            actor=actor,
            decision=ApprovalDecision.REQUEST_CHANGES,
            note=note,
        )

    def escalate(self, *, approval_id: str, actor: Identity, note: str | None = None) -> ApprovalCard:
        return self.decide(
            approval_id=approval_id,
            actor=actor,
            decision=ApprovalDecision.ESCALATED,
            note=note,
        )

    def kill(self, *, approval_id: str, actor: Identity, note: str | None = None) -> ApprovalCard:
        return self.decide(
            approval_id=approval_id, actor=actor, decision=ApprovalDecision.KILLED, note=note
        )

    def stamps_for(self, action_type: str) -> Iterable[ApprovalCard]:
        for card in self._cards.values():
            if card.action_type == action_type and card.decision is ApprovalDecision.APPROVED:
                yield card
