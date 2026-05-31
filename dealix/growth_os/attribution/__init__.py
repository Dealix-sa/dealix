"""Attribution — types, records, and analysis primitives."""

from __future__ import annotations

from dealix.growth_os.attribution.analysis import (
    AttributionBreakdown,
    group_revenue_by,
    group_revenue_by_agent,
    group_revenue_by_asset,
    group_revenue_by_campaign,
    group_revenue_by_channel,
    group_revenue_by_offer,
    group_revenue_by_partner,
)
from dealix.growth_os.attribution.record import AttributionRecord
from dealix.growth_os.attribution.types import (
    ATTRIBUTION_TYPES,
    AttributionType,
)

__all__ = [
    "ATTRIBUTION_TYPES",
    "AttributionBreakdown",
    "AttributionRecord",
    "AttributionType",
    "group_revenue_by",
    "group_revenue_by_agent",
    "group_revenue_by_asset",
    "group_revenue_by_campaign",
    "group_revenue_by_channel",
    "group_revenue_by_offer",
    "group_revenue_by_partner",
]
