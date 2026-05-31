"""Revenue attribution — only real (paid or signed) revenue is counted."""

from __future__ import annotations

from typing import Literal

from dealix.revenue_marketing.schemas import (
    AttributionType,
    MarketingTouch,
    RevenueAttribution,
)
from dealix.revenue_marketing.store import (
    RevenueMarketingStore,
    get_revenue_marketing_store,
    uid,
)

AttrDimension = Literal["channel", "campaign", "offer", "asset", "agent"]


def record_attribution(
    deal_id: str,
    revenue_sar: float,
    sources: dict[str, str | None],
    *,
    payment_received: bool,
    signed_agreement: bool,
    attribution_type: AttributionType = "multi_touch",
    store: RevenueMarketingStore | None = None,
) -> RevenueAttribution:
    """Record a revenue-attribution row.

    Raises ``ValueError('revenue_not_real_yet')`` if neither ``payment_received``
    nor ``signed_agreement`` is True (unless ``attribution_type`` is
    ``pipeline_only``, in which case pipeline-only rows are allowed).
    """
    if attribution_type != "pipeline_only" and not (payment_received or signed_agreement):
        raise ValueError("revenue_not_real_yet")
    if not deal_id:
        raise ValueError("deal_id_required")
    if revenue_sar < 0:
        raise ValueError("revenue_must_be_non_negative")

    st = store or get_revenue_marketing_store()
    attribution = RevenueAttribution(
        id=uid("att"),
        revenue_sar=float(revenue_sar),
        deal_id=deal_id,
        campaign_id=sources.get("campaign_id"),
        offer_id=sources.get("offer_id"),
        channel=sources.get("channel"),
        asset_id=sources.get("asset_id"),
        agent_id=sources.get("agent_id"),
        attribution_type=attribution_type,
        payment_received=payment_received,
        signed_agreement=signed_agreement,
    )
    st.append_attribution(attribution)
    return attribution


def attribution_chain_for_deal(
    deal_id: str,
    store: RevenueMarketingStore | None = None,
) -> list[dict[str, object]]:
    """Return ordered (oldest-first) touches + attribution snapshot for a deal."""
    st = store or get_revenue_marketing_store()
    chain: list[dict[str, object]] = []

    attributions = [a for a in st.list_attributions(limit=10_000) if a.deal_id == deal_id]
    related_campaigns = {a.campaign_id for a in attributions if a.campaign_id}
    related_offers = {a.offer_id for a in attributions if a.offer_id}

    deal_touches: list[MarketingTouch] = []
    for touch in st.list_touches(limit=100_000):
        if touch.lead_id == deal_id or (
            touch.campaign_id and touch.campaign_id in related_campaigns
        ):
            deal_touches.append(touch)
    deal_touches.sort(key=lambda t: t.occurred_at)

    campaigns_by_id = {c.id: c for c in st.list_campaigns(limit=10_000)}
    offers_by_id = {o.id: o for o in st.list_offers(limit=10_000)}

    for touch in deal_touches:
        chain.append(
            {
                "kind": "touch",
                "id": touch.id,
                "occurred_at": touch.occurred_at.isoformat(),
                "channel": touch.channel,
                "touch_type": touch.touch_type,
                "campaign_id": touch.campaign_id,
                "message_variant": touch.message_variant,
                "content_id": touch.content_id,
            },
        )

    for camp_id in related_campaigns:
        camp = campaigns_by_id.get(camp_id) if camp_id else None
        if camp:
            chain.append(
                {
                    "kind": "campaign",
                    "id": camp.id,
                    "campaign_name": camp.campaign_name,
                    "channel": camp.channel,
                    "offer_id": camp.offer_id,
                },
            )

    for offer_id in related_offers:
        off = offers_by_id.get(offer_id) if offer_id else None
        if off:
            chain.append(
                {
                    "kind": "offer",
                    "id": off.id,
                    "rung": off.rung,
                    "name_en": off.name_en,
                },
            )

    for attr in attributions:
        chain.append(
            {
                "kind": "attribution",
                "id": attr.id,
                "attribution_type": attr.attribution_type,
                "revenue_sar": attr.revenue_sar,
                "is_real_revenue": attr.is_real_revenue,
                "asset_id": attr.asset_id,
                "agent_id": attr.agent_id,
                "created_at": attr.created_at.isoformat(),
            },
        )

    return chain


def revenue_by_dimension(
    dim: AttrDimension,
    store: RevenueMarketingStore | None = None,
) -> dict[str, float]:
    """Sum *real* revenue by the requested dimension.

    Pipeline-only / unsigned rows are ignored.
    """
    st = store or get_revenue_marketing_store()
    field = f"{dim}_id" if dim != "channel" else "channel"
    out: dict[str, float] = {}
    for attr in st.list_attributions(limit=100_000):
        if not attr.is_real_revenue:
            continue
        key = getattr(attr, field, None)
        if not key:
            continue
        out[str(key)] = round(out.get(str(key), 0.0) + float(attr.revenue_sar), 2)
    return out
