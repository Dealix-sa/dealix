"""
Agent retirement — terminal state.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.agent_lifecycle.registry import (
    AgentLifecycleStage,
    AgentRegistry,
)


@dataclass
class RetirementRecord:
    agent_id: str
    from_stage: AgentLifecycleStage
    note: str


def retire_agent(
    registry: AgentRegistry,
    agent_id: str,
    *,
    approved_by: str,
    reason: str,
) -> RetirementRecord:
    if not approved_by:
        raise ValueError("retirement requires explicit approved_by identity")
    if not reason:
        raise ValueError("retirement requires a non-empty reason")
    record = registry.get(agent_id)
    prior = record.stage
    note = f"approved_by={approved_by}; reason={reason}"
    registry.transition(agent_id, AgentLifecycleStage.RETIRED, note)
    return RetirementRecord(agent_id=agent_id, from_stage=prior, note=note)
