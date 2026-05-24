"""Agent mesh — execute an ordered task plan with handler dispatch + tracing.

The mesh is the L5 (Agent) executor of the AI Stack. It takes a
:class:`TaskPlan` from the task router and a registry of handlers (callables
keyed by agent_id), runs each task through the agent runner, and produces a
stable :class:`MeshTrace` that downstream layers (governance, proof) consume.

The mesh is **deterministic for a fixed handler registry**: agents are
called in declared order, errors short-circuit non-optional tasks, and the
trace records every input hash + output summary.

Handler signature: ``handler(payload: Mapping[str, Any]) -> Mapping[str, Any]``.

Tests can register lightweight handlers via :class:`AgentMesh.register` and
call :meth:`AgentMesh.execute` without touching real LLM agents — the same
surface that production wiring uses.
"""

from __future__ import annotations

import threading
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field
from datetime import UTC
from typing import Any

from auto_client_acquisition.agent_os.agent_card import AgentCard, AgentStatus
from auto_client_acquisition.agent_os.agent_lifecycle import AgentLifecycleState
from auto_client_acquisition.agent_os.agent_runner import (
    AgentHandler,
    AgentRun,
    run_agent,
)
from auto_client_acquisition.agent_os.task_router import AgentTask, TaskPlan


@dataclass(frozen=True, slots=True)
class MeshTrace:
    """Result of executing a TaskPlan through the mesh."""

    offer_tier: str
    runs: tuple[AgentRun, ...] = field(default_factory=tuple)
    halted: bool = False
    halt_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = {
            "offer_tier": self.offer_tier,
            "runs": [r.to_dict() for r in self.runs],
            "halted": self.halted,
            "halt_reason": self.halt_reason,
        }
        return data

    @property
    def all_ok(self) -> bool:
        return not self.halted and all(r.status == "ok" for r in self.runs)

    def by_agent_id(self, agent_id: str) -> tuple[AgentRun, ...]:
        return tuple(r for r in self.runs if r.agent_id == agent_id)


class AgentMesh:
    """Registry + executor for governed agent handlers.

    A mesh holds:

    * The ``AgentCard`` for every agent that may execute (identity gate).
    * A handler callable per agent (the actual work).
    * An optional lifecycle override per agent (default: PRODUCTION).

    Production wiring registers real handlers (LLM-backed). Tests register
    stub handlers that return plain dicts.
    """

    __slots__ = ("_cards", "_handlers", "_lifecycle", "_lock")

    def __init__(self) -> None:
        self._cards: dict[str, AgentCard] = {}
        self._handlers: dict[str, AgentHandler] = {}
        self._lifecycle: dict[str, AgentLifecycleState] = {}
        self._lock = threading.RLock()

    def register(
        self,
        *,
        card: AgentCard,
        handler: AgentHandler,
        lifecycle_state: AgentLifecycleState = AgentLifecycleState.PRODUCTION,
    ) -> None:
        """Register a handler for an agent_id. Idempotent: re-registering replaces."""
        if not card.agent_id.strip():
            raise ValueError("agent_id is required")
        with self._lock:
            self._cards[card.agent_id] = card
            self._handlers[card.agent_id] = handler
            self._lifecycle[card.agent_id] = lifecycle_state

    def unregister(self, agent_id: str) -> bool:
        with self._lock:
            removed = self._cards.pop(agent_id, None) is not None
            self._handlers.pop(agent_id, None)
            self._lifecycle.pop(agent_id, None)
            return removed

    def has_agent(self, agent_id: str) -> bool:
        with self._lock:
            return agent_id in self._cards

    def registered_agents(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(sorted(self._cards))

    def execute(
        self,
        plan: TaskPlan,
        *,
        halt_on_error: bool = True,
    ) -> MeshTrace:
        """Run a task plan through the mesh in declared order.

        * **Required tasks** (``optional=False``) — a non-ok run halts the
          mesh when ``halt_on_error=True`` (default).
        * **Optional tasks** (``optional=True``) — failures are recorded but
          do not halt the mesh.
        """
        runs: list[AgentRun] = []
        halt_reason: str | None = None
        halted = False

        for task in plan.tasks:
            with self._lock:
                card = self._cards.get(task.agent_id)
                handler = self._handlers.get(task.agent_id)
                lifecycle = self._lifecycle.get(
                    task.agent_id,
                    AgentLifecycleState.PRODUCTION,
                )

            if card is None or handler is None:
                run = _missing_handler_run(task)
                runs.append(run)
                if not task.optional and halt_on_error:
                    halted = True
                    halt_reason = f"missing_handler:{task.agent_id}"
                    break
                continue

            if card.status == AgentStatus.KILLED.value:
                run = _killed_card_run(task, card=card)
                runs.append(run)
                if not task.optional and halt_on_error:
                    halted = True
                    halt_reason = f"agent_killed:{task.agent_id}"
                    break
                continue

            run = run_agent(
                card=card,
                handler=handler,
                payload=task.payload,
                lifecycle_state=lifecycle,
                metadata={"step": task.step, "purpose": task.purpose},
            )
            runs.append(run)
            if run.status != "ok" and not task.optional and halt_on_error:
                halted = True
                halt_reason = f"{run.status}:{task.agent_id}:{run.error or run.output_summary}"
                break

        return MeshTrace(
            offer_tier=plan.offer_tier,
            runs=tuple(runs),
            halted=halted,
            halt_reason=halt_reason,
        )


def _missing_handler_run(task: AgentTask) -> AgentRun:
    from datetime import datetime, timezone

    now = datetime.now(UTC).isoformat()
    return AgentRun(
        run_id=f"ar_missing_{task.agent_id}",
        agent_id=task.agent_id,
        agent_name=task.agent_id,
        status="blocked",
        started_at=now,
        completed_at=now,
        duration_ms=0,
        input_hash="",
        output_summary=f"no handler registered for agent_id={task.agent_id}",
        output=None,
        error="missing_handler",
        metadata={"step": task.step, "purpose": task.purpose},
    )


def _killed_card_run(task: AgentTask, *, card: AgentCard) -> AgentRun:
    from datetime import datetime, timezone

    now = datetime.now(UTC).isoformat()
    return AgentRun(
        run_id=f"ar_killed_{task.agent_id}",
        agent_id=task.agent_id,
        agent_name=card.name,
        status="blocked",
        started_at=now,
        completed_at=now,
        duration_ms=0,
        input_hash="",
        output_summary=f"agent killed: {card.killed_reason or 'unspecified'}",
        output=None,
        error="agent_killed",
        metadata={"step": task.step, "purpose": task.purpose},
    )


__all__ = [
    "AgentMesh",
    "MeshTrace",
]
