"""Revenue-portfolio snapshot — the 5 ladders + health warnings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dealix.revenue_marketing.schemas import OfferRung
from dealix.revenue_marketing.store import (
    RevenueMarketingStore,
    get_revenue_marketing_store,
)


@dataclass(slots=True)
class Stream:
    stream_name: OfferRung
    current_revenue_sar: float = 0.0
    pipeline_sar: float = 0.0
    margin_pct: float = 0.0
    delivery_effort: float = 0.0
    risk: float = 0.0
    repeatability: float = 0.0
    scale_potential: float = 0.0
    owner: str = "founder"
    next_action: str = ""
    offer_ids: list[str] = field(default_factory=list)


_RUNG_DEFAULTS: dict[OfferRung, dict[str, Any]] = {
    "free": {
        "margin_pct": 0.0,
        "delivery_effort": 0.2,
        "risk": 0.1,
        "repeatability": 0.9,
        "scale_potential": 0.4,
        "owner": "growth",
        "next_action": "convert_to_entry_within_30_days",
    },
    "entry": {
        "margin_pct": 0.55,
        "delivery_effort": 0.4,
        "risk": 0.2,
        "repeatability": 0.7,
        "scale_potential": 0.7,
        "owner": "founder",
        "next_action": "qualify_for_core_within_60_days",
    },
    "core": {
        "margin_pct": 0.65,
        "delivery_effort": 0.55,
        "risk": 0.25,
        "repeatability": 0.6,
        "scale_potential": 0.7,
        "owner": "founder",
        "next_action": "expand_into_expansion_offer",
    },
    "expansion": {
        "margin_pct": 0.6,
        "delivery_effort": 0.7,
        "risk": 0.3,
        "repeatability": 0.4,
        "scale_potential": 0.6,
        "owner": "founder",
        "next_action": "stabilise_then_offer_enterprise_loop",
    },
    "enterprise": {
        "margin_pct": 0.55,
        "delivery_effort": 0.9,
        "risk": 0.4,
        "repeatability": 0.2,
        "scale_potential": 0.9,
        "owner": "founder",
        "next_action": "harden_governance_for_repeat_sale",
    },
}


def current_streams(
    store: RevenueMarketingStore | None = None,
) -> list[Stream]:
    """Return one Stream per rung, filled with real revenue + pipeline data."""
    st = store or get_revenue_marketing_store()
    offers = st.list_offers(limit=10_000)
    attributions = st.list_attributions(limit=100_000)

    offers_by_rung: dict[OfferRung, list[str]] = {
        "free": [],
        "entry": [],
        "core": [],
        "expansion": [],
        "enterprise": [],
    }
    for o in offers:
        offers_by_rung.setdefault(o.rung, []).append(o.id)

    streams: list[Stream] = []
    for rung, ids in offers_by_rung.items():
        defaults = _RUNG_DEFAULTS[rung]
        current_revenue = 0.0
        pipeline = 0.0
        for a in attributions:
            if a.offer_id and a.offer_id in ids:
                if a.is_real_revenue:
                    current_revenue += float(a.revenue_sar)
                else:
                    pipeline += float(a.revenue_sar)
        streams.append(
            Stream(
                stream_name=rung,
                current_revenue_sar=round(current_revenue, 2),
                pipeline_sar=round(pipeline, 2),
                margin_pct=float(defaults["margin_pct"]),
                delivery_effort=float(defaults["delivery_effort"]),
                risk=float(defaults["risk"]),
                repeatability=float(defaults["repeatability"]),
                scale_potential=float(defaults["scale_potential"]),
                owner=str(defaults["owner"]),
                next_action=str(defaults["next_action"]),
                offer_ids=ids,
            ),
        )
    return streams


def portfolio_health(
    store: RevenueMarketingStore | None = None,
) -> dict[str, Any]:
    """Return totals + warnings (concentration, missing streams, no pipeline)."""
    streams = current_streams(store=store)
    total_revenue = round(sum(s.current_revenue_sar for s in streams), 2)
    total_pipeline = round(sum(s.pipeline_sar for s in streams), 2)
    warnings: list[str] = []

    if total_revenue > 0:
        for s in streams:
            share = s.current_revenue_sar / total_revenue if total_revenue else 0.0
            if share > 0.6:
                warnings.append(
                    f"single_stream_over_60_pct:{s.stream_name}:{round(share * 100, 1)}",
                )
    missing = [s.stream_name for s in streams if not s.offer_ids]
    for m in missing:
        warnings.append(f"missing_stream:{m}")

    if total_pipeline == 0.0 and total_revenue > 0.0:
        warnings.append("no_pipeline_to_cover_next_quarter")

    return {
        "total_revenue_sar": total_revenue,
        "total_pipeline_sar": total_pipeline,
        "streams": [
            {
                "stream_name": s.stream_name,
                "current_revenue_sar": s.current_revenue_sar,
                "pipeline_sar": s.pipeline_sar,
                "margin_pct": s.margin_pct,
                "delivery_effort": s.delivery_effort,
                "risk": s.risk,
                "repeatability": s.repeatability,
                "scale_potential": s.scale_potential,
                "owner": s.owner,
                "next_action": s.next_action,
                "offer_count": len(s.offer_ids),
            }
            for s in streams
        ],
        "warnings": warnings,
    }
