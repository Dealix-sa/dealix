"""Experiments — card schema + decision engine."""

from __future__ import annotations

from dealix.growth_os.experiments.card import ExperimentCard, ExperimentResult
from dealix.growth_os.experiments.decision_engine import (
    ExperimentDecision,
    evaluate_experiment,
)

__all__ = [
    "ExperimentCard",
    "ExperimentDecision",
    "ExperimentResult",
    "evaluate_experiment",
]
