"""Communication Intelligence Engine for Company Intelligence.

Generates contextual, style-aware message drafts across all channels.
Uses CommunicationStyle contracts to ensure consistent company voice —
from formal Arabic business to casual technical English — with per-channel
tone adaptation and cultural sensitivity.

This engine NEVER sends messages. It produces drafts that flow through
the Action → Draft → Approval chain. External sending is always gated
by human approval.

The engine is persistence-neutral: no database, network, or LLM calls.

Entity ownership:
    Uses CommunicationStyle (company_brain) contracts.
    Produces inputs for Draft (draft_generation) contracts.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
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

from dealix.company_intelligence.communication_contracts import (
    CanonicalCommunicationStyle,
    CommunicationLanguage,
    CommunicationTone,
    CulturalContext,
    ResponseLength,
)

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class MessagePurpose(StrEnum):
    """Why a message is being composed."""

    INTRODUCTION = "introduction"
    FOLLOW_UP = "follow_up"
    DISCOVERY = "discovery"
    PROPOSAL_COVER = "proposal_cover"
    OBJECTION_RESPONSE = "objection_response"
    MEETING_REQUEST = "meeting_request"
    STATUS_UPDATE = "status_update"
    THANK_YOU = "thank_you"
    ESCALATION = "escalation"
    NEGOTIATION = "negotiation"
    DELIVERY_UPDATE = "delivery_update"
    RENEWAL = "renewal"


class MessageChannel(StrEnum):
    """Channel through which the message will be delivered."""

    EMAIL = "email"
    WHATSAPP = "whatsapp"
    LINKEDIN = "linkedin"
    PHONE_SCRIPT = "phone_script"
    PROPOSAL = "proposal"
    INTERNAL = "internal"


class MessageUrgency(StrEnum):
    """Urgency level affecting tone and timing."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Stable ID
# ---------------------------------------------------------------------------


def _stable_intent_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"msgintent_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


def _stable_draft_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"msgdraft_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Message Intent — what we want to communicate
# ---------------------------------------------------------------------------


class MessageIntent(BaseModel):
    """Describes what the system wants to communicate and to whom.

    MessageIntents flow from the Action Queue into the Communication Engine,
    which uses the tenant's CommunicationStyle to produce a formatted draft.

    Key invariants:
        - is_external=True means the message goes outside the organization
          and ALWAYS requires human approval.
        - recipient_context provides cultural and relationship context.
        - intent_id is deterministic from the deduplication key.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    intent_id: NonEmptyString
    deduplication_key: NonEmptyString

    # Communication target
    purpose: MessagePurpose
    channel: MessageChannel
    urgency: MessageUrgency = MessageUrgency.NORMAL

    # Recipient context
    recipient_name: str = ""
    recipient_company: str = ""
    recipient_role: str = ""
    recipient_language: CommunicationLanguage = CommunicationLanguage.AR

    # Content direction
    key_points: tuple[str, ...] = ()
    context_notes: str = ""
    reference_ids: tuple[str, ...] = ()

    # External = requires approval
    is_external: bool = True

    # Links
    action_id: str = ""
    opportunity_id: str = ""

    # Provenance
    source_id: NonEmptyString
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def enforce_intent_invariants(self) -> MessageIntent:
        # Must have at least one key point or context note
        if len(self.key_points) == 0 and not self.context_notes:
            raise ValueError(
                "message intent requires at least one key point or context note"
            )

        # Verify deterministic ID
        expected_id = _stable_intent_id({
            "deduplication_key": self.deduplication_key,
            "tenant_id": self.tenant_id,
        })
        if self.intent_id != expected_id:
            raise ValueError("intent_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Generated Draft — output of the Communication Engine
# ---------------------------------------------------------------------------


class GeneratedDraft(BaseModel):
    """A styled message draft produced by the Communication Engine.

    GeneratedDrafts are ready for human review and approval. They capture
    the style decisions made (which tone, greeting, sign-off were used)
    and include the formatted message body.

    Key invariants:
        - requires_approval is always True for external messages.
        - execution_allowed is always False.
        - draft_id is deterministic from content hash.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    draft_id: NonEmptyString
    intent_id: NonEmptyString

    # Content
    subject: str = ""
    greeting: str = ""
    body: NonEmptyString
    sign_off: str = ""
    full_message: NonEmptyString

    # Style metadata
    tone_used: CommunicationTone
    language_used: CommunicationLanguage
    cultural_context_used: CulturalContext
    formality_level_used: float = Field(default=0.7, ge=0.0, le=1.0)
    response_length_used: ResponseLength = ResponseLength.MODERATE

    # Channel
    channel: MessageChannel
    is_external: bool = True

    # Safety — ALWAYS
    requires_approval: bool = True
    execution_allowed: bool = False

    # Scoring
    style_match_score: float = Field(default=1.0, ge=0.0, le=1.0)

    # Provenance
    style_id: str = ""
    source_id: NonEmptyString
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def enforce_draft_invariants(self) -> GeneratedDraft:
        # External messages ALWAYS require approval
        if self.is_external and not self.requires_approval:
            raise ValueError(
                "external messages always require approval"
            )

        # Execution is NEVER allowed on drafts
        if self.execution_allowed:
            raise ValueError(
                "generated drafts never authorize execution"
            )

        # Verify deterministic ID
        expected_id = _stable_draft_id({
            "body": self.body,
            "channel": self.channel.value,
            "intent_id": self.intent_id,
            "tenant_id": self.tenant_id,
        })
        if self.draft_id != expected_id:
            raise ValueError("draft_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Communication Engine — the operational intelligence
# ---------------------------------------------------------------------------


# Gulf business greetings
_GREETINGS_AR: dict[CommunicationTone, str] = {
    CommunicationTone.FORMAL: "السلام عليكم ورحمة الله وبركاته",
    CommunicationTone.PROFESSIONAL: "السلام عليكم",
    CommunicationTone.CONSULTATIVE: "مرحباً",
    CommunicationTone.FRIENDLY: "أهلاً وسهلاً",
    CommunicationTone.COMPANY_MATCHING: "",  # uses custom
}

_GREETINGS_EN: dict[CommunicationTone, str] = {
    CommunicationTone.FORMAL: "Dear",
    CommunicationTone.PROFESSIONAL: "Hello",
    CommunicationTone.CONSULTATIVE: "Hi",
    CommunicationTone.FRIENDLY: "Hey",
    CommunicationTone.COMPANY_MATCHING: "",
}

_SIGN_OFFS_AR: dict[CommunicationTone, str] = {
    CommunicationTone.FORMAL: "مع خالص التقدير والاحترام",
    CommunicationTone.PROFESSIONAL: "مع التحية",
    CommunicationTone.CONSULTATIVE: "تحياتي",
    CommunicationTone.FRIENDLY: "أتطلع للتواصل",
    CommunicationTone.COMPANY_MATCHING: "",
}

_SIGN_OFFS_EN: dict[CommunicationTone, str] = {
    CommunicationTone.FORMAL: "With highest regards",
    CommunicationTone.PROFESSIONAL: "Best regards",
    CommunicationTone.CONSULTATIVE: "Looking forward to hearing from you",
    CommunicationTone.FRIENDLY: "Talk soon",
    CommunicationTone.COMPANY_MATCHING: "",
}

# Channel constraints
_CHANNEL_MAX_LENGTH: dict[MessageChannel, int] = {
    MessageChannel.WHATSAPP: 4096,
    MessageChannel.LINKEDIN: 3000,
    MessageChannel.PHONE_SCRIPT: 1000,
    MessageChannel.EMAIL: 10000,
    MessageChannel.PROPOSAL: 50000,
    MessageChannel.INTERNAL: 50000,
}

# Urgency → formality adjustment
_URGENCY_FORMALITY_DELTA: dict[MessageUrgency, float] = {
    MessageUrgency.LOW: 0.0,
    MessageUrgency.NORMAL: 0.0,
    MessageUrgency.HIGH: 0.1,
    MessageUrgency.CRITICAL: 0.2,
}


def select_greeting(
    style: CanonicalCommunicationStyle,
    *,
    language: CommunicationLanguage | None = None,
    recipient_name: str = "",
    tone_override: CommunicationTone | None = None,
) -> str:
    """Select a culturally appropriate greeting based on style and context.

    Uses the style's template if available, otherwise falls back to
    tone-based defaults.
    """
    lang = language or style.language
    tone = tone_override or style.tone

    # Check style templates first
    if lang in (CommunicationLanguage.AR, CommunicationLanguage.BILINGUAL):
        if style.greeting_template_ar:
            greeting = style.greeting_template_ar
            if recipient_name:
                greeting = f"{greeting} {recipient_name}"
            return greeting

    if lang in (CommunicationLanguage.EN, CommunicationLanguage.BILINGUAL):
        if style.greeting_template_en:
            greeting = style.greeting_template_en
            if recipient_name:
                greeting = f"{greeting} {recipient_name}"
            return greeting

    # Fall back to tone-based defaults
    if lang == CommunicationLanguage.AR:
        base = _GREETINGS_AR.get(tone, "السلام عليكم")
    elif lang == CommunicationLanguage.EN:
        base = _GREETINGS_EN.get(tone, "Hello")
    else:
        # Bilingual: Arabic first
        ar = _GREETINGS_AR.get(tone, "السلام عليكم")
        en = _GREETINGS_EN.get(tone, "Hello")
        base = f"{ar} / {en}"

    if recipient_name and base:
        return f"{base} {recipient_name}"
    return base or ""


def select_sign_off(
    style: CanonicalCommunicationStyle,
    *,
    language: CommunicationLanguage | None = None,
    tone_override: CommunicationTone | None = None,
) -> str:
    """Select an appropriate sign-off based on style and context."""
    lang = language or style.language
    tone = tone_override or style.tone

    if lang in (CommunicationLanguage.AR, CommunicationLanguage.BILINGUAL):
        if style.sign_off_template_ar:
            return style.sign_off_template_ar

    if lang in (CommunicationLanguage.EN, CommunicationLanguage.BILINGUAL):
        if style.sign_off_template_en:
            return style.sign_off_template_en

    if lang == CommunicationLanguage.AR:
        return _SIGN_OFFS_AR.get(tone, "مع التحية")
    elif lang == CommunicationLanguage.EN:
        return _SIGN_OFFS_EN.get(tone, "Best regards")
    else:
        ar = _SIGN_OFFS_AR.get(tone, "مع التحية")
        en = _SIGN_OFFS_EN.get(tone, "Best regards")
        return f"{ar} / {en}"


def resolve_channel_tone(
    style: CanonicalCommunicationStyle,
    channel: MessageChannel,
) -> CommunicationTone:
    """Resolve the effective tone for a specific channel.

    Checks channel_tone_overrides first, then falls back to the style's
    default tone.
    """
    for override_channel, override_tone in style.channel_tone_overrides:
        if override_channel == channel.value:
            try:
                return CommunicationTone(override_tone)
            except ValueError:
                break
    return style.tone


def adjust_formality_for_urgency(
    base_formality: float,
    urgency: MessageUrgency,
) -> float:
    """Adjust formality level based on urgency — urgent messages are slightly
    more formal to convey seriousness.
    """
    delta = _URGENCY_FORMALITY_DELTA.get(urgency, 0.0)
    return min(1.0, base_formality + delta)


def format_body_for_channel(
    body: str,
    channel: MessageChannel,
    response_length: ResponseLength,
) -> str:
    """Trim or format body to fit channel constraints."""
    max_len = _CHANNEL_MAX_LENGTH.get(channel, 10000)

    # Adjust based on preferred length
    if response_length == ResponseLength.BRIEF:
        max_len = min(max_len, max_len // 2)

    if len(body) > max_len:
        return body[: max_len - 3] + "..."
    return body


def apply_custom_phrases(
    body: str,
    style: CanonicalCommunicationStyle,
) -> str:
    """Filter prohibited phrases from the body.

    Does NOT inject custom_phrases (that's the LLM's job) — only ensures
    prohibited phrases are flagged. Returns the body unchanged if clean.
    """
    for phrase in style.prohibited_phrases:
        if phrase.lower() in body.lower():
            # Replace prohibited phrase with placeholder
            body = body.replace(phrase, f"[{phrase} — prohibited]")
    return body


def assess_style_match(
    body: str,
    style: CanonicalCommunicationStyle,
) -> float:
    """Score how well a body matches the communication style (0.0–1.0).

    Checks for:
    - Prohibited phrase violations (heavy penalty)
    - Custom phrase usage (bonus)
    - Length appropriateness
    """
    score = 1.0

    # Prohibited phrase penalty
    for phrase in style.prohibited_phrases:
        if phrase.lower() in body.lower():
            score -= 0.3

    # Custom phrase bonus (if company_matching)
    if style.tone == CommunicationTone.COMPANY_MATCHING and style.custom_phrases:
        matches = sum(
            1 for phrase in style.custom_phrases
            if phrase.lower() in body.lower()
        )
        if matches > 0:
            score = min(1.0, score + 0.1 * matches)
        else:
            score -= 0.2

    return max(0.0, min(1.0, round(score, 2)))


def compose_message(
    intent: MessageIntent,
    style: CanonicalCommunicationStyle,
    *,
    body_content: str,
    subject: str = "",
) -> GeneratedDraft:
    """Compose a styled message draft from an intent and style configuration.

    This is the primary entry point for the Communication Engine. It takes
    a MessageIntent (what to say), a CommunicationStyle (how to say it),
    and raw body content, then produces a fully formatted GeneratedDraft.

    The draft is NEVER executable. External messages ALWAYS require approval.
    """
    # Resolve effective tone for this channel
    effective_tone = resolve_channel_tone(style, intent.channel)

    # Determine effective language (prefer recipient's language)
    effective_language = intent.recipient_language

    # Adjust formality for urgency
    effective_formality = adjust_formality_for_urgency(
        style.formality_level, intent.urgency
    )

    # Select greeting and sign-off
    greeting = select_greeting(
        style,
        language=effective_language,
        recipient_name=intent.recipient_name,
        tone_override=effective_tone,
    )
    sign_off = select_sign_off(
        style,
        language=effective_language,
        tone_override=effective_tone,
    )

    # Format body for channel
    formatted_body = format_body_for_channel(
        body_content,
        intent.channel,
        style.response_length,
    )

    # Apply prohibited phrase filter
    formatted_body = apply_custom_phrases(formatted_body, style)

    # Compose full message
    parts = []
    if greeting:
        parts.append(greeting)
    parts.append(formatted_body)
    if sign_off:
        parts.append(sign_off)
    full_message = "\n\n".join(parts)

    # Assess style match
    match_score = assess_style_match(formatted_body, style)

    # Build deterministic draft ID
    draft_id = _stable_draft_id({
        "body": formatted_body,
        "channel": intent.channel.value,
        "intent_id": intent.intent_id,
        "tenant_id": intent.tenant_id,
    })

    return GeneratedDraft(
        tenant_id=intent.tenant_id,
        draft_id=draft_id,
        intent_id=intent.intent_id,
        subject=subject,
        greeting=greeting,
        body=formatted_body,
        sign_off=sign_off,
        full_message=full_message,
        tone_used=effective_tone,
        language_used=effective_language,
        cultural_context_used=style.cultural_context,
        formality_level_used=effective_formality,
        response_length_used=style.response_length,
        channel=intent.channel,
        is_external=intent.is_external,
        requires_approval=True,
        execution_allowed=False,
        style_match_score=match_score,
        style_id=style.style_id,
        source_id=intent.source_id,
    )


# ---------------------------------------------------------------------------
# Builder helpers
# ---------------------------------------------------------------------------


def build_message_intent(
    *,
    tenant_id: str,
    deduplication_key: str,
    purpose: MessagePurpose,
    channel: MessageChannel,
    source_id: str,
    urgency: MessageUrgency = MessageUrgency.NORMAL,
    recipient_name: str = "",
    recipient_company: str = "",
    recipient_role: str = "",
    recipient_language: CommunicationLanguage = CommunicationLanguage.AR,
    key_points: tuple[str, ...] = (),
    context_notes: str = "",
    reference_ids: tuple[str, ...] = (),
    is_external: bool = True,
    action_id: str = "",
    opportunity_id: str = "",
) -> MessageIntent:
    """Build a deterministic message intent."""
    intent_id = _stable_intent_id({
        "deduplication_key": deduplication_key.strip(),
        "tenant_id": tenant_id.strip(),
    })

    return MessageIntent(
        tenant_id=tenant_id,
        intent_id=intent_id,
        deduplication_key=deduplication_key,
        purpose=purpose,
        channel=channel,
        urgency=urgency,
        recipient_name=recipient_name,
        recipient_company=recipient_company,
        recipient_role=recipient_role,
        recipient_language=recipient_language,
        key_points=key_points,
        context_notes=context_notes,
        reference_ids=reference_ids,
        is_external=is_external,
        action_id=action_id,
        opportunity_id=opportunity_id,
        source_id=source_id,
    )
