"""Revenue Portfolio dashboard (§20).

Aggregates revenue by stream (offer) and ranks via the Money Quality formula.
The dashboard outputs scale/keep/improve/kill verdicts so the founder weekly
loop can decide where to push and where to retire.
"""

from __future__ import annotations

from typing import Any

from dealix.revenue_marketing.attribution import money_quality_score
from dealix.revenue_marketing.schemas import OfferRecord
from dealix.revenue_marketing.store import get_revenue_marketing_store


_TIER_PROFILES = {
    "free": {
        "margin": 0.1, "repeatability": 0.9, "low_delivery_effort": 0.9,
        "upsell_potential": 0.6, "data_moat": 0.5, "partner_potential": 0.4, "risk": 0.1,
    },
    "entry": {
        "margin": 0.6, "repeatability": 0.8, "low_delivery_effort": 0.7,
        "upsell_potential": 0.8, "data_moat": 0.5, "partner_potential": 0.4, "risk": 0.15,
    },
    "core": {
        "margin": 0.7, "repeatability": 0.6, "low_delivery_effort": 0.45,
        "upsell_potential": 0.75, "data_moat": 0.65, "partner_potential": 0.55, "risk": 0.2,
    },
    "expansion": {
        "margin": 0.75, "repeatability": 0.45, "low_delivery_effort": 0.35,
        "upsell_potential": 0.55, "data_moat": 0.7, "partner_potential": 0.5, "risk": 0.3,
    },
    "enterprise": {
        "margin": 0.8, "repeatability": 0.3, "low_delivery_effort": 0.25,
        "upsell_potential": 0.5, "data_moat": 0.85, "partner_potential": 0.4, "risk": 0.45,
    },
}


def stream_money_quality(offer: OfferRecord) -> dict[str, Any]:
    profile = _TIER_PROFILES.get(offer.tier, _TIER_PROFILES["core"])
    return money_quality_score(**profile)


def portfolio_dashboard() -> dict[str, Any]:
    store = get_revenue_marketing_store()
    offers = [o for o in store.list_offers() if o.active]
    attributions = store.list_attributions()

    rev_by_offer: dict[str, float] = {}
    deals_by_offer: dict[str, int] = {}
    for a in attributions:
        if not a.offer_id:
            continue
        rev_by_offer[a.offer_id] = round(rev_by_offer.get(a.offer_id, 0.0) + a.revenue_sar, 2)
        deals_by_offer[a.offer_id] = deals_by_offer.get(a.offer_id, 0) + 1

    streams: list[dict[str, Any]] = []
    for o in offers:
        mq = stream_money_quality(o)
        streams.append(
            {
                "offer_id": o.id,
                "name_ar": o.name_ar,
                "tier": o.tier,
                "current_revenue_sar": rev_by_offer.get(o.id, 0.0),
                "deals_count": deals_by_offer.get(o.id, 0),
                "money_quality": mq["normalised"],
                "verdict": mq["verdict"],
                "inputs": mq["inputs"],
            }
        )

    streams.sort(key=lambda s: (s["money_quality"], s["current_revenue_sar"]), reverse=True)

    decisions = {"scale": [], "keep": [], "improve": [], "kill_or_rework": []}
    for s in streams:
        decisions[s["verdict"]].append(s["offer_id"])

    return {
        "total_revenue_sar": round(sum(rev_by_offer.values()), 2),
        "active_offer_count": len(offers),
        "streams": streams,
        "decisions": decisions,
        "anti_vanity_note": "Revenue counted only after payment_confirmed=True.",
    }
