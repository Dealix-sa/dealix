"""Attribution model types."""

from __future__ import annotations

from typing import Final, Literal

AttributionType = Literal[
    "first_touch",
    "last_touch",
    "multi_touch",
    "asset_influenced",
    "agent_influenced",
    "partner_influenced",
    "campaign_influenced",
]

ATTRIBUTION_TYPES: Final[tuple[AttributionType, ...]] = (
    "first_touch",
    "last_touch",
    "multi_touch",
    "asset_influenced",
    "agent_influenced",
    "partner_influenced",
    "campaign_influenced",
)


__all__ = ["ATTRIBUTION_TYPES", "AttributionType"]
