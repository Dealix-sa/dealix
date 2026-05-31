"""Global rules block PII-to-external and over-cap spend."""

from __future__ import annotations

from dealix.hermes.governance_reasoning.global_rules import evaluate


def test_global_rules_block_pii_to_external() -> None:
    result = evaluate("send_email", {"pii": True, "target": "external"})
    assert result.allowed is False
    assert "PII" in result.reason


def test_global_rules_block_over_spend() -> None:
    result = evaluate("buy_ads", {"spend_sar": 10_000})
    assert result.allowed is False


def test_global_rules_allow_safe_action() -> None:
    assert evaluate("draft_proposal", {}).allowed is True
