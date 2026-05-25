"""
CampaignQuality — rolls up message and channel quality into a single
campaign-level verdict.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.growth.channel_quality import ChannelQualityScore
from dealix.hermes.growth.message_quality import MessageQualityScore


@dataclass
class CampaignQualityScore:
    campaign_id: str
    score: float
    verified_revenue_sar: float
    grade: str
    recommendation: str


def score_campaign(
    campaign_id: str,
    *,
    channels: list[ChannelQualityScore],
    messages: list[MessageQualityScore],
    verified_revenue_sar: float,
) -> CampaignQualityScore:
    if not channels and not messages:
        return CampaignQualityScore(campaign_id, 0.0, verified_revenue_sar, "F", "No data.")
    ch_score = sum(c.score for c in channels) / max(len(channels), 1)
    msg_score = sum(m.score for m in messages) / max(len(messages), 1)
    score = round(0.6 * ch_score + 0.4 * msg_score, 4)
    if score >= 0.3 and verified_revenue_sar > 0:
        grade, rec = "A", "Scale and lock in attribution."
    elif score >= 0.15:
        grade, rec = "B", "Optimize and reallocate to the strongest channel."
    elif score >= 0.05:
        grade, rec = "C", "Investigate; consider repositioning the offer."
    else:
        grade, rec = "D", "Kill the campaign and free the spend."
    return CampaignQualityScore(campaign_id, score, verified_revenue_sar, grade, rec)
