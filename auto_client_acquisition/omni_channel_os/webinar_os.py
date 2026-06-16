"""Webinar OS — registration, reminders, and follow-up sequences. Mostly automatable."""
from __future__ import annotations

import logging

from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    ChannelAsset,
    ChannelType,
    Language,
    RiskLevel,
)

log = logging.getLogger(__name__)

_NO_AUTO_SEND = False  # webinar flows are automatable (invited list)

WEBINAR_TOPICS: dict[str, dict[str, object]] = {
    "legal": {
        "title_ar": "كيف تستفيد مكاتب المحاماة من AI بدون المساس بسرية العميل؟",
        "title_en": "AI for Legal Document Workflows Without Risking Client Confidentiality",
        "duration_min": 45,
    },
    "facilities_management": {
        "title_ar": "AI لتقارير SLA وجدولة الفنيين — بدون spreadsheets",
        "title_en": "AI for Maintenance SLA and Technician Reports — No More Spreadsheets",
        "duration_min": 45,
    },
    "consulting": {
        "title_ar": "كيف تؤتمت شركات الاستشارات المقترحات والتقارير بدون إضافة موارد؟",
        "title_en": "How Consulting Firms Can Automate Proposals and Reports Without Adding Headcount",
        "duration_min": 45,
    },
    "real_estate": {
        "title_ar": "أتمتة متابعة العملاء المحتملين في العقارات — من أول تواصل حتى الإغلاق",
        "title_en": "Automating Real Estate Lead Nurture — From First Contact to Closing",
        "duration_min": 45,
    },
    "healthcare": {
        "title_ar": "AI للإدارة الصحية: جدولة وفواتير وامتثال بدون مخاطر بيانات",
        "title_en": "AI for Healthcare Admin: Scheduling, Billing, and Compliance Without Data Risk",
        "duration_min": 45,
    },
    "executive": {
        "title_ar": "من chatbot إلى Agentic Workflow — كيف تبدأ خلال 7 أيام؟",
        "title_en": "From Chatbot to Agentic Workflow — How to Start in 7 Days",
        "duration_min": 60,
    },
    "general": {
        "title_ar": "AI Workflow Audit خلال 7 أيام بدون مخاطرة على البيانات",
        "title_en": "7-Day AI Workflow Audit Without Data Risk",
        "duration_min": 45,
    },
}


def _get_topic(sector: str) -> dict[str, object]:
    return WEBINAR_TOPICS.get(sector, WEBINAR_TOPICS["general"])


class WebinarOS:
    """Generates webinar invitation, confirmation, reminder, and follow-up assets."""

    def invitation_message(
        self,
        sector: str,
        company: str,
        name: str,
        language: Language,
    ) -> ChannelAsset:
        """Draft webinar invitation for a specific sector and company."""
        topic = _get_topic(sector)
        if language == Language.arabic:
            title = topic["title_ar"]
            body = (
                f"السلام عليكم {name}،\n"
                f"يسعدني دعوتكم لحضور webinar مجاني خاص لشركات مثل {company}:\n\n"
                f"الموضوع: {title}\n"
                f"المدة: {topic['duration_min']} دقيقة\n"
                f"التاريخ والوقت: [DATE_TIME]\n"
                "رابط التسجيل: [REGISTRATION_LINK]\n\n"
                "الـ webinar يغطي تطبيقات عملية مع أمثلة من السوق الخليجي.\n"
                "لا يتطلب خلفية تقنية."
            )
            cta = "التسجيل في الـ webinar"
            hook = f"دعوة webinar — {title}"
        else:
            title = topic["title_en"]
            body = (
                f"Hi {name},\n"
                f"I would like to invite you to a free webinar for companies like {company}:\n\n"
                f"Topic: {title}\n"
                f"Duration: {topic['duration_min']} minutes\n"
                "Date and Time: [DATE_TIME]\n"
                "Registration link: [REGISTRATION_LINK]\n\n"
                "The webinar covers practical applications with examples from the GCC market.\n"
                "No technical background required."
            )
            cta = "Register for the webinar"
            hook = f"Webinar invitation — {title}"

        log.debug("webinar_os.invitation sector=%s lang=%s", sector, language.value)

        return self._make_asset(
            company_id=company,
            asset_type=AssetType.webinar_invite,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
            is_auto_sendable=False,
        )

    def registration_confirmation(
        self,
        webinar_title: str,
        date_time: str,
        language: Language,
    ) -> ChannelAsset:
        """Registration confirmation message."""
        if language == Language.arabic:
            body = (
                "تم تسجيلكم بنجاح.\n\n"
                f"الموضوع: {webinar_title}\n"
                f"التاريخ والوقت: {date_time}\n"
                "رابط الانضمام: [JOIN_LINK]\n\n"
                "ستصلكم تذكيرات قبل 24 ساعة وساعة واحدة من بدء الـ webinar."
            )
            cta = "أضف للتقويم"
            hook = f"تأكيد التسجيل — {webinar_title}"
        else:
            body = (
                "Your registration is confirmed.\n\n"
                f"Topic: {webinar_title}\n"
                f"Date and Time: {date_time}\n"
                "Join link: [JOIN_LINK]\n\n"
                "You will receive reminders 24 hours and 1 hour before the webinar starts."
            )
            cta = "Add to calendar"
            hook = f"Registration confirmed — {webinar_title}"

        return self._make_asset(
            company_id="generic",
            asset_type=AssetType.webinar_invite,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
            is_auto_sendable=True,
        )

    def reminder_24h(
        self,
        webinar_title: str,
        join_link: str,
        language: Language,
    ) -> ChannelAsset:
        """24-hour reminder before webinar."""
        if language == Language.arabic:
            body = (
                f"تذكير: الـ webinar غداً.\n\n"
                f"الموضوع: {webinar_title}\n"
                f"رابط الانضمام: {join_link}\n\n"
                "نتطلع لرؤيتكم."
            )
            cta = "حفظ الرابط"
            hook = f"تذكير 24 ساعة — {webinar_title}"
        else:
            body = (
                f"Reminder: the webinar is tomorrow.\n\n"
                f"Topic: {webinar_title}\n"
                f"Join link: {join_link}\n\n"
                "Looking forward to seeing you."
            )
            cta = "Save the link"
            hook = f"24h reminder — {webinar_title}"

        return self._make_asset(
            company_id="generic",
            asset_type=AssetType.webinar_invite,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
            is_auto_sendable=True,
        )

    def reminder_1h(
        self,
        webinar_title: str,
        join_link: str,
        language: Language,
    ) -> ChannelAsset:
        """1-hour reminder before webinar."""
        if language == Language.arabic:
            body = (
                f"الـ webinar يبدأ خلال ساعة واحدة.\n\n"
                f"الموضوع: {webinar_title}\n"
                f"رابط الانضمام: {join_link}\n\n"
                "انضموا قبل 5 دقائق للتأكد من عمل الصوت والصورة."
            )
            cta = "الانضمام الآن"
            hook = f"تذكير ساعة واحدة — {webinar_title}"
        else:
            body = (
                f"The webinar starts in one hour.\n\n"
                f"Topic: {webinar_title}\n"
                f"Join link: {join_link}\n\n"
                "Please join 5 minutes early to ensure audio and video are working."
            )
            cta = "Join now"
            hook = f"1h reminder — {webinar_title}"

        return self._make_asset(
            company_id="generic",
            asset_type=AssetType.webinar_invite,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
            is_auto_sendable=True,
        )

    def post_webinar_followup(
        self,
        sector: str,
        language: Language,
    ) -> ChannelAsset:
        """Post-webinar follow-up with recording and next step."""
        topic = _get_topic(sector)
        if language == Language.arabic:
            title = topic["title_ar"]
            body = (
                f"شكراً لحضوركم الـ webinar: {title}\n\n"
                "رابط التسجيل: [RECORDING_LINK]\n"
                "المواد المشاركة: [MATERIALS_LINK]\n\n"
                "إذا أردتم تشخيصاً مجانياً على مسار في شركتكم — يسعدني الترتيب.\n"
                "رابط الحجز: [BOOKING_LINK]"
            )
            cta = "حجز تشخيص مجاني"
            hook = f"متابعة ما بعد الـ webinar — {title}"
        else:
            title = topic["title_en"]
            body = (
                f"Thank you for attending the webinar: {title}\n\n"
                "Recording link: [RECORDING_LINK]\n"
                "Shared materials: [MATERIALS_LINK]\n\n"
                "If you would like a free diagnostic on one workflow at your company — happy to arrange it.\n"
                "Booking link: [BOOKING_LINK]"
            )
            cta = "Book free diagnostic"
            hook = f"Post-webinar follow-up — {title}"

        return self._make_asset(
            company_id="generic",
            asset_type=AssetType.lead_ad_followup,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
            is_auto_sendable=True,
        )

    def audit_offer_message(self, language: Language) -> ChannelAsset:
        """CTA message offering the free AI Workflow Audit."""
        if language == Language.arabic:
            body = (
                "بناءً على ما ناقشناه في الـ webinar، ندعوكم للاستفادة من:\n\n"
                "AI Workflow Audit مجاني\n"
                "• 7 أيام تشخيص على مسار واحد في شركتكم\n"
                "• تقرير يحدد أين يُطبَّق AI بشكل آمن وعملي\n"
                "• بدون مخاطرة على البيانات\n"
                "• بدون التزام مسبق\n\n"
                "الأماكن محدودة هذا الشهر.\n"
                "رابط الحجز: [BOOKING_LINK]"
            )
            cta = "احجز Audit مجاني"
            hook = "عرض AI Workflow Audit المجاني"
        else:
            body = (
                "Based on what we discussed in the webinar, we invite you to benefit from:\n\n"
                "Free AI Workflow Audit\n"
                "• 7-day diagnostic on one process at your company\n"
                "• Report identifying where AI can be applied safely and practically\n"
                "• No data risk\n"
                "• No prior commitment\n\n"
                "Spots are limited this month.\n"
                "Booking link: [BOOKING_LINK]"
            )
            cta = "Book free audit"
            hook = "Free AI Workflow Audit offer"

        return self._make_asset(
            company_id="generic",
            asset_type=AssetType.webinar_invite,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
            is_auto_sendable=False,
        )

    def _make_asset(
        self,
        company_id: str,
        asset_type: AssetType,
        language: Language,
        subject_or_hook: str,
        body: str,
        cta: str,
        is_auto_sendable: bool = False,
    ) -> ChannelAsset:
        return ChannelAsset(
            company_id=company_id,
            asset_type=asset_type,
            channel=ChannelType.webinar,
            language=language,
            subject_or_hook=subject_or_hook,
            body=body,
            cta=cta,
            is_auto_sendable=is_auto_sendable,
            requires_founder_approval=not is_auto_sendable,
            risk_level=RiskLevel.low,
            approval_status="approval_required",
            sector="",
            country="",
        )


__all__ = ["WEBINAR_TOPICS", "WebinarOS"]
