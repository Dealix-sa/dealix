"""Revenue Marketing Operating Loop (§5).

Signal → Segment → Pain → Offer → Message → Channel → Lead → Deal →
Revenue → Outcome → Learning → Asset → Scale / Kill.

This is the orchestrator that takes a signal + a target segment, suggests an
offer from the ladder, drafts a campaign (in `draft` status), and returns the
full loop trace. No external sends — everything stays gated by Approval
Center via the API surface.
"""

from __future__ import annotations

from typing import Any

from dealix.revenue_marketing.offer_ladder import next_rung_upsell
from dealix.revenue_marketing.quality_gates import campaign_quality_gate
from dealix.revenue_marketing.schemas import (
    CampaignRecord,
    ChannelKind,
    MarketSignalRecord,
)
from dealix.revenue_marketing.store import get_revenue_marketing_store, uid


_DEFAULT_CHANNEL_BY_SEGMENT: dict[str, ChannelKind] = {
    "b2b_founders_ksa": "linkedin",
    "b2b_saudi_using_ai": "linkedin",
    "agency_owners": "direct_outreach",
    "consultants_ksa": "direct_outreach",
    "enterprise_pmo": "email_newsletter",
    "vc_studio": "email_newsletter",
    "saas_b2b": "linkedin",
}


def _suggest_channel(segment: str) -> ChannelKind:
    return _DEFAULT_CHANNEL_BY_SEGMENT.get(segment, "linkedin")


def _build_message_angle(segment: str, pain: str, offer_promise: str) -> str:
    """3-angle template per §12 message variants — picks one safe default."""
    return (
        f"إلى {segment}: إذا الألم '{pain}' معطل عملياتكم، "
        f"عرضنا المحكوم: {offer_promise} — كل خطوة بأدلة وموافقات."
    )


def run_marketing_loop(
    *,
    signal_id: str,
    channel_override: ChannelKind | None = None,
    success_metric: str = "qualified_calls_booked",
    scale_kill_rule: str = "scale if reply_rate >= 8% in 7 days, else kill",
) -> dict[str, Any]:
    """Execute the full loop for one signal and return the trace + draft campaign."""
    store = get_revenue_marketing_store()

    signal: MarketSignalRecord | None = next(
        (s for s in store.list_signals() if s.id == signal_id), None
    )
    if signal is None:
        raise KeyError(f"signal not found: {signal_id}")

    offer = store.get_offer(signal.suggested_offer_id) if signal.suggested_offer_id else None
    if offer is None:
        return {
            "signal_id": signal_id,
            "blocked_reason": "no_offer_matched_signal",
            "next_action": "حدّد offer_id داخل الإشارة قبل إنشاء الحملة.",
        }

    channel: ChannelKind = channel_override or _suggest_channel(signal.segment)
    campaign = CampaignRecord(
        id=uid("cmp"),
        campaign_name=f"loop:{offer.id}:{signal.segment}",
        target_segment=signal.segment,
        offer_id=offer.id,
        channel=channel,
        message_angle=_build_message_angle(signal.segment, signal.pain, offer.promise_ar),
        cta_label_ar=f"اطلب {offer.name_ar}",
        cta_path=f"/dealix-{offer.id.replace('_', '-')}",
        success_metric=success_metric,
        scale_kill_rule=scale_kill_rule,
        status="draft",
        signal_id=signal.id,
    )
    campaign = store.upsert_campaign(campaign)
    gate = campaign_quality_gate(campaign)
    upsell = next_rung_upsell(offer.id)

    return {
        "signal": signal.model_dump(mode="json"),
        "offer": offer.model_dump(mode="json"),
        "campaign_draft": campaign.model_dump(mode="json"),
        "quality_gate": gate,
        "suggested_next_rung_upsell": (
            upsell.model_dump(mode="json") if upsell is not None else None
        ),
        "loop_steps": [
            "signal",
            "segment",
            "pain",
            "offer",
            "message",
            "channel",
            "campaign_draft",
            "quality_gate",
            "queue_for_approval",
        ],
        "post_loop_actions": [
            "queue_for_approval via /api/v1/ops-autopilot/marketing/queue-approval",
            "after approval: track touches and attribute revenue",
            "weekly: run portfolio_dashboard to decide scale/kill",
        ],
    }


def signal_to_offer_recommendations() -> list[dict[str, Any]]:
    """For every signal, surface the suggested offer + confidence + channel."""
    store = get_revenue_marketing_store()
    out: list[dict[str, Any]] = []
    for sig in store.list_signals():
        offer = store.get_offer(sig.suggested_offer_id) if sig.suggested_offer_id else None
        out.append(
            {
                "signal_id": sig.id,
                "segment": sig.segment,
                "pain": sig.pain,
                "confidence": sig.confidence,
                "suggested_offer_id": sig.suggested_offer_id,
                "suggested_offer_name_ar": offer.name_ar if offer else "",
                "suggested_channel": _suggest_channel(sig.segment),
                "why_now": sig.why_now,
                "proof_target": sig.proof_target,
            }
        )
    out.sort(key=lambda r: r["confidence"], reverse=True)
    return out
