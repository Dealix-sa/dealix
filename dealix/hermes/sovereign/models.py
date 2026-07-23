"""Core objects for the Hermes sovereign value loop.

These dataclasses are intentionally deterministic and integration-light. They
represent the universal Dealix objects that existing revenue, proof, partner,
market, and customer systems can map into without being rewritten.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def _now() -> datetime:
    return datetime.now(UTC)


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


class DecisionType(StrEnum):
    EXECUTE = "execute"
    DEFER = "defer"
    KILL = "kill"
    SCALE = "scale"
    REQUEST_MORE_INFO = "request_more_info"


class ExecutionStatus(StrEnum):
    PLANNED = "planned"
    HELD_FOR_APPROVAL = "held_for_approval"
    BLOCKED = "blocked"
    EXECUTED = "executed"
    OUTCOME_REQUIRED = "outcome_required"
    COMPLETE = "complete"


class OutcomeStatus(StrEnum):
    DRAFTED = "drafted"
    SENT_MANUAL = "sent_manual"
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
    PROOF_PACK = "proof_pack"


@dataclass(slots=True)
class Signal:
    source: str
    signal_type: SignalType | str
    title: str
    content: str = ""
    confidence: float = 0.5
    sensitivity: Sensitivity | str = Sensitivity.INTERNAL
    owner: str = "Sami"
    raw_payload: dict[str, object] = field(default_factory=dict)
    processed: bool = False
    id: str = field(default_factory=lambda: _uid("sig"))
    created_at: datetime = field(default_factory=_now)


@dataclass(slots=True)
class Opportunity:
    signal_id: str
    opportunity_type: OpportunityType | str
    title: str
    description: str = ""
    estimated_value_sar: float = 0.0
    cash_speed_score: int = 1
    strategic_score: int = 1
    repeatability_score: int = 1
    data_moat_score: int = 1
    difficulty_score: int = 1
    risk_score: int = 1
    sovereignty_level: str = "S1_INTERNAL"
    recommended_action: str = "request_more_info"
    status: str = "open"
    opportunity_score: float = 0.0
    id: str = field(default_factory=lambda: _uid("opp"))
    created_at: datetime = field(default_factory=_now)


@dataclass(slots=True)
class Decision:
    opportunity_id: str
    decision_type: DecisionType | str
    context: str = ""
    options: list[str] = field(default_factory=list)
    recommendation: str = ""
    risk_level: str = "medium"
    sovereignty_level: str = "S2_SAMI_APPROVAL"
    requires_approval: bool = True
    approved_by: str | None = None
    approved_at: datetime | None = None
    id: str = field(default_factory=lambda: _uid("dec"))
    created_at: datetime = field(default_factory=_now)


@dataclass(slots=True)
class Execution:
    decision_id: str
    action_type: str
    agent_id: str = "hermes_kernel"
    permission_level: str = "L1_DRAFT"
    sovereignty_level: str = "S1_INTERNAL"
    external_action: bool = False
    requires_approval: bool = True
    expected_result: str = ""
    status: ExecutionStatus | str = ExecutionStatus.PLANNED
    id: str = field(default_factory=lambda: _uid("exe"))
    created_at: datetime = field(default_factory=_now)


@dataclass(slots=True)
class Outcome:
    execution_id: str
    status: OutcomeStatus | str
    actual_result: str = ""
    revenue_sar: float = 0.0
    time_saved_minutes: int = 0
    risk_reduced: bool = False
    learning: str = ""
    asset_review_required: bool = True
    id: str = field(default_factory=lambda: _uid("out"))
    created_at: datetime = field(default_factory=_now)


@dataclass(slots=True)
class Asset:
    outcome_id: str
    asset_type: AssetType | str
    title: str
    description: str = ""
    reusable: bool = True
    commercializable: bool = False
    asset_location: str = ""
    id: str = field(default_factory=lambda: _uid("asset"))
    created_at: datetime = field(default_factory=_now)
