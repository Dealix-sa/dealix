"""Market Production OS — canonical dataclasses + enums.

This module defines the value objects that flow through the governed
market-production pipeline (prospect -> signal -> draft -> approval ->
ramped send -> reply). It carries *no* business logic and *no* I/O so it
can be imported anywhere without side effects.

Doctrine reminders encoded here:
  - Every :class:`OutreachDraft` defaults to ``send_status="draft"``.
    Nothing in this layer constructs a draft already marked ``"sent"``.
  - Every draft carries ``governance_decision`` (set by the quality gate)
    so no output object leaves the layer without a recorded decision.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import IntEnum, StrEnum


class ProspectState(StrEnum):
    """Lifecycle of a researched company/contact."""

    RESEARCHED = "researched"
    QUALIFIED = "qualified"
    DRAFT_READY = "draft_ready"
    DRAFTED = "drafted"
    APPROVED = "approved"
    SENT = "sent"
    REPLIED = "replied"
    MEETING_BOOKED = "meeting_booked"
    PROPOSAL_NEEDED = "proposal_needed"
    PROPOSAL_SENT = "proposal_sent"
    WON = "won"
    LOST = "lost"
    NURTURE = "nurture"
    DO_NOT_CONTACT = "do_not_contact"


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REWRITE = "rewrite"
    NURTURE = "nurture"
    DO_NOT_CONTACT = "do_not_contact"


class SendStatus(StrEnum):
    """``DRAFT`` is the only value the factory ever assigns. ``SENT`` is set
    exclusively by a human-approved send path that lives outside this layer."""

    DRAFT = "draft"
    QUEUED = "queued"
    SENT = "sent"
    SUPPRESSED = "suppressed"
    BOUNCED = "bounced"


class ComplianceStatus(StrEnum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PersonalizationLevel(IntEnum):
    """P0 sector-only .. P4 bespoke proof/offer. Drafts below P1 are rejected."""

    P0 = 0
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4


class DraftKind(StrEnum):
    FIRST_TOUCH = "first_touch"
    FOLLOW_UP_1 = "follow_up_1"
    FOLLOW_UP_2 = "follow_up_2"
    PROPOSAL_INTRO = "proposal_intro"
    CLOSE_LOOP = "close_loop"


class ReplyClass(StrEnum):
    POSITIVE = "positive"
    INTERESTED_LATER = "interested_later"
    PRICE_QUESTION = "price_question"
    SEND_MORE_INFO = "send_more_info"
    WRONG_PERSON = "wrong_person"
    NOT_INTERESTED = "not_interested"
    UNSUBSCRIBE = "unsubscribe"
    ANGRY = "angry"
    AUTO_REPLY = "auto_reply"
    BOUNCE = "bounce"


class SignalKind(StrEnum):
    JOB_POSTING = "job_posting"
    WEBSITE = "website"
    CONTENT = "content"
    CAMPAIGN_LAUNCH = "campaign_launch"
    CAREERS_PAGE = "careers_page"


@dataclass(frozen=True, slots=True)
class Prospect:
    """A researched company/contact with a declared lawful source.

    ``source`` records *how* the prospect was found. Forbidden sources
    (scraping / purchased_list / cold_whatsapp / linkedin_automation) are
    rejected downstream by the quality gate via Revenue OS anti-waste.
    """

    prospect_id: str
    company: str
    sector: str
    recipient_role: str = ""
    source: str = "founder_supplied"
    region: str = "Saudi Arabia"
    score: int = 0
    state: str = ProspectState.RESEARCHED.value
    notes: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class OutreachDraft:
    """A governed cold-email draft. Never auto-sent."""

    draft_id: str
    prospect_id: str
    company: str
    sector: str
    recipient_role: str
    source: str
    kind: str
    pain_hypothesis: str
    personalization_note: str
    personalization_level: int
    offer: str
    subject: str
    body: str
    cta: str
    language: str = "ar"
    evidence_level: int = 1
    unsubscribe_included: bool = True
    risk_level: str = RiskLevel.MEDIUM.value
    compliance_status: str = ComplianceStatus.PENDING.value
    approval_status: str = ApprovalStatus.PENDING.value
    send_status: str = SendStatus.DRAFT.value
    governance_decision: str = "PENDING"
    gate_reasons: tuple[str, ...] = ()
    created_at: str = ""

    def to_dict(self) -> dict[str, object]:
        d = asdict(self)
        d["gate_reasons"] = list(self.gate_reasons)
        return d


@dataclass(frozen=True, slots=True)
class BuyingSignal:
    """A buying signal sourced from public/founder-supplied observation."""

    signal_id: str
    company: str
    sector: str
    kind: str
    detail: str
    matched_offer: str = ""
    source: str = "founder_supplied"
    detected_at: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Reply:
    """An inbound reply to an approved, sent message."""

    reply_id: str
    draft_id: str
    prospect_id: str
    text: str
    reply_class: str = ""
    next_action: str = ""
    suppress: bool = False
    received_at: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class SuppressionEntry:
    """An address/company that asked not to be contacted (permanent)."""

    email: str
    reason: str
    suppressed_at: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class SendingBatch:
    """A founder-approved, ramp-capped sending batch plan (plan only)."""

    batch_id: str
    week: int
    approved_count: int
    ramp_cap: int
    planned_sends: int
    domain_health_ok: bool
    reasons: tuple[str, ...] = ()
    created_at: str = ""

    def to_dict(self) -> dict[str, object]:
        d = asdict(self)
        d["reasons"] = list(self.reasons)
        return d


@dataclass(frozen=True, slots=True)
class ApprovalAction:
    """A founder decision recorded against a draft."""

    action_id: str
    draft_id: str
    decision: str
    note: str = ""
    decided_at: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


__all__ = [
    "ApprovalAction",
    "ApprovalStatus",
    "BuyingSignal",
    "ComplianceStatus",
    "DraftKind",
    "OutreachDraft",
    "PersonalizationLevel",
    "Prospect",
    "ProspectState",
    "Reply",
    "ReplyClass",
    "RiskLevel",
    "SendStatus",
    "SendingBatch",
    "SignalKind",
    "SuppressionEntry",
]
