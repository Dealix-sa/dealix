"""خادم Hermes — execution plans.

ExecutionPlan describes the agent/tool steps needed to act on a Decision.
It does NOT run anything — the orchestrator (or the AgentRegistry) is the
actual runtime; this module only stitches the plan together.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from dealix.hermes.core.decisions import Decision
from dealix.hermes.core.opportunities import OpportunityType
from dealix.hermes.core.schemas import Money, utcnow


class ExecutionStatus(StrEnum):
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"


class StepStatus(StrEnum):
    PENDING = "pending"
    OK = "ok"
    ERROR = "error"
    SKIPPED = "skipped"


def _new_step_id() -> str:
    return f"step_{uuid4().hex[:16]}"


def _new_plan_id() -> str:
    return f"plan_{uuid4().hex}"


class ExecutionStep(BaseModel):
    """A single agent.tool call inside a plan."""

    model_config = ConfigDict(extra="forbid")

    step_id: str = Field(default_factory=_new_step_id)
    agent_id: str = Field(..., min_length=1, max_length=128)
    tool_id: str = Field(..., min_length=1, max_length=128)
    action: str = Field(..., min_length=1, max_length=128)
    args: dict[str, Any] = Field(default_factory=dict)
    expected_outcome: str = Field(..., min_length=1, max_length=400)


class ExecutionPlan(BaseModel):
    """An ordered list of ExecutionSteps with estimated cost/time."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(default_factory=_new_plan_id)
    decision_id: str = Field(..., min_length=1)
    steps: list[ExecutionStep] = Field(..., min_length=1)
    estimated_cost: Money = Field(default_factory=lambda: Money.sar(0))
    estimated_minutes: int = Field(default=5, ge=0, le=10_080)
    sovereignty_level: str = Field(default="s0_autonomous")
    requires_approval: bool = False

    @field_validator("steps")
    @classmethod
    def _steps_unique(cls, value: list[ExecutionStep]) -> list[ExecutionStep]:
        seen: set[str] = set()
        for s in value:
            if s.step_id in seen:
                raise ValueError(f"duplicate step_id in plan: {s.step_id}")
            seen.add(s.step_id)
        return value


class StepResult(BaseModel):
    """Outcome of running a single ExecutionStep."""

    model_config = ConfigDict(extra="forbid")

    step_id: str = Field(..., min_length=1)
    status: StepStatus
    detail: str = Field(default="", max_length=2000)
    duration_ms: int = Field(default=0, ge=0)
    output: dict[str, Any] = Field(default_factory=dict)


class ExecutionResult(BaseModel):
    """Aggregate outcome of running an ExecutionPlan."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(..., min_length=1)
    step_results: list[StepResult] = Field(default_factory=list)
    status: ExecutionStatus
    started_at: datetime = Field(default_factory=utcnow)
    completed_at: datetime = Field(default_factory=utcnow)
    cost: Money = Field(default_factory=lambda: Money.sar(0))

    @model_validator(mode="after")
    def _completed_after_started(self) -> ExecutionResult:
        if self.completed_at < self.started_at:
            raise ValueError("completed_at must be >= started_at")
        return self

    @classmethod
    def from_steps(
        cls,
        plan_id: str,
        results: list[StepResult],
        started_at: datetime | None = None,
        completed_at: datetime | None = None,
        cost: Money | None = None,
    ) -> ExecutionResult:
        if not results:
            status = ExecutionStatus.FAILED
        elif all(r.status == StepStatus.OK for r in results):
            status = ExecutionStatus.COMPLETED
        elif any(r.status == StepStatus.OK for r in results):
            status = ExecutionStatus.PARTIAL
        else:
            status = ExecutionStatus.FAILED
        return cls(
            plan_id=plan_id,
            step_results=results,
            status=status,
            started_at=started_at or utcnow(),
            completed_at=completed_at or utcnow(),
            cost=cost or Money.sar(0),
        )


# ─────────────────────────────────────────────────────────────
# Planner
# ─────────────────────────────────────────────────────────────


# Maps OpportunityType → (agent_id, tool_id, action, expected_outcome, cost, mins, requires_approval)
_PLAN_TEMPLATES: dict[OpportunityType, list[dict[str, Any]]] = {
    OpportunityType.REVENUE: [
        {
            "agent_id": "ProposalFactoryAgent",
            "tool_id": "proposal_render",
            "action": "render_proposal",
            "expected_outcome": "Draft proposal PDF ready for review",
            "approval": False,
        },
        {
            "agent_id": "ProposalFactoryAgent",
            "tool_id": "email_send",
            "action": "send_email",
            "expected_outcome": "Proposal delivered to lead",
            "approval": True,
        },
    ],
    OpportunityType.PARTNER: [
        {
            "agent_id": "PartnerPitchAgent",
            "tool_id": "proposal_render",
            "action": "render_pitch",
            "expected_outcome": "Partner pitch deck drafted",
            "approval": True,
        }
    ],
    OpportunityType.PRODUCT: [
        {
            "agent_id": "OfferBuilderAgent",
            "tool_id": "landing_page_publish",
            "action": "publish_landing_test",
            "expected_outcome": "Lean landing page live for signal validation",
            "approval": True,
        }
    ],
    OpportunityType.KNOWLEDGE: [
        {
            "agent_id": "KnowledgeCuratorAgent",
            "tool_id": "crm_sync",
            "action": "update_playbook",
            "expected_outcome": "Playbook entry added & linked to entity",
            "approval": False,
        }
    ],
    OpportunityType.RISK_AVOIDANCE: [
        {
            "agent_id": "RiskOpsAgent",
            "tool_id": "crm_sync",
            "action": "log_risk_register",
            "expected_outcome": "Risk recorded & owner notified",
            "approval": False,
        }
    ],
}


# Rough cost estimates per step (SAR)
_STEP_COST_SAR: Decimal = Decimal("1.50")
_STEP_MINUTES: int = 3


class ExecutionPlanner:
    """Produce an ExecutionPlan from a Decision."""

    def plan(
        self,
        decision: Decision,
        opp_type: OpportunityType,
        sovereignty_level: str | None = None,
    ) -> ExecutionPlan:
        templates = _PLAN_TEMPLATES.get(opp_type, _PLAN_TEMPLATES[OpportunityType.KNOWLEDGE])
        steps: list[ExecutionStep] = []
        any_approval = False
        for tpl in templates:
            steps.append(
                ExecutionStep(
                    agent_id=tpl["agent_id"],
                    tool_id=tpl["tool_id"],
                    action=tpl["action"],
                    expected_outcome=tpl["expected_outcome"],
                    args={
                        "decision_id": decision.decision_id,
                        "chosen_option": decision.chosen_option,
                    },
                )
            )
            any_approval = any_approval or bool(tpl.get("approval"))

        cost = Money.sar(_STEP_COST_SAR * Decimal(len(steps)))
        return ExecutionPlan(
            decision_id=decision.decision_id,
            steps=steps,
            estimated_cost=cost,
            estimated_minutes=_STEP_MINUTES * len(steps),
            sovereignty_level=sovereignty_level or decision.sovereignty_level,
            requires_approval=any_approval,
        )


__all__ = [
    "ExecutionPlan",
    "ExecutionPlanner",
    "ExecutionResult",
    "ExecutionStatus",
    "ExecutionStep",
    "StepResult",
    "StepStatus",
]
