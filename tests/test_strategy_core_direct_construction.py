"""Direct-construction regression tests for the strategy policy core."""

from __future__ import annotations

import pytest

from dealix.strategy_core import ActionKind, Route, StrategyDefinition, StrategyStep, evaluate_step


def test_direct_step_normalizes_kind_risk_and_false_string() -> None:
    step = StrategyStep(
        action="Prepare Brief",
        kind="internal_draft",  # type: ignore[arg-type]
        risk=0,
        requires_approval="false",  # type: ignore[arg-type]
    )

    assert step.action == "prepare brief"
    assert step.kind == ActionKind.INTERNAL_DRAFT
    assert step.risk == 0.0
    assert step.requires_approval is False


def test_direct_strategy_normalizes_enabled_and_requires_typed_steps() -> None:
    strategy = StrategyDefinition(
        strategy_id="strategy_direct",
        name="Direct",
        goal="Prove strict construction.",
        enabled="false",  # type: ignore[arg-type]
        steps=(StrategyStep(action="analyze", kind=ActionKind.ANALYZE),),
    )

    assert strategy.enabled is False

    with pytest.raises(TypeError, match="StrategyStep"):
        StrategyDefinition(
            strategy_id="bad_steps",
            name="Bad",
            goal="Reject strings.",
            steps=("not-a-step",),  # type: ignore[arg-type]
        )


def test_automation_and_cold_outreach_variants_are_blocked() -> None:
    actions = (
        "cold_outreach_sequence",
        "cold_whatsapp_campaign",
        "auto_send_email",
        "linkedin_automation_dm",
        "linkedin_scrape_contacts",
    )

    for action in actions:
        decision = evaluate_step(
            StrategyStep(action=action, kind=ActionKind.INTERNAL_DRAFT),
            autonomy_level=4,
        )
        assert decision.route == Route.BLOCKED
        assert decision.external_action_allowed is False
