"""Attribute verified revenue to reusable content/proof assets."""

from __future__ import annotations

from . import _base

DIMENSION = "asset"


def attribute(asset_id: str, revenue_sar: float, evidence_pack_id: str) -> _base.AttributionRecord:
    """Attribute verified revenue to a reusable asset."""
    return _base.attribute(DIMENSION, asset_id, revenue_sar, evidence_pack_id)


def total(asset_id: str) -> float:
    """Return total verified revenue attributed to an asset."""
    return _base.total_for(DIMENSION, asset_id)
