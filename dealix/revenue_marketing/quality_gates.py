"""Marketing quality gates — anti-vanity, anti-noise (§9, §25).

A campaign or content card that misses any required field never leaves draft.
All gates return {ok, blocked_reasons, ready_to_queue_approval}.
"""

from __future__ import annotations

from typing import Any

from dealix.revenue_marketing.schemas import CampaignRecord, ContentCardRecord


_REQUIRED_CAMPAIGN_FIELDS = {
    "campaign_name": "اسم الحملة مفقود.",
    "target_segment": "الـsegment المستهدف غير محدد.",
    "offer_id": "الحملة بلا offer — ممنوع.",
    "channel": "القناة غير محددة.",
    "message_angle": "زاوية الرسالة فارغة.",
    "cta_label_ar": "CTA غير موجود.",
    "success_metric": "Metric النجاح غير محدد.",
    "scale_kill_rule": "قاعدة Scale/Kill مفقودة — كل حملة لازم لها قرار حياة.",
}


def campaign_quality_gate(campaign: CampaignRecord) -> dict[str, Any]:
    """Validate a campaign against the anti-noise checklist."""
    blocked: list[str] = []
    payload = campaign.model_dump()
    for field, msg in _REQUIRED_CAMPAIGN_FIELDS.items():
        value = payload.get(field)
        if isinstance(value, str):
            if not value.strip():
                blocked.append(f"{field}: {msg}")
        elif not value:
            blocked.append(f"{field}: {msg}")

    if campaign.budget_sar < 0:
        blocked.append("budget_sar: لا يمكن أن يكون سالبًا.")

    if campaign.status == "live" and blocked:
        blocked.append("status: لا يمكن أن تكون 'live' مع وجود ثغرات.")

    return {
        "ok": not blocked,
        "blocked_reasons": blocked,
        "ready_to_queue_approval": not blocked,
        "campaign_id": campaign.id,
    }


_REQUIRED_CONTENT_FIELDS = {
    "topic_ar": "موضوع المحتوى مفقود.",
    "target_segment": "الـsegment المستهدف غير محدد.",
    "pain": "الألم المعالج غير محدد.",
    "offer_id": "المحتوى بلا offer — مجرد noise.",
    "cta_ar": "CTA باللغة العربية مفقود.",
    "channel": "القناة غير محددة.",
}


def content_quality_gate(card: ContentCardRecord) -> dict[str, Any]:
    blocked: list[str] = []
    payload = card.model_dump()
    for field, msg in _REQUIRED_CONTENT_FIELDS.items():
        value = payload.get(field)
        if isinstance(value, str):
            if not value.strip():
                blocked.append(f"{field}: {msg}")
        elif not value:
            blocked.append(f"{field}: {msg}")

    return {
        "ok": not blocked,
        "blocked_reasons": blocked,
        "ready_to_queue_approval": not blocked,
        "card_id": card.id,
    }


def anti_vanity_review(metrics: dict[str, Any]) -> dict[str, Any]:
    """Flag metrics celebrated without downstream conversion (§25).

    Inputs example:
      {"views": 12000, "likes": 800, "leads": 2, "calls": 0, "deals": 0, "revenue_sar": 0}
    """
    views = int(metrics.get("views") or 0)
    likes = int(metrics.get("likes") or 0)
    followers = int(metrics.get("followers") or 0)
    leads = int(metrics.get("leads") or 0)
    calls = int(metrics.get("calls") or 0)
    deals = int(metrics.get("deals") or 0)
    revenue = float(metrics.get("revenue_sar") or 0.0)

    flags: list[str] = []
    if (views + likes + followers) > 1000 and leads == 0:
        flags.append("Engagement عالي بلا leads — vanity.")
    if leads > 20 and calls == 0:
        flags.append("Leads كثيرة بلا calls — قياس وهمي أو تأهيل ضعيف.")
    if calls > 10 and deals == 0 and revenue == 0:
        flags.append("Calls كثيرة بلا deals — Offer أو Price أو Proof تحت السقف.")

    score_signal = leads + (5 * calls) + (20 * deals)
    return {
        "vanity_flags_ar": flags,
        "ok": not flags,
        "conversion_signal_score": score_signal,
        "rule": "Vanity metric بدون conversion = noise.",
    }
