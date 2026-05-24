"""Apply ScaleKillEvaluator to offer-level outcomes."""

from __future__ import annotations

from dealix.hermes.core.scale import ScaleKillEvaluator, ScaleVerdict
from dealix.hermes.core.schemas import Outcome


class OfferScaleKill:
    def __init__(self, evaluator: ScaleKillEvaluator | None = None) -> None:
        self.evaluator = evaluator or ScaleKillEvaluator()

    def verdict(self, outcomes: list[Outcome]) -> ScaleVerdict:
        return self.evaluator.evaluate(outcomes)


__all__ = ["OfferScaleKill"]
