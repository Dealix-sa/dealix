"""Attribute verified revenue to acquisition channels."""

from __future__ import annotations

from . import _base

DIMENSION = "channel"


def attribute(channel: str, revenue_sar: float, evidence_pack_id: str) -> _base.AttributionRecord:
    """Attribute verified revenue to a channel."""
    return _base.attribute(DIMENSION, channel, revenue_sar, evidence_pack_id)


def total(channel: str) -> float:
    """Return total verified revenue attributed to a channel."""
    return _base.total_for(DIMENSION, channel)
