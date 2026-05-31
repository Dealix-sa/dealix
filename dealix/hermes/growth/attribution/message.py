"""Attribute verified revenue to message variants."""

from __future__ import annotations

from . import _base

DIMENSION = "message"


def attribute(variant_id: str, revenue_sar: float, evidence_pack_id: str) -> _base.AttributionRecord:
    """Attribute verified revenue to a message variant."""
    return _base.attribute(DIMENSION, variant_id, revenue_sar, evidence_pack_id)


def total(variant_id: str) -> float:
    """Return total verified revenue attributed to a message variant."""
    return _base.total_for(DIMENSION, variant_id)
