"""Retention cohorts."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RetentionCohort:
    cohort_id: str
    started_at: str
    active_count: int
    initial_count: int

    @property
    def rate(self) -> float:
        return round(self.active_count / self.initial_count, 4) if self.initial_count else 0.0


@dataclass
class RetentionLedger:
    _cohorts: list[RetentionCohort] = field(default_factory=list)

    def add(self, cohort: RetentionCohort) -> RetentionCohort:
        self._cohorts.append(cohort)
        return cohort

    def list(self) -> list[RetentionCohort]:
        return list(self._cohorts)
