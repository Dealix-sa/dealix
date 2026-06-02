"""Distribution OS data models — Prospect, Draft, Followup (deterministic, typed).

نماذج بيانات ماكينة التصريف. كل المخرجات مسودات تتطلب موافقة بشرية — لا إرسال خارجي.

Sending is never modelled here: there is intentionally **no** status that means
"sent automatically via an integration". A draft moves from ``generated`` /
``pending_approval`` to ``approved`` and then ``copied_manually`` only when a
human copies it and sends it themselves.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


def now_iso() -> str:
    """UTC ISO-8601 timestamp (single source so tests can monkeypatch)."""
    return datetime.now(UTC).isoformat()


class Channel(StrEnum):
    """Outreach channels. Every channel is manual — none implies automation."""

    EMAIL = "email"
    WHATSAPP_MANUAL = "whatsapp_manual"
    LINKEDIN_MANUAL = "linkedin_manual"
    PHONE_SCRIPT = "phone_script"
    PROPOSAL_PDF = "proposal_pdf"
    INTERNAL_NOTE = "internal_note"


#: Channels where a human must copy + send. Used by the quality gate to assert
#: the draft never carries an automated-send status.
MANUAL_SEND_CHANNELS: frozenset[Channel] = frozenset(
    {Channel.EMAIL, Channel.WHATSAPP_MANUAL, Channel.LINKEDIN_MANUAL, Channel.PHONE_SCRIPT}
)


class DraftType(StrEnum):
    OUTREACH_FIRST = "outreach_first"
    OUTREACH_FOLLOWUP_1 = "outreach_followup_1"
    OUTREACH_FOLLOWUP_2 = "outreach_followup_2"
    BREAKUP = "breakup"
    DISCOVERY_INVITE = "discovery_invite"
    DIAGNOSTIC_SUMMARY = "diagnostic_summary"
    PROPOSAL = "proposal"
    PROOF_PACK_INTRO = "proof_pack_intro"
    PAYMENT_FOLLOWUP = "payment_followup"
    ONBOARDING_MESSAGE = "onboarding_message"
    RENEWAL_UPSELL = "renewal_upsell"


class DraftStatus(StrEnum):
    """Lifecycle of a draft. No value represents an automated external send."""

    GENERATED = "generated"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    NEEDS_EDIT = "needs_edit"
    REJECTED = "rejected"
    COPIED_MANUALLY = "copied_manually"
    REPLIED = "replied"
    ARCHIVED = "archived"


#: Statuses a freshly generated draft may legitimately hold before a human acts.
QUEUEABLE_STATUSES: frozenset[DraftStatus] = frozenset(
    {DraftStatus.GENERATED, DraftStatus.PENDING_APPROVAL, DraftStatus.NEEDS_EDIT}
)


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Language(StrEnum):
    AR = "ar"
    EN = "en"


class ProspectStatus(StrEnum):
    NEW = "new"
    QUALIFIED = "qualified"
    DRAFTED = "drafted"
    CONTACTED = "contacted"
    REPLIED = "replied"
    DISCOVERY_BOOKED = "discovery_booked"
    PROPOSAL_SENT = "proposal_sent"
    WON = "won"
    LOST = "lost"
    NURTURE = "nurture"


class FollowupType(StrEnum):
    DAY_2 = "day_2"
    DAY_4 = "day_4"
    DAY_7 = "day_7"
    PROPOSAL_FOLLOWUP = "proposal_followup"
    PAYMENT_FOLLOWUP = "payment_followup"
    RENEWAL = "renewal"


class FollowupStatus(StrEnum):
    DUE = "due"
    SCHEDULED = "scheduled"
    DONE = "done"
    SKIPPED = "skipped"
    BLOCKED = "blocked"


#: Evidence levels mirror ``proof_engine.evidence.EvidenceLevel`` (L0–L5).
EVIDENCE_LEVELS: tuple[str, ...] = ("L0", "L1", "L2", "L3", "L4", "L5")


def _coerce(cls: type, data: dict[str, Any]) -> Any:
    """Build a dataclass from a dict, ignoring unknown keys (forward-compatible)."""
    known = {f.name for f in fields(cls)}
    return cls(**{k: v for k, v in data.items() if k in known})


@dataclass
class Prospect:
    """A target company at some stage of the distribution flow."""

    id: str
    company: str
    sector: str
    status: str = ProspectStatus.NEW.value
    source: str = ""
    region: str = "Saudi Arabia"
    decision_maker: str = ""
    pain_hypothesis: str = ""
    offer_angle: str = ""
    estimated_value_sar: float = 0.0
    confidence: float = 0.0
    preferred_channel: str = Channel.EMAIL.value
    created_at: str = field(default_factory=now_iso)
    last_contact_at: str | None = None
    next_action: str = ""
    next_action_date: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Prospect:
        return _coerce(cls, data)


@dataclass
class Draft:
    """A governed outreach/sales draft. Always pending approval when generated."""

    id: str
    prospect_id: str
    company: str
    sector: str
    channel: str
    draft_type: str
    language: str
    body: str
    evidence_level: str = "L1"
    risk_level: str = RiskLevel.LOW.value
    approval_required: bool = True
    status: str = DraftStatus.PENDING_APPROVAL.value
    subject: str = ""
    offer_angle: str = ""
    created_at: str = field(default_factory=now_iso)
    updated_at: str | None = None
    next_action: str = "founder_review"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Draft:
        return _coerce(cls, data)


@dataclass
class Followup:
    """A scheduled follow-up touch. Manual channels only; surfaced when due."""

    id: str
    prospect_id: str
    company: str
    due_date: str
    followup_type: str
    status: str = FollowupStatus.SCHEDULED.value
    channel: str = Channel.EMAIL.value
    draft_id: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Followup:
        return _coerce(cls, data)


__all__ = [
    "EVIDENCE_LEVELS",
    "MANUAL_SEND_CHANNELS",
    "QUEUEABLE_STATUSES",
    "Channel",
    "Draft",
    "DraftStatus",
    "DraftType",
    "Followup",
    "FollowupStatus",
    "FollowupType",
    "Language",
    "Prospect",
    "ProspectStatus",
    "RiskLevel",
    "now_iso",
]
