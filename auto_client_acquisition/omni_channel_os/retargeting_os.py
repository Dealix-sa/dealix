"""Retargeting OS — generates follow-up sequences for website visitors and ad clickers."""
from __future__ import annotations

import logging
from typing import Any

from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    ChannelAsset,
    ChannelType,
    Language,
    RiskLevel,
)

log = logging.getLogger(__name__)
_NO_AUTO_SEND = True

RETARGETING_AD_COPIES: dict[str, list[str]] = {
    "website_visitor_ar": [
        (
            "لا تزال تستكشف AI لعملياتكم?\n"
            "ابدأ بـ workflow واحد، بيانات تجريبية، وموافقة بشرية.\n"
            "تشخيص مجاني — 7 أيام."
        ),
        (
            "رأيت موقع Dealix?\n"
            "AI Workflow Audit مجاني لشركتك — لا مخاطرة على البيانات."
        ),
    ],
    "website_visitor_en": [
        (
            "Still exploring AI for operations?\n"
            "Start with one workflow, sample data, and human approval gates."
        ),
        "Visited Dealix? Get your free 7-day AI Workflow Audit.",
    ],
    "one_pager_opener_ar": [
        "فتحت الـ one-pager؟ يسعدنا نشرح التفاصيل الخاصة بقطاعكم.",
    ],
    "one_pager_opener_en": [
        "You opened our one-pager. Happy to walk you through how it applies to your sector.",
    ],
}

_PLACEHOLDER_COMPANY_ID = "retargeting_visitor"


class RetargetingOS:
    """Generates retargeting sequences for website visitors and one-pager openers."""

    _NO_AUTO_SEND = True

    def website_visitor_sequence(
        self,
        visitor_sector: str | None,
        language: str = "ar",
    ) -> list[ChannelAsset]:
        """Return a 3-touch retargeting sequence for website visitors."""
        lang = Language.arabic if language in ("ar", "arabic") else Language.english
        sector_label = visitor_sector or ("قطاعكم" if lang == Language.arabic else "your sector")

        if lang == Language.arabic:
            touches = [
                {
                    "body": (
                        f"لا تزال تستكشف AI لعمليات {sector_label}?\n"
                        "ابدأ بـ workflow واحد، بيانات تجريبية، وموافقة بشرية.\n"
                        "تشخيص مجاني — 7 أيام."
                    ),
                    "cta": "ابدأ التشخيص المجاني",
                },
                {
                    "body": (
                        f"AI Workflow Audit مجاني لشركتك في {sector_label}.\n"
                        "لا مخاطرة على البيانات — نبدأ ببيانات تجريبية فقط.\n"
                        "حجز المكان محدود."
                    ),
                    "cta": "احجز مكانك",
                },
                {
                    "body": (
                        f"هل عندكم مسار متكرر في {sector_label} يأخذ وقتاً كبيراً؟\n"
                        "Dealix يحوله إلى workflow ذكي في أسبوع واحد.\n"
                        "تواصل معنا قبل نهاية الأسبوع."
                    ),
                    "cta": "تواصل الآن",
                },
            ]
        else:
            touches = [
                {
                    "body": (
                        f"Still exploring AI for {sector_label} operations?\n"
                        "Start with one workflow, sample data, and human approval gates."
                    ),
                    "cta": "Start your free diagnostic",
                },
                {
                    "body": (
                        f"Free AI Workflow Audit for your {sector_label} company.\n"
                        "No data risk — we use sample data only.\n"
                        "Limited spots available."
                    ),
                    "cta": "Reserve your spot",
                },
                {
                    "body": (
                        f"Have a repetitive process in {sector_label} that eats up time?\n"
                        "Dealix turns it into a smart workflow in one week."
                    ),
                    "cta": "Connect now",
                },
            ]

        assets: list[ChannelAsset] = []
        for i, touch in enumerate(touches, start=1):
            assets.append(
                ChannelAsset(
                    company_id=_PLACEHOLDER_COMPANY_ID,
                    asset_type=AssetType.lead_ad_followup,
                    channel=ChannelType.retargeting,
                    language=lang,
                    subject_or_hook=f"Retargeting touch {i}",
                    body=touch["body"],
                    cta=touch["cta"],
                    is_auto_sendable=False,
                    requires_founder_approval=True,
                    risk_level=RiskLevel.low,
                    approval_status="approval_required",
                    sector=visitor_sector or "",
                    country="KSA",
                )
            )
        return assets

    def one_pager_opener_sequence(
        self,
        sector: str,
        language: str = "ar",
    ) -> list[ChannelAsset]:
        """Return a follow-up sequence for one-pager openers."""
        lang = Language.arabic if language in ("ar", "arabic") else Language.english

        if lang == Language.arabic:
            touches = [
                {
                    "body": f"فتحت الـ one-pager؟ يسعدنا نشرح التفاصيل الخاصة بقطاع {sector}.",
                    "cta": "احصل على التفاصيل",
                },
                {
                    "body": (
                        f"في {sector}، تطبيق AI Workflow يبدأ بخطوة واحدة.\n"
                        "تواصل معنا لنحدد workflow مناسب لبدء التجربة."
                    ),
                    "cta": "تحديد موعد",
                },
            ]
        else:
            touches = [
                {
                    "body": f"You opened our one-pager. Happy to walk you through how it applies to {sector}.",
                    "cta": "Get the details",
                },
                {
                    "body": (
                        f"In {sector}, AI workflow implementation starts with one step.\n"
                        "Let's identify the right workflow for a pilot."
                    ),
                    "cta": "Schedule a call",
                },
            ]

        assets: list[ChannelAsset] = []
        for i, touch in enumerate(touches, start=1):
            assets.append(
                ChannelAsset(
                    company_id=_PLACEHOLDER_COMPANY_ID,
                    asset_type=AssetType.lead_ad_followup,
                    channel=ChannelType.retargeting,
                    language=lang,
                    subject_or_hook=f"One-pager follow-up {i} — {sector}",
                    body=touch["body"],
                    cta=touch["cta"],
                    is_auto_sendable=False,
                    requires_founder_approval=True,
                    risk_level=RiskLevel.low,
                    approval_status="approval_required",
                    sector=sector,
                    country="KSA",
                )
            )
        return assets

    def ad_copy_set(
        self,
        source: str,
        sector: str | None,
        language: str = "ar",
    ) -> list[str]:
        """Return ad copy variants for a retargeting campaign."""
        lang_suffix = "ar" if language in ("ar", "arabic") else "en"
        key = f"{source}_{lang_suffix}"

        copies = RETARGETING_AD_COPIES.get(key, [])
        if not copies:
            key_generic = f"website_visitor_{lang_suffix}"
            copies = RETARGETING_AD_COPIES.get(key_generic, [])

        if sector:
            # Personalize copy with sector where possible
            return [
                c.replace("قطاعكم", sector).replace("your sector", sector)
                for c in copies
            ]
        return list(copies)

    def pixel_event_handler(self, event: str, visitor_data: dict) -> dict[str, Any]:
        """Process a pixel event and return the recommended retargeting action."""
        sector = visitor_data.get("sector") or visitor_data.get("inferred_sector")
        language = visitor_data.get("language") or "ar"

        if event in ("Lead", "CompleteRegistration"):
            action = "add_to_high_intent_audience"
            priority = "high"
        elif event in ("InitiateCheckout", "ViewContent"):
            action = "add_to_mid_intent_audience"
            priority = "medium"
        elif event == "PageView":
            action = "add_to_awareness_audience"
            priority = "low"
        else:
            action = "no_action"
            priority = "none"

        return {
            "event": event,
            "action": action,
            "priority": priority,
            "sector": sector,
            "language": language,
            "recommended_sequence": (
                "website_visitor" if action != "no_action" else None
            ),
        }


__all__ = ["RETARGETING_AD_COPIES", "RetargetingOS"]
