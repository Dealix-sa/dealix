"""خادم Hermes — outcome logging.

An Outcome captures *what happened* after an ExecutionResult lands. Spec
§26 names seven kinds of outcome the kernel cares about. Outcomes are
the seed for assets (asset.created) and the input to scale/kill.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator

from dealix.hermes.core.executions import ExecutionResult, ExecutionStatus
from dealix.hermes.core.schemas import Money, utcnow


class OutcomeKind(StrEnum):
    """Spec §26 — seven canonical outcome kinds."""

    MONEY = "money"
    DATA = "data"
    ASSET = "asset"
    PARTNER = "partner"
    ACCESS = "access"
    TRUST = "trust"
    LEARNING = "learning"


def _new_outcome_id() -> str:
    return f"out_{uuid4().hex}"


class Outcome(BaseModel):
    """A single recorded outcome from one execution."""

    model_config = ConfigDict(extra="forbid")

    outcome_id: str = Field(default_factory=_new_outcome_id)
    execution_id: str = Field(..., min_length=1)
    kind: OutcomeKind
    summary: str = Field(..., min_length=1, max_length=600)
    value: Money | None = None
    metrics: dict[str, float] = Field(default_factory=dict)
    learnings: list[str] = Field(default_factory=list, max_length=20)
    risk_flag: bool = False
    created_at: datetime = Field(default_factory=utcnow)

    @model_validator(mode="after")
    def _money_outcomes_have_value(self) -> Outcome:
        if self.kind == OutcomeKind.MONEY and self.value is None:
            raise ValueError("MONEY outcomes must include a Money value")
        return self


# ─────────────────────────────────────────────────────────────
# Logger
# ─────────────────────────────────────────────────────────────


class OutcomeLogger:
    """In-memory outcome log + factory helper."""

    def __init__(self) -> None:
        self._outcomes: list[Outcome] = []

    def log(
        self,
        execution: ExecutionResult,
        kind: OutcomeKind,
        summary: str,
        *,
        value: Money | None = None,
        metrics: dict[str, float] | None = None,
        learnings: list[str] | None = None,
        risk_flag: bool = False,
    ) -> Outcome:
        outcome = Outcome(
            execution_id=execution.plan_id,
            kind=kind,
            summary=summary,
            value=value,
            metrics=dict(metrics or {}),
            learnings=list(learnings or []),
            risk_flag=risk_flag,
        )
        self._outcomes.append(outcome)
        return outcome

    @staticmethod
    def infer_kind(execution: ExecutionResult) -> OutcomeKind:
        """Fallback heuristic for callers that don't know the kind."""
        if execution.status == ExecutionStatus.FAILED:
            return OutcomeKind.LEARNING
        if execution.cost.amount > 0:
            return OutcomeKind.ASSET
        return OutcomeKind.DATA

    def all(self) -> list[Outcome]:
        return list(self._outcomes)

    def for_execution(self, execution_id: str) -> list[Outcome]:
        return [o for o in self._outcomes if o.execution_id == execution_id]

    def by_kind(self, kind: OutcomeKind) -> list[Outcome]:
        return [o for o in self._outcomes if o.kind == kind]

    def total_money(self) -> Money:
        total = sum(
            (o.value.amount for o in self._outcomes if o.value is not None),
            start=Money.sar(0).amount,
        )
        return Money.sar(total)

    def to_dict(self) -> dict[str, Any]:
        return {"count": len(self._outcomes), "outcomes": [o.model_dump(mode="json") for o in self._outcomes]}


__all__ = [
    "Outcome",
    "OutcomeKind",
    "OutcomeLogger",
]
