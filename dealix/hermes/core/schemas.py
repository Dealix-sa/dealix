"""
Hermes canonical schemas.

These types are the universal shape every layer of the Kernel speaks.
The Kernel is intentionally domain-agnostic: a Signal can be a customer
inquiry, a partner intro, a market report, a personal asset move, or a
risk alert. The pipeline is the same.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

SignalType = Literal[
    "customer",
    "partner",
    "market",
    "product",
    "risk",
    "finance",
    "training",
    "report",
    "api",
    "venture",
    "legal",
    "technical",
    "personal",
]

OpportunityType = Literal[
    "customer",
    "partner",
    "product",
    "training",
    "report",
    "governance",
    "api",
    "marketplace",
    "venture",
    "investor",
    "personal_wealth",
    "risk_reduction",
]

OutcomeStatus = Literal[
    "planned",
    "drafted",
    "sent",
    "replied",
    "booked",
    "won",
    "lost",
    "ignored",
    "asset_created",
]

AssetType = Literal[
    "case_study",
    "template",
    "playbook",
    "dataset",
    "proposal",
    "landing_page",
    "training_material",
    "policy",
    "report",
    "workflow",
    "agent_template",
    "sector_kit",
    "partner_pack",
]


def _utcnow() -> datetime:
    return datetime.now(UTC)


class HermesSignal(BaseModel):
    source: str
    signal_type: SignalType
    title: str
    content: str
    raw_payload: dict[str, Any] = Field(default_factory=dict)
    detected_at: datetime = Field(default_factory=_utcnow)


class HermesOpportunity(BaseModel):
    opportunity_type: OpportunityType
    title: str
    description: str
    target_entity: str | None = None
    estimated_value_sar: float | None = None
    cash_speed_score: int = Field(ge=1, le=5)
    strategic_score: int = Field(ge=1, le=5)
    difficulty_score: int = Field(ge=1, le=5)
    risk_score: int = Field(ge=1, le=5)
    repeatability_score: int = Field(ge=1, le=5)
    data_moat_score: int = Field(ge=1, le=5)
    sovereignty_level: str
    recommended_action: str
    recommended_agent: str


class HermesDecisionMemo(BaseModel):
    opportunity_id: str | None = None
    decision_title: str
    context: str
    options: list[str]
    recommendation: str
    expected_impact: str
    risks: list[str]
    sovereignty_level: str
    approval_required: bool
    next_steps: list[str]


class HermesExecutionPlan(BaseModel):
    decision_id: str | None = None
    action_type: str
    agent_id: str
    permission_level: str
    steps: list[str]
    expected_result: str
    requires_approval: bool


class HermesOutcome(BaseModel):
    execution_id: str | None = None
    outcome_type: str
    expected_result: str
    actual_result: str | None = None
    status: OutcomeStatus
    revenue_sar: float | None = None
    time_saved_minutes: int | None = None
    risk_reduced: bool = False
    learning: str | None = None


class HermesAsset(BaseModel):
    outcome_id: str | None = None
    asset_type: AssetType
    title: str
    description: str
    reusable: bool = True
    asset_location: str | None = None
