"""Attribution engine — convert touches + deal payment into revenue records.

The hard rule from §8: revenue is only attributed after payment confirmation
(or a signed agreement). Anything earlier is pipeline, not money.

Supports five attribution types:
- first_touch:       100% credit to the earliest touch's channel/campaign
- last_touch:        100% credit to the latest touch's channel/campaign
- multi_touch:       linear share across all touches
- asset_influenced:  union of asset_ids found in the touch chain
- agent_influenced:  union of agent_ids found in the touch chain
"""

from __future__ import annotations

from typing import Any

from dealix.revenue_marketing.schemas import (
    AttributionType,
    MarketingTouchRecord,
    RevenueAttributionRecord,
)
from dealix.revenue_marketing.store import get_revenue_marketing_store, uid


def _channel_weights(touches: list[MarketingTouchRecord], attribution_type: AttributionType) -> dict[str, float]:
    if not touches:
        return {}
    if attribution_type == "first_touch":
        first = touches[0]
        return {first.channel or "unknown": 1.0}
    if attribution_type == "last_touch":
        last = touches[-1]
        return {last.channel or "unknown": 1.0}
    if attribution_type == "multi_touch":
        weight = 1.0 / len(touches)
        agg: dict[str, float] = {}
        for t in touches:
            ch = t.channel or "unknown"
            agg[ch] = round(agg.get(ch, 0.0) + weight, 4)
        return agg
    # asset/agent attribution still split channel revenue evenly
    return {t.channel or "unknown": round(1.0 / len(touches), 4) for t in touches}


def attribute_revenue(
    *,
    deal_id: str,
    revenue_sar: float,
    lead_id: str | None = None,
    attribution_type: AttributionType = "multi_touch",
    payment_confirmed: bool = True,
    money_quality: float = 0.6,
    primary_source: str = "",
    secondary_source: str = "",
) -> RevenueAttributionRecord:
    """Compute attribution from the lead's touch history and append a record.

    Refuses to record unless `payment_confirmed=True` — keeps vanity pipeline
    out of the revenue ledger (§8 anti-vanity).
    """
    if not payment_confirmed:
        raise ValueError("payment_confirmed=False: revenue cannot be attributed")
    if revenue_sar < 0:
        raise ValueError("revenue_sar must be >= 0")

    store = get_revenue_marketing_store()
    touches = store.list_touches(lead_id=lead_id) if lead_id else []

    asset_ids: list[str] = []
    agent_ids: list[str] = []
    influenced_by: list[str] = []
    campaign_id: str | None = None
    offer_id: str | None = None
    channel: str | None = None

    for t in touches:
        if t.asset_id and t.asset_id not in asset_ids:
            asset_ids.append(t.asset_id)
        if t.agent_id and t.agent_id not in agent_ids:
            agent_ids.append(t.agent_id)
        if t.content_id and t.content_id not in influenced_by:
            influenced_by.append(t.content_id)
        if t.message_variant and t.message_variant not in influenced_by:
            influenced_by.append(f"variant:{t.message_variant}")

    if touches:
        chosen = touches[0] if attribution_type == "first_touch" else touches[-1]
        campaign_id = chosen.campaign_id
        channel = chosen.channel
        if campaign_id:
            for c in store.list_campaigns():
                if c.id == campaign_id:
                    offer_id = c.offer_id
                    break

    if not primary_source:
        primary_source = channel or "direct"

    record = RevenueAttributionRecord(
        id=uid("attr"),
        revenue_sar=revenue_sar,
        deal_id=deal_id,
        primary_source=primary_source,
        secondary_source=secondary_source,
        campaign_id=campaign_id,
        offer_id=offer_id,
        channel=channel,
        asset_ids=asset_ids,
        agent_ids=agent_ids,
        influenced_by=influenced_by,
        attribution_type=attribution_type,
        payment_confirmed=True,
        money_quality=money_quality,
    )
    store.append_attribution(record)
    return record


def influenced_assets(*, lead_id: str) -> dict[str, list[str]]:
    """Return assets/agents/content that touched a single lead's journey."""
    touches = get_revenue_marketing_store().list_touches(lead_id=lead_id)
    return {
        "asset_ids": sorted({t.asset_id for t in touches if t.asset_id}),
        "agent_ids": sorted({t.agent_id for t in touches if t.agent_id}),
        "content_ids": sorted({t.content_id for t in touches if t.content_id}),
        "channels": sorted({t.channel for t in touches if t.channel}),
        "campaign_ids": sorted({t.campaign_id for t in touches if t.campaign_id}),
    }


def money_quality_score(
    *,
    margin: float,
    repeatability: float,
    low_delivery_effort: float,
    upsell_potential: float,
    data_moat: float,
    partner_potential: float,
    risk: float,
) -> dict[str, Any]:
    """Money Quality = margin + repeatability + low delivery + upsell + data + partner - risk.

    Each input is normalised to [0, 1] (risk too — higher risk = bigger penalty).
    Output range theoretical: [-1, 6]. Reported normalised to [-1, 2] for the UI.
    """
    raw = (
        margin
        + repeatability
        + low_delivery_effort
        + upsell_potential
        + data_moat
        + partner_potential
        - risk
    )
    # 6 positive terms max + 1 risk penalty → squash to roughly [-1, 2]
    normalised = max(-1.0, min(2.0, raw / 3.0))
    return {
        "raw": round(raw, 3),
        "normalised": round(normalised, 3),
        "verdict": _money_quality_verdict(normalised),
        "inputs": {
            "margin": margin,
            "repeatability": repeatability,
            "low_delivery_effort": low_delivery_effort,
            "upsell_potential": upsell_potential,
            "data_moat": data_moat,
            "partner_potential": partner_potential,
            "risk": risk,
        },
    }


def _money_quality_verdict(score: float) -> str:
    if score >= 1.2:
        return "scale"
    if score >= 0.8:
        return "keep"
    if score >= 0.4:
        return "improve"
    return "kill_or_rework"


def attribution_dashboard() -> dict[str, Any]:
    """Aggregate revenue by source/offer/channel for the dashboard view."""
    rows = get_revenue_marketing_store().list_attributions()

    total = sum(r.revenue_sar for r in rows)
    by_channel: dict[str, float] = {}
    by_offer: dict[str, float] = {}
    by_source: dict[str, float] = {}
    by_attr_type: dict[str, float] = {}
    by_asset: dict[str, float] = {}

    for r in rows:
        if r.channel:
            by_channel[r.channel] = round(by_channel.get(r.channel, 0.0) + r.revenue_sar, 2)
        if r.offer_id:
            by_offer[r.offer_id] = round(by_offer.get(r.offer_id, 0.0) + r.revenue_sar, 2)
        by_source[r.primary_source] = round(by_source.get(r.primary_source, 0.0) + r.revenue_sar, 2)
        by_attr_type[r.attribution_type] = round(by_attr_type.get(r.attribution_type, 0.0) + r.revenue_sar, 2)
        for aid in r.asset_ids:
            by_asset[aid] = round(by_asset.get(aid, 0.0) + r.revenue_sar, 2)

    return {
        "total_revenue_sar": round(total, 2),
        "deals_count": len(rows),
        "by_channel": by_channel,
        "by_offer": by_offer,
        "by_primary_source": by_source,
        "by_attribution_type": by_attr_type,
        "top_revenue_assets": sorted(by_asset.items(), key=lambda kv: kv[1], reverse=True)[:10],
    }
