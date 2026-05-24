"""Sovereignty gate — keep the founder as the only commercial authority."""

from __future__ import annotations

from dealix.hermes.sovereignty import (
    SOVEREIGN_ONLY_ACTIONS,
    SovereigntyLevel,
    evaluate,
    required_level_for,
)


def test_sovereign_only_actions_never_autonomous() -> None:
    for action in SOVEREIGN_ONLY_ACTIONS:
        result = evaluate(action, agent_max_level=SovereigntyLevel.L5_LOW_RISK_AUTONOMOUS)
        assert result.allowed is False
        assert result.requires_approval is True
        assert result.level == SovereigntyLevel.L6_SOVEREIGN_ONLY


def test_external_actions_require_approval() -> None:
    result = evaluate("send_external_message")
    assert result.allowed is False
    assert result.requires_approval is True
    assert result.level == SovereigntyLevel.L4_EXTERNAL_APPROVAL


def test_internal_draft_is_allowed_for_default_agent() -> None:
    result = evaluate("draft_outreach")
    assert result.allowed is True
    assert result.requires_approval is False


def test_unknown_actions_default_to_approval() -> None:
    result = evaluate("rebrand_company")
    assert result.requires_approval is True


def test_required_level_for_read_is_observe() -> None:
    assert required_level_for("read_leads") == SovereigntyLevel.L0_OBSERVE
