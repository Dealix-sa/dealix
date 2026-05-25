"""Attribute verified revenue to campaigns."""

from __future__ import annotations

from . import _base

DIMENSION = "campaign"


def attribute(campaign_id: str, revenue_sar: float, evidence_pack_id: str) -> _base.AttributionRecord:
    """Attribute verified revenue to a campaign."""
    return _base.attribute(DIMENSION, campaign_id, revenue_sar, evidence_pack_id)


def total(campaign_id: str) -> float:
    """Return total verified revenue attributed to a campaign."""
    return _base.total_for(DIMENSION, campaign_id)
