"""Outreach draft — the canonical draft-only object for the Market Production OS.

A draft is never a send. Every ``OutreachDraft`` is produced by the draft
factory, scored by ``draft_quality_gate``, and only ever leaves the system
through the founder approval queue (``approval_center``). No field stores raw
PII: the recipient is identified by an opaque ``recipient_ref`` (caller-supplied
hash / CRM id), never an email or phone number — this keeps committed samples
and logs clean for ``data_os.pii_flags_for_row``.

Doctrine: drafts carry ``governance_decision = "approval_required"`` from birth
and ``send_status = "draft"``. Nothing in this module sends, charges, or scrapes.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# Controlled vocabularies (kept as module constants so the quality gate and
# reports share one source of truth).
EVIDENCE_LEVELS: tuple[str, ...] = ("L0", "L1", "L2", "L3", "L4", "L5")
RISK_LEVELS: tuple[str, ...] = ("low", "medium", "high")
PERSONALIZATION_TIERS: tuple[str, ...] = ("P0", "P1", "P2", "P3")
SEQUENCE_STEPS: tuple[str, ...] = (
    "first_touch",
    "follow_up_1",
    "follow_up_2",
    "proposal_intro",
    "close_loop",
)
LANGUAGES: tuple[str, ...] = ("ar", "en", "ar_en")

# Default daily mix for the 250-draft factory (drafts, not sends).
DAILY_DRAFT_MIX: dict[str, int] = {
    "first_touch": 100,
    "follow_up_1": 75,
    "follow_up_2": 50,
    "proposal_intro": 15,
    "close_loop": 10,
}

_DEFAULT_FORBIDDEN_ACTIONS: tuple[str, ...] = (
    "auto_send",
    "cold_whatsapp",
    "linkedin_automation",
    "scraping",
    "purchased_list",
    "send_without_approval",
)


class OutreachDraft(BaseModel):
    """A single draft-only outreach artifact awaiting founder approval."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    draft_id: str
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    # Targeting (non-PII labels + opaque refs only).
    prospect_ref: str = ""
    company_label: str = ""  # e.g. "Riyadh marketing agency (mid)" — never a person
    sector: str = ""
    region: str = "Saudi Arabia"
    recipient_role: str = ""  # e.g. "Marketing Director" — a role, not a name
    recipient_ref: str = ""  # opaque hash / CRM id — NEVER an email or phone
    signal_ref: str = ""  # links to a company_signal record

    # Reasoning.
    pain_hypothesis: str = ""
    personalization_note: str = ""
    personalization_tier: Literal["P0", "P1", "P2", "P3"] = "P0"

    # Offer linkage (operational id; pricing is governed in docs/commercial).
    offer: str = ""
    offer_matched: bool = False

    # Content.
    subject: str = ""
    body_ar: str = ""
    body_en: str = ""
    cta: str = ""
    language: Literal["ar", "en", "ar_en"] = "ar"

    # Compliance + risk posture.
    evidence_level: str = ""  # one of EVIDENCE_LEVELS; empty == missing (flagged)
    risk_level: Literal["low", "medium", "high"] = "low"
    unsubscribe_included: bool = False

    # Sequence + lifecycle.
    sequence_step: Literal[
        "first_touch", "follow_up_1", "follow_up_2", "proposal_intro", "close_loop"
    ] = "first_touch"
    approval_status: str = "approval_required"
    send_status: Literal["draft", "approved", "queued", "sent", "rejected"] = "draft"

    # Doctrine envelope — drafts are never auto-allowed.
    governance_decision: str = "approval_required"
    forbidden_actions: list[str] = Field(
        default_factory=lambda: list(_DEFAULT_FORBIDDEN_ACTIONS)
    )

    def combined_text(self) -> str:
        """Subject + both body variants — the surface the quality gate scans."""
        return "\n".join(p for p in (self.subject, self.body_ar, self.body_en, self.cta) if p)


__all__ = [
    "DAILY_DRAFT_MIX",
    "EVIDENCE_LEVELS",
    "LANGUAGES",
    "PERSONALIZATION_TIERS",
    "RISK_LEVELS",
    "SEQUENCE_STEPS",
    "OutreachDraft",
]
