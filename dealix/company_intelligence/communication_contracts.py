"""Canonical CommunicationStyle contracts for Company Intelligence.

A CommunicationStyle defines how Dealix communicates on behalf of a tenant —
tone, formality, language, cultural context, and channel-specific preferences.
It feeds the Draft generation pipeline and ensures consistent, configurable
voice across all customer interactions.

The models are persistence-neutral: no database, network, or LLM calls.

Entity ownership: CommunicationStyle → company_brain
    (communication style and tone configuration per tenant).
Required fields: tenant_id, tone, formality_level, source_id.
Forbidden parallel names: MessageTone, VoiceProfile.
"""
from __future__ import annotations

import json
from enum import StrEnum
from hashlib import sha256
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class CommunicationTone(StrEnum):
    """Tone profiles for tenant communication."""

    FORMAL = "formal"
    PROFESSIONAL = "professional"
    CONSULTATIVE = "consultative"
    FRIENDLY = "friendly"
    COMPANY_MATCHING = "company_matching"


class CommunicationLanguage(StrEnum):
    """Language preferences for generated communication."""

    AR = "ar"
    EN = "en"
    BILINGUAL = "bilingual"


class CulturalContext(StrEnum):
    """Cultural context that shapes communication patterns."""

    GULF_BUSINESS = "gulf_business"
    INTERNATIONAL = "international"
    TECHNICAL = "technical"


class ResponseLength(StrEnum):
    """Preferred length of generated responses and drafts."""

    BRIEF = "brief"
    MODERATE = "moderate"
    DETAILED = "detailed"


class CommunicationStyleStatus(StrEnum):
    """Lifecycle states for a communication style configuration."""

    DRAFT = "draft"
    ACTIVE = "active"
    UNDER_REVIEW = "under_review"
    RETIRED = "retired"


# ---------------------------------------------------------------------------
# Stable ID generation
# ---------------------------------------------------------------------------


def _stable_style_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"commstyle_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Canonical CommunicationStyle contract
# ---------------------------------------------------------------------------


class CanonicalCommunicationStyle(BaseModel):
    """One tenant-scoped communication style configuration.

    CommunicationStyles control how Dealix generates messages, proposals,
    and all customer-facing content. They are configurable per tenant and
    can be tuned along multiple axes: tone, formality, language, cultural
    context, and channel-specific overrides.

    Key invariants:
      - formality_level must be between 0 and 1.
      - At least one evidence reference is required.
      - Company-matching tone requires custom_phrases to be non-empty.
      - Style ID is deterministic from tenant + name.
      - prohibited_phrases cannot overlap with custom_phrases.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    style_id: NonEmptyString

    # Style configuration
    name: NonEmptyString
    tone: CommunicationTone = CommunicationTone.PROFESSIONAL
    language: CommunicationLanguage = CommunicationLanguage.AR
    cultural_context: CulturalContext = CulturalContext.GULF_BUSINESS
    formality_level: float = Field(default=0.7, ge=0.0, le=1.0)
    response_length: ResponseLength = ResponseLength.MODERATE

    # Templates
    greeting_template_ar: str = ""
    greeting_template_en: str = ""
    sign_off_template_ar: str = ""
    sign_off_template_en: str = ""

    # Company voice — custom vocabulary and phrases to use/avoid
    custom_phrases: tuple[str, ...] = ()
    prohibited_phrases: tuple[str, ...] = ()

    # Channel-specific tone overrides (channel → tone value)
    channel_tone_overrides: tuple[tuple[str, str], ...] = ()

    # Status
    status: CommunicationStyleStatus = CommunicationStyleStatus.DRAFT
    description: str = ""

    # Scoring
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Evidence
    evidence_refs: tuple[str, ...] = ()

    # Provenance
    source_id: NonEmptyString

    @model_validator(mode="after")
    def enforce_communication_invariants(self) -> CanonicalCommunicationStyle:
        # At least one evidence reference
        if len(self.evidence_refs) == 0:
            raise ValueError(
                "communication style requires at least one evidence reference"
            )

        # Company-matching tone requires custom_phrases
        if (
            self.tone == CommunicationTone.COMPANY_MATCHING
            and len(self.custom_phrases) == 0
        ):
            raise ValueError(
                "company_matching tone requires at least one custom phrase"
            )

        # Prohibited and custom phrases must not overlap
        custom_set = set(self.custom_phrases)
        prohibited_set = set(self.prohibited_phrases)
        overlap = custom_set & prohibited_set
        if overlap:
            raise ValueError(
                f"custom_phrases and prohibited_phrases overlap: {sorted(overlap)}"
            )

        # Channel tone overrides must reference valid tones
        valid_tones = {t.value for t in CommunicationTone}
        for channel, tone_value in self.channel_tone_overrides:
            if tone_value not in valid_tones:
                raise ValueError(
                    f"invalid tone '{tone_value}' in channel override for '{channel}'"
                )

        # Verify deterministic ID
        expected_id = _stable_style_id({
            "name": self.name,
            "tenant_id": self.tenant_id,
        })
        if self.style_id != expected_id:
            raise ValueError("style_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------

_STYLE_TRANSITIONS: dict[CommunicationStyleStatus, frozenset[CommunicationStyleStatus]] = {
    CommunicationStyleStatus.DRAFT: frozenset(
        {CommunicationStyleStatus.ACTIVE, CommunicationStyleStatus.RETIRED}
    ),
    CommunicationStyleStatus.ACTIVE: frozenset(
        {CommunicationStyleStatus.UNDER_REVIEW, CommunicationStyleStatus.RETIRED}
    ),
    CommunicationStyleStatus.UNDER_REVIEW: frozenset(
        {CommunicationStyleStatus.ACTIVE, CommunicationStyleStatus.RETIRED}
    ),
    CommunicationStyleStatus.RETIRED: frozenset(),  # terminal
}


def valid_style_transitions_from(
    status: CommunicationStyleStatus,
) -> frozenset[CommunicationStyleStatus]:
    """Return the set of valid target states from *status*."""
    return _STYLE_TRANSITIONS.get(status, frozenset())


def is_valid_style_transition(
    from_status: CommunicationStyleStatus,
    to_status: CommunicationStyleStatus,
) -> bool:
    """Check whether *from_status* → *to_status* is a valid transition."""
    return to_status in valid_style_transitions_from(from_status)


def transition_style(
    style: CanonicalCommunicationStyle,
    *,
    to_status: CommunicationStyleStatus,
) -> CanonicalCommunicationStyle:
    """Return a new CanonicalCommunicationStyle with *to_status* applied.

    Raises ValueError on invalid transitions. The original is never mutated.
    """
    if not is_valid_style_transition(style.status, to_status):
        raise ValueError(
            f"invalid communication style transition: "
            f"{style.status.value} → {to_status.value}"
        )
    updates: dict[str, Any] = {"status": to_status}
    return type(style).model_validate({**style.model_dump(), **updates})


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_communication_style(
    *,
    tenant_id: str,
    name: str,
    source_id: str,
    tone: CommunicationTone = CommunicationTone.PROFESSIONAL,
    language: CommunicationLanguage = CommunicationLanguage.AR,
    cultural_context: CulturalContext = CulturalContext.GULF_BUSINESS,
    formality_level: float = 0.7,
    response_length: ResponseLength = ResponseLength.MODERATE,
    greeting_template_ar: str = "",
    greeting_template_en: str = "",
    sign_off_template_ar: str = "",
    sign_off_template_en: str = "",
    custom_phrases: tuple[str, ...] = (),
    prohibited_phrases: tuple[str, ...] = (),
    channel_tone_overrides: tuple[tuple[str, str], ...] = (),
    status: CommunicationStyleStatus = CommunicationStyleStatus.DRAFT,
    description: str = "",
    confidence: float = 0.5,
    evidence_refs: tuple[str, ...] = ("manual_configuration",),
) -> CanonicalCommunicationStyle:
    """Build a deterministic, tenant-scoped communication style."""

    style_id = _stable_style_id({
        "name": name.strip(),
        "tenant_id": tenant_id.strip(),
    })

    return CanonicalCommunicationStyle(
        tenant_id=tenant_id,
        style_id=style_id,
        name=name,
        tone=tone,
        language=language,
        cultural_context=cultural_context,
        formality_level=formality_level,
        response_length=response_length,
        greeting_template_ar=greeting_template_ar,
        greeting_template_en=greeting_template_en,
        sign_off_template_ar=sign_off_template_ar,
        sign_off_template_en=sign_off_template_en,
        custom_phrases=custom_phrases,
        prohibited_phrases=prohibited_phrases,
        channel_tone_overrides=channel_tone_overrides,
        status=status,
        description=description,
        confidence=confidence,
        evidence_refs=evidence_refs,
        source_id=source_id,
    )
