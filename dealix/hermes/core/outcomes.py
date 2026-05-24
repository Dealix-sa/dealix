"""OutcomeLedger — the recorded result of every execution.

The no-orphan invariant is the entire point here: every COMPLETED
execution must produce an outcome. Audit queries this ledger to flag
dangling executions.
"""

from __future__ import annotations

from dealix.hermes.core.schemas import Execution, ExecutionStatus, Outcome, OutcomeStatus


class OutcomeLedger:
    def __init__(self) -> None:
        self._by_id: dict[str, Outcome] = {}
        self._by_execution: dict[str, str] = {}

    def record(self, outcome: Outcome) -> Outcome:
        if outcome.execution_id in self._by_execution:
            raise ValueError(
                f"Execution {outcome.execution_id} already has an outcome ({self._by_execution[outcome.execution_id]})."
            )
        self._by_id[outcome.id] = outcome
        self._by_execution[outcome.execution_id] = outcome.id
        return outcome

    def for_execution(self, execution_id: str) -> Outcome | None:
        outcome_id = self._by_execution.get(execution_id)
        return self._by_id.get(outcome_id) if outcome_id else None

    def has_outcome(self, execution_id: str) -> bool:
        return execution_id in self._by_execution

    def all(self) -> list[Outcome]:
        return list(self._by_id.values())

    def wins(self) -> list[Outcome]:
        return [o for o in self._by_id.values() if o.status == OutcomeStatus.WIN]

    def total_revenue_sar(self) -> float:
        return sum(o.revenue_sar for o in self._by_id.values())

    def orphan_executions(self, executions: list[Execution]) -> list[Execution]:
        """COMPLETED executions with no outcome are orphans."""
        return [
            e
            for e in executions
            if e.status == ExecutionStatus.COMPLETED and not self.has_outcome(e.id)
        ]


__all__ = ["OutcomeLedger"]
