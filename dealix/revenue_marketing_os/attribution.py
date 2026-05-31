"""
Revenue attribution computation.

The Money Loop asks: which channel/campaign/asset/agent/partner
actually produced this riyal? This module answers in three steps:

1. Resolve all *verified* revenue records.
2. Resolve all touches for the same ``lead_id``.
3. Apply a chosen attribution model (first / last / multi-touch) and
   return per-channel and per-campaign sums.

NOTE: This module does not write to the store. It only computes;
the API layer chooses whether to persist the result.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from dealix.revenue_marketing_os.schemas import (
    AttributionRecord,
    RevenueRecord,
    TouchRecord,
)
from dealix.revenue_marketing_os.scoring import revenue_is_real


def _touches_for_lead(
    touches: Iterable[TouchRecord], lead_id: str
) -> list[TouchRecord]:
    rows = [t for t in touches if t.lead_id == lead_id]
    rows.sort(key=lambda x: x.occurred_at)
    return rows


def compute_attribution(
    *,
    revenue: RevenueRecord,
    touches: Iterable[TouchRecord],
    model: str = "multi_touch",
) -> list[AttributionRecord]:
    """
    Compute attribution rows for one verified revenue event.

    Models supported:
      - ``first_touch``  — full credit to the earliest touch.
      - ``last_touch``   — full credit to the most recent touch.
      - ``multi_touch``  — equal-weight credit across every touch.
    """
    if not revenue_is_real(revenue.model_dump()):
        return []

    lead_touches = _touches_for_lead(touches, revenue.lead_id) if revenue.lead_id else []
    if not lead_touches:
        # No touches recorded — credit the revenue's own campaign+channel.
        return [
            AttributionRecord(
                id=f"att_self_{revenue.id}",
                revenue_id=revenue.id,
                deal_id=revenue.deal_id,
                campaign_id=revenue.campaign_id,
                lead_id=revenue.lead_id,
                offer_id=revenue.source_offer_id,
                channel=revenue.channel,
                attribution_type="channel_influenced",
                weight=1.0,
                amount_sar=revenue.amount_sar,
            )
        ]

    if model == "first_touch":
        chosen = [lead_touches[0]]
        attribution_type = "first_touch"
    elif model == "last_touch":
        chosen = [lead_touches[-1]]
        attribution_type = "last_touch"
    else:
        chosen = list(lead_touches)
        attribution_type = "multi_touch"

    weight = 1.0 / len(chosen)
    out: list[AttributionRecord] = []
    for idx, t in enumerate(chosen):
        out.append(
            AttributionRecord(
                id=f"att_{model}_{revenue.id}_{idx}",
                revenue_id=revenue.id,
                deal_id=revenue.deal_id,
                campaign_id=t.campaign_id or revenue.campaign_id,
                lead_id=revenue.lead_id,
                offer_id=revenue.source_offer_id,
                channel=t.channel,
                attribution_type=attribution_type,  # type: ignore[arg-type]
                weight=weight,
                amount_sar=round(revenue.amount_sar * weight, 2),
            )
        )
    return out


def summarize_attribution(
    rows: Iterable[AttributionRecord],
) -> dict[str, dict[str, float]]:
    """Aggregate attribution amount by channel, campaign, and offer."""
    by_channel: dict[str, float] = defaultdict(float)
    by_campaign: dict[str, float] = defaultdict(float)
    by_offer: dict[str, float] = defaultdict(float)
    by_type: dict[str, float] = defaultdict(float)
    for r in rows:
        by_channel[r.channel] += r.amount_sar
        if r.campaign_id:
            by_campaign[r.campaign_id] += r.amount_sar
        if r.offer_id:
            by_offer[r.offer_id] += r.amount_sar
        by_type[r.attribution_type] += r.amount_sar
    return {
        "by_channel": {k: round(v, 2) for k, v in by_channel.items()},
        "by_campaign": {k: round(v, 2) for k, v in by_campaign.items()},
        "by_offer": {k: round(v, 2) for k, v in by_offer.items()},
        "by_attribution_type": {k: round(v, 2) for k, v in by_type.items()},
    }
