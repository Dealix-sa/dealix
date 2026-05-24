"""Dashboard snapshot — anti-vanity by construction.

Each section is paired with a downstream conversion or revenue measure so the
summary never shows engagement-only numbers.
"""

from __future__ import annotations

from typing import Any

from dealix.revenue_marketing.attribution import revenue_by_dimension
from dealix.revenue_marketing.marketing_graph import (
    best_message_variants_by_reply_rate,
    top_channels_by_qualified_leads,
    top_offers_by_close_rate,
)
from dealix.revenue_marketing.store import (
    RevenueMarketingStore,
    get_revenue_marketing_store,
)


def _safe_div(num: float, den: float) -> float:
    return round((num / den), 4) if den else 0.0


def dashboard_snapshot(
    store: RevenueMarketingStore | None = None,
) -> dict[str, Any]:
    """Return the full dashboard snapshot."""
    st = store or get_revenue_marketing_store()
    campaigns = st.list_campaigns(limit=10_000)
    leads = st.list_leads(limit=100_000)
    touches = st.list_touches(limit=100_000)
    attributions = st.list_attributions(limit=100_000)

    # ── Revenue by campaign + supporting cost-per-x metrics ─────────
    rev_by_campaign = revenue_by_dimension("campaign", store=st)
    rev_by_offer = revenue_by_dimension("offer", store=st)
    rev_by_asset = revenue_by_dimension("asset", store=st)
    rev_attr_total = round(sum(rev_by_campaign.values()), 2)

    leads_count = len(leads)
    calls_count = sum(1 for t in touches if (t.touch_type or "").lower() in {"call", "meeting"})
    wins_count = sum(1 for a in attributions if a.is_real_revenue)
    total_budget = sum(c.budget_sar for c in campaigns)

    top_campaigns_by_revenue = [
        {"campaign_id": cid, "revenue_sar": rev_by_campaign[cid]}
        for cid in sorted(rev_by_campaign, key=lambda k: rev_by_campaign[k], reverse=True)
    ][:5]

    # ── Red flags — anti-vanity guard rails ─────────────────────────
    red_flags: list[str] = []
    engagement_touches = sum(
        1
        for t in touches
        if (t.touch_type or "").lower() in {"view", "impression", "like", "share"}
    )
    if engagement_touches > 0 and leads_count == 0:
        red_flags.append("engagement_without_leads")
    if leads_count > 0 and calls_count == 0:
        red_flags.append("leads_without_calls")
    proposal_count = sum(1 for t in touches if (t.touch_type or "").lower() == "proposal")
    if calls_count > 0 and proposal_count == 0:
        red_flags.append("calls_without_proposals")
    if proposal_count > 0 and wins_count == 0:
        red_flags.append("proposals_without_wins")
    if total_budget > 0 and rev_attr_total == 0:
        red_flags.append("spend_without_attribution")

    content_without_cta = sum(
        1 for c in campaigns if c.status in {"active", "approval_pending"} and not c.message_angle
    )
    if content_without_cta > 0:
        red_flags.append("content_without_cta")

    campaign_without_outcome = sum(
        1 for c in campaigns if c.status == "active" and rev_by_campaign.get(c.id, 0.0) == 0.0
    )
    if campaign_without_outcome > 0:
        red_flags.append("campaign_without_outcome")

    return {
        "top_campaigns_by_revenue": top_campaigns_by_revenue,
        "top_channels_by_qualified_leads": top_channels_by_qualified_leads(
            n=5,
            store=st,
        ),
        "top_content_by_pipeline": [
            {"offer_id": oid, "pipeline_or_revenue_sar": rev_by_offer[oid]}
            for oid in sorted(rev_by_offer, key=lambda k: rev_by_offer[k], reverse=True)
        ][:5],
        "top_offers_by_close_rate": top_offers_by_close_rate(n=5, store=st),
        "best_message_variants": best_message_variants_by_reply_rate(n=5, store=st),
        "cost_per_lead": _safe_div(total_budget, leads_count),
        "cost_per_call": _safe_div(total_budget, calls_count),
        "cost_per_won_deal": _safe_div(total_budget, wins_count),
        "revenue_attributed_total": rev_attr_total,
        "assets_influencing_revenue": [
            {"asset_id": aid, "revenue_sar": rev_by_asset[aid]}
            for aid in sorted(rev_by_asset, key=lambda k: rev_by_asset[k], reverse=True)
        ],
        "red_flags": red_flags,
        "stats": st.stats(),
    }
