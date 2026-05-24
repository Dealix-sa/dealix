"""Lightweight experiment tracker for offer pilots."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Experiment:
    id: str
    offer_id: str
    hypothesis: str
    success_metric: str
    success_threshold: float
    samples: int = 0
    wins: int = 0
    closed: bool = False
    closed_at: datetime | None = None

    @property
    def rate(self) -> float:
        return (self.wins / self.samples) if self.samples else 0.0


@dataclass
class ExperimentRegistry:
    _by_id: dict[str, Experiment] = field(default_factory=dict)

    def open(self, *, offer_id: str, hypothesis: str, success_metric: str, success_threshold: float) -> Experiment:
        exp = Experiment(
            id=f"exp_{uuid.uuid4().hex[:10]}",
            offer_id=offer_id,
            hypothesis=hypothesis,
            success_metric=success_metric,
            success_threshold=success_threshold,
        )
        self._by_id[exp.id] = exp
        return exp

    def record(self, experiment_id: str, *, win: bool) -> Experiment:
        exp = self._by_id[experiment_id]
        if exp.closed:
            raise ValueError("Experiment is closed.")
        exp.samples += 1
        if win:
            exp.wins += 1
        return exp

    def close(self, experiment_id: str) -> Experiment:
        exp = self._by_id[experiment_id]
        exp.closed = True
        exp.closed_at = datetime.now(timezone.utc)
        return exp

    def get(self, experiment_id: str) -> Experiment:
        return self._by_id[experiment_id]


__all__ = ["Experiment", "ExperimentRegistry"]
