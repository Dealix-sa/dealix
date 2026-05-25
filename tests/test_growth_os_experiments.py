"""Experiment decision tests."""

from __future__ import annotations

from dealix.growth_os.experiments.card import ExperimentCard, ExperimentResult
from dealix.growth_os.experiments.decision_engine import evaluate_experiment


def _card(min_sample: int = 100) -> ExperimentCard:
    return ExperimentCard(
        experiment_id="exp_1",
        hypothesis="Variant B will outperform A on signups",
        audience="founders",
        variant_a="copy A",
        variant_b="copy B",
        success_metric="signups",
        minimum_sample=min_sample,
    )


def test_under_sample_returns_insufficient_data() -> None:
    res = ExperimentResult(
        variant_a_outcome=10, variant_b_outcome=20,
        variant_a_sample=10, variant_b_sample=10,
    )
    decision = evaluate_experiment(_card(min_sample=100), res)
    assert decision.decision == "insufficient_data"


def test_2x_b_wins_scales_b() -> None:
    res = ExperimentResult(
        variant_a_outcome=10, variant_b_outcome=25,
        variant_a_sample=200, variant_b_sample=200,
    )
    decision = evaluate_experiment(_card(min_sample=100), res)
    assert decision.decision == "scale_variant_b"
    assert decision.lift >= 1.0


def test_2x_a_wins_scales_a() -> None:
    res = ExperimentResult(
        variant_a_outcome=30, variant_b_outcome=5,
        variant_a_sample=200, variant_b_sample=200,
    )
    decision = evaluate_experiment(_card(min_sample=100), res)
    assert decision.decision == "scale_variant_a"


def test_equal_outcomes_iterate() -> None:
    res = ExperimentResult(
        variant_a_outcome=10, variant_b_outcome=10,
        variant_a_sample=200, variant_b_sample=200,
    )
    decision = evaluate_experiment(_card(min_sample=100), res)
    assert decision.decision == "iterate"


def test_both_zero_outcomes_kill() -> None:
    res = ExperimentResult(
        variant_a_outcome=0, variant_b_outcome=0,
        variant_a_sample=200, variant_b_sample=200,
    )
    decision = evaluate_experiment(_card(min_sample=100), res)
    assert decision.decision == "kill"
