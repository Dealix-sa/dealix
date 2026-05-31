"""
Hermes Kernel canonical schemas.

The seven phases each have one core contract. Schemas are Pydantic v2,
strict, immutable through the kernel boundary, and serializable.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _sid() -> str:
    return f"sig_{uuid.uuid4().hex[:16]}"


def _oid() -> str:
    return f"opp_{uuid.uuid4().hex[:16]}"


def _did() -> str:
    return f"dec_{uuid.uuid4().hex[:16]}"


def _eid() -> str:
    return f"exe_{uuid.uuid4().hex[:16]}"


def _outid() -> str:
    return f"out_{uuid.uuid4().hex[:16]}"


def _aid() -> str:
    return f"ast_{uuid.uuid4().hex[:16]}"


# ── Enumerations ────────────────────────────────────────────────────


class SignalSource(StrEnum):
    sami = "sami"
    customer = "customer"
    partner = "partner"
    market = "market"
    github = "github"
    email = "email"
    whatsapp = "whatsapp"
    web = "web"
    agent = "agent"
    system = "system"


class SignalType(StrEnum):
    customer = "customer"
    partner = "partner"
    product = "product"
    market = "market"
    risk = "risk"
    money = "money"
    training = "training"
    venture = "venture"
    api = "api"
    trust = "trust"
    personal = "personal"


class SignalSensitivity(StrEnum):
    public = "public"
    internal = "internal"
    confidential = "confidential"
    restricted = "restricted"
    sovereign = "sovereign"


class SovereigntyLevel(StrEnum):
    """Doctrine: every action carries one of these six levels."""

    S0_AUTO_SAFE = "S0_AUTO_SAFE"
    S1_INTERNAL = "S1_INTERNAL"
    S2_SAMI_APPROVAL = "S2_SAMI_APPROVAL"
    S3_SOVEREIGN_MEMO = "S3_SOVEREIGN_MEMO"
    S4_SOVEREIGN_ONLY = "S4_SOVEREIGN_ONLY"
    S5_NEVER_AUTONOMOUS = "S5_NEVER_AUTONOMOUS"


class OpportunityType(StrEnum):
    customer = "customer"
    partner = "partner"
    product = "product"
    training = "training"
    governance = "governance"
    report = "report"
    api = "api"
    marketplace = "marketplace"
    venture = "venture"
    personal_wealth = "personal_wealth"


class RecommendedAction(StrEnum):
    execute = "execute"
    defer = "defer"
    kill = "kill"
    escalate = "escalate"


class ExecutionStatus(StrEnum):
    planned = "planned"
    awaiting_approval = "awaiting_approval"
    approved = "approved"
    in_flight = "in_flight"
    completed = "completed"
    failed = "failed"
    blocked = "blocked"
    killed = "killed"


class OutcomeStatus(StrEnum):
    drafted = "drafted"
    sent = "sent"
    replied = "replied"
    booked = "booked"
    won = "won"
    lost = "lost"
    paid = "paid"
    ignored = "ignored"
    risk_blocked = "risk_blocked"


class AssetType(StrEnum):
    template = "template"
    playbook = "playbook"
    case_study = "case_study"
    dataset = "dataset"
    workflow = "workflow"
    prompt_pack = "prompt_pack"
    report = "report"
    proposal = "proposal"
    landing_page = "landing_page"
    offer = "offer"
    evidence_pack = "evidence_pack"


# ── The seven kernel contracts ──────────────────────────────────────


class Signal(BaseModel):
    """Phase 1: every input enters as a Signal. No Signal is ever discarded."""

    model_config = ConfigDict(extra="forbid")

    signal_id: str = Field(default_factory=_sid)
    source: SignalSource
    signal_type: SignalType
    title: str = Field(..., min_length=1, max_length=240)
    content: str = Field(..., min_length=1)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    sensitivity: SignalSensitivity = SignalSensitivity.internal
    workspace_id: str = "dealix_internal"
    owner: str = "Sami"
    tags: list[str] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=_now)
    archived_at: str | None = None
    classified: bool = False


class Opportunity(BaseModel):
    """Phase 2: a Signal that crossed the value threshold."""

    model_config = ConfigDict(extra="forbid")

    opportunity_id: str = Field(default_factory=_oid)
    signal_id: str
    opportunity_type: OpportunityType
    title: str
    description: str = ""
    estimated_value_sar: float = Field(default=0.0, ge=0.0)
    cash_speed_score: int = Field(default=0, ge=0, le=5)
    strategic_score: int = Field(default=0, ge=0, le=5)
    repeatability_score: int = Field(default=0, ge=0, le=5)
    data_moat_score: int = Field(default=0, ge=0, le=5)
    difficulty_score: int = Field(default=0, ge=0, le=5)
    risk_score: int = Field(default=0, ge=0, le=5)
    composite_score: float = 0.0
    sovereignty_level: SovereigntyLevel = SovereigntyLevel.S1_INTERNAL
    recommended_action: RecommendedAction = RecommendedAction.defer
    assigned_engine: str | None = None
    owner: str = "Sami"
    created_at: str = Field(default_factory=_now)


class Decision(BaseModel):
    """Phase 3: an Opportunity becomes a structured Decision memo."""

    model_config = ConfigDict(extra="forbid")

    decision_id: str = Field(default_factory=_did)
    opportunity_id: str
    title: str
    memo: str
    recommendation: RecommendedAction
    sovereignty_level: SovereigntyLevel
    requires_approval: bool = False
    approval_id: str | None = None
    rationale: str = ""
    risks: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    expected_outcome: str = ""
    created_at: str = Field(default_factory=_now)


class Execution(BaseModel):
    """Phase 4: a Decision turned into a concrete, policy-checked plan."""

    model_config = ConfigDict(extra="forbid")

    execution_id: str = Field(default_factory=_eid)
    decision_id: str
    agent_id: str
    tools: list[str] = Field(default_factory=list)
    status: ExecutionStatus = ExecutionStatus.planned
    payload: dict[str, Any] = Field(default_factory=dict)
    sovereignty_level: SovereigntyLevel
    trust_check_passed: bool = False
    approval_required: bool = False
    approval_id: str | None = None
    blocked_reason: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    created_at: str = Field(default_factory=_now)


class Outcome(BaseModel):
    """Phase 5: what actually happened after Execution."""

    model_config = ConfigDict(extra="forbid")

    outcome_id: str = Field(default_factory=_outid)
    execution_id: str
    status: OutcomeStatus
    actual_result: str
    revenue_sar: float = 0.0
    cost_sar: float = 0.0
    margin_sar: float = 0.0
    learning: str = ""
    asset_review_required: bool = False
    asset_id: str | None = None
    revenue_verified: bool = False
    attribution_links: list[str] = Field(default_factory=list)
    metrics: dict[str, float] = Field(default_factory=dict)
    created_at: str = Field(default_factory=_now)


class Asset(BaseModel):
    """Phase 6: durable, reusable IP harvested from an Outcome."""

    model_config = ConfigDict(extra="forbid")

    asset_id: str = Field(default_factory=_aid)
    outcome_id: str | None = None
    asset_type: AssetType
    title: str
    description: str = ""
    artifact_uri: str | None = None
    reuse_count: int = 0
    revenue_attributed_sar: float = 0.0
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    moat_score: float = Field(default=0.0, ge=0.0, le=1.0)
    scaled: bool = False
    killed: bool = False
    tags: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now)


# ── Lifecycle event envelope ─────────────────────────────────────────


class LifecycleEvent(BaseModel):
    """Event emitted at every phase transition."""

    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:16]}")
    event_type: Literal[
        "signal.captured",
        "signal.classified",
        "opportunity.created",
        "opportunity.scored",
        "decision.created",
        "decision.approved",
        "decision.denied",
        "execution.planned",
        "execution.held",
        "execution.dispatched",
        "execution.completed",
        "outcome.logged",
        "asset.created",
        "asset.scaled",
        "asset.killed",
    ]
    entity_id: str
    workspace_id: str = "dealix_internal"
    actor: str = "system"
    sovereignty_level: SovereigntyLevel = SovereigntyLevel.S0_AUTO_SAFE
    payload: dict[str, Any] = Field(default_factory=dict)
    occurred_at: str = Field(default_factory=_now)
