"""Verticals scale / kill — wraps the core ScaleKillEvaluator with hooks."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.scale import ScaleKillEvaluator, ScaleVerdict
from dealix.hermes.core.schemas import Outcome


@dataclass
class VentureKillScale:
    evaluator: ScaleKillEvaluator

    def verdict(self, outcomes: list[Outcome]) -> ScaleVerdict:
        return self.evaluator.evaluate(outcomes)


__all__ = ["VentureKillScale"]
