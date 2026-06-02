"""Entity models + controlled vocabularies for the Revenue Execution OS.

Every entity is a frozen dataclass with ``to_dict`` / ``from_dict`` so it can
round-trip through the JSONL stores. Status / type / channel values are
``StrEnum`` members (which *are* strings) so they serialize cleanly while
still giving callers a single source of allowed values.
"""

from __future__ import annotations

import dataclasses
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


def now_iso() -> str:
    """Current UTC timestamp in ISO-8601 (shared by factories + stores)."""
    return datetime.now(UTC).isoformat()


# ── Controlled vocabularies ────────────────────────────────────────────────


class DraftStatus(StrEnum):
    GENERATED = "generated"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_EDIT = "needs_edit"
    COPIED_MANUALLY = "copied_manually"
    SENT_VIA_INTEGRATION = "sent_via_integration"
    REPLIED = "replied"
    ARCHIVED = "archived"


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


class Channel(StrEnum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    LINKEDIN = "linkedin"
    PHONE = "phone"
    PROPOSAL = "proposal"
    PAYMENT = "payment"


class PaymentHandoffStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SENT = "sent"
    PAID = "paid"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class ProposalStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    SENT = "sent"


class Outcome(StrEnum):
    OPEN = "open"
    WON = "won"
    LOST = "lost"


class FollowupStatus(StrEnum):
    DUE = "due"
    COMPLETED = "completed"
    SKIPPED = "skipped"


# Draft statuses that are safe to surface as "ready for manual sending".
APPROVED_DRAFT_STATUSES: frozenset[str] = frozenset(
    {DraftStatus.APPROVED, DraftStatus.COPIED_MANUALLY}
)
# Draft statuses still awaiting a founder decision.
OPEN_DRAFT_STATUSES: frozenset[str] = frozenset(
    {DraftStatus.GENERATED, DraftStatus.PENDING_APPROVAL, DraftStatus.NEEDS_EDIT}
)


def _pick(cls: type, data: dict[str, Any]) -> dict[str, Any]:
    """Keep only keys that are fields of ``cls`` (resilient to extra/missing)."""
    names = {f.name for f in dataclasses.fields(cls)}
    return {k: v for k, v in data.items() if k in names}


# ── Entities ───────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Prospect:
    prospect_id: str = ""
    company: str = ""
    contact_name: str = ""
    sector: str = ""
    region: str = "Saudi Arabia"
    lead_source: str = ""
    stage: str = "new"
    notes: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Prospect:
        return cls(**_pick(cls, data))


@dataclass(frozen=True, slots=True)
class Draft:
    draft_id: str = ""
    prospect_id: str = ""
    draft_type: str = DraftType.OUTREACH_FIRST
    channel: str = Channel.EMAIL
    status: str = DraftStatus.PENDING_APPROVAL
    approval_required: bool = True
    subject: str = ""
    body_ar: str = ""
    body_en: str = ""
    evidence_level: int = 0
    governance_decision: str = "DRAFT_ONLY"
    issues: list[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Draft:
        return cls(**_pick(cls, data))


@dataclass(frozen=True, slots=True)
class Followup:
    followup_id: str = ""
    prospect_id: str = ""
    reason: str = ""
    channel: str = Channel.EMAIL
    suggested_draft_type: str = DraftType.OUTREACH_FOLLOWUP_1
    due_date: str = ""
    status: str = FollowupStatus.DUE
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Followup:
        return cls(**_pick(cls, data))


@dataclass(frozen=True, slots=True)
class Proposal:
    proposal_id: str = ""
    prospect_id: str = ""
    sector: str = ""
    offer_key: str = ""
    problem: str = ""
    solution: str = ""
    scope: list[str] = field(default_factory=list)
    out_of_scope: list[str] = field(default_factory=list)
    timeline: str = ""
    price_label: str = ""
    evidence_level: int = 0
    assumptions: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    next_step: str = ""
    status: str = ProposalStatus.PENDING_APPROVAL
    governance_decision: str = "DRAFT_ONLY"
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Proposal:
        return cls(**_pick(cls, data))


@dataclass(frozen=True, slots=True)
class ProofPackRef:
    proof_pack_id: str = ""
    prospect_id: str = ""
    customer_id: str = ""
    sections: dict[str, str] = field(default_factory=dict)
    sections_complete: bool = False
    score: int = 0
    evidence_level: int = 0
    status: str = "draft"
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProofPackRef:
        return cls(**_pick(cls, data))


@dataclass(frozen=True, slots=True)
class PaymentHandoff:
    handoff_id: str = ""
    prospect_id: str = ""
    proposal_id: str = ""
    offer_key: str = ""
    amount_label: str = ""
    status: str = PaymentHandoffStatus.DRAFT
    preconditions: dict[str, bool] = field(default_factory=dict)
    blocking_reasons: list[str] = field(default_factory=list)
    governance_decision: str = "REQUIRE_APPROVAL"
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PaymentHandoff:
        return cls(**_pick(cls, data))


@dataclass(frozen=True, slots=True)
class Renewal:
    renewal_id: str = ""
    customer_id: str = ""
    current_offer_key: str = ""
    next_offer_key: str = ""
    trigger: str = ""
    due_date: str = ""
    status: str = "open"
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Renewal:
        return cls(**_pick(cls, data))


@dataclass(frozen=True, slots=True)
class WinLoss:
    record_id: str = ""
    prospect_id: str = ""
    company: str = ""
    sector: str = ""
    channel: str = Channel.EMAIL
    offer_key: str = ""
    outcome: str = Outcome.OPEN
    reason: str = ""
    objection: str = ""
    lesson: str = ""
    next_change: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WinLoss:
        return cls(**_pick(cls, data))


__all__ = [
    "APPROVED_DRAFT_STATUSES",
    "OPEN_DRAFT_STATUSES",
    "Channel",
    "Draft",
    "DraftStatus",
    "DraftType",
    "Followup",
    "FollowupStatus",
    "Outcome",
    "PaymentHandoff",
    "PaymentHandoffStatus",
    "ProofPackRef",
    "Proposal",
    "ProposalStatus",
    "Prospect",
    "Renewal",
    "WinLoss",
    "now_iso",
]
