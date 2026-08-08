"""Tests for the Communication Intelligence Engine.

Covers message composition, style adaptation, channel formatting,
greeting/sign-off selection, and safety invariants.
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.communication_contracts import (
    CommunicationLanguage,
    CommunicationTone,
    CulturalContext,
    ResponseLength,
    build_communication_style,
)
from dealix.company_intelligence.communication_engine import (
    GeneratedDraft,
    MessageChannel,
    MessageIntent,
    MessagePurpose,
    MessageUrgency,
    adjust_formality_for_urgency,
    apply_custom_phrases,
    assess_style_match,
    build_message_intent,
    compose_message,
    format_body_for_channel,
    resolve_channel_tone,
    select_greeting,
    select_sign_off,
)

TENANT = "tenant_test_comm"
SOURCE = "test_source"


def _make_style(**overrides):
    defaults = {
        "tenant_id": TENANT,
        "name": "default_style",
        "source_id": SOURCE,
    }
    defaults.update(overrides)
    return build_communication_style(**defaults)


def _make_intent(**overrides):
    defaults = {
        "tenant_id": TENANT,
        "deduplication_key": "test_key_001",
        "purpose": MessagePurpose.INTRODUCTION,
        "channel": MessageChannel.EMAIL,
        "source_id": SOURCE,
        "key_points": ("introduce service",),
    }
    defaults.update(overrides)
    return build_message_intent(**defaults)


# -----------------------------------------------------------------------
# MessageIntent tests
# -----------------------------------------------------------------------


class TestMessageIntent:
    def test_build_intent_deterministic_id(self):
        i1 = _make_intent()
        i2 = _make_intent()
        assert i1.intent_id == i2.intent_id
        assert i1.intent_id.startswith("msgintent_")

    def test_different_keys_different_ids(self):
        i1 = _make_intent(deduplication_key="key_a")
        i2 = _make_intent(deduplication_key="key_b")
        assert i1.intent_id != i2.intent_id

    def test_requires_key_points_or_context(self):
        with pytest.raises(ValueError, match="key point or context"):
            _make_intent(key_points=(), context_notes="")

    def test_context_notes_alone_is_valid(self):
        intent = _make_intent(
            key_points=(), context_notes="follow up on pilot"
        )
        assert intent.context_notes == "follow up on pilot"

    def test_external_default_true(self):
        intent = _make_intent()
        assert intent.is_external is True

    def test_internal_message(self):
        intent = _make_intent(is_external=False)
        assert intent.is_external is False


# -----------------------------------------------------------------------
# Greeting and Sign-off tests
# -----------------------------------------------------------------------


class TestGreetingSelection:
    def test_formal_arabic_greeting(self):
        style = _make_style(tone=CommunicationTone.FORMAL)
        greeting = select_greeting(style)
        assert "السلام عليكم ورحمة الله وبركاته" in greeting

    def test_professional_english_greeting(self):
        style = _make_style(
            tone=CommunicationTone.PROFESSIONAL,
            language=CommunicationLanguage.EN,
        )
        greeting = select_greeting(style, language=CommunicationLanguage.EN)
        assert "Hello" in greeting

    def test_greeting_with_recipient_name(self):
        style = _make_style()
        greeting = select_greeting(style, recipient_name="محمد")
        assert "محمد" in greeting

    def test_custom_template_takes_precedence(self):
        style = _make_style(greeting_template_ar="أهلاً يا صديقي")
        greeting = select_greeting(style)
        assert "أهلاً يا صديقي" in greeting

    def test_bilingual_greeting(self):
        style = _make_style(language=CommunicationLanguage.BILINGUAL)
        greeting = select_greeting(
            style, language=CommunicationLanguage.BILINGUAL
        )
        assert "/" in greeting  # Arabic / English format


class TestSignOffSelection:
    def test_formal_arabic_sign_off(self):
        style = _make_style(tone=CommunicationTone.FORMAL)
        sign_off = select_sign_off(style)
        assert "التقدير" in sign_off

    def test_professional_english_sign_off(self):
        style = _make_style(language=CommunicationLanguage.EN)
        sign_off = select_sign_off(style, language=CommunicationLanguage.EN)
        assert "regards" in sign_off.lower()

    def test_custom_template_sign_off(self):
        style = _make_style(sign_off_template_ar="شكراً جزيلاً")
        sign_off = select_sign_off(style)
        assert "شكراً جزيلاً" in sign_off


# -----------------------------------------------------------------------
# Channel tone resolution
# -----------------------------------------------------------------------


class TestChannelTone:
    def test_default_tone_without_override(self):
        style = _make_style(tone=CommunicationTone.PROFESSIONAL)
        tone = resolve_channel_tone(style, MessageChannel.EMAIL)
        assert tone == CommunicationTone.PROFESSIONAL

    def test_channel_override_applied(self):
        style = _make_style(
            tone=CommunicationTone.PROFESSIONAL,
            channel_tone_overrides=(("whatsapp", "friendly"),),
        )
        tone = resolve_channel_tone(style, MessageChannel.WHATSAPP)
        assert tone == CommunicationTone.FRIENDLY

    def test_unmatched_channel_uses_default(self):
        style = _make_style(
            channel_tone_overrides=(("whatsapp", "friendly"),),
        )
        tone = resolve_channel_tone(style, MessageChannel.EMAIL)
        assert tone == CommunicationTone.PROFESSIONAL  # default


# -----------------------------------------------------------------------
# Formality adjustment
# -----------------------------------------------------------------------


class TestFormalityAdjustment:
    def test_normal_urgency_no_change(self):
        result = adjust_formality_for_urgency(0.7, MessageUrgency.NORMAL)
        assert result == 0.7

    def test_high_urgency_increases_formality(self):
        result = adjust_formality_for_urgency(0.7, MessageUrgency.HIGH)
        assert result == pytest.approx(0.8)

    def test_critical_urgency_capped_at_one(self):
        result = adjust_formality_for_urgency(0.9, MessageUrgency.CRITICAL)
        assert result == 1.0


# -----------------------------------------------------------------------
# Body formatting
# -----------------------------------------------------------------------


class TestBodyFormatting:
    def test_short_body_unchanged(self):
        body = "مرحباً، أود التعريف بخدماتنا"
        result = format_body_for_channel(
            body, MessageChannel.EMAIL, ResponseLength.MODERATE
        )
        assert result == body

    def test_long_body_truncated_for_whatsapp(self):
        body = "x" * 5000
        result = format_body_for_channel(
            body, MessageChannel.WHATSAPP, ResponseLength.MODERATE
        )
        assert len(result) <= 4096
        assert result.endswith("...")

    def test_brief_mode_reduces_length(self):
        body = "x" * 3000
        result = format_body_for_channel(
            body, MessageChannel.EMAIL, ResponseLength.BRIEF
        )
        # Brief cuts max_len in half (10000 -> 5000)
        assert len(result) <= 5000


# -----------------------------------------------------------------------
# Custom phrases and style matching
# -----------------------------------------------------------------------


class TestCustomPhrases:
    def test_prohibited_phrase_replaced(self):
        style = _make_style(prohibited_phrases=("guaranteed",))
        result = apply_custom_phrases(
            "We guaranteed results", style
        )
        assert "prohibited" in result

    def test_clean_body_unchanged(self):
        style = _make_style(prohibited_phrases=("guaranteed",))
        body = "We expect positive outcomes"
        result = apply_custom_phrases(body, style)
        assert result == body


class TestStyleMatch:
    def test_clean_body_scores_high(self):
        style = _make_style()
        score = assess_style_match("professional message body", style)
        assert score >= 0.8

    def test_prohibited_phrase_penalizes(self):
        style = _make_style(prohibited_phrases=("guaranteed",))
        score = assess_style_match("We guaranteed results", style)
        assert score < 1.0

    def test_company_matching_without_phrases_penalizes(self):
        style = _make_style(
            tone=CommunicationTone.COMPANY_MATCHING,
            custom_phrases=("يسعدنا خدمتكم",),
        )
        score = assess_style_match("generic message", style)
        assert score < 1.0

    def test_company_matching_with_phrases_bonuses(self):
        style = _make_style(
            tone=CommunicationTone.COMPANY_MATCHING,
            custom_phrases=("يسعدنا خدمتكم",),
        )
        score = assess_style_match("يسعدنا خدمتكم في كل وقت", style)
        assert score >= 0.9


# -----------------------------------------------------------------------
# compose_message — full pipeline
# -----------------------------------------------------------------------


class TestComposeMessage:
    def test_compose_basic_email(self):
        style = _make_style()
        intent = _make_intent()
        draft = compose_message(
            intent, style,
            body_content="أود التعريف بخدماتنا في مجال الذكاء الصناعي",
        )
        assert isinstance(draft, GeneratedDraft)
        assert draft.tenant_id == TENANT
        assert draft.intent_id == intent.intent_id
        assert draft.channel == MessageChannel.EMAIL
        assert draft.requires_approval is True
        assert draft.execution_allowed is False

    def test_compose_includes_greeting_and_signoff(self):
        style = _make_style(tone=CommunicationTone.FORMAL)
        intent = _make_intent()
        draft = compose_message(
            intent, style,
            body_content="محتوى الرسالة",
        )
        assert draft.greeting != ""
        assert draft.sign_off != ""
        assert draft.greeting in draft.full_message
        assert draft.sign_off in draft.full_message

    def test_compose_whatsapp_shorter(self):
        style = _make_style()
        intent = _make_intent(channel=MessageChannel.WHATSAPP)
        long_body = "x" * 5000
        draft = compose_message(intent, style, body_content=long_body)
        assert len(draft.body) <= 4096

    def test_compose_deterministic_id(self):
        style = _make_style()
        intent = _make_intent()
        body = "test body content"
        d1 = compose_message(intent, style, body_content=body)
        d2 = compose_message(intent, style, body_content=body)
        assert d1.draft_id == d2.draft_id
        assert d1.draft_id.startswith("msgdraft_")

    def test_external_always_requires_approval(self):
        style = _make_style()
        intent = _make_intent(is_external=True)
        draft = compose_message(
            intent, style, body_content="external message"
        )
        assert draft.requires_approval is True
        assert draft.is_external is True

    def test_internal_still_requires_approval(self):
        """Even internal drafts require approval in draft form."""
        style = _make_style()
        intent = _make_intent(is_external=False)
        draft = compose_message(
            intent, style, body_content="internal update"
        )
        assert draft.requires_approval is True

    def test_style_metadata_captured(self):
        style = _make_style(
            tone=CommunicationTone.CONSULTATIVE,
            cultural_context=CulturalContext.INTERNATIONAL,
        )
        intent = _make_intent(
            recipient_language=CommunicationLanguage.EN,
        )
        draft = compose_message(
            intent, style, body_content="Hello, I'd like to discuss."
        )
        assert draft.tone_used == CommunicationTone.CONSULTATIVE
        assert draft.cultural_context_used == CulturalContext.INTERNATIONAL
        assert draft.style_id == style.style_id


# -----------------------------------------------------------------------
# Safety invariants
# -----------------------------------------------------------------------


class TestSafetyInvariants:
    def test_execution_allowed_always_false(self):
        """GeneratedDraft cannot have execution_allowed=True."""
        style = _make_style()
        intent = _make_intent()
        draft = compose_message(
            intent, style, body_content="test"
        )
        assert draft.execution_allowed is False

        # Cannot construct with execution_allowed=True
        with pytest.raises(ValueError, match="never authorize execution"):
            GeneratedDraft(
                tenant_id=TENANT,
                draft_id=draft.draft_id,
                intent_id=intent.intent_id,
                body="test",
                full_message="test",
                tone_used=CommunicationTone.PROFESSIONAL,
                language_used=CommunicationLanguage.AR,
                cultural_context_used=CulturalContext.GULF_BUSINESS,
                channel=MessageChannel.EMAIL,
                requires_approval=True,
                execution_allowed=True,
                source_id=SOURCE,
            )

    def test_external_must_require_approval(self):
        """External drafts cannot bypass approval."""
        with pytest.raises(ValueError, match="external.*require.*approval"):
            GeneratedDraft(
                tenant_id=TENANT,
                draft_id="msgdraft_fake",
                intent_id="msgintent_fake",
                body="test",
                full_message="test",
                tone_used=CommunicationTone.PROFESSIONAL,
                language_used=CommunicationLanguage.AR,
                cultural_context_used=CulturalContext.GULF_BUSINESS,
                channel=MessageChannel.EMAIL,
                is_external=True,
                requires_approval=False,
                execution_allowed=False,
                source_id=SOURCE,
            )
