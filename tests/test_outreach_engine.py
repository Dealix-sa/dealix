"""Tests for the Outreach Sequencing Engine.

Covers sequence planning, message generation, response classification,
sequence analysis, safety invariants, and bilingual output.
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.outreach_engine import (
    DEFAULT_SEQUENCE_TEMPLATE,
    CadenceSpeed,
    OutreachChannel,
    OutreachSequence,
    ResponseType,
    SequenceAnalysis,
    SequenceStatus,
    TouchPoint,
    TouchStatus,
    TouchType,
    analyze_sequences,
    classify_response,
    plan_sequence,
)

TENANT = "tenant_test_outreach"
SOURCE = "test_source"


# -----------------------------------------------------------------------
# Sequence planning
# -----------------------------------------------------------------------


class TestSequencePlanning:
    def test_basic_sequence(self):
        seq = plan_sequence(
            tenant_id=TENANT,
            prospect_name="Ahmad",
            prospect_company="TestCo",
            prospect_email="ahmad@testco.sa",
            sector="saas",
            source_id=SOURCE,
        )
        assert isinstance(seq, OutreachSequence)
        assert seq.tenant_id == TENANT
        assert seq.prospect_name == "Ahmad"
        assert seq.prospect_company == "TestCo"
        assert len(seq.touches) == 5  # Default template has 5 touches
        assert seq.status == SequenceStatus.PLANNED
        assert seq.auto_send is False
        assert seq.approval_required is True

    def test_deterministic_id(self):
        s1 = plan_sequence(
            tenant_id=TENANT, prospect_name="Ahmad",
            prospect_company="TestCo", source_id=SOURCE,
        )
        s2 = plan_sequence(
            tenant_id=TENANT, prospect_name="Ahmad",
            prospect_company="TestCo", source_id=SOURCE,
        )
        assert s1.sequence_id == s2.sequence_id
        assert s1.sequence_id.startswith("sequence_")

    def test_touch_types_match_template(self):
        seq = plan_sequence(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co", source_id=SOURCE,
        )
        actual_types = tuple(t.touch_type for t in seq.touches)
        assert actual_types == DEFAULT_SEQUENCE_TEMPLATE

    def test_cadence_affects_timing(self):
        aggressive = plan_sequence(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co", cadence=CadenceSpeed.AGGRESSIVE,
            source_id=SOURCE,
        )
        slow = plan_sequence(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co", cadence=CadenceSpeed.SLOW,
            source_id=SOURCE,
        )
        # Slow cadence should have larger day offsets
        agg_last = aggressive.touches[-1].day_offset
        slow_last = slow.touches[-1].day_offset
        assert slow_last > agg_last

    def test_whatsapp_channel(self):
        seq = plan_sequence(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co",
            channel=OutreachChannel.WHATSAPP,
            source_id=SOURCE,
        )
        assert seq.primary_channel == OutreachChannel.WHATSAPP
        for t in seq.touches:
            assert t.channel == OutreachChannel.WHATSAPP

    def test_custom_touch_types(self):
        custom = (TouchType.INTRO, TouchType.FOLLOW_UP, TouchType.BREAKUP)
        seq = plan_sequence(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co", touch_types=custom,
            source_id=SOURCE,
        )
        assert len(seq.touches) == 3
        assert seq.touches[0].touch_type == TouchType.INTRO

    def test_bilingual_messages(self):
        seq = plan_sequence(
            tenant_id=TENANT, prospect_name="محمد",
            prospect_company="شركة تست",
            sector="saas", source_id=SOURCE,
        )
        first = seq.touches[0]
        assert first.body_ar  # Arabic message exists
        assert first.body_en  # English message exists
        assert "محمد" in first.body_ar
        assert "محمد" in first.body_en

    def test_all_touches_are_drafts(self):
        seq = plan_sequence(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co", source_id=SOURCE,
        )
        for t in seq.touches:
            assert t.status == TouchStatus.DRAFT
            assert t.auto_send is False
            assert t.approval_required is True

    def test_opt_out_wording_in_messages(self):
        seq = plan_sequence(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co", source_id=SOURCE,
        )
        for t in seq.touches:
            assert "إيقاف" in t.body_ar or "إيقاف" in t.body_ar
            assert "STOP" in t.body_en or "unsubscribe" in t.body_en.lower()


# -----------------------------------------------------------------------
# Response classification
# -----------------------------------------------------------------------


class TestResponseClassification:
    def test_opt_out_english(self):
        assert classify_response("Please STOP messaging me") == ResponseType.OPT_OUT

    def test_opt_out_arabic(self):
        assert classify_response("إيقاف الرسائل") == ResponseType.OPT_OUT

    def test_positive_english(self):
        assert classify_response("Yes, sounds good!") == ResponseType.POSITIVE

    def test_positive_arabic(self):
        assert classify_response("أكيد يناسبني") == ResponseType.POSITIVE

    def test_interested(self):
        assert classify_response("tell me more about pricing") == ResponseType.INTERESTED

    def test_question(self):
        assert classify_response("How does it work?") == ResponseType.QUESTION

    def test_objection(self):
        assert classify_response("too expensive for us") == ResponseType.OBJECTION

    def test_not_now(self):
        assert classify_response("not now, maybe later") == ResponseType.NOT_NOW

    def test_referral(self):
        assert classify_response("try reaching out to our VP") == ResponseType.REFERRAL

    def test_negative(self):
        assert classify_response("no") == ResponseType.NEGATIVE

    def test_empty_no_response(self):
        assert classify_response("") == ResponseType.NO_RESPONSE

    def test_case_insensitive(self):
        assert classify_response("SOUNDS GOOD") == ResponseType.POSITIVE


# -----------------------------------------------------------------------
# Sequence analysis
# -----------------------------------------------------------------------


class TestSequenceAnalysis:
    def test_empty_analysis(self):
        analysis = analyze_sequences(
            tenant_id=TENANT, sequences=[], source_id=SOURCE,
        )
        assert analysis.total_sequences == 0
        assert analysis.reply_rate == 0.0

    def test_basic_analysis(self):
        seq = plan_sequence(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co", source_id=SOURCE,
        )
        analysis = analyze_sequences(
            tenant_id=TENANT, sequences=[seq], source_id=SOURCE,
        )
        assert isinstance(analysis, SequenceAnalysis)
        assert analysis.total_sequences == 1

    def test_deterministic_id(self):
        a1 = analyze_sequences(
            tenant_id=TENANT, sequences=[], source_id=SOURCE,
        )
        a2 = analyze_sequences(
            tenant_id=TENANT, sequences=[], source_id=SOURCE,
        )
        assert a1.analysis_id == a2.analysis_id
        assert a1.analysis_id.startswith("seqanalysis_")


# -----------------------------------------------------------------------
# Safety invariants
# -----------------------------------------------------------------------


class TestOutreachEngineSafety:
    def test_touch_point_never_auto_send(self):
        with pytest.raises(ValueError, match="auto_send must be False"):
            TouchPoint(auto_send=True)

    def test_sequence_never_auto_send(self):
        with pytest.raises(ValueError, match="auto_send must be False"):
            OutreachSequence(
                tenant_id=TENANT, auto_send=True,
                approval_required=True, source_id=SOURCE,
            )

    def test_sequence_requires_approval(self):
        with pytest.raises(ValueError, match="approval_required must be True"):
            OutreachSequence(
                tenant_id=TENANT, auto_send=False,
                approval_required=False, source_id=SOURCE,
            )
