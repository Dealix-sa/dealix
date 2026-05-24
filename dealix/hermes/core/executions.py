"""Execution Layer — plans, holds, and runs actions under sovereignty + trust."""

from __future__ import annotations

from threading import RLock
from typing import Any

from dealix.hermes.core.schemas import (
    Decision,
    Execution,
    PermissionLevel,
    SovereigntyLevel,
)


class ExecutionStore:
    def __init__(self) -> None:
        self._items: dict[str, Execution] = {}
        self._lock = RLock()

    def plan(
        self,
        decision: Decision,
        *,
        agent_id: str,
        action_type: str,
        permission_level: PermissionLevel | str = PermissionLevel.L1_DRAFT,
        external_action: bool = False,
        expected_result: str = "",
        payload: dict[str, Any] | None = None,
    ) -> Execution:
        perm = PermissionLevel(permission_level)
        sov = SovereigntyLevel(decision.sovereignty_level)
        # Approval is required if external, if commitment, or if sovereignty demands it.
        requires_approval = (
            external_action
            or perm in {PermissionLevel.L3_EXTERNAL_SEND, PermissionLevel.L4_COMMITMENT}
            or sov in {
                SovereigntyLevel.S2_SAMI_APPROVAL,
                SovereigntyLevel.S4_SOVEREIGN_ONLY,
                SovereigntyLevel.S5_NEVER_AUTONOMOUS,
            }
        )
        exe = Execution(
            decision_id=decision.id,
            agent_id=agent_id,
            action_type=action_type,
            permission_level=perm,
            external_action=external_action,
            requires_approval=requires_approval,
            expected_result=expected_result,
            payload=payload or {},
            status="planned",
        )
        with self._lock:
            self._items[exe.id] = exe
        return exe

    def get(self, execution_id: str) -> Execution | None:
        with self._lock:
            return self._items.get(execution_id)

    def set_status(
        self,
        execution_id: str,
        status: str,
        *,
        block_reason: str | None = None,
    ) -> Execution | None:
        with self._lock:
            exe = self._items.get(execution_id)
            if exe is None:
                return None
            updates: dict[str, Any] = {"status": status}
            if block_reason is not None:
                updates["block_reason"] = block_reason
            updated = exe.model_copy(update=updates)
            self._items[execution_id] = updated
            return updated

    def list(self, *, status: str | None = None) -> list[Execution]:
        with self._lock:
            items = list(self._items.values())
        if status:
            items = [e for e in items if e.status == status]
        return sorted(items, key=lambda e: e.created_at, reverse=True)

    def clear(self) -> None:
        with self._lock:
            self._items.clear()


_default_store: ExecutionStore | None = None


def get_execution_store() -> ExecutionStore:
    global _default_store
    if _default_store is None:
        _default_store = ExecutionStore()
    return _default_store
