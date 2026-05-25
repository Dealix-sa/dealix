"""Content-to-Cash map — every content type has a CTA and a paid offer."""

from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from dealix.growth_os.content_engine.content_types import ContentType


class CTAMapping(BaseModel):
    model_config = ConfigDict(extra="forbid")

    content_type: ContentType
    cta_label_ar: str
    cta_label_en: str
    cta_path: str = Field(..., min_length=1)
    offer_key: str = Field(..., min_length=1)
    offer_label_ar: str
    offer_label_en: str


CONTENT_TO_CASH: Final[dict[ContentType, CTAMapping]] = {
    "trust": CTAMapping(
        content_type="trust",
        cta_label_ar="اطلب AI Trust Kit",
        cta_label_en="Request the AI Trust Kit",
        cta_path="/offers/ai-trust-kit",
        offer_key="ai_trust_kit",
        offer_label_ar="حزمة الثقة في AI",
        offer_label_en="AI Trust Kit",
    ),
    "revenue": CTAMapping(
        content_type="revenue",
        cta_label_ar="احجز Revenue Diagnostic",
        cta_label_en="Book a Revenue Diagnostic",
        cta_path="/offers/revenue-hunter",
        offer_key="revenue_hunter",
        offer_label_ar="صياد الإيراد",
        offer_label_en="Revenue Hunter",
    ),
    "partner": CTAMapping(
        content_type="partner",
        cta_label_ar="انضم لبرنامج الوكالات",
        cta_label_en="Join the Agency Program",
        cta_path="/partners/agency-program",
        offer_key="agency_white_label",
        offer_label_ar="منصة بعلامة الوكالة",
        offer_label_en="Agency White-label",
    ),
    "executive": CTAMapping(
        content_type="executive",
        cta_label_ar="اطلب جلسة تنفيذية",
        cta_label_en="Request an Executive Briefing",
        cta_path="/offers/executive-briefing",
        offer_key="executive_briefing",
        offer_label_ar="إحاطة تنفيذية",
        offer_label_en="Executive Briefing",
    ),
    "market_radar": CTAMapping(
        content_type="market_radar",
        cta_label_ar="اشترك في Market Radar",
        cta_label_en="Subscribe to Market Radar",
        cta_path="/offers/market-radar",
        offer_key="market_radar_subscription",
        offer_label_ar="اشتراك رادار السوق",
        offer_label_en="Market Radar Subscription",
    ),
}


def cta_for(content_type: ContentType) -> CTAMapping:
    return CONTENT_TO_CASH[content_type]


def list_cta_mappings() -> list[CTAMapping]:
    return list(CONTENT_TO_CASH.values())


__all__ = ["CONTENT_TO_CASH", "CTAMapping", "cta_for", "list_cta_mappings"]
