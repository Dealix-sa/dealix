"""Canonical domain contracts for Dealix's multi-department Commercial Universe.

The contracts are deterministic and side-effect free. They model strategy,
approvals, meetings, and relationship memory without sending messages, booking
calendars, charging customers, or mutating external systems.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


class Department(StrEnum):
    SALES = "sales"
    PARTNERSHIPS = "partnerships"
    MARKETING = "marketing"
    MARKET_ACCESS = "market_access"
    CHANNEL_DISTRIBUTION = "channel_distribution"
    SERVICE_EXCHANGE = "service_exchange"
    B2G_READINESS = "b2g_readiness"
    CUSTOMER_SUCCESS = "customer_success"
    RENEWAL_EXPANSION = "renewal_expansion"


class ObjectiveType(StrEnum):
    REVENUE = "revenue"
    STRATEGIC_PARTNERSHIP = "strategic_partnership"
    CO_MARKETING = "co_marketing"
    MARKET_ENTRY = "market_entry"
    CHANNEL_GROWTH = "channel_growth"
    SERVICE_EXCHANGE = "service_exchange"
    B2G_READINESS = "b2g_readiness"
    RETENTION = "retention"
    EXPANSION = "expansion"


class RelationshipType(StrEnum):
    PROSPECT = "prospect"
    CUSTOMER = "customer"
    STRATEGIC_PARTNER = "strategic_partner"
    REFERRAL_PARTNER = "referral_partner"
    CHANNEL_PARTNER = "channel_partner"
    DISTRIBUTOR = "distributor"
    IMPLEMENTATION_PARTNER = "implementation_partner"
    TECHNOLOGY_PARTNER = "technology_partner"
    CO_MARKETING_PARTNER = "co_marketing_partner"
    SERVICE_EXCHANGE_PARTNER = "service_exchange_partner"
    SUPPLIER_VENDOR = "supplier_vendor"
    INVESTOR_LENDER = "investor_lender"
    GOVERNMENT_PROCUREMENT = "government_procurement"


class PermissionStatus(StrEnum):
    UNKNOWN = "unknown"
    RESEARCH_ONLY = "research_only"
    WARM_INTRO = "warm_intro"
    OPTED_IN = "opted_in"
    EXISTING_RELATIONSHIP = "existing_relationship"
    EXPLICIT_APPROVAL = "explicit_approval"
    OPTED_OUT = "opted_out"


CONTACTABLE_PERMISSION_STATUSES = frozenset(
    {
        PermissionStatus.WARM_INTRO,
        PermissionStatus.OPTED_IN,
        PermissionStatus.EXISTING_RELATIONSHIP,
        PermissionStatus.EXPLICIT_APPROVAL,
    }
)


class LifecycleStage(StrEnum):
    RESEARCH = "research"
    QUALIFIED = "qualified"
    STRATEGY_READY = "strategy_ready"
    AWAITING_APPROVAL = "awaiting_approval"
    CONTACTED = "contacted"
    ENGAGED = "engaged"
    MEETING_SCHEDULED = "meeting_scheduled"
    NEGOTIATING = "negotiating"
    PROPOSAL = "proposal"
    ACTIVE = "active"
    WON = "won"
    LOST = "lost"
    PAUSED = "paused"


class ActionMode(StrEnum):
    INTERNAL = "internal"
    DRAFT_ONLY = "draft_only"
    APPROVAL_REQUIRED = "approval_required"
    BLOCKED = "blocked"


class Channel(StrEnum):
    INTERNAL = "internal"
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    LINKEDIN_MANUAL = "linkedin_manual"
    PHONE = "phone"
    MEETING = "meeting"
    CALENDAR = "calendar"
    DOCUMENT = "document"


class OfferType(StrEnum):
    OPPORTUNITY_SNAPSHOT = "opportunity_snapshot"
    REVENUE_PROOF_SPRINT = "revenue_proof_sprint"
    REVENUE_COMMAND_PILOT = "revenue_command_pilot"
    SAUDI_MARKET_ACCESS_SPRINT = "saudi_market_access_sprint"
    B2G_READINESS_SPRINT = "b2g_readiness_sprint"
    PARTNER_DISTRIBUTOR_DESK = "partner_distributor_desk"
    CO_MARKETING_SPRINT = "co_marketing_sprint"
    SERVICE_EXCHANGE_PILOT = "service_exchange_pilot"
    AI_COMPANY_OS_SETUP = "ai_company_os_setup"
    CUSTOMER_SUCCESS_REVIEW = "customer_success_review"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"


class ApprovalOption(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"
    EDIT = "edit"


def _required(value: str, field_name: str) -> str:
    normalized = " ".join(value.strip().split())
    if not normalized:
        raise ValueError(f"{field_name} is required")
    return normalized


def _score(value: int, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")
    if not 0 <= value <= 100:
        raise ValueError(f"{field_name} must be between 0 and 100")
    return value


@dataclass(frozen=True)
class CommercialObjective:
    tenant_id: str
    department: Department
    objective_type: ObjectiveType
    title: str
    success_metric: str
    objective_id: str = field(default_factory=lambda: f"obj_{uuid4().hex[:12]}")
    description: str = ""
    priority: int = 50
    status: str = "active"
    policy: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "tenant_id", _required(self.tenant_id, "tenant_id"))
        object.__setattr__(self, "title", _required(self.title, "title"))
        object.__setattr__(self, "success_metric", _required(self.success_metric, "success_metric"))
        object.__setattr__(self, "priority", _score(self.priority, "priority"))
        if self.status not in {"draft", "active", "paused", "completed", "cancelled"}:
            raise ValueError("unsupported objective status")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["department"] = self.department.value
        payload["objective_type"] = self.objective_type.value
        return payload


@dataclass(frozen=True)
class ValueExchange:
    tenant_gives: tuple[str, ...]
    tenant_receives: tuple[str, ...]
    counterparty_gives: tuple[str, ...] = ()
    counterparty_receives: tuple[str, ...] = ()
    cash_component_sar: int | None = None
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.tenant_gives:
            raise ValueError("tenant_gives must contain at least one value item")
        if not self.tenant_receives:
            raise ValueError("tenant_receives must contain at least one value item")
        if self.cash_component_sar is not None:
            if isinstance(self.cash_component_sar, bool) or not isinstance(self.cash_component_sar, int):
                raise TypeError("cash_component_sar must be an integer or null")
            if self.cash_component_sar < 0:
                raise ValueError("cash_component_sar must be non-negative")

    @property
    def is_service_exchange(self) -> bool:
        return self.cash_component_sar in {None, 0} and bool(self.counterparty_gives)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["is_service_exchange"] = self.is_service_exchange
        return payload


@dataclass(frozen=True)
class RelationshipContext:
    tenant_id: str
    account_id: str
    account_name: str
    objective: CommercialObjective
    relationship_type: RelationshipType
    permission_status: PermissionStatus
    relationship_id: str = field(default_factory=lambda: f"rel_{uuid4().hex[:12]}")
    lifecycle_stage: LifecycleStage = LifecycleStage.RESEARCH
    contact_id: str | None = None
    source_ref: str = ""
    allowed_use: str = "business_contact_research_only"
    strategic_fit_score: int = 50
    trust_score: int = 50
    urgency_score: int = 50
    evidence_refs: tuple[str, ...] = ()
    known_needs: tuple[str, ...] = ()
    known_capabilities: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        tenant_id = _required(self.tenant_id, "tenant_id")
        if tenant_id != self.objective.tenant_id:
            raise ValueError("relationship and objective must belong to the same tenant")
        object.__setattr__(self, "tenant_id", tenant_id)
        object.__setattr__(self, "account_id", _required(self.account_id, "account_id"))
        object.__setattr__(self, "account_name", _required(self.account_name, "account_name"))
        object.__setattr__(self, "strategic_fit_score", _score(self.strategic_fit_score, "strategic_fit_score"))
        object.__setattr__(self, "trust_score", _score(self.trust_score, "trust_score"))
        object.__setattr__(self, "urgency_score", _score(self.urgency_score, "urgency_score"))
        if self.permission_status is PermissionStatus.OPTED_OUT and self.lifecycle_stage not in {
            LifecycleStage.LOST,
            LifecycleStage.PAUSED,
            LifecycleStage.RESEARCH,
        }:
            raise ValueError("opted-out relationships cannot be active or contacted")

    @property
    def contact_permission_confirmed(self) -> bool:
        return self.permission_status in CONTACTABLE_PERMISSION_STATUSES

    @property
    def priority_score(self) -> int:
        score = round(
            self.strategic_fit_score * 0.45
            + self.trust_score * 0.25
            + self.urgency_score * 0.30
        )
        if not self.contact_permission_confirmed:
            score = min(score, 40)
        if self.permission_status is PermissionStatus.OPTED_OUT:
            return 0
        return max(0, min(100, score))

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["objective"] = self.objective.to_dict()
        payload["relationship_type"] = self.relationship_type.value
        payload["permission_status"] = self.permission_status.value
        payload["lifecycle_stage"] = self.lifecycle_stage.value
        payload["contact_permission_confirmed"] = self.contact_permission_confirmed
        payload["priority_score"] = self.priority_score
        return payload


@dataclass(frozen=True)
class StrategicOffer:
    offer_type: OfferType
    title: str
    value_exchange: ValueExchange
    scope: tuple[str, ...]
    proof_requirements: tuple[str, ...]
    success_metric: str
    term_notes: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "title", _required(self.title, "title"))
        object.__setattr__(self, "success_metric", _required(self.success_metric, "success_metric"))
        if not self.scope:
            raise ValueError("offer scope is required")
        if not self.proof_requirements:
            raise ValueError("proof requirements are required")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["offer_type"] = self.offer_type.value
        payload["value_exchange"] = self.value_exchange.to_dict()
        return payload


@dataclass(frozen=True)
class StrategicRecommendation:
    tenant_id: str
    relationship_id: str
    department: Department
    objective_type: ObjectiveType
    relationship_type: RelationshipType
    recommended_offer: StrategicOffer
    rationale: tuple[str, ...]
    negotiation_posture: str
    objections_to_expect: tuple[str, ...]
    red_lines: tuple[str, ...]
    next_move: str
    recommended_channel: Channel
    requires_approval: bool
    external_action_allowed: bool = False

    def __post_init__(self) -> None:
        if self.external_action_allowed:
            raise ValueError("commercial recommendations cannot authorize external execution")
        if self.recommended_channel is not Channel.INTERNAL and not self.requires_approval:
            raise ValueError("external-channel recommendations require approval")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["department"] = self.department.value
        payload["objective_type"] = self.objective_type.value
        payload["relationship_type"] = self.relationship_type.value
        payload["recommended_offer"] = self.recommended_offer.to_dict()
        payload["recommended_channel"] = self.recommended_channel.value
        return payload


@dataclass(frozen=True)
class ActionEnvelope:
    tenant_id: str
    department: Department
    relationship_id: str
    account_id: str
    action_type: str
    action_mode: ActionMode
    channel: Channel
    summary_ar: str
    rationale: str
    risk_level: RiskLevel
    proof_target: str
    opportunity_id: str | None = None
    contact_id: str | None = None
    meeting_plan_id: str | None = None
    draft_payload: dict[str, Any] = field(default_factory=dict)
    evidence_refs: tuple[str, ...] = ()
    approval_options: tuple[ApprovalOption, ...] = (
        ApprovalOption.APPROVE,
        ApprovalOption.REJECT,
        ApprovalOption.EDIT,
    )
    action_id: str = field(default_factory=lambda: f"act_{uuid4().hex[:12]}")
    external_action_allowed: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        object.__setattr__(self, "tenant_id", _required(self.tenant_id, "tenant_id"))
        object.__setattr__(self, "relationship_id", _required(self.relationship_id, "relationship_id"))
        object.__setattr__(self, "account_id", _required(self.account_id, "account_id"))
        object.__setattr__(self, "action_type", _required(self.action_type, "action_type"))
        object.__setattr__(self, "summary_ar", _required(self.summary_ar, "summary_ar"))
        object.__setattr__(self, "rationale", _required(self.rationale, "rationale"))
        object.__setattr__(self, "proof_target", _required(self.proof_target, "proof_target"))
        if self.external_action_allowed:
            raise ValueError("action envelopes cannot authorize external execution")
        if self.channel is Channel.INTERNAL and self.action_mode is ActionMode.APPROVAL_REQUIRED:
            raise ValueError("purely internal actions should not require external approval")
        if self.channel is not Channel.INTERNAL and self.action_mode not in {
            ActionMode.DRAFT_ONLY,
            ActionMode.APPROVAL_REQUIRED,
            ActionMode.BLOCKED,
        }:
            raise ValueError("external-channel actions must be draft-only, approval-required, or blocked")

    @property
    def is_external(self) -> bool:
        return self.channel is not Channel.INTERNAL

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["department"] = self.department.value
        payload["action_mode"] = self.action_mode.value
        payload["channel"] = self.channel.value
        payload["risk_level"] = self.risk_level.value
        payload["approval_options"] = [option.value for option in self.approval_options]
        payload["created_at"] = self.created_at.isoformat()
        payload["is_external"] = self.is_external
        return payload


@dataclass(frozen=True)
class MeetingPlan:
    tenant_id: str
    relationship_id: str
    account_id: str
    department: Department
    objective: str
    agenda: tuple[str, ...]
    discovery_questions: tuple[str, ...]
    negotiation_plan: tuple[str, ...]
    required_evidence: tuple[str, ...]
    participants: tuple[str, ...] = ()
    proposed_slots: tuple[str, ...] = ()
    opportunity_id: str | None = None
    meeting_plan_id: str = field(default_factory=lambda: f"mtp_{uuid4().hex[:12]}")
    booking_requires_approval: bool = True
    external_action_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "tenant_id", _required(self.tenant_id, "tenant_id"))
        object.__setattr__(self, "relationship_id", _required(self.relationship_id, "relationship_id"))
        object.__setattr__(self, "account_id", _required(self.account_id, "account_id"))
        object.__setattr__(self, "objective", _required(self.objective, "objective"))
        if not self.agenda or not self.discovery_questions or not self.required_evidence:
            raise ValueError("meeting plan requires agenda, discovery questions, and evidence")
        if self.external_action_allowed:
            raise ValueError("meeting plans cannot book or invite externally")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["department"] = self.department.value
        return payload
