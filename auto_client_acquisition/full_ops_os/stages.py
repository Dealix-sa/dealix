"""Full Ops Sales System — the 12-stage golden chain.

Each stage carries the canonical ``action_type`` it produces so the
orchestrator can classify it (A/R/S) and decide auto-execution vs.
approval routing. See ``docs/full_ops_sales_os/ARCHITECTURE.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class Stage(IntEnum):
    """The 12 ordered stages of the sell-deliver-expand loop."""

    SIGNAL_INTAKE = 1
    ENRICHMENT = 2
    SCORING = 3
    PAIN_EXTRACTION = 4
    QUALIFICATION = 5
    PRIORITIZATION = 6
    DRAFT_GENERATION = 7
    APPROVAL_GATE = 8
    DELIVERY = 9
    PROOF = 10
    EXPANSION = 11
    LEARNING = 12


@dataclass(frozen=True, slots=True)
class StageSpec:
    """Static description of one stage."""

    stage: Stage
    name: str
    action_type: str
    module: str

    @property
    def event_type(self) -> str:
        return f"dealix.full_ops.stage.{self.stage.name.lower()}"

    @property
    def event_source(self) -> str:
        return f"dealix/full_ops/{self.stage.name.lower()}"


STAGE_SPECS: dict[Stage, StageSpec] = {
    Stage.SIGNAL_INTAKE: StageSpec(
        Stage.SIGNAL_INTAKE, "Signal Intake", "lead_intake", "data_os"
    ),
    Stage.ENRICHMENT: StageSpec(
        Stage.ENRICHMENT, "Enrichment", "enrichment_query", "revenue_os"
    ),
    Stage.SCORING: StageSpec(
        Stage.SCORING, "Scoring", "icp_match", "sales_os"
    ),
    Stage.PAIN_EXTRACTION: StageSpec(
        Stage.PAIN_EXTRACTION, "Pain Extraction", "pain_extract", "full_ops_os"
    ),
    Stage.QUALIFICATION: StageSpec(
        Stage.QUALIFICATION, "Qualification", "qualification_questions", "sales_os"
    ),
    Stage.PRIORITIZATION: StageSpec(
        Stage.PRIORITIZATION, "Prioritization", "pipeline_prioritize", "revenue_pipeline"
    ),
    Stage.DRAFT_GENERATION: StageSpec(
        Stage.DRAFT_GENERATION, "Draft Generation", "proposal_generate_draft", "sales_os"
    ),
    Stage.APPROVAL_GATE: StageSpec(
        Stage.APPROVAL_GATE, "Approval Gate", "outreach_send", "approval_center"
    ),
    Stage.DELIVERY: StageSpec(
        Stage.DELIVERY, "Delivery", "delivery_step", "proof_architecture_os"
    ),
    Stage.PROOF: StageSpec(
        Stage.PROOF, "Proof", "proof_pack_assemble", "proof_architecture_os"
    ),
    Stage.EXPANSION: StageSpec(
        Stage.EXPANSION, "Expansion", "expansion_assess", "adoption_os"
    ),
    Stage.LEARNING: StageSpec(
        Stage.LEARNING, "Learning", "learning_capture", "friction_log"
    ),
}

STAGES: tuple[StageSpec, ...] = tuple(STAGE_SPECS[s] for s in Stage)


def stage_spec(stage: Stage) -> StageSpec:
    """Return the spec for a stage."""
    return STAGE_SPECS[stage]


def first_stage() -> Stage:
    """The entry stage of the chain."""
    return Stage.SIGNAL_INTAKE


def next_stage(stage: Stage) -> Stage | None:
    """Return the stage after ``stage``, or None if it is the last."""
    if stage == Stage.LEARNING:
        return None
    return Stage(int(stage) + 1)


__all__ = [
    "Stage",
    "StageSpec",
    "STAGE_SPECS",
    "STAGES",
    "stage_spec",
    "first_stage",
    "next_stage",
]
