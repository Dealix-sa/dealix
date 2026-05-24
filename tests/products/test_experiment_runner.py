"""Tests for `dealix.products.experiment.ExperimentRunner`."""

from __future__ import annotations

import pytest

from dealix.hermes.core.outcomes import Outcome, OutcomeKind
from dealix.hermes.core.schemas import Money
from dealix.products.experiment import (
    Experiment,
    ExperimentRunner,
    ExperimentStatus,
    ExperimentVerdict,
)


def _money_outcome(amount: float = 1500) -> Outcome:
    return Outcome(
        execution_id="plan_x",
        kind=OutcomeKind.MONEY,
        summary="paid pilot",
        value=Money.sar(amount),
        metrics={"repeatable": 1.0},
    )


def _learning_only_outcome() -> Outcome:
    return Outcome(
        execution_id="plan_y",
        kind=OutcomeKind.LEARNING,
        summary="postmortem note",
        learnings=["did not convert"],
        metrics={"explain_effort": 0.9, "channel_unknown": 1.0, "time_drain": 1.0},
    )


def test_start_marks_experiment_running() -> None:
    runner = ExperimentRunner()
    exp = Experiment(
        name="exp-1",
        hypothesis="Adding a follow-up doubles conversion",
        minimum_outcomes=3,
    )
    started = runner.start(exp)
    assert started.status == ExperimentStatus.RUNNING
    assert started.started_at is not None
    with pytest.raises(ValueError):
        runner.start(exp)  # duplicate


def test_record_result_appends_outcome() -> None:
    runner = ExperimentRunner()
    exp = runner.start(
        Experiment(name="exp-2", hypothesis="x", minimum_outcomes=2)
    )
    out = _money_outcome()
    updated = runner.record_result(exp.experiment_id, out)
    assert len(updated.outcomes) == 1
    assert updated.outcomes[0].outcome_id == out.outcome_id


def test_assess_scale_when_many_money_outcomes() -> None:
    runner = ExperimentRunner()
    exp = runner.start(
        Experiment(name="exp-scale", hypothesis="scales", minimum_outcomes=3)
    )
    runner.record_result(exp.experiment_id, _money_outcome(2000))
    runner.record_result(exp.experiment_id, _money_outcome(3000))
    runner.record_result(exp.experiment_id, _money_outcome(5000))
    runner.record_result(
        exp.experiment_id,
        Outcome(
            execution_id="plan_z",
            kind=OutcomeKind.ASSET,
            summary="template",
        ),
    )
    verdict = runner.assess(exp.experiment_id)
    assert verdict == ExperimentVerdict.SCALE
    assert runner.get(exp.experiment_id).status == ExperimentStatus.DECIDED


def test_assess_kill_when_only_learnings_and_risk_signals() -> None:
    runner = ExperimentRunner()
    exp = runner.start(
        Experiment(name="exp-kill", hypothesis="will fail", minimum_outcomes=2)
    )
    runner.record_result(exp.experiment_id, _learning_only_outcome())
    runner.record_result(
        exp.experiment_id,
        _learning_only_outcome().model_copy(update={"risk_flag": True}),
    )
    verdict = runner.assess(exp.experiment_id)
    assert verdict == ExperimentVerdict.KILL


def test_assess_hold_when_below_minimum_outcomes() -> None:
    runner = ExperimentRunner()
    exp = runner.start(
        Experiment(name="exp-hold", hypothesis="need more data", minimum_outcomes=5)
    )
    runner.record_result(exp.experiment_id, _money_outcome())
    verdict = runner.assess(exp.experiment_id)
    assert verdict == ExperimentVerdict.HOLD
    # Hold doesn't transition status to decided.
    assert runner.get(exp.experiment_id).status == ExperimentStatus.RUNNING
