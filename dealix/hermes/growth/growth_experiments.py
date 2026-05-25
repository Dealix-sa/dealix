"""
Growth Experiments — كل experiment له decision_rule واضحة قبل البدء، ولا
يُعتبر منتهيًا قبل أن نقرر expand / kill / iterate بشكل صريح.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import StrEnum


class ExperimentVerdict(StrEnum):
    PENDING = "pending"
    EXPAND = "expand"
    KILL = "kill"
    ITERATE = "iterate"


@dataclass
class Experiment:
    experiment_id: str
    hypothesis: str
    decision_rule: str  # eg "expand if cpql < 250 SAR over 50 leads"
    target_metric: str
    target_threshold: float
    sample_size_min: int
    notes: str | None = None


@dataclass
class ExperimentResult:
    experiment_id: str
    samples: int
    measured: float
    verdict: ExperimentVerdict
    rationale: str
    next_action: str


class GrowthExperimentBook:
    def __init__(self) -> None:
        self._experiments: dict[str, Experiment] = {}
        self._results: list[ExperimentResult] = []
        self._lock = threading.Lock()

    def register(self, experiment: Experiment) -> Experiment:
        if not experiment.decision_rule:
            raise ValueError("experiment requires a decision_rule")
        with self._lock:
            if experiment.experiment_id in self._experiments:
                raise ValueError(
                    f"experiment `{experiment.experiment_id}` already registered"
                )
            self._experiments[experiment.experiment_id] = experiment
        return experiment

    def decide(
        self,
        experiment_id: str,
        *,
        samples: int,
        measured: float,
        next_action: str,
    ) -> ExperimentResult:
        with self._lock:
            exp = self._experiments.get(experiment_id)
        if exp is None:
            raise KeyError(experiment_id)
        if samples < exp.sample_size_min:
            verdict = ExperimentVerdict.PENDING
            rationale = (
                f"sample {samples} below min {exp.sample_size_min} — keep running"
            )
        elif measured >= exp.target_threshold:
            verdict = ExperimentVerdict.EXPAND
            rationale = (
                f"measured {measured} >= threshold {exp.target_threshold}"
            )
        elif measured < exp.target_threshold * 0.5:
            verdict = ExperimentVerdict.KILL
            rationale = (
                f"measured {measured} < 50% of threshold {exp.target_threshold}"
            )
        else:
            verdict = ExperimentVerdict.ITERATE
            rationale = (
                f"measured {measured} between 50% and 100% of threshold"
            )
        result = ExperimentResult(
            experiment_id=experiment_id,
            samples=samples,
            measured=measured,
            verdict=verdict,
            rationale=rationale,
            next_action=next_action,
        )
        with self._lock:
            self._results.append(result)
        return result


__all__ = [
    "Experiment",
    "ExperimentResult",
    "ExperimentVerdict",
    "GrowthExperimentBook",
]
