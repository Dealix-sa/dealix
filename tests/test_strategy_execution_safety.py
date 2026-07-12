"""Safety invariants for the Strategy Execution OS and Money Now Sprint.

These tests pin the non-negotiable rules: draft-only, level 5 blocked, revenue
only on payment_received, and no forbidden claims in generated content.
"""

from __future__ import annotations

from datetime import date

import pytest

from dealix.strategy_execution import (
    growth_engine,
    money_now,
    orchestrator,
    strategy_registry,
)
from dealix.strategy_execution.money_now import EvidenceEvent
from dealix.strategy_execution.safety_gate import clamp_autonomy
from dealix.strategy_execution.schemas import MAX_ENABLED_AUTONOMY_LEVEL, AutonomyLevel


def test_all_required_strategies_present() -> None:
    assert strategy_registry.missing_required() == []
    strategies = strategy_registry.load_strategies()
    assert len(strategies) >= len(strategy_registry.REQUIRED_STRATEGIES)


def test_level_five_is_blocked() -> None:
    assert int(MAX_ENABLED_AUTONOMY_LEVEL) < int(AutonomyLevel.EXTERNAL_EXECUTION)
    assert clamp_autonomy(5) < int(AutonomyLevel.EXTERNAL_EXECUTION)
    assert clamp_autonomy(99) == int(MAX_ENABLED_AUTONOMY_LEVEL)


def test_run_day_is_draft_only_and_produces_queues() -> None:
    result = orchestrator.run_day(
        autonomy_level=3, limit=50, mode="draft-only", run_date=date(2026, 1, 1), write=False
    )
    assert result.strategies
    # External-facing steps are never executed internally.
    for action in result.actions:
        if action.requires_approval:
            assert action.status in {"queued_for_approval", "blocked"}


def test_run_day_rejects_non_draft_mode() -> None:
    with pytest.raises(ValueError):
        orchestrator.run_day(mode="live", write=False)


def test_revenue_only_recognized_on_payment_received() -> None:
    assert money_now.recognized_revenue([]) == 0
    assert (
        money_now.recognized_revenue(
            [EvidenceEvent(prospect="A", event="message_sent_manually")]
        )
        == 0
    )
    assert (
        money_now.recognized_revenue([EvidenceEvent(prospect="A", event="payment_received")])
        == money_now.TOP_OFFER["price_sar"]
    )


def test_content_queue_has_no_forbidden_claims() -> None:
    content = growth_engine.build_content_queue(date(2026, 1, 1))
    assert growth_engine.content_has_forbidden_claims(content) == []


def test_money_now_plan_has_no_more_than_ten_prospects() -> None:
    plan = money_now.build_plan()
    assert len(plan.prospects) <= 10
    assert plan.top_offer["price_sar"] == 499
