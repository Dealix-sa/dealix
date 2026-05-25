"""Attribute verified revenue to AI engine visibility (GEO)."""

from __future__ import annotations

from . import _base

DIMENSION = "geo"


def attribute(engine: str, revenue_sar: float, evidence_pack_id: str) -> _base.AttributionRecord:
    """Attribute verified revenue to an AI engine surface."""
    return _base.attribute(DIMENSION, engine, revenue_sar, evidence_pack_id)


def total(engine: str) -> float:
    """Return total verified revenue attributed to an AI engine surface."""
    return _base.total_for(DIMENSION, engine)
