"""Canonical core objects for Hermes.

Six immutable-ish core objects flow through every module:

    Signal      — something noticed from the world.
    Opportunity — a scored, classified hypothesis derived from a signal.
    Decision    — a sovereign choice about what to do with the opportunity.
    Execution   — the actual planned/run action set.
    Outcome     — the recorded result.
    Asset       — a reusable artifact harvested from the outcome.

Every domain-specific module (money, products, partners, ...) reuses these
shapes. Domain-specific data lives in the ``payload`` dict, never as
parallel hierarchies.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from dealix.hermes.sovereignty.levels import SovereigntyLevel


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class CoreObject(BaseModel):
    """Base for every Hermes object. Holds identity + lineage."""

    model_config = ConfigDict(extra="forbid", frozen=False)

    id: str
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)
    owner: str = Field(description="The sovereign owner. Default: 'sami'.")
    payload: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)

    def touch(self) -> None:
        self.updated_at = _now()


# --------------------------------------------------------------------------
# Signal
# --------------------------------------------------------------------------


class SignalStatus(str, Enum):
    NEW = "new"
    CLASSIFIED = "classified"
    CONVERTED = "converted"   # turned into an opportunity
    ARCHIVED = "archived"     # explicitly dismissed


class Signal(CoreObject):
    """Something the system noticed.

    A signal is *just* a fact. Whether it matters is the opportunity's job.
    """

    source: str = Field(description="email|market|partner|customer|internal|...")
    domain: str = Field(description="money|product|partner|customer|market|...")
    summary: str
    status: SignalStatus = SignalStatus.NEW
    risk_hint: str = "low"  # low|medium|high — informational only

    @classmethod
    def make(cls, *, source: str, domain: str, summary: str, owner: str = "sami", **extra: Any) -> "Signal":
        return cls(id=_new_id("sig"), source=source, domain=domain, summary=summary, owner=owner, **extra)


# --------------------------------------------------------------------------
# Opportunity
# --------------------------------------------------------------------------


class OpportunityStatus(str, Enum):
    DRAFT = "draft"
    SCORED = "scored"
    QUEUED = "queued"
    DECIDED = "decided"
    DROPPED = "dropped"


class Opportunity(CoreObject):
    """A scored hypothesis. Must point back at one signal."""

    signal_id: str
    domain: str
    title: str
    score: Optional[float] = None        # 0..1, populated by scoring engine
    score_breakdown: dict[str, float] = Field(default_factory=dict)
    estimated_value_sar: float = 0.0
    confidence: float = 0.5              # 0..1
    risk_level: str = "low"
    status: OpportunityStatus = OpportunityStatus.DRAFT
    sovereignty_level: SovereigntyLevel = SovereigntyLevel.S1_INTERNAL

    @field_validator("score")
    @classmethod
    def _score_range(cls, v: Optional[float]) -> Optional[float]:
        if v is None:
            return v
        if not 0.0 <= v <= 1.0:
            raise ValueError("Opportunity.score must be in [0,1].")
        return v

    @field_validator("confidence")
    @classmethod
    def _confidence_range(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValueError("Opportunity.confidence must be in [0,1].")
        return v

    @classmethod
    def make(cls, *, signal_id: str, domain: str, title: str, owner: str = "sami", **extra: Any) -> "Opportunity":
        return cls(id=_new_id("opp"), signal_id=signal_id, domain=domain, title=title, owner=owner, **extra)


# --------------------------------------------------------------------------
# Decision
# --------------------------------------------------------------------------


class DecisionStatus(str, Enum):
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    AUTO_APPROVED = "auto_approved"
    BLOCKED = "blocked"  # sovereignty kill switch / forbidden action


class Decision(CoreObject):
    """A sovereign choice about an opportunity.

    Decisions are the only place an action becomes 'allowed to execute'.
    They always carry an explicit sovereignty level and reasoning.
    """

    opportunity_id: str
    action: str                           # short verb phrase, e.g. "send_proposal"
    sovereignty_level: SovereigntyLevel
    status: DecisionStatus = DecisionStatus.PENDING_APPROVAL
    rationale: str
    approver: Optional[str] = None
    approved_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    evidence_pack_id: Optional[str] = None

    @classmethod
    def make(
        cls,
        *,
        opportunity_id: str,
        action: str,
        sovereignty_level: SovereigntyLevel,
        rationale: str,
        owner: str = "sami",
        **extra: Any,
    ) -> "Decision":
        return cls(
            id=_new_id("dec"),
            opportunity_id=opportunity_id,
            action=action,
            sovereignty_level=sovereignty_level,
            rationale=rationale,
            owner=owner,
            **extra,
        )

    @property
    def is_executable(self) -> bool:
        return self.status in {DecisionStatus.APPROVED, DecisionStatus.AUTO_APPROVED}


# --------------------------------------------------------------------------
# Execution
# --------------------------------------------------------------------------


class ExecutionStatus(str, Enum):
    PLANNED = "planned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Execution(CoreObject):
    """The actual planned/run actions for an approved decision."""

    decision_id: str
    agent_id: Optional[str] = None        # which Hermes agent executed
    tool_ids: list[str] = Field(default_factory=list)
    steps: list[dict[str, Any]] = Field(default_factory=list)
    status: ExecutionStatus = ExecutionStatus.PLANNED
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    @classmethod
    def make(cls, *, decision_id: str, owner: str = "sami", **extra: Any) -> "Execution":
        return cls(id=_new_id("exe"), decision_id=decision_id, owner=owner, **extra)


# --------------------------------------------------------------------------
# Outcome
# --------------------------------------------------------------------------


class OutcomeStatus(str, Enum):
    WIN = "win"
    LOSS = "loss"
    NEUTRAL = "neutral"
    PENDING = "pending"


class Outcome(CoreObject):
    """Recorded result of an execution. Required before an asset can form."""

    execution_id: str
    status: OutcomeStatus = OutcomeStatus.PENDING
    metric_name: Optional[str] = None
    metric_value: Optional[float] = None
    revenue_sar: float = 0.0
    notes: str = ""

    @classmethod
    def make(cls, *, execution_id: str, owner: str = "sami", **extra: Any) -> "Outcome":
        return cls(id=_new_id("out"), execution_id=execution_id, owner=owner, **extra)


# --------------------------------------------------------------------------
# Asset
# --------------------------------------------------------------------------


class AssetStatus(str, Enum):
    DRAFT = "draft"
    REUSABLE = "reusable"
    COMMERCIALIZED = "commercialized"
    RETIRED = "retired"


class Asset(CoreObject):
    """A reusable artifact harvested from an outcome.

    Assets are the moat. Templates, playbooks, prompts, sector kits,
    pricing curves, partner cards — anything reusable.
    """

    outcome_id: str
    kind: str                              # template|playbook|prompt|...
    title: str
    summary: str
    status: AssetStatus = AssetStatus.DRAFT
    reuse_count: int = 0
    revenue_attributed_sar: float = 0.0

    @classmethod
    def make(cls, *, outcome_id: str, kind: str, title: str, summary: str, owner: str = "sami", **extra: Any) -> "Asset":
        return cls(
            id=_new_id("ast"),
            outcome_id=outcome_id,
            kind=kind,
            title=title,
            summary=summary,
            owner=owner,
            **extra,
        )


# --------------------------------------------------------------------------
# Structured output — required shape for every Agent reply.
# --------------------------------------------------------------------------


class StructuredOutput(BaseModel):
    """Every Hermes agent must return this shape. Free-form text is rejected."""

    model_config = ConfigDict(extra="forbid")

    summary: str
    risk_level: str = "low"  # low|medium|high
    sovereignty_level: SovereigntyLevel
    recommended_action: str
    approval_required: bool
    expected_outcome: str
    next_steps: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)

    @field_validator("risk_level")
    @classmethod
    def _risk_level_known(cls, v: str) -> str:
        if v not in {"low", "medium", "high"}:
            raise ValueError(f"unknown risk_level: {v}")
        return v


__all__ = [
    "Asset",
    "AssetStatus",
    "CoreObject",
    "Decision",
    "DecisionStatus",
    "Execution",
    "ExecutionStatus",
    "Opportunity",
    "OpportunityStatus",
    "Outcome",
    "OutcomeStatus",
    "Signal",
    "SignalStatus",
    "StructuredOutput",
]
