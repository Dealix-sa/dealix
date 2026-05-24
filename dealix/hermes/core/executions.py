"""Execution Planner — turns an approved decision into ordered steps.

The planner never *runs* steps; it returns a plan. The orchestrator + the
relevant agents/tools are responsible for execution under the sovereignty
gate and trust check.
"""

from __future__ import annotations

from collections.abc import Iterable

from dealix.hermes.core.schemas import (
    DecisionMemo,
    ExecutionPlan,
    ExecutionStatus,
    ExecutionStep,
    Opportunity,
)


class ExecutionPlanner:
    def __init__(self) -> None:
        self._plans: dict[str, ExecutionPlan] = {}

    def draft_plan(
        self,
        *,
        opportunity: Opportunity,
        memo: DecisionMemo | None,
        steps: Iterable[ExecutionStep],
    ) -> ExecutionPlan:
        step_list = list(steps)
        if not step_list:
            raise ValueError("execution plan must include at least one step")

        plan = ExecutionPlan(
            opportunity_id=opportunity.opportunity_id,
            memo_id=memo.memo_id if memo else None,
            steps=step_list,
            status=(
                ExecutionStatus.PENDING_APPROVAL
                if memo and memo.approval_required and memo.approved_at is None
                else ExecutionStatus.PLANNED
            ),
        )
        self._plans[plan.plan_id] = plan
        return plan

    def mark(self, plan_id: str, status: ExecutionStatus) -> ExecutionPlan:
        plan = self._plans.get(plan_id)
        if plan is None:
            raise KeyError(plan_id)
        plan = plan.model_copy(update={"status": status})
        self._plans[plan_id] = plan
        return plan

    def get(self, plan_id: str) -> ExecutionPlan | None:
        return self._plans.get(plan_id)

    def all(self) -> list[ExecutionPlan]:
        return list(self._plans.values())

    def in_flight(self) -> list[ExecutionPlan]:
        return [
            p
            for p in self._plans.values()
            if p.status
            in {ExecutionStatus.PLANNED, ExecutionStatus.IN_PROGRESS, ExecutionStatus.APPROVED}
        ]


__all__ = ["ExecutionPlanner"]
