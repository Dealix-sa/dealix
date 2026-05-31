"""Conversion funnel: stages, rates, and bottleneck diagnosis (§15)."""

from __future__ import annotations

from typing import Any

from dealix.revenue_marketing.schemas import FunnelSnapshotRecord
from dealix.revenue_marketing.store import get_revenue_marketing_store


_HEALTHY_RATES = {
    "visitor_to_lead": 0.03,
    "lead_to_qualified": 0.40,
    "qualified_to_call": 0.50,
    "call_to_proposal": 0.60,
    "proposal_to_win": 0.30,
    "win_to_payment": 0.90,
    "payment_to_retainer": 0.25,
}


def _ratio(num: int, denom: int) -> float:
    return round(num / denom, 4) if denom else 0.0


def funnel_conversion_rates(snapshot: FunnelSnapshotRecord) -> dict[str, float]:
    return {
        "visitor_to_lead": _ratio(snapshot.leads, snapshot.visitors),
        "lead_to_qualified": _ratio(snapshot.qualified_leads, snapshot.leads),
        "qualified_to_call": _ratio(snapshot.calls_booked, snapshot.qualified_leads),
        "call_to_proposal": _ratio(snapshot.proposals_sent, snapshot.calls_booked),
        "proposal_to_win": _ratio(snapshot.won, snapshot.proposals_sent),
        "win_to_payment": _ratio(snapshot.paid, snapshot.won),
        "payment_to_retainer": _ratio(snapshot.retainers, snapshot.paid),
    }


_FIX_HINTS = {
    "visitor_to_lead": "ضعّف الاحتكاك في الـCTA أو جرّب lead magnet مختلف.",
    "lead_to_qualified": "حسّن ICP filter أو سؤال تأهيل قبل الـcall.",
    "qualified_to_call": "ضع slot واضح في الرسالة (Calendly) واحذف خطوات الحجز الزائدة.",
    "call_to_proposal": "أعد صياغة الـDiscovery — الألم غير واضح أو السعر يُذكر بدري.",
    "proposal_to_win": "أضف Proof Pack + قسّم Scope إلى Pilot أصغر.",
    "win_to_payment": "راجع Moyasar/فاتورة + سرعة إرسال الفاتورة بعد القرار.",
    "payment_to_retainer": "أرسل Value Report خلال 14 يوم + عرّض Monthly Revenue Command.",
}


def bottleneck_diagnosis(snapshot: FunnelSnapshotRecord) -> dict[str, Any]:
    """Find the worst-performing stage vs the healthy baseline."""
    rates = funnel_conversion_rates(snapshot)
    gaps: list[tuple[str, float, float]] = []
    for stage, actual in rates.items():
        baseline = _HEALTHY_RATES[stage]
        gap = baseline - actual
        gaps.append((stage, actual, gap))

    gaps.sort(key=lambda t: t[2], reverse=True)
    worst_stage, worst_actual, worst_gap = gaps[0]

    return {
        "snapshot_id": snapshot.id,
        "period_label": snapshot.period_label,
        "rates": rates,
        "healthy_baseline": _HEALTHY_RATES,
        "bottleneck_stage": worst_stage,
        "bottleneck_actual": round(worst_actual, 4),
        "bottleneck_baseline": _HEALTHY_RATES[worst_stage],
        "bottleneck_gap": round(max(worst_gap, 0.0), 4),
        "fix_hint_ar": _FIX_HINTS[worst_stage],
        "all_gaps": [
            {"stage": s, "actual": round(a, 4), "gap": round(max(g, 0.0), 4)}
            for s, a, g in gaps
        ],
    }


def latest_funnel_dashboard() -> dict[str, Any]:
    snaps = get_revenue_marketing_store().list_funnel_snapshots(limit=1)
    if not snaps:
        return {"empty": True, "message": "no funnel snapshot recorded yet"}
    s = snaps[0]
    return {
        "snapshot": s.model_dump(mode="json"),
        "rates": funnel_conversion_rates(s),
        "bottleneck": bottleneck_diagnosis(s),
    }
