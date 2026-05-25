"""Decision logic for a revenue stream card."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

from dealix.growth_os.streams.stream_card import RevenueStreamCard

Action = Literal[
    "scale",
    "optimize",
    "reprice",
    "bundle",
    "partner_led",
    "pause",
    "kill",
]


class StreamDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stream_key: str
    action: Action
    reason_ar: str
    reason_en: str


def decide_stream_action(card: RevenueStreamCard) -> StreamDecision:
    """Pure decision based on margin, retainer potential, effort, and risk."""
    high_margin = card.margin_pct >= 0.55
    healthy_margin = card.margin_pct >= 0.35
    high_retainer = card.retainer_potential >= 0.7
    low_risk = card.risk == "low"
    heavy_effort = card.effort_hours_per_unit >= 40

    if high_margin and high_retainer and low_risk and not heavy_effort:
        return StreamDecision(
            stream_key=card.stream_key,
            action="scale",
            reason_ar="هامش مرتفع وإمكان تحويله إلى retainer مع مخاطر منخفضة",
            reason_en="High margin and retainer potential with low risk",
        )

    if card.margin_pct < 0.20 and heavy_effort:
        return StreamDecision(
            stream_key=card.stream_key,
            action="kill",
            reason_ar="هامش منخفض جدًا مقابل جهد تسليم ثقيل",
            reason_en="Margin too low for the delivery burden",
        )

    if card.margin_pct < 0.30 and not heavy_effort:
        return StreamDecision(
            stream_key=card.stream_key,
            action="reprice",
            reason_ar="هامش ضعيف يستوجب إعادة تسعير",
            reason_en="Weak margin warrants a reprice",
        )

    if card.risk == "high":
        return StreamDecision(
            stream_key=card.stream_key,
            action="pause",
            reason_ar="مخاطر عالية تستوجب التوقف للمراجعة",
            reason_en="High risk warrants a pause for review",
        )

    if card.bucket == "partner" and high_retainer:
        return StreamDecision(
            stream_key=card.stream_key,
            action="partner_led",
            reason_ar="مسار شركاء بإمكان retainer مرتفع",
            reason_en="Partner-led with high retainer potential",
        )

    if healthy_margin and not high_retainer:
        return StreamDecision(
            stream_key=card.stream_key,
            action="bundle",
            reason_ar="هامش معقول لكن يحتاج تحزيمًا لرفع التكرار",
            reason_en="Healthy margin but needs bundling to lift repeat",
        )

    return StreamDecision(
        stream_key=card.stream_key,
        action="optimize",
        reason_ar="تحتاج تحسينات تشغيلية قبل توسيع النطاق",
        reason_en="Needs operational tuning before scaling",
    )


__all__ = ["Action", "StreamDecision", "decide_stream_action"]
