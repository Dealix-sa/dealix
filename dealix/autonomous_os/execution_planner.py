"""
Execution Planner — turns a Strategy into a routed ExecutionPlan.

The planner does not execute anything. It expands each strategy step, asks
the SafetyGate where the step should go (auto-draft / approval / blocked),
and records the routing decision on the step. The orchestrator consumes the
plan and dispatches to the queues.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .safety_gate import Route, SafetyGate
from .strategy_registry import Strategy, StrategyStep


@dataclass
class PlannedStep:
    strategy_id: str
    action: str
    kind: str
    channel: str | None
    offer: str | None
    risk: float
    route: str
    reason: str
    output: str | None
    description: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategy_id": self.strategy_id,
            "action": self.action,
            "kind": self.kind,
            "channel": self.channel,
            "offer": self.offer,
            "risk": self.risk,
            "route": self.route,
            "reason": self.reason,
            "output": self.output,
            "description": self.description,
        }


@dataclass
class ExecutionPlan:
    strategy_id: str
    strategy_name: str
    language: str
    steps: list[PlannedStep] = field(default_factory=list)

    @property
    def auto_steps(self) -> list[PlannedStep]:
        return [s for s in self.steps if s.route == Route.AUTO_DRAFT.value]

    @property
    def approval_steps(self) -> list[PlannedStep]:
        return [s for s in self.steps if s.route == Route.APPROVAL.value]

    @property
    def blocked_steps(self) -> list[PlannedStep]:
        return [s for s in self.steps if s.route == Route.BLOCKED.value]

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategy_id": self.strategy_id,
            "strategy_name": self.strategy_name,
            "language": self.language,
            "counts": {
                "auto": len(self.auto_steps),
                "approval": len(self.approval_steps),
                "blocked": len(self.blocked_steps),
            },
            "steps": [s.to_dict() for s in self.steps],
        }


class ExecutionPlanner:
    def __init__(self, gate: SafetyGate) -> None:
        self.gate = gate

    def _plan_step(self, strategy: Strategy, step: StrategyStep) -> PlannedStep:
        decision = self.gate.evaluate(
            action=step.action,
            kind=step.kind,
            channel=step.channel,
            risk=step.risk,
            requires_approval=step.requires_approval,
        )
        return PlannedStep(
            strategy_id=strategy.id,
            action=step.action,
            kind=step.kind,
            channel=step.channel,
            offer=step.offer,
            risk=step.risk,
            route=decision.route.value,
            reason=decision.reason,
            output=step.output,
            description=step.description,
        )

    def plan(self, strategy: Strategy) -> ExecutionPlan:
        plan = ExecutionPlan(
            strategy_id=strategy.id,
            strategy_name=strategy.name,
            language=strategy.language,
        )
        for step in strategy.steps:
            plan.steps.append(self._plan_step(strategy, step))
        return plan
