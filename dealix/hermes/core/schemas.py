"""
Hermes core objects — Signal, Opportunity, Decision, Execution, Outcome, Asset.

These are the immutable shapes that flow through the kernel pipeline.
Every shape carries enough metadata for sovereignty, trust, audit, and
outcome accounting. Models are ``extra='forbid'`` so unknown fields fail
fast (cf. the project's approval-store convention).
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


# ── Enums ──────────────────────────────────────────────────────────


class SovereigntyLevel(StrEnum):
    """Sovereignty classification for any action."""

    S0_AGENT_FREE = "S0_AGENT_FREE"          # Internal, reversible, no PII, low risk
    S1_INTERNAL = "S1_INTERNAL"              # Internal drafts, no external send
    S2_SAMI_APPROVAL = "S2_SAMI_APPROVAL"    # Needs Sami before execution
    S3_SAMI_REVIEW = "S3_SAMI_REVIEW"        # Pre-approved policy but reviewed after
    S4_SOVEREIGN_ONLY = "S4_SOVEREIGN_ONLY"  # Public API, marketplace, MCP, contracts, pricing
    S5_NEVER_AUTONOMOUS = "S5_NEVER_AUTONOMOUS"  # Money transfer, signing, data leak


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PermissionLevel(StrEnum):
    L0_READ = "L0_READ"
    L1_DRAFT = "L1_DRAFT"
    L2_INTERNAL_WRITE = "L2_INTERNAL_WRITE"
    L3_EXTERNAL_SEND = "L3_EXTERNAL_SEND"
    L4_COMMITMENT = "L4_COMMITMENT"


class Sensitivity(StrEnum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class SignalType(StrEnum):
    CUSTOMER = "customer"
    PARTNER = "partner"
    PRODUCT = "product"
    MARKET = "market"
    RISK = "risk"
    MONEY = "money"
    TRAINING = "training"
    VENTURE = "venture"
    API = "api"
    TRUST = "trust"
    PERSONAL = "personal"


class OpportunityType(StrEnum):
    CUSTOMER = "customer"
    PARTNER = "partner"
    PRODUCT = "product"
    TRAINING = "training"
    GOVERNANCE = "governance"
    REPORT = "report"
    API = "api"
    MARKETPLACE = "marketplace"
    VENTURE = "venture"
    PERSONAL_WEALTH = "personal_wealth"


class OutcomeStatus(StrEnum):
    DRAFTED = "drafted"
    SENT = "sent"
    REPLIED = "replied"
    BOOKED = "booked"
    WON = "won"
    LOST = "lost"
    PAID = "paid"
    IGNORED = "ignored"
    RISK_BLOCKED = "risk_blocked"


class AssetType(StrEnum):
    TEMPLATE = "template"
    PLAYBOOK = "playbook"
    CASE_STUDY = "case_study"
    REPORT = "report"
    POLICY = "policy"
    TRAINING_MATERIAL = "training_material"
    SECTOR_KIT = "sector_kit"
    WORKFLOW = "workflow"


# ── Base model ─────────────────────────────────────────────────────


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)


# ── Core objects ───────────────────────────────────────────────────


class Signal(_Strict):
    """Any input that may carry value."""

    id: str = Field(default_factory=lambda: _new_id("sig"))
    source: str
    signal_type: SignalType
    title: str
    content: str = ""
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    sensitivity: Sensitivity = Sensitivity.INTERNAL
    raw_payload: dict[str, Any] = Field(default_factory=dict)
    owner: str = "Sami"
    processed: bool = False
    created_at: datetime = Field(default_factory=_now)


class Opportunity(_Strict):
    """A signal evaluated into a monetizable / strategic opportunity."""

    id: str = Field(default_factory=lambda: _new_id("opp"))
    signal_id: str
    opportunity_type: OpportunityType
    title: str
    description: str = ""
    estimated_value_sar: float = 0.0
    cash_speed_score: int = Field(default=1, ge=1, le=5)
    strategic_score: int = Field(default=1, ge=1, le=5)
    repeatability_score: int = Field(default=1, ge=1, le=5)
    data_moat_score: int = Field(default=1, ge=1, le=5)
    difficulty_score: int = Field(default=1, ge=1, le=5)
    risk_score: int = Field(default=1, ge=1, le=5)
    sovereignty_level: SovereigntyLevel = SovereigntyLevel.S1_INTERNAL
    recommended_action: str = ""
    status: str = "open"
    score: float = 0.0
    created_at: datetime = Field(default_factory=_now)


class Decision(_Strict):
    """A bounded choice on a strong opportunity."""

    id: str = Field(default_factory=lambda: _new_id("dec"))
    opportunity_id: str
    decision_type: str  # execute | defer | kill | scale | request_more_info
    context: str = ""
    options: list[str] = Field(default_factory=list)
    recommendation: str = ""
    risk_level: RiskLevel = RiskLevel.LOW
    sovereignty_level: SovereigntyLevel = SovereigntyLevel.S1_INTERNAL
    requires_approval: bool = True
    approved_by: str | None = None
    approved_at: datetime | None = None
    rejection_reason: str | None = None
    created_at: datetime = Field(default_factory=_now)


class Execution(_Strict):
    """The action a decision triggers."""

    id: str = Field(default_factory=lambda: _new_id("exe"))
    decision_id: str
    agent_id: str
    action_type: str
    permission_level: PermissionLevel = PermissionLevel.L1_DRAFT
    external_action: bool = False
    requires_approval: bool = True
    expected_result: str = ""
    payload: dict[str, Any] = Field(default_factory=dict)
    status: str = "planned"  # planned | held | running | done | blocked
    block_reason: str | None = None
    created_at: datetime = Field(default_factory=_now)


class Outcome(_Strict):
    """Mandatory record after any execution."""

    id: str = Field(default_factory=lambda: _new_id("out"))
    execution_id: str
    status: OutcomeStatus
    actual_result: str = ""
    revenue_sar: float = 0.0
    time_saved_minutes: int = 0
    risk_reduced: bool = False
    learning: str = ""
    asset_review_required: bool = True
    asset_id: str | None = None
    created_at: datetime = Field(default_factory=_now)


class Asset(_Strict):
    """A reusable artifact distilled from an outcome."""

    id: str = Field(default_factory=lambda: _new_id("asset"))
    outcome_id: str
    asset_type: AssetType
    title: str
    description: str = ""
    reusable: bool = True
    commercializable: bool = False
    asset_location: str = ""
    created_at: datetime = Field(default_factory=_now)


# ── Trust objects ──────────────────────────────────────────────────


class AgentRecord(_Strict):
    id: str
    name: str
    mission: str
    domain: str
    owner: str = "Sami"
    max_sovereignty_level: SovereigntyLevel
    allowed_tools: list[str] = Field(default_factory=list)
    forbidden_tools: list[str] = Field(default_factory=list)
    kpis: list[str] = Field(default_factory=list)
    status: str = "active"
    created_at: datetime = Field(default_factory=_now)


class ToolRecord(_Strict):
    id: str
    name: str
    tool_type: str
    owner: str = "Sami"
    risk_level: RiskLevel
    requires_approval: bool = True
    enabled: bool = False
    data_scope: str = "tenant_only"
    allowed_agents: list[str] = Field(default_factory=list)
    audit_required: bool = True
    created_at: datetime = Field(default_factory=_now)


class ApprovalRequest(_Strict):
    id: str = Field(default_factory=lambda: _new_id("apr"))
    requested_by_agent: str
    action_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    sovereignty_level: SovereigntyLevel
    risk_level: RiskLevel
    status: str = "pending"  # pending | approved | rejected | blocked
    approved_by: str | None = None
    approved_at: datetime | None = None
    rejection_reason: str | None = None
    created_at: datetime = Field(default_factory=_now)


class AuditEvent(_Strict):
    id: str = Field(default_factory=lambda: _new_id("aud"))
    agent_id: str = ""
    tool_id: str = ""
    action_type: str
    payload_hash: str = ""
    risk_level: RiskLevel = RiskLevel.LOW
    sovereignty_level: SovereigntyLevel = SovereigntyLevel.S0_AGENT_FREE
    approval_id: str | None = None
    result: str = ""
    created_at: datetime = Field(default_factory=_now)
