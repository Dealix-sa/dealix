"""Typed data models for the Dealix Commercial Growth OS v2.

Every commercial artefact — accounts, growth cards, replies, negotiation
drafts, booking options, proposal briefs, follow-up tasks, pipeline events,
delivery handoffs and the command-room snapshot — is represented here as a
dataclass with a stable ``to_dict`` serialisation.

These models carry *no behaviour and no side effects*. They never send,
never write to a calendar, and never finalise pricing. Safety enforcement
lives in :mod:`app.commercial.safety`; intelligence lives in the dedicated
desk modules.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

# ── Controlled vocabularies ───────────────────────────────────────────────────

COMMERCIAL_MOTIONS = (
    "sales_prospecting",
    "partnership_outreach",
    "proposal_push",
    "revival",
    "upsell",
    "retention",
    "referral",
    "renewal",
    "customer_success_expansion",
    "market_watch",
)

CHANNELS = (
    "email",
    "whatsapp",
    "linkedin_manual",
    "phone",
    "partner_referral",
    "website_form",
)

PIPELINE_STAGES = (
    "researched",
    "verified",
    "drafted",
    "reviewed",
    "approved",
    "sent",
    "replied",
    "meeting_ready",
    "meeting_booked",
    "proposal_ready",
    "proposal_sent",
    "negotiating",
    "won",
    "lost",
    "nurture",
    "delivery_handoff",
)

# Stage transitions that may never happen without explicit human approval.
APPROVAL_GATED_STAGES = (
    "approved",
    "sent",
    "proposal_sent",
    "won",
    "lost",
    "delivery_handoff",
)

REPLY_TYPES = (
    "interested",
    "send_details",
    "price_objection",
    "not_now",
    "no_interest",
    "wrong_person",
    "referral",
    "partnership_interest",
    "contract_request",
    "meeting_request",
    "support_question",
    "unsubscribe",
    "unknown",
)

RISK_LEVELS = ("low", "medium", "high")


def _to_dict(obj: Any) -> Any:
    """Recursively serialise dataclasses to plain JSON-friendly dicts."""
    return asdict(obj)


# ── Core entities ──────────────────────────────────────────────────────────────


@dataclass
class CommercialAccount:
    account_id: str
    company_name: str
    sector: str = ""
    city: str = ""
    website: str = ""
    source_url: str = ""
    source_type: str = ""  # client_provided | public_website | partner | referral
    verification_status: str = "unverified"  # unverified | verified | rejected
    contactability_status: str = "unknown"  # unknown | contactable | blocked | opted_out
    public_email: str = ""
    whatsapp: str = ""
    phone: str = ""
    linkedin_url: str = ""
    pain_hypothesis: str = ""
    icp_score: float = 0.0
    recommended_motion: str = ""
    recommended_product: str = ""
    owner: str = "unassigned"
    risk_level: str = "medium"
    # opt-in state used by safety gates
    whatsapp_opt_in: bool = False
    email_opt_out: bool = False

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass
class GrowthCard:
    card_id: str
    account_id: str
    motion: str
    recommended_channel: str
    draft_message_ar: str = ""
    draft_message_en: str = ""
    buttons: list[str] = field(default_factory=list)
    owner_decision: str = "pending"  # pending | send | book | hold | discard
    approval_required: bool = True
    send_status: str = "draft"  # draft | approved | sent | blocked
    next_action: str = ""
    risk_level: str = "medium"

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass
class ReplyClassification:
    reply_id: str
    card_id: str
    reply_type: str
    sentiment: str  # positive | neutral | negative
    intent: str
    recommended_action: str
    risk_level: str = "low"

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass
class NegotiationDraft:
    negotiation_id: str
    card_id: str
    objection_type: str
    allowed_response: str
    forbidden_commitments: list[str] = field(default_factory=list)
    scope_adjustment_options: list[str] = field(default_factory=list)
    approval_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass
class BookingOption:
    booking_id: str
    card_id: str
    duration_minutes: int = 30
    timezone: str = "Asia/Riyadh"
    suggested_slots: list[str] = field(default_factory=list)
    agenda: list[str] = field(default_factory=list)
    attendees: list[str] = field(default_factory=list)
    preparation_notes: list[str] = field(default_factory=list)
    calendar_write_enabled: bool = False
    booking_status: str = "proposed"  # proposed | confirmed | booked | declined

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass
class ProposalBrief:
    proposal_id: str
    card_id: str
    package_name: str
    scope: list[str] = field(default_factory=list)
    deliverables: list[str] = field(default_factory=list)
    timeline: str = ""
    pricing_range_sar: str = ""
    out_of_scope: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    final_price_allowed: bool = False
    approval_required: bool = True
    status: str = "draft"  # draft | reviewed | approved | sent

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass
class FollowUpTask:
    task_id: str
    card_id: str
    due_in_days: int
    channel: str
    owner: str = "unassigned"
    draft_note: str = ""
    status: str = "open"  # open | done | skipped

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass
class PipelineEvent:
    event_id: str
    account_id: str
    stage: str
    previous_stage: str = ""
    next_stage: str = ""
    evidence: str = ""
    owner: str = "unassigned"
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass
class DeliveryHandoff:
    handoff_id: str
    account_id: str
    proposal_id: str = ""
    required_inputs: list[str] = field(default_factory=list)
    kickoff_agenda: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    proof_pack_plan: list[str] = field(default_factory=list)
    status: str = "pending_approval"  # pending_approval | ready | active

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass
class CommandRoomSnapshot:
    generated_at: str
    summary: dict[str, Any] = field(default_factory=dict)
    accounts: list[dict[str, Any]] = field(default_factory=list)
    cards: list[dict[str, Any]] = field(default_factory=list)
    replies: list[dict[str, Any]] = field(default_factory=list)
    negotiation_drafts: list[dict[str, Any]] = field(default_factory=list)
    booking_options: list[dict[str, Any]] = field(default_factory=list)
    proposal_briefs: list[dict[str, Any]] = field(default_factory=list)
    followup_tasks: list[dict[str, Any]] = field(default_factory=list)
    delivery_handoffs: list[dict[str, Any]] = field(default_factory=list)
    risks: list[dict[str, Any]] = field(default_factory=list)
    decision_queue: list[dict[str, Any]] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)
