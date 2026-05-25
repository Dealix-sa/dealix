"""
Promotion-readiness evaluation.

Codifies section 102's promotion rules: an agent cannot move from
Draft-Only to Approval-Gated unless it has demonstrated measurable
trust over a minimum run volume.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.agent_lifecycle.registry import (
    AgentLifecycleStage,
    AgentRecord,
)

DRAFT_TO_APPROVAL_MIN_RUNS = 50
DRAFT_TO_APPROVAL_MIN_TRUST = 0.95
DRAFT_TO_APPROVAL_MAX_CORRECTION = 0.10
APPROVAL_TO_LIMITED_MIN_RUNS = 200
APPROVAL_TO_LIMITED_MIN_TRUST = 0.97
LIMITED_TO_MONITORED_MIN_RUNS = 500


@dataclass
class PromotionCheck:
    name: str
    passed: bool
    detail: str


@dataclass
class AgentEvaluation:
    target_stage: AgentLifecycleStage
    ready: bool
    checks: list[PromotionCheck]

    @property
    def failing(self) -> list[PromotionCheck]:
        return [c for c in self.checks if not c.passed]


def _eval_draft_to_approval(record: AgentRecord) -> list[PromotionCheck]:
    return [
        PromotionCheck(
            name="min_runs",
            passed=record.runs >= DRAFT_TO_APPROVAL_MIN_RUNS,
            detail=f"runs={record.runs} need>={DRAFT_TO_APPROVAL_MIN_RUNS}",
        ),
        PromotionCheck(
            name="no_critical_incidents",
            passed=record.critical_incidents == 0,
            detail=f"critical_incidents={record.critical_incidents}",
        ),
        PromotionCheck(
            name="trust_pass_rate",
            passed=record.trust_pass_rate >= DRAFT_TO_APPROVAL_MIN_TRUST,
            detail=(
                f"trust_pass_rate={record.trust_pass_rate:.3f} "
                f"need>={DRAFT_TO_APPROVAL_MIN_TRUST}"
            ),
        ),
        PromotionCheck(
            name="correction_rate",
            passed=record.correction_rate <= DRAFT_TO_APPROVAL_MAX_CORRECTION,
            detail=(
                f"correction_rate={record.correction_rate:.3f} "
                f"need<={DRAFT_TO_APPROVAL_MAX_CORRECTION}"
            ),
        ),
        PromotionCheck(
            name="outcomes_logged",
            passed=record.outcomes_logged >= max(1, record.runs // 2),
            detail=f"outcomes_logged={record.outcomes_logged}",
        ),
        PromotionCheck(
            name="owner_set",
            passed=bool(record.owner),
            detail=f"owner={record.owner!r}",
        ),
        PromotionCheck(
            name="tool_scope_declared",
            passed=len(record.tool_scope) > 0,
            detail=f"tool_scope={list(record.tool_scope)}",
        ),
    ]


def _eval_approval_to_limited(record: AgentRecord) -> list[PromotionCheck]:
    return [
        PromotionCheck(
            name="min_runs",
            passed=record.runs >= APPROVAL_TO_LIMITED_MIN_RUNS,
            detail=f"runs={record.runs} need>={APPROVAL_TO_LIMITED_MIN_RUNS}",
        ),
        PromotionCheck(
            name="trust_pass_rate",
            passed=record.trust_pass_rate >= APPROVAL_TO_LIMITED_MIN_TRUST,
            detail=(
                f"trust_pass_rate={record.trust_pass_rate:.3f} "
                f"need>={APPROVAL_TO_LIMITED_MIN_TRUST}"
            ),
        ),
        PromotionCheck(
            name="no_critical_incidents_30d_window",
            passed=record.critical_incidents == 0,
            detail=(
                "critical_incidents must be 0 across the agent's lifetime "
                "before unlocking limited autonomy"
            ),
        ),
    ]


def _eval_limited_to_monitored(record: AgentRecord) -> list[PromotionCheck]:
    return [
        PromotionCheck(
            name="min_runs",
            passed=record.runs >= LIMITED_TO_MONITORED_MIN_RUNS,
            detail=f"runs={record.runs} need>={LIMITED_TO_MONITORED_MIN_RUNS}",
        ),
        PromotionCheck(
            name="trust_pass_rate",
            passed=record.trust_pass_rate >= APPROVAL_TO_LIMITED_MIN_TRUST,
            detail=(
                f"trust_pass_rate={record.trust_pass_rate:.3f} "
                f"need>={APPROVAL_TO_LIMITED_MIN_TRUST}"
            ),
        ),
    ]


_EVALUATORS = {
    AgentLifecycleStage.APPROVAL_GATED: _eval_draft_to_approval,
    AgentLifecycleStage.LIMITED_AUTONOMY: _eval_approval_to_limited,
    AgentLifecycleStage.MONITORED: _eval_limited_to_monitored,
}


def evaluate_promotion_readiness(
    record: AgentRecord, target: AgentLifecycleStage
) -> AgentEvaluation:
    evaluator = _EVALUATORS.get(target)
    if evaluator is None:
        return AgentEvaluation(
            target_stage=target,
            ready=True,
            checks=[
                PromotionCheck(
                    name="no_runtime_gate",
                    passed=True,
                    detail=(
                        f"target stage '{target.value}' has no runtime promotion "
                        "checks; lifecycle ordering is enforced separately"
                    ),
                )
            ],
        )
    checks = evaluator(record)
    return AgentEvaluation(
        target_stage=target,
        ready=all(c.passed for c in checks),
        checks=checks,
    )
