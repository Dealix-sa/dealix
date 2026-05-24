"""خادم المنتج — ExperimentRunner.

Experiments wrap a hypothesis, a minimum result count, and a stream of
recorded outcomes. The runner produces a SCALE / KILL / HOLD verdict
that reuses the kernel ScaleKillRecommender so the decision rules stay
in one place.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.outcomes import Outcome
from dealix.hermes.core.scale import (
    ScaleKillKind,
    ScaleKillRecommendation,
    ScaleKillRecommender,
)
from dealix.hermes.core.schemas import utcnow


class ExperimentStatus(StrEnum):
    DRAFT = "draft"
    RUNNING = "running"
    DECIDED = "decided"


class ExperimentVerdict(StrEnum):
    SCALE = "scale"
    KILL = "kill"
    HOLD = "hold"

    @classmethod
    def from_scale_kind(cls, kind: ScaleKillKind) -> ExperimentVerdict:
        return {
            ScaleKillKind.SCALE: cls.SCALE,
            ScaleKillKind.KILL: cls.KILL,
            ScaleKillKind.HOLD: cls.HOLD,
        }[kind]


def _new_experiment_id() -> str:
    return f"exp_{uuid4().hex[:16]}"


class Experiment(BaseModel):
    """A product experiment definition."""

    model_config = ConfigDict(extra="forbid")

    experiment_id: str = Field(default_factory=_new_experiment_id)
    name: str = Field(..., min_length=1, max_length=160)
    hypothesis: str = Field(..., min_length=1, max_length=600)
    minimum_outcomes: int = Field(default=3, ge=1, le=200)
    started_at: datetime | None = None
    status: ExperimentStatus = ExperimentStatus.DRAFT
    outcomes: list[Outcome] = Field(default_factory=list, max_length=500)
    verdict: ExperimentVerdict | None = None
    last_recommendation: ScaleKillRecommendation | None = None


# ─────────────────────────────────────────────────────────────
# Runner
# ─────────────────────────────────────────────────────────────


class ExperimentRunner:
    """In-memory experiment registry + verdict computation."""

    def __init__(self, recommender: ScaleKillRecommender | None = None) -> None:
        self._experiments: dict[str, Experiment] = {}
        self._recommender = recommender or ScaleKillRecommender()

    def start(self, experiment: Experiment) -> Experiment:
        if experiment.experiment_id in self._experiments:
            raise ValueError(
                f"experiment already registered: {experiment.experiment_id}"
            )
        running = experiment.model_copy(
            update={
                "status": ExperimentStatus.RUNNING,
                "started_at": utcnow(),
            }
        )
        self._experiments[running.experiment_id] = running
        return running

    def record_result(self, experiment_id: str, outcome: Outcome) -> Experiment:
        exp = self._get(experiment_id)
        if exp.status == ExperimentStatus.DECIDED:
            raise ValueError(
                f"experiment {experiment_id} already decided; cannot record"
            )
        updated_outcomes = list(exp.outcomes) + [outcome]
        updated = exp.model_copy(update={"outcomes": updated_outcomes})
        self._experiments[experiment_id] = updated
        return updated

    def assess(self, experiment_id: str) -> ExperimentVerdict:
        exp = self._get(experiment_id)
        if len(exp.outcomes) < exp.minimum_outcomes:
            self._experiments[experiment_id] = exp.model_copy(
                update={"last_recommendation": None}
            )
            return ExperimentVerdict.HOLD
        recommendation = self._recommender.recommend(exp.outcomes)
        verdict = ExperimentVerdict.from_scale_kind(recommendation.kind)
        self._experiments[experiment_id] = exp.model_copy(
            update={
                "status": ExperimentStatus.DECIDED,
                "verdict": verdict,
                "last_recommendation": recommendation,
            }
        )
        return verdict

    def get(self, experiment_id: str) -> Experiment:
        return self._get(experiment_id)

    def all(self) -> list[Experiment]:
        return list(self._experiments.values())

    def _get(self, experiment_id: str) -> Experiment:
        try:
            return self._experiments[experiment_id]
        except KeyError as exc:
            raise KeyError(f"unknown experiment: {experiment_id}") from exc


__all__ = [
    "Experiment",
    "ExperimentRunner",
    "ExperimentStatus",
    "ExperimentVerdict",
]
