"""Pydantic models for the Hermes kernel.

The kernel pipeline is:
    Signal → Opportunity → Decision → Execution → Trust → Outcome → Asset

Each step has a strongly-typed model so the orchestrator can hand off
between agents without losing context. All models are JSON-serialisable
so they can be persisted to the ledgers or shipped over the API.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timezone
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.sovereignty import SovereigntyLevel


def _utcnow() -> datetime:
    return datetime.now(UTC)


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class HermesBase(BaseModel):
    """Common config — frozen-ish, JSON friendly, no extras."""

    # Keep enums as enums in-process so set membership + `is` checks work.
    # JSON serialisation through `model_dump(mode="json")` still emits values.
    model_config = ConfigDict(extra="forbid")


# ── Signal ────────────────────────────────────────────────────────────


class SignalSource(StrEnum):
    INBOUND_LEAD = "inbound_lead"
    OUTBOUND_RESEARCH = "outbound_research"
    PARTNER_REFERRAL = "partner_referral"
    SECTOR_RADAR = "sector_radar"
    SUPPORT_CHANNEL = "support_channel"
    INTERNAL_OBSERVATION = "internal_observation"
    MARKET_NEWS = "market_news"


class Signal(HermesBase):
    id: str = Field(default_factory=lambda: _new_id("sig"))
    source: SignalSource
    sector: str | None = None
    region: str = "SA"
    payload: dict[str, Any] = Field(default_factory=dict)
    raw_text: str | None = None
    captured_at: datetime = Field(default_factory=_utcnow)
    tenant_id: str | None = None


# ── Opportunity ───────────────────────────────────────────────────────


class Opportunity(HermesBase):
    id: str = Field(default_factory=lambda: _new_id("opp"))
    signal_id: str
    title: str
    sector: str | None = None
    buyer_persona: str | None = None
    pain_hypothesis: str | None = None
    recommended_offer: str | None = None
    estimated_value_sar: float | None = None
    cash_speed_score: int = Field(0, ge=0, le=100)
    close_probability: float = Field(0.0, ge=0.0, le=1.0)
    strategic_value_score: int = Field(0, ge=0, le=100)
    risk_score: int = Field(0, ge=0, le=100)
    money_priority_score: float = 0.0
    sovereignty_level: SovereigntyLevel = SovereigntyLevel.L2_INTERNAL_TASK
    created_at: datetime = Field(default_factory=_utcnow)


# ── Decision ──────────────────────────────────────────────────────────


class DecisionVerdict(StrEnum):
    PURSUE = "pursue"
    DEFER = "defer"
    DROP = "drop"
    ESCALATE = "escalate"


class Decision(HermesBase):
    id: str = Field(default_factory=lambda: _new_id("dec"))
    opportunity_id: str
    verdict: DecisionVerdict
    rationale: str
    next_action: str
    sovereignty_level: SovereigntyLevel
    requires_approval: bool = False
    approval_status: Literal["pending", "approved", "rejected", "n/a"] = "n/a"
    decided_at: datetime = Field(default_factory=_utcnow)


# ── Execution ─────────────────────────────────────────────────────────


class ExecutionStatus(StrEnum):
    DRAFTED = "drafted"
    QUEUED = "queued"
    BLOCKED = "blocked"
    EXECUTED = "executed"
    FAILED = "failed"


class Execution(HermesBase):
    id: str = Field(default_factory=lambda: _new_id("exe"))
    decision_id: str
    agent_id: str
    tool_id: str | None = None
    status: ExecutionStatus = ExecutionStatus.DRAFTED
    artifact: dict[str, Any] = Field(default_factory=dict)
    started_at: datetime = Field(default_factory=_utcnow)
    finished_at: datetime | None = None
    error: str | None = None


# ── Trust check ───────────────────────────────────────────────────────


class TrustCheckOutcome(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    ESCALATE = "escalate"


class TrustCheckResult(HermesBase):
    id: str = Field(default_factory=lambda: _new_id("trust"))
    target_id: str
    target_kind: Literal["decision", "execution", "proposal", "message"]
    outcome: TrustCheckOutcome
    violations: list[str] = Field(default_factory=list)
    notes: str | None = None
    checked_at: datetime = Field(default_factory=_utcnow)


# ── Outcome ───────────────────────────────────────────────────────────


class OutcomeKind(StrEnum):
    DEAL_WON = "deal_won"
    DEAL_LOST = "deal_lost"
    MEETING_BOOKED = "meeting_booked"
    REPLY_RECEIVED = "reply_received"
    NO_REPLY = "no_reply"
    OBJECTION_RAISED = "objection_raised"
    UPSELL_ACCEPTED = "upsell_accepted"
    PILOT_STARTED = "pilot_started"
    PILOT_FAILED = "pilot_failed"


class Outcome(HermesBase):
    id: str = Field(default_factory=lambda: _new_id("out"))
    decision_id: str | None = None
    execution_id: str | None = None
    opportunity_id: str | None = None
    kind: OutcomeKind
    value_sar: float | None = None
    sector: str | None = None
    offer: str | None = None
    notes: str | None = None
    learned_at: datetime = Field(default_factory=_utcnow)


# ── Asset ─────────────────────────────────────────────────────────────


class AssetKind(StrEnum):
    CASE_STUDY = "case_study"
    TEMPLATE = "template"
    PLAYBOOK = "playbook"
    DATASET = "dataset"
    POLICY = "policy"
    PROPOSAL = "proposal"
    TRAINING_DECK = "training_deck"
    LANDING_PAGE = "landing_page"
    WORKFLOW = "workflow"
    AGENT_TEMPLATE = "agent_template"
    SECTOR_KIT = "sector_kit"
    PARTNER_KIT = "partner_kit"


class Asset(HermesBase):
    id: str = Field(default_factory=lambda: _new_id("ast"))
    kind: AssetKind
    title: str
    summary: str
    source_outcome_id: str | None = None
    body: dict[str, Any] = Field(default_factory=dict)
    reusable: bool = True
    created_at: datetime = Field(default_factory=_utcnow)


# ── Money action ──────────────────────────────────────────────────────


class MoneyActionSource(StrEnum):
    DIRECT_CLIENT = "direct_client"
    PARTNER = "partner"
    WHITE_LABEL = "white_label"
    REPORT = "report"
    TRAINING = "training"
    SAAS = "saas"
    ENTERPRISE_PMO = "enterprise_pmo"
    API = "api"
    MARKETPLACE = "marketplace"
    VERTICAL = "vertical"
    TENDER = "tender"
    INVESTOR = "investor"
    CUSTOM = "custom"


class MoneyAction(HermesBase):
    id: str = Field(default_factory=lambda: _new_id("money"))
    title: str
    source: MoneyActionSource
    estimated_value_sar: float | None = None
    cash_speed_score: int = Field(0, ge=0, le=100)
    close_probability: float = Field(0.0, ge=0.0, le=1.0)
    strategic_value_score: int = Field(0, ge=0, le=100)
    risk_score: int = Field(0, ge=0, le=100)
    next_action: str
    sovereignty_level: SovereigntyLevel = SovereigntyLevel.L2_INTERNAL_TASK
    opportunity_id: str | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    money_priority_score: float = 0.0


# ── Sovereign brief / console ─────────────────────────────────────────


class SovereignBrief(HermesBase):
    generated_at: datetime = Field(default_factory=_utcnow)
    fastest_cash_actions: list[MoneyAction] = Field(default_factory=list)
    highest_strategic_opportunities: list[Opportunity] = Field(default_factory=list)
    pending_approvals: list[Decision] = Field(default_factory=list)
    blocked_risks: list[dict[str, Any]] = Field(default_factory=list)
    kill_recommendations: list[str] = Field(default_factory=list)
    scale_recommendations: list[str] = Field(default_factory=list)
    notes: str | None = None
