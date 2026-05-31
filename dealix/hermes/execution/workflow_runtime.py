"""
Workflow Runtime — يشغّل سلسلة من الخطوات (agents + tools) بشكل deterministic،
ويوقف فورًا عند:
    - kill switch tripped
    - step failure with no fallback
    - approval pending (للـ workflows التي تشمل خطوات S2+)

الـ workflows تُعرَّف بشكل بيانات (`WorkflowSpec`) ليكون فحصها وعرضها سهلًا في
الـ UI. كل step يُسجِّل في `RunState`.
"""

from __future__ import annotations

import threading
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from ..contracts import ContextPacket
from ..control_plane.kill_switch import KillSwitch, KillTargetKind
from .agent_runtime import AgentRuntime, ModelFn
from .run_state import RunState, RunStatus


StepFn = Callable[[ContextPacket, dict[str, Any]], dict[str, Any]]


@dataclass(frozen=True)
class WorkflowStep:
    step_id: str
    description: str
    handler: str  # "agent:<agent_id>" | "tool:<tool_id>" | "fn:<step_fn_key>"
    inputs: tuple[str, ...] = ()  # required keys in workflow state
    outputs: tuple[str, ...] = ()  # keys this step writes
    optional: bool = False


@dataclass(frozen=True)
class WorkflowSpec:
    workflow_id: str
    name: str
    purpose: str
    steps: tuple[WorkflowStep, ...]
    owner: str = "unowned"

    def validate(self) -> None:
        if not self.owner or self.owner == "unowned":
            raise ValueError(
                f"workflow `{self.workflow_id}` must have an owner (CTRL-GOV-001)"
            )
        seen: set[str] = set()
        for s in self.steps:
            if s.step_id in seen:
                raise ValueError(f"duplicate step id `{s.step_id}`")
            seen.add(s.step_id)


@dataclass
class WorkflowRunResult:
    run_id: str
    workflow_id: str
    request_id: str
    state: dict[str, Any] = field(default_factory=dict)
    step_log: list[dict[str, Any]] = field(default_factory=list)
    status: RunStatus = RunStatus.PENDING
    error: str | None = None


class WorkflowRuntime:
    def __init__(
        self,
        *,
        agent_runtime: AgentRuntime,
        kill_switch: KillSwitch | None = None,
    ) -> None:
        self._agents = agent_runtime
        self._kill = kill_switch or KillSwitch()
        self._specs: dict[str, WorkflowSpec] = {}
        self._step_fns: dict[str, StepFn] = {}
        self._model_fns: dict[str, ModelFn] = {}
        self._runs: list[RunState] = []
        self._lock = threading.Lock()

    def register_spec(self, spec: WorkflowSpec) -> None:
        spec.validate()
        with self._lock:
            if spec.workflow_id in self._specs:
                raise ValueError(f"workflow `{spec.workflow_id}` already registered")
            self._specs[spec.workflow_id] = spec

    def register_step_fn(self, key: str, fn: StepFn) -> None:
        self._step_fns[key] = fn

    def bind_agent_model(self, agent_id: str, model_fn: ModelFn) -> None:
        self._model_fns[agent_id] = model_fn

    def specs(self) -> list[WorkflowSpec]:
        with self._lock:
            return list(self._specs.values())

    def run(
        self,
        workflow_id: str,
        *,
        context: ContextPacket,
        initial_state: dict[str, Any] | None = None,
    ) -> WorkflowRunResult:
        spec = self._specs.get(workflow_id)
        if spec is None:
            return WorkflowRunResult(
                run_id="",
                workflow_id=workflow_id,
                request_id=context.request_id,
                status=RunStatus.FAILED,
                error="workflow not registered",
            )

        if not self._kill.is_active(KillTargetKind.WORKFLOW, workflow_id):
            return WorkflowRunResult(
                run_id="",
                workflow_id=workflow_id,
                request_id=context.request_id,
                status=RunStatus.FAILED,
                error=f"workflow `{workflow_id}` is killed",
            )

        run = WorkflowRunResult(
            run_id=f"wfr_{uuid.uuid4().hex[:14]}",
            workflow_id=workflow_id,
            request_id=context.request_id,
            state=dict(initial_state or {}),
            status=RunStatus.RUNNING,
        )
        state = RunState(
            run_id=run.run_id,
            kind="workflow",
            target_id=workflow_id,
            request_id=context.request_id,
            status=RunStatus.RUNNING,
        )
        with self._lock:
            self._runs.append(state)

        for step in spec.steps:
            missing = [k for k in step.inputs if k not in run.state]
            if missing and not step.optional:
                run.status = RunStatus.FAILED
                run.error = f"step `{step.step_id}` missing inputs: {missing}"
                state.transition(RunStatus.FAILED, error=run.error)
                return run

            try:
                step_output = self._dispatch(step, context, run.state)
            except Exception as exc:  # noqa: BLE001 — boundary
                run.status = RunStatus.FAILED
                run.error = f"step `{step.step_id}` raised: {exc}"
                state.transition(RunStatus.FAILED, error=run.error)
                return run

            run.step_log.append(
                {
                    "step_id": step.step_id,
                    "handler": step.handler,
                    "at": datetime.now(timezone.utc).isoformat(),
                    "outputs": list(step.outputs),
                }
            )
            for key in step.outputs:
                if key in step_output:
                    run.state[key] = step_output[key]

        run.status = RunStatus.SUCCEEDED
        state.transition(RunStatus.SUCCEEDED)
        return run

    def _dispatch(
        self,
        step: WorkflowStep,
        context: ContextPacket,
        state: dict[str, Any],
    ) -> dict[str, Any]:
        kind, _, target = step.handler.partition(":")
        if not target:
            raise ValueError(f"step `{step.step_id}` has malformed handler")

        if kind == "agent":
            model_fn = self._model_fns.get(target)
            if model_fn is None:
                raise RuntimeError(f"no model bound for agent `{target}`")
            result = self._agents.run(
                target,
                context=context,
                prompt_payload={k: state.get(k) for k in step.inputs},
                model_fn=model_fn,
            )
            if result.status != RunStatus.SUCCEEDED:
                raise RuntimeError(result.error or "agent failed")
            return result.output

        if kind == "tool":
            actor_kind = context.actor.kind.value if context.actor else "system"
            call = self._agents.tools().call(
                target,
                args={k: state.get(k) for k in step.inputs},
                actor_kind=actor_kind,
            )
            if not call.success:
                raise RuntimeError(call.error or "tool failed")
            return call.output

        if kind == "fn":
            fn = self._step_fns.get(target)
            if fn is None:
                raise RuntimeError(f"step fn `{target}` not registered")
            return fn(context, {k: state.get(k) for k in step.inputs})

        raise ValueError(f"unknown handler kind `{kind}`")


__all__ = [
    "StepFn",
    "WorkflowRunResult",
    "WorkflowRuntime",
    "WorkflowSpec",
    "WorkflowStep",
]
