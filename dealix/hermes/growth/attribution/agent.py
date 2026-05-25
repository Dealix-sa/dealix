"""Attribute verified revenue to agents that participated in the workflow."""

from __future__ import annotations

from . import _base

DIMENSION = "agent"


def attribute(agent_id: str, revenue_sar: float, evidence_pack_id: str) -> _base.AttributionRecord:
    """Attribute verified revenue to an agent."""
    return _base.attribute(DIMENSION, agent_id, revenue_sar, evidence_pack_id)


def total(agent_id: str) -> float:
    """Return total verified revenue attributed to an agent."""
    return _base.total_for(DIMENSION, agent_id)
