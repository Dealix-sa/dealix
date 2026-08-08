"""Tests for CommunicationStyle contracts — tone, language, and style governance."""
from __future__ import annotations

import pytest

from dealix.company_intelligence.communication_contracts import (
    CanonicalCommunicationStyle,
    CommunicationLanguage,
    CommunicationStyleStatus,
    CommunicationTone,
    CulturalContext,
    ResponseLength,
    build_communication_style,
    is_valid_style_transition,
    transition_style,
    valid_style_transitions_from,
)

# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


class TestBuildCommunicationStyle:
    """build_communication_style produces a valid, deterministic style."""

    def test_default_style(self) -> None:
        style = build_communication_style(
            tenant_id="t1",
            name="Default Business",
            source_id="src1",
        )
        assert style.tenant_id == "t1"
        assert style.name == "Default Business"
        assert style.tone == CommunicationTone.PROFESSIONAL
        assert style.language == CommunicationLanguage.AR
        assert style.cultural_context == CulturalContext.GULF_BUSINESS
        assert style.formality_level == 0.7
        assert style.response_length == ResponseLength.MODERATE
        assert style.status == CommunicationStyleStatus.DRAFT
        assert style.style_id.startswith("commstyle_")

    def test_deterministic_id(self) -> None:
        s1 = build_communication_style(
            tenant_id="t1", name="Style A", source_id="src1"
        )
        s2 = build_communication_style(
            tenant_id="t1", name="Style A", source_id="src2"
        )
        assert s1.style_id == s2.style_id  # same tenant + name → same ID

    def test_different_names_different_ids(self) -> None:
        s1 = build_communication_style(
            tenant_id="t1", name="Style A", source_id="src1"
        )
        s2 = build_communication_style(
            tenant_id="t1", name="Style B", source_id="src1"
        )
        assert s1.style_id != s2.style_id

    def test_formal_arabic_style(self) -> None:
        style = build_communication_style(
            tenant_id="t1",
            name="Formal Arabic",
            source_id="src1",
            tone=CommunicationTone.FORMAL,
            language=CommunicationLanguage.AR,
            cultural_context=CulturalContext.GULF_BUSINESS,
            formality_level=0.95,
            greeting_template_ar="السلام عليكم ورحمة الله وبركاته",
            sign_off_template_ar="مع خالص التحيات",
        )
        assert style.tone == CommunicationTone.FORMAL
        assert style.formality_level == 0.95
        assert "السلام" in style.greeting_template_ar

    def test_company_matching_style(self) -> None:
        style = build_communication_style(
            tenant_id="t1",
            name="Acme Voice",
            source_id="src1",
            tone=CommunicationTone.COMPANY_MATCHING,
            custom_phrases=("innovation-first", "partner-driven"),
        )
        assert style.tone == CommunicationTone.COMPANY_MATCHING
        assert len(style.custom_phrases) == 2

    def test_bilingual_consultative(self) -> None:
        style = build_communication_style(
            tenant_id="t1",
            name="Bilingual Consultant",
            source_id="src1",
            tone=CommunicationTone.CONSULTATIVE,
            language=CommunicationLanguage.BILINGUAL,
            greeting_template_ar="مرحبا",
            greeting_template_en="Hello",
        )
        assert style.language == CommunicationLanguage.BILINGUAL
        assert style.greeting_template_ar == "مرحبا"
        assert style.greeting_template_en == "Hello"

    def test_channel_tone_overrides(self) -> None:
        style = build_communication_style(
            tenant_id="t1",
            name="Multi-Channel",
            source_id="src1",
            channel_tone_overrides=(
                ("email", "formal"),
                ("whatsapp", "friendly"),
            ),
        )
        assert len(style.channel_tone_overrides) == 2

    def test_prohibited_phrases(self) -> None:
        style = build_communication_style(
            tenant_id="t1",
            name="Safe Style",
            source_id="src1",
            prohibited_phrases=("guaranteed", "مضمون", "100%"),
        )
        assert "guaranteed" in style.prohibited_phrases
        assert "مضمون" in style.prohibited_phrases


# ---------------------------------------------------------------------------
# Invariant enforcement
# ---------------------------------------------------------------------------


class TestCommunicationInvariants:
    """Model validator enforces communication style invariants."""

    def test_company_matching_requires_custom_phrases(self) -> None:
        with pytest.raises(ValueError, match="company_matching tone requires"):
            build_communication_style(
                tenant_id="t1",
                name="Bad Match",
                source_id="src1",
                tone=CommunicationTone.COMPANY_MATCHING,
                custom_phrases=(),  # empty → should fail
            )

    def test_no_evidence_raises(self) -> None:
        with pytest.raises(ValueError, match="at least one evidence reference"):
            build_communication_style(
                tenant_id="t1",
                name="No Evidence",
                source_id="src1",
                evidence_refs=(),
            )

    def test_overlap_custom_prohibited_raises(self) -> None:
        with pytest.raises(ValueError, match="overlap"):
            build_communication_style(
                tenant_id="t1",
                name="Overlap",
                source_id="src1",
                custom_phrases=("innovative",),
                prohibited_phrases=("innovative",),
            )

    def test_invalid_channel_override_tone_raises(self) -> None:
        with pytest.raises(ValueError, match="invalid tone"):
            build_communication_style(
                tenant_id="t1",
                name="Bad Override",
                source_id="src1",
                channel_tone_overrides=(("email", "aggressive"),),
            )

    def test_formality_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            build_communication_style(
                tenant_id="t1",
                name="Too Formal",
                source_id="src1",
                formality_level=1.5,
            )

    def test_frozen_model(self) -> None:
        style = build_communication_style(
            tenant_id="t1", name="Frozen", source_id="src1"
        )
        with pytest.raises(Exception):
            style.tone = CommunicationTone.FORMAL  # type: ignore[misc]


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


class TestCommunicationStyleTransitions:
    """Transition helpers enforce the style lifecycle."""

    def test_valid_transitions_from_draft(self) -> None:
        valid = valid_style_transitions_from(CommunicationStyleStatus.DRAFT)
        assert CommunicationStyleStatus.ACTIVE in valid
        assert CommunicationStyleStatus.RETIRED in valid

    def test_valid_transitions_from_active(self) -> None:
        valid = valid_style_transitions_from(CommunicationStyleStatus.ACTIVE)
        assert CommunicationStyleStatus.UNDER_REVIEW in valid
        assert CommunicationStyleStatus.RETIRED in valid

    def test_retired_is_terminal(self) -> None:
        valid = valid_style_transitions_from(CommunicationStyleStatus.RETIRED)
        assert len(valid) == 0

    def test_transition_draft_to_active(self) -> None:
        style = build_communication_style(
            tenant_id="t1", name="Activate", source_id="src1"
        )
        assert style.status == CommunicationStyleStatus.DRAFT
        active = transition_style(style, to_status=CommunicationStyleStatus.ACTIVE)
        assert active.status == CommunicationStyleStatus.ACTIVE
        assert active.style_id == style.style_id

    def test_invalid_transition_raises(self) -> None:
        style = build_communication_style(
            tenant_id="t1", name="Invalid", source_id="src1"
        )
        with pytest.raises(ValueError, match="invalid communication style transition"):
            transition_style(style, to_status=CommunicationStyleStatus.UNDER_REVIEW)

    def test_full_lifecycle(self) -> None:
        style = build_communication_style(
            tenant_id="t1", name="Lifecycle", source_id="src1"
        )
        style = transition_style(style, to_status=CommunicationStyleStatus.ACTIVE)
        style = transition_style(style, to_status=CommunicationStyleStatus.UNDER_REVIEW)
        style = transition_style(style, to_status=CommunicationStyleStatus.ACTIVE)
        style = transition_style(style, to_status=CommunicationStyleStatus.RETIRED)
        assert style.status == CommunicationStyleStatus.RETIRED

    def test_is_valid_transition_helper(self) -> None:
        assert is_valid_style_transition(
            CommunicationStyleStatus.DRAFT,
            CommunicationStyleStatus.ACTIVE,
        )
        assert not is_valid_style_transition(
            CommunicationStyleStatus.RETIRED,
            CommunicationStyleStatus.ACTIVE,
        )


# ---------------------------------------------------------------------------
# ID preservation across transitions
# ---------------------------------------------------------------------------


class TestStyleIdPreservation:
    """Deterministic IDs survive model_validate round-trips."""

    def test_id_stable_across_transitions(self) -> None:
        style = build_communication_style(
            tenant_id="t1", name="Stable", source_id="src1"
        )
        original_id = style.style_id
        active = transition_style(style, to_status=CommunicationStyleStatus.ACTIVE)
        assert active.style_id == original_id
        retired = transition_style(active, to_status=CommunicationStyleStatus.RETIRED)
        assert retired.style_id == original_id
