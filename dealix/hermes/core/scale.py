"""Scale / Kill evaluator.

After enough outcomes accumulate against a given asset / offer / vertical,
the kernel suggests one of: SCALE, HOLD, KILL. The default thresholds are
deliberately conservative; domains may override.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from dealix.hermes.core.schemas import Outcome, OutcomeStatus


class ScaleVerdict(str, Enum):
    SCALE = "scale"
    HOLD = "hold"
    KILL = "kill"


@dataclass
class ScaleKillEvaluator:
    min_samples: int = 5
    win_rate_scale: float = 0.6
    win_rate_kill: float = 0.2

    def evaluate(self, outcomes: list[Outcome]) -> ScaleVerdict:
        finalized = [o for o in outcomes if o.status != OutcomeStatus.PENDING]
        if len(finalized) < self.min_samples:
            return ScaleVerdict.HOLD
        wins = sum(1 for o in finalized if o.status == OutcomeStatus.WIN)
        rate = wins / len(finalized)
        if rate >= self.win_rate_scale:
            return ScaleVerdict.SCALE
        if rate <= self.win_rate_kill:
            return ScaleVerdict.KILL
        return ScaleVerdict.HOLD


__all__ = ["ScaleKillEvaluator", "ScaleVerdict"]
