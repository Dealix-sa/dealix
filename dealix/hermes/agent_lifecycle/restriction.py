"""
Restriction — downgrade an agent's stage in response to incidents.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from dealix.hermes.agent_lifecycle.registry import (
    AgentLifecycleStage,
    AgentRegistry,
)


class RestrictionReason(StrEnum):
    CRITICAL_INCIDENT = "critical_incident"
    POLICY_VIOLATION = "policy_violation"
    LOW_TRUST = "low_trust"
    SUSPECTED_INJECTION = "suspected_injection"
    OWNER_REQUEST = "owner_request"
    SECURITY_REVIEW = "security_review"


@dataclass
class RestrictionAction:
    agent_id: str
    from_stage: AgentLifecycleStage
    to_stage: AgentLifecycleStage
    reason: RestrictionReason
    note: str


def restrict_agent(
    registry: AgentRegistry,
    agent_id: str,
    reason: RestrictionReason,
    *,
    requested_by: str,
    target_stage: AgentLifecycleStage = AgentLifecycleStage.RESTRICTED,
    note: str = "",
) -> RestrictionAction:
    record = registry.get(agent_id)
    if target_stage not in (
        AgentLifecycleStage.RESTRICTED,
        AgentLifecycleStage.DRAFT_ONLY,
        AgentLifecycleStage.APPROVAL_GATED,
    ):
        raise ValueError(
            f"restriction must target RESTRICTED/DRAFT_ONLY/APPROVAL_GATED, "
            f"not {target_stage.value}"
        )
    prior = record.stage
    full_note = (
        f"reason={reason.value}; requested_by={requested_by}"
        + (f"; {note}" if note else "")
    )
    registry.transition(agent_id, target_stage, full_note)
    return RestrictionAction(
        agent_id=agent_id,
        from_stage=prior,
        to_stage=target_stage,
        reason=reason,
        note=full_note,
    )
