"""WhatsApp OS — opt-in reply flows and qualification sequences. OPT-IN REQUIRED."""
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

_NO_AUTO_SEND = False  # inbound opt-in flows can be auto-sent
_OPT_IN_REQUIRED = True  # NEVER cold WhatsApp blast

_WORKFLOW_TYPES = {
    "1": {"ar": "تقارير ومتابعة داخلية", "en": "Internal reporting and follow-up"},
    "2": {"ar": "صيانة/بلاغات/SLA", "en": "Maintenance / tickets / SLA"},
    "3": {"ar": "مستندات ومعرفة داخلية", "en": "Documents and internal knowledge"},
    "4": {"ar": "مبيعات ومتابعة عملاء", "en": "Sales and client follow-up"},
    "5": {"ar": "خدمة عملاء", "en": "Customer service"},
    "6": {"ar": "غير ذلك", "en": "Other"},
}

_OFFER_ROUTES: dict[str, dict[str, str]] = {
    "1": {
        "ar": "ممتاز — تقارير المتابعة الداخلية من أكثر المجالات التي يُطبَّق فيها AI بشكل فوري.",
        "en": "Great — internal reporting and follow-up is one of the fastest areas to apply AI.",
    },
    "2": {
        "ar": "ممتاز — workflows الصيانة والـ SLA قابلة للأتمتة بشكل كبير مع موافقة بشرية.",
        "en": "Great — maintenance and SLA workflows can be highly automated with human approval.",
    },
    "3": {
        "ar": "ممتاز — بناء قاعدة معرفية ذكية يوفر وقتاً كبيراً على الفريق.",
        "en": "Great — building an intelligent knowledge base saves significant team time.",
    },
    "4": {
        "ar": "ممتاز — أتمتة متابعة العملاء من أعلى الفرص في Dealix.",
        "en": "Great — automating client follow-up is one of the top opportunities we work on.",
    },
    "5": {
        "ar": "ممتاز — خدمة العملاء الآلية مع تصعيد بشري تحل مشكلة وقت الاستجابة.",
        "en": "Great — automated customer service with human escalation solves response time issues.",
    },
    "6": {
        "ar": "شكراً، سأرسل لكم نبذة عامة عن كيف يعمل Dealix وتحددون أين تروا الفائدة.",
        "en": "Thank you — I will send a general overview of how Dealix works and you can identify where you see value.",
    },
}


class WhatsAppOS:
    """Generates WhatsApp opt-in reply flows. Cold outreach is never permitted."""

    _OPT_IN_REQUIRED = True

    def welcome_message(self, lead: dict, language: Language) -> ChannelAsset:
        """Post-opt-in welcome message."""
        name = lead.get("name", "[Name]")
        if language == Language.arabic:
            body = (
                f"السلام عليكم {name}، معك Sami من Dealix.\n"
                "وصلنا اهتمامكم بـ AI Workflow Audit.\n"
                "حتى أرسل أفضل نبذة لكم، أي مسار أقرب لاحتياجكم؟\n"
                "1 - تقارير ومتابعة داخلية\n"
                "2 - صيانة/بلاغات/SLA\n"
                "3 - مستندات ومعرفة داخلية\n"
                "4 - مبيعات ومتابعة عملاء\n"
                "5 - خدمة عملاء\n"
                "6 - غير ذلك"
            )
            cta = "اختر رقم المسار"
        else:
            body = (
                f"Hi {name}, this is Sami from Dealix.\n"
                "We received your interest in an AI Workflow Audit.\n"
                "To send the most relevant overview, which process is closest to your need?\n"
                "1 - Internal reporting and follow-up\n"
                "2 - Maintenance / tickets / SLA\n"
                "3 - Documents and internal knowledge\n"
                "4 - Sales and client follow-up\n"
                "5 - Customer service\n"
                "6 - Other"
            )
            cta = "Reply with a number"
        return self._make_asset(
            company_id=lead.get("company_id", "unknown"),
            asset_type=AssetType.whatsapp_optin_reply,
            language=language,
            subject_or_hook="Welcome / qualification entry",
            body=body,
            cta=cta,
            is_auto_sendable=True,
        )

    def qualification_questions(self, language: Language) -> ChannelAsset:
        """Menu-based qualification: 5 workflow type options."""
        if language == Language.arabic:
            body = (
                "حتى نحدد أفضل حل لكم، أخبرونا:\n"
                "1 - تقارير ومتابعة داخلية\n"
                "2 - صيانة/بلاغات/SLA\n"
                "3 - مستندات ومعرفة داخلية\n"
                "4 - مبيعات ومتابعة عملاء\n"
                "5 - خدمة عملاء\n"
                "6 - غير ذلك\n"
                "أرسل رقم الخيار المناسب."
            )
            cta = "أرسل رقم الخيار"
        else:
            body = (
                "To identify the best solution for you, please tell us:\n"
                "1 - Internal reporting and follow-up\n"
                "2 - Maintenance / tickets / SLA\n"
                "3 - Documents and internal knowledge\n"
                "4 - Sales and client follow-up\n"
                "5 - Customer service\n"
                "6 - Other\n"
                "Reply with the option number."
            )
            cta = "Reply with option number"
        return self._make_asset(
            company_id="generic",
            asset_type=AssetType.whatsapp_qualification,
            language=language,
            subject_or_hook="Qualification menu",
            body=body,
            cta=cta,
            is_auto_sendable=True,
        )

    def offer_router_message(self, workflow_type: str, language: Language) -> ChannelAsset:
        """Routes to correct offer based on workflow type selection."""
        route = _OFFER_ROUTES.get(workflow_type, _OFFER_ROUTES["6"])
        key = "ar" if language == Language.arabic else "en"
        body_intro = route[key]
        if language == Language.arabic:
            body = (
                f"{body_intro}\n\n"
                "سأرسل لكم الآن نبذة مختصرة عن كيفية تطبيق Dealix على هذا المسار تحديداً."
            )
            cta = "إرسال النبذة"
        else:
            body = (
                f"{body_intro}\n\n"
                "I will now send you a brief overview of how Dealix applies to this specific workflow."
            )
            cta = "Send overview"
        return self._make_asset(
            company_id="generic",
            asset_type=AssetType.whatsapp_optin_reply,
            language=language,
            subject_or_hook=f"Offer router — workflow type {workflow_type}",
            body=body,
            cta=cta,
            is_auto_sendable=True,
        )

    def booking_link_message(self, offer: str, language: Language) -> ChannelAsset:
        """Sends booking link with context."""
        if language == Language.arabic:
            body = (
                f"بناءً على اهتمامكم بـ {offer}، إليكم رابط لحجز جلسة تشخيص مجانية مدتها 20 دقيقة:\n"
                "[BOOKING_LINK]\n\n"
                "الجلسة على مسار واحد تختارونه — بدون التزام مسبق."
            )
            cta = "احجز موعد"
        else:
            body = (
                f"Based on your interest in {offer}, here is a link to book a free 20-minute diagnostic session:\n"
                "[BOOKING_LINK]\n\n"
                "The session covers one workflow of your choice — no commitment required."
            )
            cta = "Book a session"
        return self._make_asset(
            company_id="generic",
            asset_type=AssetType.whatsapp_optin_reply,
            language=language,
            subject_or_hook="Booking link delivery",
            body=body,
            cta=cta,
            is_auto_sendable=True,
        )

    def one_pager_delivery(self, sector: str, language: Language) -> ChannelAsset:
        """Delivers relevant one-pager link."""
        if language == Language.arabic:
            body = (
                f"هذه نبذة مختصرة عن كيفية تطبيق Dealix في مجال {sector}:\n"
                "[ONE_PAGER_LINK]\n\n"
                "إذا كان فيها شيء يناسبكم — أخبروني وأرتب جلسة توضيحية بدون التزام."
            )
            cta = "مراجعة النبذة"
        else:
            body = (
                f"Here is a brief overview of how Dealix applies in the {sector} space:\n"
                "[ONE_PAGER_LINK]\n\n"
                "If anything resonates, let me know and I will arrange a no-commitment demo."
            )
            cta = "Review overview"
        return self._make_asset(
            company_id="generic",
            asset_type=AssetType.whatsapp_optin_reply,
            language=language,
            subject_or_hook=f"One-pager delivery — {sector}",
            body=body,
            cta=cta,
            is_auto_sendable=True,
        )

    def reminder_message(self, language: Language) -> ChannelAsset:
        """24h reminder before booked call."""
        if language == Language.arabic:
            body = (
                "تذكير: موعدكم مع Sami من Dealix غداً.\n"
                "الوقت: [TIME]\n"
                "الرابط: [CALL_LINK]\n\n"
                "إذا احتجتم تعديل الموعد أرسلوا لي وأرتب بدل."
            )
            cta = "تأكيد الحضور"
        else:
            body = (
                "Reminder: your call with Sami from Dealix is tomorrow.\n"
                "Time: [TIME]\n"
                "Link: [CALL_LINK]\n\n"
                "If you need to reschedule, just let me know."
            )
            cta = "Confirm attendance"
        return self._make_asset(
            company_id="generic",
            asset_type=AssetType.whatsapp_optin_reply,
            language=language,
            subject_or_hook="24h reminder before call",
            body=body,
            cta=cta,
            is_auto_sendable=True,
        )

    def post_call_followup(self, language: Language) -> ChannelAsset:
        """Post-call follow-up with proposal or next step."""
        if language == Language.arabic:
            body = (
                "شكراً لوقتكم اليوم — كان نقاشاً مثمراً.\n\n"
                "كما ذكرنا، الخطوة التالية:\n"
                "[NEXT_STEP]\n\n"
                "سأرسل لكم [DOCUMENT_OR_PROPOSAL] خلال [TIMEFRAME].\n"
                "أي أسئلة — أنا متاح."
            )
            cta = "تأكيد الخطوات التالية"
        else:
            body = (
                "Thank you for your time today — it was a productive discussion.\n\n"
                "As discussed, the next step:\n"
                "[NEXT_STEP]\n\n"
                "I will send you [DOCUMENT_OR_PROPOSAL] within [TIMEFRAME].\n"
                "Any questions — I am available."
            )
            cta = "Confirm next steps"
        return self._make_asset(
            company_id="generic",
            asset_type=AssetType.whatsapp_optin_reply,
            language=language,
            subject_or_hook="Post-call follow-up",
            body=body,
            cta=cta,
            is_auto_sendable=False,  # needs personalization before sending
        )

    def _make_asset(
        self,
        company_id: str,
        asset_type: AssetType,
        language: Language,
        subject_or_hook: str,
        body: str,
        cta: str,
        is_auto_sendable: bool = True,
    ) -> ChannelAsset:
        assert _OPT_IN_REQUIRED, "_OPT_IN_REQUIRED gate violated"
        return ChannelAsset(
            company_id=company_id,
            asset_type=asset_type,
            channel=ChannelType.whatsapp_optin,
            language=language,
            subject_or_hook=subject_or_hook,
            body=body,
            cta=cta,
            is_auto_sendable=is_auto_sendable,
            requires_founder_approval=False,
            risk_level=RiskLevel.low,
            approval_status="approval_required",
            sector="",
            country="",
        )


__all__ = ["WhatsAppOS"]
