"""Stage → agent dispatch for the Full Ops Sales System.

Maps each of the 12 stages to its primary worker agent and domain
director, and verifies the integrity of the registered agent pyramid.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.agent_os import AgentStatus, AutonomyLevel, get_agent
from auto_client_acquisition.full_ops_os.agents import (
    CONDUCTOR_ID,
    EXTERNAL_FACING_MAX_LEVEL,
    FULL_OPS_AGENT_SPECS,
)
from auto_client_acquisition.full_ops_os.stages import Stage

# Primary worker agent for each stage.
STAGE_WORKER: dict[Stage, str] = {
    Stage.SIGNAL_INTAKE: "lead-intake-agent",
    Stage.ENRICHMENT: "enrichment-agent",
    Stage.SCORING: "scoring-agent",
    Stage.PAIN_EXTRACTION: "pain-extraction-agent",
    Stage.QUALIFICATION: "qualification-agent",
    Stage.PRIORITIZATION: "prioritization-agent",
    Stage.DRAFT_GENERATION: "draft-agent",
    Stage.APPROVAL_GATE: "followup-agent",
    Stage.DELIVERY: "proof-agent",
    Stage.PROOF: "proof-agent",
    Stage.EXPANSION: "expansion-agent",
    Stage.LEARNING: "friction-agent",
}

# Domain director responsible for each stage.
STAGE_DIRECTOR: dict[Stage, str] = {
    **{s: "sales-director" for s in (
        Stage.SIGNAL_INTAKE, Stage.ENRICHMENT, Stage.SCORING,
        Stage.PAIN_EXTRACTION, Stage.QUALIFICATION, Stage.PRIORITIZATION,
        Stage.DRAFT_GENERATION, Stage.APPROVAL_GATE,
    )},
    **{s: "delivery-director" for s in (Stage.DELIVERY, Stage.PROOF)},
    **{s: "growth-director" for s in (Stage.EXPANSION, Stage.LEARNING)},
}


def agent_for_stage(stage: Stage) -> str:
    """Return the worker agent id that performs a stage."""
    return STAGE_WORKER[stage]


def director_for_stage(stage: Stage) -> str:
    """Return the domain director agent id that owns a stage."""
    return STAGE_DIRECTOR[stage]


@dataclass(frozen=True, slots=True)
class IntegrityIssue:
    agent_id: str
    problem: str


def verify_agent_pyramid_integrity() -> list[IntegrityIssue]:
    """Check the registered pyramid against the doctrine.

    Returns a list of issues — empty means the pyramid is sound.
    """
    issues: list[IntegrityIssue] = []

    conductor = get_agent(CONDUCTOR_ID)
    if conductor is None:
        issues.append(IntegrityIssue(CONDUCTOR_ID, "conductor not registered"))
    elif conductor.autonomy_level != int(AutonomyLevel.L4_AUTO_WITH_AUDIT):
        issues.append(IntegrityIssue(CONDUCTOR_ID, "conductor must be L4"))
    elif not conductor.kill_switch_owner.strip():
        issues.append(IntegrityIssue(CONDUCTOR_ID, "L4 conductor needs a kill_switch_owner"))

    for spec in FULL_OPS_AGENT_SPECS:
        card = get_agent(spec.agent_id)
        if card is None:
            issues.append(IntegrityIssue(spec.agent_id, "not registered"))
            continue
        if card.status == AgentStatus.KILLED.value:
            issues.append(IntegrityIssue(spec.agent_id, "agent is killed"))
        # Tier 2 workers may never exceed the external-facing draft cap.
        if spec.tier == 2 and card.autonomy_level > int(EXTERNAL_FACING_MAX_LEVEL):
            issues.append(
                IntegrityIssue(spec.agent_id, "worker exceeds L2_DRAFT cap")
            )

    return issues


__all__ = [
    "STAGE_WORKER",
    "STAGE_DIRECTOR",
    "IntegrityIssue",
    "agent_for_stage",
    "director_for_stage",
    "verify_agent_pyramid_integrity",
]
