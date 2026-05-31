"""
Experiment metrics — keep experiments honest.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExperimentMetrics:
    experiment_id: str
    sample_size: int
    primary_metric_delta: float
    confidence_interval_low: float
    confidence_interval_high: float
    powered: bool
    verdict: str
    notes: list[str]


def score_experiment(
    experiment_id: str,
    *,
    control_n: int,
    treatment_n: int,
    control_metric: float,
    treatment_metric: float,
    confidence_interval: tuple[float, float],
    min_detectable_effect: float = 0.05,
) -> ExperimentMetrics:
    sample_size = control_n + treatment_n
    delta = treatment_metric - control_metric
    ci_low, ci_high = confidence_interval
    powered = sample_size >= 100 and abs(delta) >= min_detectable_effect
    notes: list[str] = []
    if sample_size < 100:
        notes.append(f"underpowered sample size {sample_size} < 100")
    if abs(delta) < min_detectable_effect:
        notes.append(
            f"observed delta {delta:+.3f} below MDE {min_detectable_effect}"
        )
    if ci_low <= 0 <= ci_high:
        verdict = "inconclusive"
        notes.append("confidence interval crosses zero")
    elif delta > 0:
        verdict = "ship"
    else:
        verdict = "kill"

    return ExperimentMetrics(
        experiment_id=experiment_id,
        sample_size=sample_size,
        primary_metric_delta=round(delta, 4),
        confidence_interval_low=ci_low,
        confidence_interval_high=ci_high,
        powered=powered,
        verdict=verdict,
        notes=notes,
    )
