"""Task router — convert an AI Stack input into an ordered agent task list.

The router is **pure and deterministic**: same input → same task list. It does
not call agents, does not check governance, and does not touch the network.
That keeps it trivial to unit test and to reason about under all 5 offer tiers.

Task lists are tied to the offer tier (free_diagnostic / sprint_499 /
data_pack_1500 / managed_ops / custom_ai). Each task names the canonical
agent ID and the handler signature the agent mesh will look up.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class AgentTask:
    """One step in an ordered agent task list."""

    step: int
    agent_id: str
    purpose: str
    payload: Mapping[str, Any]
    requires_governance: bool = True
    optional: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["payload"] = dict(self.payload)
        return data


# Canonical agent ids for the AI Stack — these names match the registered
# AgentCard ids the agent mesh expects to find in the registry.
AGENT_ICP = "icp_matcher"
AGENT_PAIN = "pain_extractor"
AGENT_QUALIFICATION = "qualification"
AGENT_PROPOSAL = "proposal"
AGENT_OUTREACH_DRAFT = "outreach_draft"
AGENT_SECTOR_INTEL = "sector_intel"
AGENT_RETAINER_RECOMMEND = "retainer_recommend"


# Offer tier → canonical task pipelines. Order matters; the agent mesh
# executes tasks sequentially and may short-circuit on governance blocks.
_OFFER_PIPELINES: dict[str, tuple[tuple[str, str, bool, bool], ...]] = {
    # (agent_id, purpose, requires_governance, optional)
    "free_diagnostic": (
        (AGENT_ICP, "classify_fit_band", True, False),
        (AGENT_PAIN, "extract_pain_points", True, False),
    ),
    "sprint_499": (
        (AGENT_ICP, "classify_fit_band", True, False),
        (AGENT_PAIN, "extract_pain_points", True, False),
        (AGENT_QUALIFICATION, "score_qualification", True, False),
        (AGENT_PROPOSAL, "draft_sprint_proposal", True, False),
    ),
    "data_pack_1500": (
        (AGENT_ICP, "classify_fit_band", True, False),
        (AGENT_PAIN, "extract_pain_points", True, False),
        (AGENT_SECTOR_INTEL, "summarize_sector_signal", True, True),
        (AGENT_QUALIFICATION, "score_qualification", True, False),
        (AGENT_PROPOSAL, "draft_data_pack_proposal", True, False),
    ),
    "managed_ops": (
        (AGENT_ICP, "classify_fit_band", True, False),
        (AGENT_PAIN, "extract_pain_points", True, False),
        (AGENT_SECTOR_INTEL, "summarize_sector_signal", True, True),
        (AGENT_QUALIFICATION, "score_qualification", True, False),
        (AGENT_PROPOSAL, "draft_managed_ops_proposal", True, False),
        (AGENT_RETAINER_RECOMMEND, "recommend_retainer_tier", True, False),
    ),
    "custom_ai": (
        (AGENT_ICP, "classify_fit_band", True, False),
        (AGENT_PAIN, "extract_pain_points", True, False),
        (AGENT_SECTOR_INTEL, "summarize_sector_signal", True, True),
        (AGENT_QUALIFICATION, "score_qualification", True, False),
        (AGENT_PROPOSAL, "draft_custom_ai_proposal", True, False),
        (AGENT_RETAINER_RECOMMEND, "recommend_retainer_tier", True, False),
    ),
}


@dataclass(frozen=True, slots=True)
class TaskPlan:
    """An ordered list of agent tasks plus its source offer tier."""

    offer_tier: str
    tasks: tuple[AgentTask, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "offer_tier": self.offer_tier,
            "tasks": [t.to_dict() for t in self.tasks],
        }


def plan_for_offer(
    *,
    offer_tier: str,
    base_payload: Mapping[str, Any],
) -> TaskPlan:
    """Build the canonical task plan for an offer tier.

    The same ``base_payload`` is attached to every task — agents pick the
    fields they need. This keeps the orchestrator simple: one payload per
    run, never reshaped between agents.
    """
    pipeline = _OFFER_PIPELINES.get(offer_tier)
    if pipeline is None:
        raise ValueError(
            f"unknown offer_tier: {offer_tier!r} (allowed: {sorted(_OFFER_PIPELINES)})"
        )
    tasks: list[AgentTask] = []
    for idx, (agent_id, purpose, gov, optional) in enumerate(pipeline, start=1):
        tasks.append(
            AgentTask(
                step=idx,
                agent_id=agent_id,
                purpose=purpose,
                payload=dict(base_payload),
                requires_governance=gov,
                optional=optional,
            )
        )
    return TaskPlan(offer_tier=offer_tier, tasks=tuple(tasks))


def supported_offer_tiers() -> tuple[str, ...]:
    """Return the offer tiers the task router knows how to plan for."""
    return tuple(sorted(_OFFER_PIPELINES))


def agents_required_for_tier(offer_tier: str) -> tuple[str, ...]:
    pipeline = _OFFER_PIPELINES.get(offer_tier)
    if pipeline is None:
        raise ValueError(f"unknown offer_tier: {offer_tier!r}")
    return tuple(step[0] for step in pipeline)


__all__ = [
    "AGENT_ICP",
    "AGENT_OUTREACH_DRAFT",
    "AGENT_PAIN",
    "AGENT_PROPOSAL",
    "AGENT_QUALIFICATION",
    "AGENT_RETAINER_RECOMMEND",
    "AGENT_SECTOR_INTEL",
    "AgentTask",
    "TaskPlan",
    "agents_required_for_tier",
    "plan_for_offer",
    "supported_offer_tiers",
]
