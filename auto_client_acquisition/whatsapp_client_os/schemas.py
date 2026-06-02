"""WhatsApp Client OS — schemas.

Frozen dataclasses + StrEnums for the client-facing WhatsApp operating
experience: sessions, message events, action cards, flow state, readiness
assessments, and permissions.

Doctrine (enforced elsewhere by tests):
- No raw PII in any persisted record. Sessions store ``wa_id_hash`` (a
  truncated SHA-256 of the WhatsApp id), never the raw phone number, and
  message text is redacted before persistence.
- Every client-facing action object carries a ``governance_decision``.
- No live external send originates here; the layer is preview/draft/approval
  only.
"""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def hash_wa_id(wa_id: str) -> str:
    """Stable, non-reversible handle for a WhatsApp id. Never store raw phone."""
    digest = hashlib.sha256(wa_id.strip().encode("utf-8")).hexdigest()
    return f"wa_{digest[:16]}"


class PermissionLevel(StrEnum):
    """Graduated permission ladder. L5 never granted over WhatsApp text."""

    L0_CHAT_ONLY = "L0"
    L1_CLIENT_UPLOAD = "L1"
    L2_CRM_READ = "L2"
    L3_CREATE_DRAFTS = "L3"
    L4_SEND_AFTER_APPROVAL = "L4"
    L5_SENSITIVE = "L5"


def permission_rank(level: PermissionLevel | str) -> int:
    value = level.value if isinstance(level, PermissionLevel) else str(level)
    try:
        return int(value.lstrip("Ll"))
    except ValueError:
        return 0


class FlowId(StrEnum):
    """The controlled business flows. WhatsApp is flows, not open chat."""

    NEW_CLIENT_WELCOME = "new_client_welcome"
    READINESS_SCAN = "readiness_scan"
    SERVICE_RECOMMENDATION = "service_recommendation"
    PERMISSION_COLLECTION = "permission_collection"
    DRAFT_REVIEW = "draft_review"
    PROPOSAL_REVIEW = "proposal_review"
    PROOF_PACK_DELIVERY = "proof_pack_delivery"
    PAYMENT_HANDOFF = "payment_handoff"
    ONBOARDING = "onboarding"
    WEEKLY_REPORT = "weekly_report"
    SUPPORT_HANDOFF = "support_handoff"
    RENEWAL_UPSELL = "renewal_upsell"


class Intent(StrEnum):
    """Deterministic intent classes the router can emit."""

    WELCOME = "welcome"
    START_SCAN = "start_scan"
    RECOMMEND_ME = "recommend_me"  # "ما أعرف — اقترح علي"
    VIEW_SERVICES = "view_services"
    REVIEW_PROPOSAL = "review_proposal"
    REVIEW_DRAFT = "review_draft"
    BUILD_FOLLOWUP = "build_followup"
    GIVE_PERMISSION = "give_permission"
    PROOF_PACK = "proof_pack"
    START_PAYMENT = "start_payment"
    RENEWAL = "renewal"
    REQUEST_SUPPORT = "request_support"
    REQUEST_HUMAN = "request_human"
    UNKNOWN = "unknown"
    BLOCKED_UNSAFE = "blocked_unsafe"


class ActionCardKind(StrEnum):
    RECOMMENDATION = "recommendation"
    APPROVAL = "approval"
    PERMISSION = "permission"
    PROPOSAL = "proposal"
    PROOF_PACK = "proof_pack"
    PAYMENT_HANDOFF = "payment_handoff"
    ONBOARDING = "onboarding"
    SUPPORT_ESCALATION = "support_escalation"
    RENEWAL = "renewal"


class HandoffReason(StrEnum):
    ANGRY = "angry"
    PRICING_COMMITMENT = "pricing_commitment"
    LEGAL_CONTRACT = "legal_contract"
    SENSITIVE_DATA = "sensitive_data"
    DATA_DELETION = "data_deletion"
    DISSATISFIED = "dissatisfied"
    LOW_CONFIDENCE = "low_confidence"
    LOOP_LIMIT = "loop_limit"
    EXPLICIT_REQUEST = "explicit_request"


class SupportCategory(StrEnum):
    TECHNICAL = "technical"
    DATA = "data"
    REPORT = "report"
    DRAFT_QUALITY = "draft_quality"
    PERMISSION = "permission"
    BILLING = "billing"
    URGENT_COMPLAINT = "urgent_complaint"
    GENERAL = "general"


class EvidenceLevel(StrEnum):
    """L0-L5 evidence ladder, mirrored from the Decision Passport product."""

    L0 = "L0"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"
    L5 = "L5"


@dataclass(frozen=True, slots=True)
class ClientSession:
    session_id: str = field(default_factory=lambda: f"wsx_{uuid4().hex[:12]}")
    wa_id_hash: str = ""
    company: str = ""
    current_flow: str = FlowId.NEW_CLIENT_WELCOME.value
    permission_level: str = PermissionLevel.L0_CHAT_ONLY.value
    last_intent: str = Intent.WELCOME.value
    turn_count: int = 0
    handoff_open: bool = False
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class MessageEvent:
    event_id: str = field(default_factory=lambda: f"wmsg_{uuid4().hex[:12]}")
    session_id: str = ""
    direction: str = "inbound"  # inbound | outbound
    intent: str = Intent.UNKNOWN.value
    text_redacted: str = ""  # PII-redacted before persistence
    card_id: str = ""
    occurred_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ActionCard:
    card_id: str = field(default_factory=lambda: f"card_{uuid4().hex[:12]}")
    session_id: str = ""
    kind: str = ActionCardKind.RECOMMENDATION.value
    title_ar: str = ""
    title_en: str = ""
    body_ar: str = ""
    body_en: str = ""
    options: tuple[dict[str, str], ...] = ()
    evidence_level: str = EvidenceLevel.L0.value
    risk: str = "low"  # low | medium | high
    governance_decision: str = ""
    created_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["options"] = [dict(o) for o in self.options]
        return data


@dataclass(frozen=True, slots=True)
class FlowState:
    session_id: str = ""
    flow: str = FlowId.NEW_CLIENT_WELCOME.value
    step: str = "start"
    answers: dict[str, str] = field(default_factory=dict)
    completed: bool = False
    next_action: str = ""
    updated_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ClientAssessment:
    assessment_id: str = field(default_factory=lambda: f"asmt_{uuid4().hex[:12]}")
    session_id: str = ""
    company: str = ""
    axis_scores: dict[str, int] = field(default_factory=dict)
    revenue_readiness: int = 0
    follow_up_maturity: int = 0
    automation_readiness: int = 0
    risk: str = "medium"
    recommended_offer_id: str = ""
    recommendation_reason_ar: str = ""
    recommendation_reason_en: str = ""
    plan_steps_ar: tuple[str, ...] = ()
    evidence_level: str = EvidenceLevel.L1.value
    governance_decision: str = ""
    created_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["plan_steps_ar"] = list(self.plan_steps_ar)
        return data


@dataclass(frozen=True, slots=True)
class ClientPermission:
    permission_id: str = field(default_factory=lambda: f"perm_{uuid4().hex[:12]}")
    session_id: str = ""
    level: str = PermissionLevel.L0_CHAT_ONLY.value
    scopes: tuple[str, ...] = ()
    granted_via: str = "whatsapp"  # whatsapp | secure_portal
    integration: str = ""
    audit_ref: str = ""
    governance_decision: str = ""
    created_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["scopes"] = list(self.scopes)
        return data


__all__ = [
    "ActionCard",
    "ActionCardKind",
    "ClientAssessment",
    "ClientPermission",
    "ClientSession",
    "EvidenceLevel",
    "FlowId",
    "FlowState",
    "HandoffReason",
    "Intent",
    "MessageEvent",
    "PermissionLevel",
    "SupportCategory",
    "hash_wa_id",
    "permission_rank",
]
