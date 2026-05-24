"""Canonical schemas for the Hermes pipeline.

These are the only contracts the rest of the codebase may import. Stage
implementations and API routers translate to/from these models — they do
not invent their own.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, NonNegativeFloat, field_validator

from dealix.hermes import ValueOutput
from dealix.hermes.sovereignty import SovereigntyLevel


def _now() -> datetime:
    return datetime.now(UTC)


def _uuid() -> str:
    return str(uuid4())


# ───────────────────────────── Signal ─────────────────────────────


class SignalSource(StrEnum):
    INBOUND_LEAD = "inbound_lead"
    OUTBOUND_REPLY = "outbound_reply"
    PARTNER = "partner"
    EVENT = "event"
    MARKET_NEWS = "market_news"
    OPEN_DATA = "open_data"
    TENDER = "tender"
    REGULATION = "regulation"
    COMPETITOR = "competitor"
    CUSTOMER_CONVERSATION = "customer_conversation"
    INTERNAL_TELEMETRY = "internal_telemetry"
    FOUNDER_NOTE = "founder_note"


class Signal(BaseModel):
    """A raw input — the atomic unit of intake."""

    signal_id: str = Field(default_factory=_uuid)
    source: SignalSource
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(min_length=1, max_length=2000)
    raw_payload: dict[str, Any] = Field(default_factory=dict)
    captured_at: datetime = Field(default_factory=_now)
    captured_by: str = Field(min_length=1)  # agent_id or "sami"
    tags: list[str] = Field(default_factory=list)


# ─────────────────────────── Opportunity ──────────────────────────


class OpportunityKind(StrEnum):
    DIRECT_DEAL = "direct_deal"
    PARTNERSHIP = "partnership"
    WHITE_LABEL = "white_label"
    TRAINING = "training"
    REPORT = "report"
    SAAS = "saas"
    API = "api"
    PMO = "pmo"
    MARKETPLACE = "marketplace"
    VENTURE = "venture"
    INVESTOR = "investor"
    TENDER = "tender"
    ACQUISITION = "acquisition"
    LICENSE = "license"


class Opportunity(BaseModel):
    """A scored, actionable target derived from one or more signals."""

    opportunity_id: str = Field(default_factory=_uuid)
    source_signal_ids: list[str] = Field(min_length=1)
    kind: OpportunityKind
    title: str
    buyer_segment: str
    estimated_value_sar: NonNegativeFloat
    close_probability: float = Field(ge=0.0, le=1.0)
    fit_score: float = Field(ge=0.0, le=1.0)
    urgency_score: float = Field(ge=0.0, le=1.0)
    risk_score: float = Field(ge=0.0, le=1.0)
    expected_value_sar: NonNegativeFloat = 0.0
    proposed_value_outputs: list[ValueOutput] = Field(min_length=1)
    created_at: datetime = Field(default_factory=_now)
    notes: str = ""

    @field_validator("proposed_value_outputs")
    @classmethod
    def _reject_waste(cls, v: list[ValueOutput]) -> list[ValueOutput]:
        if any(x is ValueOutput.WASTE for x in v):
            raise ValueError("WASTE is not a proposable value output")
        if not v:
            raise ValueError("at least one value output is required")
        return v


# ──────────────────────────── Decision ────────────────────────────


class DecisionMemo(BaseModel):
    """A written memo recording the *why* before any action runs.

    Memos are mandatory for S3+ actions; recommended for S2. They double as
    the audit trail when an outcome is later reviewed.
    """

    memo_id: str = Field(default_factory=_uuid)
    opportunity_id: str
    recommendation: str = Field(min_length=10)
    rationale: str = Field(min_length=10)
    alternatives: list[str] = Field(default_factory=list)
    sovereignty_level: SovereigntyLevel
    approval_required: bool
    written_by: str
    written_at: datetime = Field(default_factory=_now)
    approved_by: str | None = None
    approved_at: datetime | None = None


# ──────────────────────────── Execution ───────────────────────────


class ExecutionStatus(StrEnum):
    PLANNED = "planned"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    BLOCKED_BY_TRUST = "blocked_by_trust"
    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"


class ExecutionStep(BaseModel):
    step_id: str = Field(default_factory=_uuid)
    description: str
    owner: str  # agent_id or human
    tool: str | None = None
    expected_duration_minutes: int = Field(ge=0, default=15)
    status: ExecutionStatus = ExecutionStatus.PLANNED


class ExecutionPlan(BaseModel):
    plan_id: str = Field(default_factory=_uuid)
    opportunity_id: str
    memo_id: str | None = None
    steps: list[ExecutionStep] = Field(min_length=1)
    status: ExecutionStatus = ExecutionStatus.PLANNED
    created_at: datetime = Field(default_factory=_now)


# ────────────────────────────── Outcome ───────────────────────────


class OutcomeKind(StrEnum):
    WON = "won"
    LOST = "lost"
    REPLIED = "replied"
    IGNORED = "ignored"
    PAID = "paid"
    ASSET_CREATED = "asset_created"
    RISK_BLOCKED = "risk_blocked"
    LEARNING = "learning"


class Outcome(BaseModel):
    outcome_id: str = Field(default_factory=_uuid)
    opportunity_id: str
    plan_id: str | None = None
    kind: OutcomeKind
    realised_value_sar: NonNegativeFloat = 0.0
    realised_outputs: list[ValueOutput] = Field(default_factory=list)
    summary: str
    recorded_by: str
    recorded_at: datetime = Field(default_factory=_now)
    asset_review_done: bool = False
    next_action: str | None = None


# ─────────────────────────────── Asset ────────────────────────────


class AssetKind(StrEnum):
    TEMPLATE = "template"
    PLAYBOOK = "playbook"
    CASE_STUDY = "case_study"
    DATASET = "dataset"
    OFFER = "offer"
    REPORT = "report"
    POLICY = "policy"
    PROPOSAL = "proposal"
    WORKFLOW = "workflow"


class Asset(BaseModel):
    asset_id: str = Field(default_factory=_uuid)
    kind: AssetKind
    title: str
    summary: str
    body: str  # markdown or jinja2 source
    derived_from_outcome_ids: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    created_by: str
    created_at: datetime = Field(default_factory=_now)
    version: int = 1
    reusable: bool = True


# ───────────────────────────── Scale ────────────────────────────


class ScaleVerdict(StrEnum):
    SCALE = "scale"
    HOLD = "hold"
    KILL = "kill"


class ScaleDecision(BaseModel):
    decision_id: str = Field(default_factory=_uuid)
    target: str  # offer / vertical / agent / partner / campaign id
    target_kind: str
    verdict: ScaleVerdict
    reason: str
    metrics_snapshot: dict[str, float] = Field(default_factory=dict)
    decided_by: str
    decided_at: datetime = Field(default_factory=_now)


__all__ = [
    "Signal",
    "SignalSource",
    "Opportunity",
    "OpportunityKind",
    "DecisionMemo",
    "ExecutionPlan",
    "ExecutionStep",
    "ExecutionStatus",
    "Outcome",
    "OutcomeKind",
    "Asset",
    "AssetKind",
    "ScaleDecision",
    "ScaleVerdict",
]
