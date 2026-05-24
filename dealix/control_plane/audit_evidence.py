"""
Section 60 — Audit & Evidence.

Every meaningful event leaves an `AuditEvent`. Eight triggers create a
full `EvidencePack` — the immutable record that ships with enterprise
proposals, MCP reviews, partner agreements, etc.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from dealix.control_plane.approval_center import SovereigntyLevel


class EvidenceTrigger(StrEnum):
    ENTERPRISE_PROPOSAL = "enterprise_proposal"
    AI_TRUST_KIT = "ai_trust_kit"
    MCP_REVIEW = "mcp_review"
    PARTNER_AGREEMENT = "partner_agreement"
    NEW_VERTICAL = "new_vertical"
    PUBLIC_API = "public_api"
    MARKETPLACE = "marketplace"
    SENSITIVE_DATA_WORKFLOW = "sensitive_data_workflow"


@dataclass(frozen=True)
class AuditEvent:
    audit_id: str
    actor_type: str
    actor_id: str
    action_type: str
    risk_level: str
    sovereignty_level: SovereigntyLevel
    result: str
    tool_id: str | None = None
    workspace_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "actor_type": self.actor_type,
            "actor_id": self.actor_id,
            "action_type": self.action_type,
            "tool_id": self.tool_id,
            "risk_level": self.risk_level,
            "sovereignty_level": self.sovereignty_level.value,
            "result": self.result,
            "workspace_id": self.workspace_id,
            "metadata": dict(self.metadata),
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class EvidencePack:
    pack_id: str
    trigger: EvidenceTrigger
    decision: dict[str, Any]
    context: dict[str, Any] = field(default_factory=dict)
    signals: list[dict[str, Any]] = field(default_factory=list)
    opportunity_score: dict[str, Any] | None = None
    alternatives: list[dict[str, Any]] = field(default_factory=list)
    risks: list[dict[str, Any]] = field(default_factory=list)
    policies_applied: list[dict[str, Any]] = field(default_factory=list)
    trust_checks: list[dict[str, Any]] = field(default_factory=list)
    approvals: list[dict[str, Any]] = field(default_factory=list)
    recommended_action: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "pack_id": self.pack_id,
            "trigger": self.trigger.value,
            "decision": dict(self.decision),
            "context": dict(self.context),
            "signals": list(self.signals),
            "opportunity_score": self.opportunity_score,
            "alternatives": list(self.alternatives),
            "risks": list(self.risks),
            "policies_applied": list(self.policies_applied),
            "trust_checks": list(self.trust_checks),
            "approvals": list(self.approvals),
            "recommended_action": self.recommended_action,
            "created_at": self.created_at.isoformat(),
        }


class AuditLog:
    def __init__(self) -> None:
        self._events: list[AuditEvent] = []
        self._packs: dict[str, EvidencePack] = {}

    def record(
        self,
        *,
        actor_type: str,
        actor_id: str,
        action_type: str,
        risk_level: str = "low",
        sovereignty_level: SovereigntyLevel = SovereigntyLevel.S0_AUTO,
        result: str = "ok",
        tool_id: str | None = None,
        workspace_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AuditEvent:
        event = AuditEvent(
            audit_id=f"aud_{uuid.uuid4().hex[:12]}",
            actor_type=actor_type,
            actor_id=actor_id,
            action_type=action_type,
            risk_level=risk_level,
            sovereignty_level=sovereignty_level,
            result=result,
            tool_id=tool_id,
            workspace_id=workspace_id,
            metadata=dict(metadata or {}),
        )
        self._events.append(event)
        return event

    def events(
        self,
        *,
        actor_id: str | None = None,
        action_type: str | None = None,
        workspace_id: str | None = None,
    ) -> list[AuditEvent]:
        events: Iterable[AuditEvent] = self._events
        if actor_id is not None:
            events = (e for e in events if e.actor_id == actor_id)
        if action_type is not None:
            events = (e for e in events if e.action_type == action_type)
        if workspace_id is not None:
            events = (e for e in events if e.workspace_id == workspace_id)
        return list(events)

    def open_pack(
        self,
        *,
        trigger: EvidenceTrigger,
        decision: dict[str, Any],
        context: dict[str, Any] | None = None,
        recommended_action: str | None = None,
    ) -> EvidencePack:
        pack = EvidencePack(
            pack_id=f"ev_{uuid.uuid4().hex[:12]}",
            trigger=trigger,
            decision=dict(decision),
            context=dict(context or {}),
            recommended_action=recommended_action,
        )
        self._packs[pack.pack_id] = pack
        return pack

    def get_pack(self, pack_id: str) -> EvidencePack:
        try:
            return self._packs[pack_id]
        except KeyError as exc:
            raise KeyError(f"unknown evidence pack: {pack_id}") from exc

    def packs(self) -> list[EvidencePack]:
        return list(self._packs.values())
