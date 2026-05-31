"""Growth experiments with explicit hypothesis, metric, kill rule."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ExperimentStatus(StrEnum):
    proposed = "proposed"
    approved = "approved"
    running = "running"
    completed = "completed"
    killed = "killed"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _xid() -> str:
    return f"exp_{uuid.uuid4().hex[:16]}"


class GrowthExperiment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    experiment_id: str = Field(default_factory=_xid)
    title: str
    hypothesis: str
    primary_metric: str
    success_threshold: float
    kill_rule: str
    status: ExperimentStatus = ExperimentStatus.proposed
    observed_metric: float | None = None
    created_at: str = Field(default_factory=_now)


@dataclass
class GrowthExperimentStore:
    _experiments: dict[str, GrowthExperiment] = field(default_factory=dict)

    def propose(self, exp: GrowthExperiment) -> GrowthExperiment:
        self._experiments[exp.experiment_id] = exp
        return exp

    def transition(self, experiment_id: str, status: ExperimentStatus) -> GrowthExperiment:
        e = self._experiments[experiment_id]
        updated = e.model_copy(update={"status": status})
        self._experiments[experiment_id] = updated
        return updated

    def list(self) -> list[GrowthExperiment]:
        return list(self._experiments.values())

    def get(self, experiment_id: str) -> GrowthExperiment:
        return self._experiments[experiment_id]
