"""Phase 4: Execution planning, policy validation, hold/dispatch."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from dealix.hermes.kernel.schemas import (
    Decision,
    Execution,
    ExecutionStatus,
    LifecycleEvent,
    SovereigntyLevel,
)


@dataclass
class ExecutionStore:
    _executions: dict[str, Execution] = field(default_factory=dict)
    _events: list[LifecycleEvent] = field(default_factory=list)

    def plan(
        self,
        decision: Decision,
        *,
        agent_id: str,
        tools: list[str],
        payload: dict | None = None,
    ) -> Execution:
        execution = Execution(
            decision_id=decision.decision_id,
            agent_id=agent_id,
            tools=tools,
            payload=payload or {},
            sovereignty_level=decision.sovereignty_level,
            approval_required=decision.requires_approval,
            approval_id=decision.approval_id,
            status=ExecutionStatus.awaiting_approval if decision.requires_approval else ExecutionStatus.planned,
        )
        self._executions[execution.execution_id] = execution
        self._events.append(LifecycleEvent(
            event_type="execution.planned",
            entity_id=execution.execution_id,
            sovereignty_level=execution.sovereignty_level,
            payload={"agent_id": agent_id, "tools": tools},
        ))
        if decision.requires_approval:
            self._events.append(LifecycleEvent(
                event_type="execution.held",
                entity_id=execution.execution_id,
                sovereignty_level=execution.sovereignty_level,
                payload={"reason": "approval_required"},
            ))
        return execution

    def mark_trust_check(self, execution_id: str, passed: bool, reason: str | None = None) -> Execution:
        e = self._executions[execution_id]
        update = {"trust_check_passed": passed}
        if not passed:
            update["status"] = ExecutionStatus.blocked
            update["blocked_reason"] = reason or "trust_check_failed"
        self._executions[execution_id] = e.model_copy(update=update)
        return self._executions[execution_id]

    def dispatch(self, execution_id: str) -> Execution:
        e = self._executions[execution_id]
        if e.approval_required and e.status != ExecutionStatus.approved:
            raise PermissionError(f"execution {execution_id} requires approval before dispatch")
        if not e.trust_check_passed:
            raise PermissionError(f"execution {execution_id} has not passed trust check")
        updated = e.model_copy(update={
            "status": ExecutionStatus.in_flight,
            "started_at": datetime.now(UTC).isoformat(),
        })
        self._executions[execution_id] = updated
        self._events.append(LifecycleEvent(
            event_type="execution.dispatched",
            entity_id=execution_id,
            sovereignty_level=updated.sovereignty_level,
        ))
        return updated

    def approve(self, execution_id: str) -> Execution:
        e = self._executions[execution_id]
        updated = e.model_copy(update={"status": ExecutionStatus.approved})
        self._executions[execution_id] = updated
        return updated

    def complete(self, execution_id: str) -> Execution:
        e = self._executions[execution_id]
        updated = e.model_copy(update={
            "status": ExecutionStatus.completed,
            "completed_at": datetime.now(UTC).isoformat(),
        })
        self._executions[execution_id] = updated
        self._events.append(LifecycleEvent(
            event_type="execution.completed",
            entity_id=execution_id,
            sovereignty_level=updated.sovereignty_level,
        ))
        return updated

    def kill(self, execution_id: str, reason: str = "") -> Execution:
        e = self._executions[execution_id]
        updated = e.model_copy(update={"status": ExecutionStatus.killed, "blocked_reason": reason})
        self._executions[execution_id] = updated
        return updated

    def get(self, execution_id: str) -> Execution:
        return self._executions[execution_id]

    def list(self) -> list[Execution]:
        return list(self._executions.values())

    def events(self) -> list[LifecycleEvent]:
        return list(self._events)
