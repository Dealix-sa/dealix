"""ExecutionPlanner — turn an approved decision into a runnable execution.

The planner does **not** invoke tools. It owns the lifecycle and lineage.
Actual tool invocation lives in the Trust Gateway (so we can interpose
auditing, scopes, and the MCP gateway).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from dealix.hermes.core.schemas import Decision, Execution, ExecutionStatus


class ExecutionPlanner:
    def __init__(self) -> None:
        self._by_id: dict[str, Execution] = {}

    def plan(self, *, decision: Decision, agent_id: str, steps: list[dict], tool_ids: Iterable[str] = ()) -> Execution:
        if not decision.is_executable:
            raise PermissionError(
                f"Decision {decision.id} is not executable (status={decision.status.value})."
            )
        exe = Execution.make(decision_id=decision.id, agent_id=agent_id, owner=decision.owner)
        exe.steps = list(steps)
        exe.tool_ids = list(tool_ids)
        self._by_id[exe.id] = exe
        return exe

    def start(self, execution_id: str) -> Execution:
        exe = self._by_id[execution_id]
        exe.status = ExecutionStatus.RUNNING
        exe.started_at = datetime.now(timezone.utc)
        exe.touch()
        return exe

    def complete(self, execution_id: str) -> Execution:
        exe = self._by_id[execution_id]
        exe.status = ExecutionStatus.COMPLETED
        exe.finished_at = datetime.now(timezone.utc)
        exe.touch()
        return exe

    def fail(self, execution_id: str, *, reason: str) -> Execution:
        exe = self._by_id[execution_id]
        exe.status = ExecutionStatus.FAILED
        exe.finished_at = datetime.now(timezone.utc)
        exe.payload["failure_reason"] = reason
        exe.touch()
        return exe

    def cancel(self, execution_id: str) -> Execution:
        exe = self._by_id[execution_id]
        exe.status = ExecutionStatus.CANCELLED
        exe.finished_at = datetime.now(timezone.utc)
        exe.touch()
        return exe

    def get(self, execution_id: str) -> Execution:
        return self._by_id[execution_id]

    def all(self) -> list[Execution]:
        return list(self._by_id.values())

    def by_status(self, status: ExecutionStatus) -> list[Execution]:
        return [e for e in self._by_id.values() if e.status == status]


__all__ = ["ExecutionPlanner"]
