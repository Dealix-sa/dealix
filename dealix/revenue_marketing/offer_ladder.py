"""5-rung offer ladder lookup helpers (§29)."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from dealix.revenue_marketing.schemas import OfferRecord, OfferTier
from dealix.revenue_marketing.store import get_revenue_marketing_store

_LADDER_ORDER: tuple[OfferTier, ...] = ("free", "entry", "core", "expansion", "enterprise")


def offer_ladder_catalog() -> dict[str, Any]:
    """Return the ladder grouped by tier with active offers only."""
    offers = [o for o in get_revenue_marketing_store().list_offers() if o.active]
    by_tier: dict[OfferTier, list[OfferRecord]] = defaultdict(list)
    for o in offers:
        by_tier[o.tier].append(o)

    rungs: list[dict[str, Any]] = []
    for tier in _LADDER_ORDER:
        rung_offers = sorted(by_tier.get(tier, []), key=lambda o: o.price_min_sar)
        rungs.append(
            {
                "tier": tier,
                "count": len(rung_offers),
                "offers": [o.model_dump(mode="json") for o in rung_offers],
            }
        )

    return {
        "ladder_order": list(_LADDER_ORDER),
        "rungs": rungs,
        "total_offers": sum(len(b) for b in by_tier.values()),
    }


def ladder_offer_by_id(offer_id: str) -> OfferRecord | None:
    return get_revenue_marketing_store().get_offer(offer_id)


def next_rung_upsell(offer_id: str) -> OfferRecord | None:
    """Suggest the next rung's strongest offer (highest money_quality)."""
    store = get_revenue_marketing_store()
    current = store.get_offer(offer_id)
    if current is None:
        return None
    idx = _LADDER_ORDER.index(current.tier)
    if idx >= len(_LADDER_ORDER) - 1:
        return None
    next_tier = _LADDER_ORDER[idx + 1]
    candidates = [o for o in store.list_offers() if o.active and o.tier == next_tier]
    if not candidates:
        return None
    return max(candidates, key=lambda o: o.money_quality)
