"""Identity card for the Executive Orchestrator.

Capped at ``L3_RECOMMEND`` with an empty ``allowed_tools`` tuple — the
orchestrator recommends and queues, it holds no tool that could send or
charge. The founder owns its kill switch.
"""

from __future__ import annotations

from auto_client_acquisition.agent_os import (
    AgentCard,
    AutonomyLevel,
    get_agent,
    new_card,
    register_agent,
)

EXECUTIVE_AGENT_ID = "executive_orchestrator"


def build_executive_agent_card() -> AgentCard:
    """Build the orchestrator's identity card (no side effects)."""
    return new_card(
        agent_id=EXECUTIVE_AGENT_ID,
        name="Dealix Executive Orchestrator",
        owner="founder",
        purpose=(
            "Convene the 7 role briefs, synthesize one executive brief, and "
            "queue every external action for founder approval. Queues and "
            "prepares — never sends, never charges."
        ),
        autonomy_level=AutonomyLevel.L3_RECOMMEND,
        allowed_tools=[],
        kill_switch_owner="founder",
        notes="allowed_tools intentionally empty — queues-never-sends.",
    )


def ensure_registered() -> AgentCard:
    """Register the orchestrator card once; idempotent under concurrency."""
    existing = get_agent(EXECUTIVE_AGENT_ID)
    if existing is not None:
        return existing
    card = build_executive_agent_card()
    try:
        return register_agent(card)
    except ValueError:
        # Lost a registration race — return whatever landed.
        return get_agent(EXECUTIVE_AGENT_ID) or card


__all__ = [
    "EXECUTIVE_AGENT_ID",
    "build_executive_agent_card",
    "ensure_registered",
]
