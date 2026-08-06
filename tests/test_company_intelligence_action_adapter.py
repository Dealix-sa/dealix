"""Tests for the normalize_next_best_action adapter.

Verifies that operational NextBestAction recommendations are correctly
bridged to CanonicalAction without escalating authority.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from dealix.company_intelligence import (
    ActionStatus,
    ActionType,
    AutonomyLevel,
    CanonicalAction,
    RiskLevel,
)
from dealix.company_intelligence.action_adapter import normalize_next_best_action


def _nba(**overrides: object) -> SimpleNamespace:
    """Build a duck-typed NextBestAction-like object."""
    values: dict[str, object] = {
        "action": "send_email_with_value_first_intro",
        "channel": "email",
        "rationale": "Start with a value-first email",
        "expected_reply_lift": 1.0,
        "confidence": 0.55,
        "playbook_id": None,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


# ---------------------------------------------------------------------------
# Basic normalization
# ---------------------------------------------------------------------------


class TestNormalizeNextBestActionBasic:
    """Core normalization behavior."""

    def test_produces_canonical_action(self) -> None:
        action = normalize_next_best_action(
            _nba(), tenant_id="tenant-a", opportunity_id="opp-1"
        )
        assert isinstance(action, CanonicalAction)
        assert action.tenant_id == "tenant-a"
        assert action.opportunity_id == "opp-1"
        assert action.status == ActionStatus.QUEUED
        assert action.approval_required is True

    def test_frozen_immutability(self) -> None:
        action = normalize_next_best_action(
            _nba(), tenant_id="t", opportunity_id="o"
        )
        with pytest.raises(Exception):
            action.status = ActionStatus.COMPLETED  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Channel → ActionType mapping
# ---------------------------------------------------------------------------


class TestChannelMapping:
    """Verify channel → ActionType mapping."""

    @pytest.mark.parametrize(
        ("channel", "expected"),
        [
            ("email", ActionType.PREPARE_DRAFT),
            ("whatsapp", ActionType.PREPARE_DRAFT),
            ("linkedin", ActionType.PREPARE_DRAFT),
            ("call", ActionType.SCHEDULE_MEETING),
            ("meeting", ActionType.SCHEDULE_MEETING),
            ("manual", ActionType.INTERNAL_UPDATE),
        ],
    )
    def test_channel_to_action_type(
        self, channel: str, expected: ActionType
    ) -> None:
        action = normalize_next_best_action(
            _nba(channel=channel), tenant_id="t", opportunity_id="o"
        )
        assert action.action_type == expected

    def test_unknown_channel_fallback_to_internal(self) -> None:
        action = normalize_next_best_action(
            _nba(channel="carrier_pigeon"),
            tenant_id="t",
            opportunity_id="o",
        )
        assert action.action_type == ActionType.INTERNAL_UPDATE


# ---------------------------------------------------------------------------
# External effect and autonomy
# ---------------------------------------------------------------------------


class TestExternalEffects:
    """Verify external effect and autonomy level derivation."""

    @pytest.mark.parametrize("channel", ["email", "whatsapp", "linkedin"])
    def test_external_channels_set_external_effect(self, channel: str) -> None:
        action = normalize_next_best_action(
            _nba(channel=channel), tenant_id="t", opportunity_id="o"
        )
        assert action.external_effect is True
        assert action.autonomy_level == AutonomyLevel.L4_CONTROLLED_EXECUTE
        assert action.approval_required is True

    @pytest.mark.parametrize("channel", ["manual", "call", "meeting"])
    def test_non_external_channels_no_external_effect(self, channel: str) -> None:
        action = normalize_next_best_action(
            _nba(channel=channel), tenant_id="t", opportunity_id="o"
        )
        assert action.external_effect is False
        assert action.autonomy_level == AutonomyLevel.L2_DRAFT


# ---------------------------------------------------------------------------
# Risk level derivation
# ---------------------------------------------------------------------------


class TestRiskLevel:
    """Verify risk level derivation from channel + confidence."""

    def test_external_low_confidence_high_risk(self) -> None:
        action = normalize_next_best_action(
            _nba(channel="whatsapp", confidence=0.3),
            tenant_id="t",
            opportunity_id="o",
        )
        assert action.risk_level == RiskLevel.HIGH

    def test_external_high_confidence_medium_risk(self) -> None:
        action = normalize_next_best_action(
            _nba(channel="email", confidence=0.8),
            tenant_id="t",
            opportunity_id="o",
        )
        assert action.risk_level == RiskLevel.MEDIUM

    def test_manual_channel_low_risk(self) -> None:
        action = normalize_next_best_action(
            _nba(channel="manual", confidence=0.3),
            tenant_id="t",
            opportunity_id="o",
        )
        assert action.risk_level == RiskLevel.LOW


# ---------------------------------------------------------------------------
# Priority inputs
# ---------------------------------------------------------------------------


class TestPriorityInputs:
    """Verify priority input derivation."""

    def test_high_lift_high_impact(self) -> None:
        action = normalize_next_best_action(
            _nba(expected_reply_lift=3.0),
            tenant_id="t",
            opportunity_id="o",
        )
        assert action.impact == 1.0

    def test_zero_lift_minimum_impact(self) -> None:
        action = normalize_next_best_action(
            _nba(expected_reply_lift=0.0),
            tenant_id="t",
            opportunity_id="o",
        )
        assert action.impact == 0.1

    def test_moderate_lift_moderate_impact(self) -> None:
        action = normalize_next_best_action(
            _nba(expected_reply_lift=1.5),
            tenant_id="t",
            opportunity_id="o",
        )
        assert action.impact == 0.5

    def test_confidence_used_in_action(self) -> None:
        action = normalize_next_best_action(
            _nba(confidence=0.85),
            tenant_id="t",
            opportunity_id="o",
        )
        assert action.confidence == 0.85

    def test_priority_score_computed(self) -> None:
        action = normalize_next_best_action(
            _nba(), tenant_id="t", opportunity_id="o"
        )
        assert action.priority_score > 0


# ---------------------------------------------------------------------------
# Trigger and objective
# ---------------------------------------------------------------------------


class TestTriggerAndObjective:
    """Verify trigger and objective derivation."""

    def test_trigger_contains_action_name(self) -> None:
        action = normalize_next_best_action(
            _nba(action="propose_demo_within_24h"),
            tenant_id="t",
            opportunity_id="o",
        )
        assert "propose_demo_within_24h" in action.trigger

    def test_objective_is_rationale(self) -> None:
        action = normalize_next_best_action(
            _nba(rationale="Speed wins in Saudi B2B"),
            tenant_id="t",
            opportunity_id="o",
        )
        assert action.objective == "Speed wins in Saudi B2B"


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


class TestDeterminism:
    """Verify deterministic action_id generation."""

    def test_same_recommendation_same_id(self) -> None:
        a = normalize_next_best_action(
            _nba(), tenant_id="t", opportunity_id="o"
        )
        b = normalize_next_best_action(
            _nba(), tenant_id="t", opportunity_id="o"
        )
        assert a.action_id == b.action_id

    def test_different_tenant_different_id(self) -> None:
        a = normalize_next_best_action(
            _nba(), tenant_id="t1", opportunity_id="o"
        )
        b = normalize_next_best_action(
            _nba(), tenant_id="t2", opportunity_id="o"
        )
        assert a.action_id != b.action_id


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestValidation:
    """Verify input validation."""

    def test_rejects_empty_action(self) -> None:
        with pytest.raises(ValueError, match="action"):
            normalize_next_best_action(
                _nba(action=""),
                tenant_id="t",
                opportunity_id="o",
            )

    def test_confidence_clamped(self) -> None:
        action = normalize_next_best_action(
            _nba(confidence=1.5),
            tenant_id="t",
            opportunity_id="o",
        )
        assert action.confidence == 1.0
