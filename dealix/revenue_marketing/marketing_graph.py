"""In-memory Marketing Intelligence Graph built from the store.

The graph is a snapshot — it is rebuilt on demand so callers always see the
current state of audiences, offers, campaigns, leads, attributions, and
outcomes.
"""

from __future__ import annotations

from typing import Any

from dealix.revenue_marketing.scoring import classify_outcome
from dealix.revenue_marketing.store import (
    RevenueMarketingStore,
    get_revenue_marketing_store,
)


def _safe_id(prefix: str, value: str | None) -> str:
    return f"{prefix}:{value}" if value else ""


def build_graph(
    store: RevenueMarketingStore | None = None,
) -> dict[str, Any]:
    """Return ``{nodes, edges}`` for the current store state."""
    st = store or get_revenue_marketing_store()

    audiences = st.list_audiences(limit=10_000)
    offers = st.list_offers(limit=10_000)
    messages = st.list_messages(limit=10_000)
    campaigns = st.list_campaigns(limit=10_000)
    leads = st.list_leads(limit=10_000)
    touches = st.list_touches(limit=100_000)
    attributions = st.list_attributions(limit=10_000)

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    for a in audiences:
        nodes.append({"id": _safe_id("audience", a.id), "kind": "audience", "name": a.name})
        for pain in a.pain_points:
            pain_id = _safe_id("pain", pain)
            nodes.append({"id": pain_id, "kind": "pain", "name": pain})
            edges.append({"src": _safe_id("audience", a.id), "dst": pain_id, "rel": "has_pain"})

    for o in offers:
        nodes.append(
            {
                "id": _safe_id("offer", o.id),
                "kind": "offer",
                "name": o.name_en,
                "rung": o.rung,
                "target_segment": o.target_segment,
            },
        )
        pain_id = _safe_id("pain", o.pain_addressed)
        if o.pain_addressed:
            nodes.append({"id": pain_id, "kind": "pain", "name": o.pain_addressed})
            edges.append({"src": _safe_id("offer", o.id), "dst": pain_id, "rel": "addresses_pain"})

    for m in messages:
        nodes.append(
            {
                "id": _safe_id("message", m.id),
                "kind": "message",
                "name": m.headline_en,
                "angle": m.angle,
            },
        )
        if m.offer_id:
            edges.append(
                {
                    "src": _safe_id("message", m.id),
                    "dst": _safe_id("offer", m.offer_id),
                    "rel": "sells_offer",
                },
            )

    for c in campaigns:
        nodes.append(
            {
                "id": _safe_id("campaign", c.id),
                "kind": "campaign",
                "name": c.campaign_name,
                "channel": c.channel,
                "status": c.status,
            },
        )
        ch_id = _safe_id("channel", c.channel)
        nodes.append({"id": ch_id, "kind": "channel", "name": c.channel})
        edges.append({"src": _safe_id("campaign", c.id), "dst": ch_id, "rel": "uses_channel"})
        if c.offer_id:
            edges.append(
                {
                    "src": _safe_id("campaign", c.id),
                    "dst": _safe_id("offer", c.offer_id),
                    "rel": "promotes_offer",
                },
            )

    for lead in leads:
        nodes.append(
            {
                "id": _safe_id("lead", lead.id),
                "kind": "lead",
                "name": lead.id,
                "score": lead.overall_score,
            },
        )
        if lead.campaign_id:
            edges.append(
                {
                    "src": _safe_id("campaign", lead.campaign_id),
                    "dst": _safe_id("lead", lead.id),
                    "rel": "produced_lead",
                },
            )

    for t in touches:
        if t.campaign_id and t.lead_id:
            edges.append(
                {
                    "src": _safe_id("campaign", t.campaign_id),
                    "dst": _safe_id("lead", t.lead_id),
                    "rel": "touched_lead",
                    "touch_type": t.touch_type,
                },
            )

    for a in attributions:
        deal_id = _safe_id("deal", a.deal_id)
        nodes.append({"id": deal_id, "kind": "deal", "name": a.deal_id})
        outcome_id = _safe_id("outcome", f"{a.deal_id}:revenue")
        nodes.append(
            {
                "id": outcome_id,
                "kind": "outcome",
                "name": "revenue_recognised",
                "is_real_revenue": a.is_real_revenue,
            },
        )
        edges.append({"src": deal_id, "dst": outcome_id, "rel": "produced_outcome"})
        if a.campaign_id:
            edges.append(
                {
                    "src": _safe_id("campaign", a.campaign_id),
                    "dst": deal_id,
                    "rel": "attributed_to_deal",
                },
            )
        if a.offer_id:
            edges.append(
                {
                    "src": _safe_id("offer", a.offer_id),
                    "dst": deal_id,
                    "rel": "sold_in_deal",
                },
            )
        if a.asset_id:
            asset_id = _safe_id("asset", a.asset_id)
            nodes.append({"id": asset_id, "kind": "asset", "name": a.asset_id})
            edges.append({"src": asset_id, "dst": deal_id, "rel": "influenced_deal"})

    # Deduplicate nodes by id, preserving first-seen attributes.
    seen: dict[str, dict[str, Any]] = {}
    for n in nodes:
        if not n.get("id"):
            continue
        seen.setdefault(n["id"], n)
    return {"nodes": list(seen.values()), "edges": edges}


# ────────────────────────── query helpers ─────────────────────────────


def _safe_div(num: float, den: float) -> float:
    return (num / den) if den else 0.0


def top_offers_by_close_rate(
    n: int = 5,
    store: RevenueMarketingStore | None = None,
) -> list[dict[str, Any]]:
    st = store or get_revenue_marketing_store()
    offers = st.list_offers(limit=10_000)
    attributions = st.list_attributions(limit=100_000)
    leads = st.list_leads(limit=100_000)
    out: list[dict[str, Any]] = []
    for offer in offers:
        wins = sum(1 for a in attributions if a.offer_id == offer.id and a.is_real_revenue)
        lead_count = sum(
            1
            for lead in leads
            if any(
                t.lead_id == lead.id and t.campaign_id and offer.id
                for t in st.list_touches(limit=100_000)
            )
        )
        out.append(
            {
                "offer_id": offer.id,
                "offer_name": offer.name_en,
                "wins": wins,
                "leads": lead_count,
                "close_rate": round(_safe_div(wins, lead_count), 4),
            },
        )
    out.sort(key=lambda r: r["close_rate"], reverse=True)
    return out[:n]


def top_channels_by_qualified_leads(
    n: int = 5,
    qualification_threshold: float = 0.5,
    store: RevenueMarketingStore | None = None,
) -> list[dict[str, Any]]:
    st = store or get_revenue_marketing_store()
    leads = st.list_leads(limit=100_000)
    touches = st.list_touches(limit=100_000)
    lead_channel: dict[str, str] = {}
    for t in touches:
        if t.lead_id and t.channel and t.lead_id not in lead_channel:
            lead_channel[t.lead_id] = t.channel
    counts: dict[str, int] = {}
    for lead in leads:
        if lead.overall_score < qualification_threshold:
            continue
        ch = lead_channel.get(lead.id, lead.source or "unknown")
        counts[ch] = counts.get(ch, 0) + 1
    items = [{"channel": k, "qualified_leads": v} for k, v in counts.items()]
    items.sort(key=lambda r: r["qualified_leads"], reverse=True)
    return items[:n]


def best_message_variants_by_reply_rate(
    n: int = 5,
    store: RevenueMarketingStore | None = None,
) -> list[dict[str, Any]]:
    st = store or get_revenue_marketing_store()
    touches = st.list_touches(limit=100_000)
    sent: dict[str, int] = {}
    replied: dict[str, int] = {}
    for t in touches:
        if not t.message_variant:
            continue
        sent[t.message_variant] = sent.get(t.message_variant, 0) + 1
        if (t.touch_type or "").lower() == "reply":
            replied[t.message_variant] = replied.get(t.message_variant, 0) + 1
    out = []
    for variant, total in sent.items():
        out.append(
            {
                "message_variant": variant,
                "sent": total,
                "replies": replied.get(variant, 0),
                "reply_rate": round(_safe_div(replied.get(variant, 0), total), 4),
            },
        )
    out.sort(key=lambda r: r["reply_rate"], reverse=True)
    return out[:n]


def pains_by_call_rate(
    n: int = 5,
    store: RevenueMarketingStore | None = None,
) -> list[dict[str, Any]]:
    st = store or get_revenue_marketing_store()
    leads = st.list_leads(limit=100_000)
    touches = st.list_touches(limit=100_000)
    calls_by_lead = {
        t.lead_id
        for t in touches
        if t.lead_id and (t.touch_type or "").lower() in {"call", "meeting"}
    }
    pain_total: dict[str, int] = {}
    pain_calls: dict[str, int] = {}
    for lead in leads:
        if not lead.pain:
            continue
        pain_total[lead.pain] = pain_total.get(lead.pain, 0) + 1
        if lead.id in calls_by_lead:
            pain_calls[lead.pain] = pain_calls.get(lead.pain, 0) + 1
    out = []
    for pain, total in pain_total.items():
        out.append(
            {
                "pain": pain,
                "leads": total,
                "calls": pain_calls.get(pain, 0),
                "call_rate": round(_safe_div(pain_calls.get(pain, 0), total), 4),
            },
        )
    out.sort(key=lambda r: r["call_rate"], reverse=True)
    return out[:n]


def partners_by_revenue(
    n: int = 5,
    store: RevenueMarketingStore | None = None,
) -> list[dict[str, Any]]:
    st = store or get_revenue_marketing_store()
    rev: dict[str, float] = {}
    for a in st.list_attributions(limit=100_000):
        if not a.is_real_revenue or not a.agent_id:
            continue
        rev[a.agent_id] = round(rev.get(a.agent_id, 0.0) + float(a.revenue_sar), 2)
    items = [{"partner": k, "revenue_sar": v} for k, v in rev.items()]
    items.sort(key=lambda r: r["revenue_sar"], reverse=True)
    return items[:n]


__all__ = [
    "best_message_variants_by_reply_rate",
    "build_graph",
    "classify_outcome",  # convenience re-export for callers
    "pains_by_call_rate",
    "partners_by_revenue",
    "top_channels_by_qualified_leads",
    "top_offers_by_close_rate",
]
