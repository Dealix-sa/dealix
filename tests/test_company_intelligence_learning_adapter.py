"""Tests for the learning adapter — flywheel LearningEvent and WinLoss normalization.

Covers both ``normalize_learning_event`` and ``normalize_win_loss`` with
fail-closed defaults, evidence-ref assembly, confidence mapping, and
canonical contract invariants.
"""
from __future__ import annotations

import types
from datetime import UTC, datetime, timezone

import pytest

from dealix.company_intelligence.learning_adapter import (
    _KIND_MAP,
    _OUTCOME_CONFIDENCE,
    _OUTCOME_TYPE,
    _resolve_kind,
    normalize_learning_event,
    normalize_win_loss,
)
from dealix.company_intelligence.outcome_contracts import (
    CanonicalLearningEvent,
    LearningEventType,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_event(**overrides):
    """Build a minimal flywheel-style event namespace."""
    defaults = {
        "kind": "lead_scored",
        "customer_handle": "acme",
        "timestamp": datetime(2025, 6, 1, 12, 0, tzinfo=UTC),
        "sector": "tech",
        "channel": "email",
        "offer": "pilot",
        "succeeded": True,
        "notes_en": "Good response rate",
        "notes_ar": "",
    }
    defaults.update(overrides)
    return types.SimpleNamespace(**defaults)


def _make_win_loss(**overrides):
    """Build a minimal WinLoss-style record namespace."""
    defaults = {
        "outcome": "won",
        "company": "Acme Corp",
        "lesson": "Fast onboarding",
        "next_change": "Reduce pilot scope",
        "sector": "saas",
        "channel": "whatsapp",
        "offer": "pilot_30",
        "reason": "price",
        "objection": "too_expensive",
        "created_at": datetime(2025, 7, 1, 10, 0, tzinfo=UTC),
    }
    defaults.update(overrides)
    return types.SimpleNamespace(**defaults)


# ===================================================================
# Test _resolve_kind mapping
# ===================================================================


class TestResolveKind:
    """Verify kind → LearningEventType mapping."""

    def test_all_mapped_kinds(self):
        """Every entry in _KIND_MAP resolves to its documented type."""
        for kind, expected in _KIND_MAP.items():
            assert _resolve_kind(kind) == expected

    def test_case_insensitive(self):
        assert _resolve_kind("Lead_Scored") == LearningEventType.TARGETING
        assert _resolve_kind("MANUAL_MESSAGE_SENT") == LearningEventType.MESSAGE

    def test_whitespace_stripped(self):
        assert _resolve_kind("  demo_booked  ") == LearningEventType.OFFER

    def test_unknown_kind_fails_closed_to_targeting(self):
        assert _resolve_kind("completely_unknown") == LearningEventType.TARGETING
        assert _resolve_kind("") == LearningEventType.TARGETING

    def test_kind_coverage(self):
        """All seven canonical LearningEventType values are reachable."""
        mapped_types = set(_KIND_MAP.values())
        assert mapped_types == set(LearningEventType)


# ===================================================================
# Test normalize_learning_event — happy path
# ===================================================================


class TestNormalizeLearningEventHappyPath:
    """Canonical output from valid flywheel events."""

    def test_basic_event(self):
        event = _make_event()
        result = normalize_learning_event(event, tenant_id="t1")

        assert isinstance(result, CanonicalLearningEvent)
        assert result.tenant_id == "t1"
        assert result.event_type == LearningEventType.TARGETING
        assert result.confidence == 0.7  # succeeded=True
        assert result.hypothesis_only is True
        assert result.approval_required is True
        assert result.applied is False
        assert result.official_policy_change_allowed is False

    def test_evidence_refs_include_context(self):
        event = _make_event(
            kind="manual_message_sent",
            customer_handle="beta",
            sector="fintech",
            channel="linkedin",
            offer="diagnostic",
        )
        result = normalize_learning_event(event, tenant_id="t1")

        assert "flywheel:manual_message_sent" in result.evidence_refs
        assert "customer:beta" in result.evidence_refs
        assert "sector:fintech" in result.evidence_refs
        assert "channel:linkedin" in result.evidence_refs
        assert "offer:diagnostic" in result.evidence_refs

    def test_succeeded_true_confidence(self):
        result = normalize_learning_event(
            _make_event(succeeded=True), tenant_id="t1"
        )
        assert result.confidence == 0.7

    def test_succeeded_false_confidence(self):
        result = normalize_learning_event(
            _make_event(succeeded=False), tenant_id="t1"
        )
        assert result.confidence == 0.4

    def test_succeeded_none_confidence(self):
        result = normalize_learning_event(
            _make_event(succeeded=None), tenant_id="t1"
        )
        assert result.confidence == 0.5

    def test_recommended_change_from_notes_en(self):
        result = normalize_learning_event(
            _make_event(notes_en="Improve targeting", notes_ar=""),
            tenant_id="t1",
        )
        assert result.recommended_change == "Improve targeting"

    def test_recommended_change_falls_back_to_notes_ar(self):
        result = normalize_learning_event(
            _make_event(notes_en="", notes_ar="تحسين الاستهداف"),
            tenant_id="t1",
        )
        assert result.recommended_change == "تحسين الاستهداف"

    def test_recommended_change_fallback_default(self):
        result = normalize_learning_event(
            _make_event(notes_en="", notes_ar="", customer_handle="gamma"),
            tenant_id="t1",
        )
        assert "lead_scored" in result.recommended_change
        assert "gamma" in result.recommended_change

    def test_timestamp_preserved(self):
        ts = datetime(2025, 3, 15, 8, 30, tzinfo=UTC)
        result = normalize_learning_event(
            _make_event(timestamp=ts), tenant_id="t1"
        )
        assert result.created_at == ts


# ===================================================================
# Test normalize_learning_event — edge cases
# ===================================================================


class TestNormalizeLearningEventEdgeCases:
    """Edge-case and fail-closed behavior."""

    def test_empty_kind_raises(self):
        with pytest.raises(ValueError, match="non-empty kind"):
            normalize_learning_event(_make_event(kind=""), tenant_id="t1")

    def test_none_kind_raises(self):
        with pytest.raises(ValueError, match="non-empty kind"):
            normalize_learning_event(_make_event(kind=None), tenant_id="t1")

    def test_unknown_kind_defaults_to_targeting(self):
        result = normalize_learning_event(
            _make_event(kind="invented_kind"), tenant_id="t1"
        )
        assert result.event_type == LearningEventType.TARGETING

    def test_missing_customer_handle(self):
        result = normalize_learning_event(
            _make_event(customer_handle=""), tenant_id="t1"
        )
        # Should still produce a valid event without customer ref
        assert not any(r.startswith("customer:") for r in result.evidence_refs)

    def test_missing_optional_context_fields(self):
        event = _make_event(sector="", channel="", offer="")
        result = normalize_learning_event(event, tenant_id="t1")
        refs = result.evidence_refs
        assert not any(r.startswith("sector:") for r in refs)
        assert not any(r.startswith("channel:") for r in refs)
        assert not any(r.startswith("offer:") for r in refs)

    def test_none_timestamp_uses_utc_now(self):
        result = normalize_learning_event(
            _make_event(timestamp=None), tenant_id="t1"
        )
        assert result.created_at.tzinfo is not None

    def test_iso_string_timestamp(self):
        result = normalize_learning_event(
            _make_event(timestamp="2025-06-15T14:30:00+00:00"),
            tenant_id="t1",
        )
        assert result.created_at.year == 2025
        assert result.created_at.month == 6

    def test_naive_datetime_gets_utc(self):
        naive = datetime(2025, 1, 1, 0, 0)
        result = normalize_learning_event(
            _make_event(timestamp=naive), tenant_id="t1"
        )
        assert result.created_at.tzinfo is not None

    def test_invalid_timestamp_string_fallback(self):
        result = normalize_learning_event(
            _make_event(timestamp="not-a-date"), tenant_id="t1"
        )
        assert result.created_at.tzinfo is not None


# ===================================================================
# Test normalize_learning_event — kind mapping coverage
# ===================================================================


class TestKindMappingCoverage:
    """Verify representative kinds map to expected types."""

    @pytest.mark.parametrize(
        "kind, expected_type",
        [
            ("signal_created", LearningEventType.TARGETING),
            ("lead_created", LearningEventType.TARGETING),
            ("lead_scored", LearningEventType.TARGETING),
            ("churn_risk_detected", LearningEventType.TARGETING),
            ("decision_passport_created", LearningEventType.DATA_QUALITY),
            ("manual_message_sent", LearningEventType.MESSAGE),
            ("reply_received", LearningEventType.MESSAGE),
            ("action_created", LearningEventType.NEGOTIATION),
            ("action_approved", LearningEventType.NEGOTIATION),
            ("action_rejected", LearningEventType.NEGOTIATION),
            ("demo_booked", LearningEventType.OFFER),
            ("pilot_requested", LearningEventType.OFFER),
            ("upsell_offered", LearningEventType.OFFER),
            ("upsell_accepted", LearningEventType.OFFER),
            ("diagnostic_delivered", LearningEventType.DELIVERY),
            ("payment_confirmed", LearningEventType.DELIVERY),
            ("delivery_started", LearningEventType.DELIVERY),
            ("proof_created", LearningEventType.DELIVERY),
            ("monthly_started", LearningEventType.DELIVERY),
            ("feature_request_received", LearningEventType.TECHNICAL),
        ],
    )
    def test_kind_mapping(self, kind, expected_type):
        result = normalize_learning_event(
            _make_event(kind=kind), tenant_id="t1"
        )
        assert result.event_type == expected_type


# ===================================================================
# Test normalize_win_loss — happy path
# ===================================================================


class TestNormalizeWinLossHappyPath:
    """Canonical output from valid win/loss records."""

    def test_won_outcome(self):
        record = _make_win_loss(outcome="won")
        result = normalize_win_loss(record, tenant_id="t1")

        assert isinstance(result, CanonicalLearningEvent)
        assert result.tenant_id == "t1"
        assert result.event_type == LearningEventType.NEGOTIATION
        assert result.confidence == 0.7
        assert result.hypothesis_only is True
        assert result.approval_required is True
        assert result.applied is False

    def test_lost_outcome(self):
        result = normalize_win_loss(
            _make_win_loss(outcome="lost"), tenant_id="t1"
        )
        assert result.event_type == LearningEventType.NEGOTIATION
        assert result.confidence == 0.5

    def test_no_decision_outcome(self):
        result = normalize_win_loss(
            _make_win_loss(outcome="no_decision"), tenant_id="t1"
        )
        assert result.event_type == LearningEventType.TARGETING
        assert result.confidence == 0.3

    def test_evidence_refs_include_context(self):
        record = _make_win_loss(
            company="Beta Co",
            sector="logistics",
            channel="phone",
            offer="sprint",
            reason="timing",
            objection="budget",
        )
        result = normalize_win_loss(record, tenant_id="t1")

        assert "win_loss:won" in result.evidence_refs
        assert "company:Beta Co" in result.evidence_refs
        assert "sector:logistics" in result.evidence_refs
        assert "channel:phone" in result.evidence_refs
        assert "offer:sprint" in result.evidence_refs
        assert "reason:timing" in result.evidence_refs
        assert "objection:budget" in result.evidence_refs

    def test_recommended_change_from_lesson_and_next(self):
        result = normalize_win_loss(
            _make_win_loss(lesson="Quick demo works", next_change="Do more demos"),
            tenant_id="t1",
        )
        assert "Quick demo works" in result.recommended_change
        assert "Next: Do more demos" in result.recommended_change
        assert " | " in result.recommended_change

    def test_recommended_change_lesson_only(self):
        result = normalize_win_loss(
            _make_win_loss(lesson="Price was right", next_change=""),
            tenant_id="t1",
        )
        assert result.recommended_change == "Price was right"

    def test_recommended_change_next_change_only(self):
        result = normalize_win_loss(
            _make_win_loss(lesson="", next_change="Reduce scope"),
            tenant_id="t1",
        )
        assert result.recommended_change == "Next: Reduce scope"

    def test_created_at_preserved(self):
        ts = datetime(2025, 8, 1, 15, 0, tzinfo=UTC)
        result = normalize_win_loss(
            _make_win_loss(created_at=ts), tenant_id="t1"
        )
        assert result.created_at == ts


# ===================================================================
# Test normalize_win_loss — edge cases
# ===================================================================


class TestNormalizeWinLossEdgeCases:
    """Edge-case and fail-closed behavior for win/loss normalization."""

    def test_empty_lesson_and_next_change_raises(self):
        with pytest.raises(ValueError, match="non-empty lesson or next_change"):
            normalize_win_loss(
                _make_win_loss(lesson="", next_change=""),
                tenant_id="t1",
            )

    def test_unknown_outcome_defaults(self):
        result = normalize_win_loss(
            _make_win_loss(outcome="unknown_status"),
            tenant_id="t1",
        )
        assert result.event_type == LearningEventType.TARGETING
        assert result.confidence == 0.3

    def test_none_outcome_defaults(self):
        result = normalize_win_loss(
            _make_win_loss(outcome=None),
            tenant_id="t1",
        )
        assert result.event_type == LearningEventType.TARGETING
        assert result.confidence == 0.3

    def test_missing_company(self):
        result = normalize_win_loss(
            _make_win_loss(company=""), tenant_id="t1"
        )
        assert not any(r.startswith("company:") for r in result.evidence_refs)

    def test_missing_optional_fields(self):
        record = _make_win_loss(sector="", channel="", offer="", reason="", objection="")
        result = normalize_win_loss(record, tenant_id="t1")
        refs = result.evidence_refs
        assert not any(r.startswith("sector:") for r in refs)
        assert not any(r.startswith("channel:") for r in refs)
        assert not any(r.startswith("offer:") for r in refs)
        assert not any(r.startswith("reason:") for r in refs)
        assert not any(r.startswith("objection:") for r in refs)

    def test_none_created_at_uses_utc_now(self):
        result = normalize_win_loss(
            _make_win_loss(created_at=None), tenant_id="t1"
        )
        assert result.created_at.tzinfo is not None

    def test_iso_string_created_at(self):
        result = normalize_win_loss(
            _make_win_loss(created_at="2025-07-20T09:00:00+03:00"),
            tenant_id="t1",
        )
        assert result.created_at.year == 2025

    def test_naive_datetime_gets_utc(self):
        naive = datetime(2025, 5, 1, 12, 0)
        result = normalize_win_loss(
            _make_win_loss(created_at=naive), tenant_id="t1"
        )
        assert result.created_at.tzinfo is not None

    def test_invalid_created_at_fallback(self):
        result = normalize_win_loss(
            _make_win_loss(created_at="garbage"), tenant_id="t1"
        )
        assert result.created_at.tzinfo is not None

    def test_outcome_case_insensitive(self):
        result = normalize_win_loss(
            _make_win_loss(outcome="WON"), tenant_id="t1"
        )
        assert result.confidence == 0.7
        assert result.event_type == LearningEventType.NEGOTIATION


# ===================================================================
# Test canonical contract invariants
# ===================================================================


class TestCanonicalInvariants:
    """Verify all canonical governance invariants hold."""

    def test_learning_event_frozen(self):
        result = normalize_learning_event(_make_event(), tenant_id="t1")
        with pytest.raises(Exception):
            result.confidence = 0.99

    def test_win_loss_frozen(self):
        result = normalize_win_loss(_make_win_loss(), tenant_id="t1")
        with pytest.raises(Exception):
            result.confidence = 0.99

    def test_learning_id_deterministic(self):
        event = _make_event()
        r1 = normalize_learning_event(event, tenant_id="t1")
        r2 = normalize_learning_event(event, tenant_id="t1")
        assert r1.learning_id == r2.learning_id

    def test_win_loss_id_deterministic(self):
        record = _make_win_loss()
        r1 = normalize_win_loss(record, tenant_id="t1")
        r2 = normalize_win_loss(record, tenant_id="t1")
        assert r1.learning_id == r2.learning_id

    def test_different_tenants_different_ids(self):
        event = _make_event()
        r1 = normalize_learning_event(event, tenant_id="t1")
        r2 = normalize_learning_event(event, tenant_id="t2")
        assert r1.learning_id != r2.learning_id

    def test_evidence_refs_sorted(self):
        result = normalize_learning_event(
            _make_event(sector="z_sector", channel="a_channel"),
            tenant_id="t1",
        )
        assert result.evidence_refs == sorted(result.evidence_refs)

    def test_win_loss_evidence_refs_sorted(self):
        result = normalize_win_loss(
            _make_win_loss(sector="z", channel="a"),
            tenant_id="t1",
        )
        assert result.evidence_refs == sorted(result.evidence_refs)

    def test_never_marks_applied(self):
        """Adapter must never mark a learning event as applied."""
        r1 = normalize_learning_event(_make_event(), tenant_id="t1")
        r2 = normalize_win_loss(_make_win_loss(), tenant_id="t1")
        assert r1.applied is False
        assert r2.applied is False

    def test_never_grants_policy_authority(self):
        """Adapter must never grant official policy change authority."""
        r1 = normalize_learning_event(_make_event(), tenant_id="t1")
        r2 = normalize_win_loss(_make_win_loss(), tenant_id="t1")
        assert r1.official_policy_change_allowed is False
        assert r2.official_policy_change_allowed is False

    def test_always_hypothesis_only(self):
        r1 = normalize_learning_event(_make_event(), tenant_id="t1")
        r2 = normalize_win_loss(_make_win_loss(), tenant_id="t1")
        assert r1.hypothesis_only is True
        assert r2.hypothesis_only is True

    def test_always_approval_required(self):
        r1 = normalize_learning_event(_make_event(), tenant_id="t1")
        r2 = normalize_win_loss(_make_win_loss(), tenant_id="t1")
        assert r1.approval_required is True
        assert r2.approval_required is True


# ===================================================================
# Test outcome confidence and type mapping constants
# ===================================================================


class TestOutcomeMappingConstants:
    """Verify the win/loss mapping dictionaries cover expected values."""

    def test_confidence_values(self):
        assert _OUTCOME_CONFIDENCE["won"] == 0.7
        assert _OUTCOME_CONFIDENCE["lost"] == 0.5
        assert _OUTCOME_CONFIDENCE["no_decision"] == 0.3

    def test_type_values(self):
        assert _OUTCOME_TYPE["won"] == LearningEventType.NEGOTIATION
        assert _OUTCOME_TYPE["lost"] == LearningEventType.NEGOTIATION
        assert _OUTCOME_TYPE["no_decision"] == LearningEventType.TARGETING


# ===================================================================
# Test duck-typing resilience
# ===================================================================


class TestDuckTypingResilience:
    """Adapter works with any object providing the expected attributes."""

    def test_dict_like_event(self):
        """A dict won't have getattr-accessible attrs, but a namespace will."""

        class DictEvent:
            kind = "reply_received"
            customer_handle = "delta"
            timestamp = datetime(2025, 4, 1, tzinfo=UTC)
            sector = ""
            channel = ""
            offer = ""
            succeeded = None
            notes_en = "test"
            notes_ar = ""

        result = normalize_learning_event(DictEvent(), tenant_id="t1")
        assert result.event_type == LearningEventType.MESSAGE

    def test_partial_win_loss(self):
        """Win/loss with only required fields still produces valid output."""

        class MinimalWinLoss:
            outcome = "lost"
            company = ""
            lesson = "Need better pricing"
            next_change = ""
            sector = ""
            channel = ""
            offer = ""
            reason = ""
            objection = ""
            created_at = None

        result = normalize_win_loss(MinimalWinLoss(), tenant_id="t1")
        assert result.event_type == LearningEventType.NEGOTIATION
        assert result.confidence == 0.5
        assert result.recommended_change == "Need better pricing"
