"""Quality gates for the Revenue Marketing Engine.

These gates run before a campaign is activated or a content draft is approved
and surface missing fields. An empty return list means the artifact passes.
"""

from __future__ import annotations

from typing import Any

from dealix.revenue_marketing.schemas import MarketingCampaign

# Engagement-only metrics that must always be paired with a downstream
# conversion before we let them onto the dashboard. Avoids vanity readouts.
_VANITY_METRICS: frozenset[str] = frozenset(
    {
        "impressions",
        "reach",
        "views",
        "video_views",
        "likes",
        "reactions",
        "followers",
        "follower_growth",
        "engagement_rate",
        "ctr",
        "click_through_rate",
    },
)


def validate_campaign(campaign: MarketingCampaign) -> list[str]:
    """Return a list of missing-field reasons. Empty list means pass."""
    missing: list[str] = []
    if not (campaign.target_segment or "").strip():
        missing.append("target_segment_missing")
    if not (campaign.offer_id or "").strip():
        missing.append("offer_id_missing")
    if not (campaign.channel or "").strip():
        missing.append("channel_missing")
    if not (campaign.message_angle or "").strip():
        missing.append("message_angle_missing")
    if not (campaign.success_metric or "").strip():
        missing.append("success_metric_missing")
    if not (campaign.scale_kill_rule or "").strip():
        missing.append("scale_kill_rule_missing")
    return missing


def validate_content(content: dict[str, Any]) -> list[str]:
    """Validate a content payload before approval."""
    required = ("target_segment", "pain", "offer_id", "cta", "success_metric", "tracking")
    missing: list[str] = []
    for field in required:
        value = content.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(f"{field}_missing")
    return missing


def enforce_no_vanity(metric_name: str, downstream_conversion_count: int) -> bool:
    """Return False when an engagement metric has zero downstream conversion.

    Non-engagement metrics always pass; engagement metrics require at least one
    downstream conversion before they may show up in the dashboard summary.
    """
    name = (metric_name or "").strip().lower()
    if name not in _VANITY_METRICS:
        return True
    return int(downstream_conversion_count) > 0
