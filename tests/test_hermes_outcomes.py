"""Tests for outcome → asset promotion and the Kernel stores."""

from __future__ import annotations

from dealix.hermes.core.outcomes import OutcomeStore
from dealix.hermes.core.schemas import HermesOutcome
from dealix.hermes.orchestrator import HermesOrchestrator


def test_won_outcome_promotes_to_asset() -> None:
    orchestrator = HermesOrchestrator()
    outcome = HermesOutcome(
        outcome_type="sales_close",
        expected_result="close deal",
        actual_result="closed 2,999 SAR",
        status="won",
        revenue_sar=2999,
    )
    asset = orchestrator.outcome_to_asset(outcome)
    assert asset is not None
    assert asset.asset_type == "playbook"
    assert asset.reusable is True


def test_lost_outcome_with_learning_promotes() -> None:
    orchestrator = HermesOrchestrator()
    outcome = HermesOutcome(
        outcome_type="sales_close",
        expected_result="close deal",
        actual_result="declined: timing",
        status="lost",
        learning="Buyer needs Q3 budget cycle.",
    )
    asset = orchestrator.outcome_to_asset(outcome)
    assert asset is not None


def test_ignored_outcome_without_learning_does_not_promote() -> None:
    orchestrator = HermesOrchestrator()
    outcome = HermesOutcome(
        outcome_type="ping",
        expected_result="reply",
        status="ignored",
    )
    asset = orchestrator.outcome_to_asset(outcome)
    assert asset is None


def test_outcome_store_aggregates_revenue() -> None:
    store = OutcomeStore()
    store.add(
        HermesOutcome(
            outcome_type="sales_close",
            expected_result="close",
            status="won",
            revenue_sar=499,
        )
    )
    store.add(
        HermesOutcome(
            outcome_type="sales_close",
            expected_result="close",
            status="won",
            revenue_sar=2999,
        )
    )
    assert store.total_revenue_sar() == 3498
    assert len(store.wins()) == 2
