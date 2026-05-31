"""Attribute verified revenue to ecosystem partners."""

from __future__ import annotations

from . import _base

DIMENSION = "partner"


def attribute(partner_id: str, revenue_sar: float, evidence_pack_id: str) -> _base.AttributionRecord:
    """Attribute verified revenue to a partner."""
    return _base.attribute(DIMENSION, partner_id, revenue_sar, evidence_pack_id)


def total(partner_id: str) -> float:
    """Return total verified revenue attributed to a partner."""
    return _base.total_for(DIMENSION, partner_id)
