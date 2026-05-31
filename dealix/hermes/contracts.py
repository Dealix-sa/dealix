"""
Hermes contracts — العقود المشتركة بين كل الطبقات.

كل request يدخل Hermes يُحوَّل إلى `ContextPacket` ويخرج عبر `HermesResponse`
بنفس الشكل في كل مكان (API، Agents، Workflows). هذا يضمن أن:

    - الـ UI تستهلك شكلًا واحدًا.
    - الـ Trust Gate يعرف الـ claims بالضبط.
    - الـ Audit Gate يسجّل تتبعًا موحّدًا.
    - الـ Approval Gate يحوّل أي فعل حساس بنفس الواجهة.

لا تستورد هذا الملف من شيء خارج `dealix/hermes/`.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Literal


# ────────────────────────────────────────────────────────────────
# Sovereignty levels (S0..S5) — مرتبطة بـ sovereignty.py لكن
# نضعها هنا أيضًا لأن كل العقود تستهلكها.
# ────────────────────────────────────────────────────────────────


class SovereigntyLevel(StrEnum):
    S0_INTERNAL_DRAFT = "S0_INTERNAL_DRAFT"
    S1_INTERNAL_AUTO = "S1_INTERNAL_AUTO"
    S2_SAMI_APPROVAL = "S2_SAMI_APPROVAL"  # founder approval (sami = صامي)
    S3_LEGAL_APPROVAL = "S3_LEGAL_APPROVAL"
    S4_BOARD_APPROVAL = "S4_BOARD_APPROVAL"
    S5_BLOCKED = "S5_BLOCKED"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DataSensitivity(StrEnum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    REGULATED = "regulated"  # PDPL / financial / personal


class ActorKind(StrEnum):
    FOUNDER = "founder"
    INTERNAL_USER = "internal_user"
    CUSTOMER = "customer"
    PARTNER = "partner"
    AGENT = "agent"
    SYSTEM = "system"
    PUBLIC = "public"


class OutputKind(StrEnum):
    DRAFT = "draft"
    PROPOSAL = "proposal"
    MESSAGE = "message"
    REPORT = "report"
    ASSET = "asset"
    DECISION = "decision"
    ACTION = "action"


# ────────────────────────────────────────────────────────────────
# Identity & Context
# ────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Actor:
    actor_id: str
    kind: ActorKind
    display_name: str | None = None
    org_id: str | None = None
    customer_id: str | None = None
    partner_id: str | None = None


@dataclass
class ContextPacket:
    """Single shape that every Hermes request flows through."""

    request_id: str = field(default_factory=lambda: f"req_{uuid.uuid4().hex[:12]}")
    actor: Actor | None = None
    intent: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    data_sensitivity: DataSensitivity = DataSensitivity.INTERNAL
    declared_output_kind: OutputKind = OutputKind.DRAFT
    customer_id: str | None = None
    partner_id: str | None = None
    workspace_id: str | None = None
    locale: Literal["ar", "en"] = "ar"
    correlation_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tags: list[str] = field(default_factory=list)

    def child(self, **overrides: Any) -> "ContextPacket":
        """Branch a context packet for a sub-step while preserving lineage."""
        data = self.__dict__.copy()
        data.update(overrides)
        data["request_id"] = f"{self.request_id}.{uuid.uuid4().hex[:6]}"
        data["correlation_id"] = self.correlation_id or self.request_id
        data["created_at"] = datetime.now(timezone.utc)
        return ContextPacket(**data)


# ────────────────────────────────────────────────────────────────
# Risk + Approval + Audit
# ────────────────────────────────────────────────────────────────


@dataclass
class RiskAssessment:
    risk_level: RiskLevel
    sovereignty_level: SovereigntyLevel
    approval_required: bool
    reasons: list[str] = field(default_factory=list)
    controls_triggered: list[str] = field(default_factory=list)


@dataclass
class ApprovalRequirement:
    required: bool
    approver_role: str | None = None
    ticket_id: str | None = None
    reason: str | None = None


@dataclass
class AuditEvent:
    event_id: str
    request_id: str
    stage: str  # "gate.policy", "gate.trust", "agent.run", "tool.call", ...
    actor_id: str | None
    outcome: Literal["pass", "deny", "hold", "executed", "error"]
    payload_summary: dict[str, Any]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ────────────────────────────────────────────────────────────────
# Unified API/runtime response — Section 58 of the spec.
# ────────────────────────────────────────────────────────────────


@dataclass
class HermesResponse:
    success: bool
    data: dict[str, Any] = field(default_factory=dict)
    risk: dict[str, Any] = field(default_factory=dict)
    next_actions: list[dict[str, Any]] = field(default_factory=list)
    events_emitted: list[str] = field(default_factory=list)
    error: dict[str, Any] | None = None

    @classmethod
    def from_risk(
        cls,
        *,
        data: dict[str, Any],
        risk: RiskAssessment,
        next_actions: list[dict[str, Any]] | None = None,
        events_emitted: list[str] | None = None,
    ) -> "HermesResponse":
        return cls(
            success=True,
            data=data,
            risk={
                "risk_level": risk.risk_level.value,
                "sovereignty_level": risk.sovereignty_level.value,
                "approval_required": risk.approval_required,
                "reasons": risk.reasons,
                "controls_triggered": risk.controls_triggered,
            },
            next_actions=next_actions or [],
            events_emitted=events_emitted or [],
        )

    @classmethod
    def denied(cls, *, reason: str, risk: RiskAssessment) -> "HermesResponse":
        return cls(
            success=False,
            data={},
            risk={
                "risk_level": risk.risk_level.value,
                "sovereignty_level": risk.sovereignty_level.value,
                "approval_required": risk.approval_required,
                "reasons": risk.reasons,
                "controls_triggered": risk.controls_triggered,
            },
            next_actions=[],
            events_emitted=["hermes.request.denied"],
            error={"code": "denied", "message": reason},
        )

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "success": self.success,
            "data": self.data,
            "risk": self.risk,
            "next_actions": self.next_actions,
            "events_emitted": self.events_emitted,
        }
        if self.error is not None:
            out["error"] = self.error
        return out


# ────────────────────────────────────────────────────────────────
# Gate result — what every gate returns to the runtime.
# ────────────────────────────────────────────────────────────────


@dataclass
class GateResult:
    stage: str
    passed: bool
    risk_delta: list[str] = field(default_factory=list)
    sovereignty_override: SovereigntyLevel | None = None
    approval_required: bool = False
    reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


__all__ = [
    "Actor",
    "ActorKind",
    "ApprovalRequirement",
    "AuditEvent",
    "ContextPacket",
    "DataSensitivity",
    "GateResult",
    "HermesResponse",
    "OutputKind",
    "RiskAssessment",
    "RiskLevel",
    "SovereigntyLevel",
]
