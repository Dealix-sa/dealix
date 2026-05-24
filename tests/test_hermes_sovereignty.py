"""Tests for the Hermes sovereignty gate."""

from __future__ import annotations

from dealix.hermes.sovereignty import (
    NEVER_AUTONOMOUS_ACTIONS,
    SOVEREIGN_ONLY_ACTIONS,
    SovereigntyLevel,
    classify_action,
)


def test_sovereign_only_action_requires_sami() -> None:
    result = classify_action("launch_marketplace")
    assert result.allowed is False
    assert result.requires_sami_approval is True
    assert result.level == SovereigntyLevel.S4_SOVEREIGN_ONLY


def test_never_autonomous_action_blocked() -> None:
    result = classify_action("make_financial_transfer")
    assert result.allowed is False
    assert result.level == SovereigntyLevel.S5_NEVER_AUTONOMOUS
    assert result.requires_memo is True


def test_internal_action_allowed() -> None:
    result = classify_action("internal_create_task")
    assert result.allowed is True
    assert result.level == SovereigntyLevel.S1_INTERNAL


def test_external_action_requires_approval() -> None:
    result = classify_action("external_send_email")
    assert result.allowed is False
    assert result.level == SovereigntyLevel.S2_SAMI_APPROVAL


def test_sensitive_data_routes_to_sovereign_memo() -> None:
    result = classify_action("internal_review", contains_sensitive_data=True)
    assert result.allowed is False
    assert result.level == SovereigntyLevel.S3_SOVEREIGN_MEMO


def test_unknown_action_defaults_to_safe() -> None:
    result = classify_action("compute_score")
    assert result.allowed is True
    assert result.level == SovereigntyLevel.S0_AUTO_SAFE


def test_sovereign_only_set_includes_money_and_marketplace() -> None:
    assert "transfer_money" in SOVEREIGN_ONLY_ACTIONS
    assert "launch_marketplace" in SOVEREIGN_ONLY_ACTIONS
    assert "make_financial_transfer" in NEVER_AUTONOMOUS_ACTIONS
