"""Decide whether to scale, iterate, or kill an experiment."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from dealix.growth_os.experiments.card import ExperimentCard, ExperimentResult

Decision = Literal[
    "insufficient_data",
    "scale_variant_a",
    "scale_variant_b",
    "iterate",
    "kill",
]


class ExperimentDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    experiment_id: str
    decision: Decision
    reason_ar: str
    reason_en: str
    lift: float = Field(default=0.0)


def evaluate_experiment(
    card: ExperimentCard, result: ExperimentResult
) -> ExperimentDecision:
    """Return a decision honoring ``minimum_sample`` and a 2x lift rule."""
    if (
        result.variant_a_sample < card.minimum_sample
        or result.variant_b_sample < card.minimum_sample
    ):
        return ExperimentDecision(
            experiment_id=card.experiment_id,
            decision="insufficient_data",
            reason_ar="حجم العينة أقل من الحد الأدنى",
            reason_en="Sample size below the minimum",
            lift=0.0,
        )

    a = result.variant_a_outcome
    b = result.variant_b_outcome

    if a == 0 and b == 0:
        return ExperimentDecision(
            experiment_id=card.experiment_id,
            decision="kill",
            reason_ar="لا نتائج من أي متغيّر",
            reason_en="No outcomes from either variant",
            lift=0.0,
        )

    if b >= 2 * a and b > 0:
        lift = (b - a) / a if a > 0 else float("inf")
        return ExperimentDecision(
            experiment_id=card.experiment_id,
            decision="scale_variant_b",
            reason_ar="المتغيّر B تجاوز ضعف A",
            reason_en="Variant B exceeded 2x of A",
            lift=round(lift, 4) if a > 0 else 0.0,
        )

    if a >= 2 * b and a > 0:
        lift = (a - b) / b if b > 0 else float("inf")
        return ExperimentDecision(
            experiment_id=card.experiment_id,
            decision="scale_variant_a",
            reason_ar="المتغيّر A تجاوز ضعف B",
            reason_en="Variant A exceeded 2x of B",
            lift=round(lift, 4) if b > 0 else 0.0,
        )

    lift = (b - a) / a if a > 0 else 0.0
    return ExperimentDecision(
        experiment_id=card.experiment_id,
        decision="iterate",
        reason_ar="الفرق ضمن نطاق التكرار",
        reason_en="Delta within the iterate band",
        lift=round(lift, 4),
    )


__all__ = ["Decision", "ExperimentDecision", "evaluate_experiment"]
