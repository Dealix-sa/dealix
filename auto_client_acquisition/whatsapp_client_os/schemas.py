"""Schemas for the Dealix WhatsApp Client OS (client-facing).

This is the client-facing WhatsApp operating surface (distinct from the
internal, founder-only ``whatsapp_decision_bot``). It models a governed,
menu-driven business workflow assistant — never a general-purpose chatbot.

Doctrine (non-negotiable, enforced in code + tests):
- No API keys / secrets requested in WhatsApp text (use a secure portal link).
- No cold WhatsApp, no LinkedIn automation, no scraping.
- Human approval for any external commitment; human handoff for ambiguity,
  sensitive data, pricing, contracts and complaints.
- Every recommendation is tied to the product catalog and an evidence level.
- All actions are logged.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# ── Permission ladder L0–L5 ──────────────────────────────────────────────
PermissionLevel = Literal["L0", "L1", "L2", "L3", "L4", "L5"]

# ── Conversation stages (state machine) ──────────────────────────────────
SessionStage = Literal[
    "new",
    "menu",
    "assessment_in_progress",
    "assessment_complete",
    "recommendation",
    "permission_request",
    "awaiting_secure_input",
    "draft_review",
    "proposal",
    "payment_handoff",
    "onboarding",
    "support",
    "human_handoff",
    "closed",
]

# ── Intents (deterministic; never free-form LLM dispatch) ────────────────
ClientIntent = Literal[
    "welcome",
    "diagnose",
    "campaign_followup",
    "connect_tools",
    "review_report",
    "support",
    "not_sure",  # «ما أعرف — اقترح علي»
    "send_file_link",
    "assessment_start",
    "assessment_answer",
    "approve",
    "reject",
    "edit",
    "simplify",
    "permission_grant",
    "permission_deny",
    "request_proposal",
    "book_call",
    "human_handoff",
    "blocked_unsafe",
    "unknown",
]

CardKind = Literal["menu", "action", "approval", "permission", "recommendation", "report"]
RiskLevel = Literal["low", "medium", "high"]

# Evidence levels mirror the platform Decision Passport (L0–L5).
EvidenceLevel = Literal["L0", "L1", "L2", "L3", "L4", "L5"]

MessageDirection = Literal["inbound", "outbound"]


class CardOption(BaseModel):
    """A single tappable option/button on a card.

    ``intent`` is the deterministic intent the option maps to; ``id`` is the
    stable button id used in WhatsApp interactive payloads.
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    label_ar: str
    intent: ClientIntent = "unknown"
    payload: dict[str, Any] = Field(default_factory=dict)


class ClientCard(BaseModel):
    """A logical card rendered to the client (menu / action / approval / …).

    Every card carries an explicit ``requires_approval`` flag and an
    ``evidence_level`` so no claim or external action escapes governance.
    """

    model_config = ConfigDict(extra="forbid")

    card_id: str
    kind: CardKind
    title_ar: str
    body_ar: str = ""
    reason_ar: str = ""
    options: list[CardOption] = Field(default_factory=list, max_length=10)
    risk: RiskLevel = "low"
    evidence_level: EvidenceLevel = "L0"
    requires_approval: bool = False
    catalog_ref: str = ""  # product/offer this card is tied to
    safety_summary: str = "no_live_send_no_secrets_in_chat"


class IntentResult(BaseModel):
    """Outcome of deterministic intent classification."""

    model_config = ConfigDict(extra="forbid")

    intent: ClientIntent
    confidence: float = 1.0
    matched: list[str] = Field(default_factory=list)
    requires_human: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    raw_text: str = ""


class InboundMessage(BaseModel):
    """A normalized inbound WhatsApp message (the API/webhook intake envelope).

    Exactly one of ``text`` or ``button_id`` is meaningful per turn. Secrets
    must never be sent here — the policy guard blocks and refuses to store them.
    """

    model_config = ConfigDict(extra="forbid")

    client_handle: str = Field(..., min_length=1)
    text: str = ""
    button_id: str = ""
    company_name: str = ""
    session_id: str = ""
    locale: Literal["ar", "en"] = "ar"
    is_complaint: bool = False


class WhatsAppSession(BaseModel):
    """A governed client session. Tenant-scoped by ``client_handle``."""

    model_config = ConfigDict(extra="forbid")

    session_id: str
    client_handle: str  # phone handle / opaque id (never raw PII in logs)
    company_name: str = ""
    locale: Literal["ar", "en"] = "ar"
    stage: SessionStage = "new"
    permission_level: PermissionLevel = "L0"
    last_intent: ClientIntent = "welcome"
    assessment_id: str = ""
    message_count: int = 0
    handoff_requested: bool = False
    consent_record_exists: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    meta: dict[str, Any] = Field(default_factory=dict)


# ── Permissions ──────────────────────────────────────────────────────────
class PermissionRequest(BaseModel):
    """A single permission the client is asked to grant."""

    model_config = ConfigDict(extra="forbid")

    permission_id: str
    level: PermissionLevel
    system: str = ""  # e.g. "HubSpot", "Calendar"
    scope: str = ""  # e.g. "read contacts"
    purpose_ar: str = ""
    risk: RiskLevel = "low"
    duration_days: int = 30
    secure_portal_required: bool = False
    manual_alternative_ar: str = ""


class PermissionGrant(BaseModel):
    """A recorded grant/deny decision (audit row)."""

    model_config = ConfigDict(extra="forbid")

    permission_id: str
    client_handle: str
    level: PermissionLevel
    granted: bool
    via_secure_portal: bool = False
    decided_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    note: str = ""


# ── Readiness assessment («Dealix Company Readiness Scan») ───────────────
AssessmentAxis = Literal[
    "lead_flow",
    "channel_chaos",
    "follow_up",
    "crm",
    "decision_maker",
    "offer_clarity",
    "reporting",
    "automation_readiness",
    "compliance_privacy",
    "urgency",
]


class AssessmentAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    axis: AssessmentAxis
    option_id: str
    score: int = Field(ge=0, le=10)


class ReadinessScore(BaseModel):
    """Three pillar sub-scores + overall, on a 0–100 scale."""

    model_config = ConfigDict(extra="forbid")

    revenue_readiness: int = Field(ge=0, le=100)
    follow_up_maturity: int = Field(ge=0, le=100)
    automation_readiness: int = Field(ge=0, le=100)
    overall: int = Field(ge=0, le=100)
    risk: RiskLevel = "medium"


class ClientAssessment(BaseModel):
    """A completed (or in-progress) readiness scan + its recommendation."""

    model_config = ConfigDict(extra="forbid")

    assessment_id: str
    client_handle: str
    company_name: str = ""
    answers: list[AssessmentAnswer] = Field(default_factory=list)
    score: ReadinessScore | None = None
    recommended_offer: str = ""  # service_catalog id, e.g. "free_mini_diagnostic"
    recommended_offer_ar: str = ""
    rationale_ar: list[str] = Field(default_factory=list)
    first_workflow_ar: str = ""
    required_permissions: list[str] = Field(default_factory=list)
    next_action_ar: str = ""
    evidence_level: EvidenceLevel = "L1"
    completed: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# ── Human handoff ────────────────────────────────────────────────────────
HandoffReason = Literal[
    "ambiguity",
    "sensitive_data",
    "pricing_negotiation",
    "contract",
    "complaint",
    "explicit_request",
    "permission_l5",
    "secrets_attempt",
    "repeated_unknown",
]


class HandoffRequest(BaseModel):
    """An escalation packet handed to a human (founder/CSM) with full context."""

    model_config = ConfigDict(extra="forbid")

    handoff_id: str
    session_id: str
    client_handle: str
    reason: HandoffReason
    summary_ar: str = ""
    last_messages: list[str] = Field(default_factory=list, max_length=10)
    suggested_action_ar: str = ""
    urgency: RiskLevel = "medium"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    safety_summary: str = "context_preserved_no_pii_in_logs"


__all__ = [
    "AssessmentAnswer",
    "AssessmentAxis",
    "CardKind",
    "CardOption",
    "ClientAssessment",
    "ClientCard",
    "ClientIntent",
    "EvidenceLevel",
    "HandoffReason",
    "HandoffRequest",
    "InboundMessage",
    "IntentResult",
    "MessageDirection",
    "PermissionGrant",
    "PermissionLevel",
    "PermissionRequest",
    "ReadinessScore",
    "RiskLevel",
    "SessionStage",
    "WhatsAppSession",
]
