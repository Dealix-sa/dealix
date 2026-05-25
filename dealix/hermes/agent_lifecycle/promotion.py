"""
Promotion gate.

`promote()` is the only legal way to advance an agent's stage. It
enforces both lifecycle ordering AND runtime evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.agent_lifecycle.evaluation import (
    AgentEvaluation,
    evaluate_promotion_readiness,
)
from dealix.hermes.agent_lifecycle.registry import (
    AgentLifecycleStage,
    AgentRegistry,
    is_forward_promotion,
)


class PromotionError(RuntimeError):
    """Raised when a requested promotion violates the lifecycle."""


@dataclass
class PromotionResult:
    agent_id: str
    from_stage: AgentLifecycleStage
    to_stage: AgentLifecycleStage
    evaluation: AgentEvaluation
    note: str


def promote(
    registry: AgentRegistry,
    agent_id: str,
    target: AgentLifecycleStage,
    *,
    approved_by: str,
    note: str = "",
) -> PromotionResult:
    record = registry.get(agent_id)
    if not approved_by:
        raise PromotionError("promotion requires an explicit approved_by identity")
    if not is_forward_promotion(record.stage, target):
        raise PromotionError(
            f"illegal stage transition: {record.stage.value} → {target.value}"
        )
    evaluation = evaluate_promotion_readiness(record, target)
    if not evaluation.ready:
        failing = ", ".join(c.name for c in evaluation.failing)
        raise PromotionError(
            f"promotion checks failed for {agent_id} → {target.value}: {failing}"
        )
    full_note = f"approved_by={approved_by}" + (f"; {note}" if note else "")
    registry.transition(agent_id, target, full_note)
    return PromotionResult(
        agent_id=agent_id,
        from_stage=record.history[-2][1] if len(record.history) >= 2 else record.stage,
        to_stage=target,
        evaluation=evaluation,
        note=full_note,
    )
