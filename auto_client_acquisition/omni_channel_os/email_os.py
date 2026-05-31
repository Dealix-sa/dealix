"""Email OS — bilingual sector-specific email draft generator. DRAFT_ONLY, no auto-send."""
from __future__ import annotations

import logging
from dataclasses import dataclass

from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    BuyerPersona,
    ChannelAsset,
    ChannelType,
    Company,
    Language,
    RiskLevel,
    Sector,
)

log = logging.getLogger(__name__)

_NO_AUTO_SEND = True

# ---------------------------------------------------------------------------
# Subject line templates per sector
# ---------------------------------------------------------------------------

SUBJECT_LINES: dict[str, dict[str, str]] = {
    "legal": {
        "ar": "سؤال سريع عن workflows مكتب [Company]",
        "en": "Quick question about [Company]'s document workflows",
    },
    "facilities_management": {
        "ar": "كيف تقلل تقارير SLA اليدوية في [Company]؟",
        "en": "Reducing manual SLA reports at [Company]",
    },
    "consulting": {
        "ar": "أتمتة المقترحات والمتابعة في [Company]",
        "en": "Automating proposals and follow-up at [Company]",
    },
    "real_estate": {
        "ar": "متابعة العملاء المحتملين بدون جهد يدوي — [Company]",
        "en": "Automated lead nurture for [Company]",
    },
    "healthcare": {
        "ar": "تقليل الأعباء الإدارية في [Company] بدون مخاطر امتثال",
        "en": "Reducing admin burden at [Company] without compliance risk",
    },
    "education_training": {
        "ar": "أتمتة التسجيل والشهادات في [Company]",
        "en": "Automating enrollment and certificates at [Company]",
    },
    "international_company": {
        "ar": "دخول السوق السعودي بسرعة — [Company]",
        "en": "GCC market entry support for [Company]",
    },
    "local_sme": {
        "ar": "تنظيم عمليات [Company] بدون موارد إضافية",
        "en": "Streamlining [Company] operations without extra headcount",
    },
    "government_adjacent": {
        "ar": "أتمتة توثيق المناقصات في [Company]",
        "en": "Tender documentation automation for [Company]",
    },
    "default": {
        "ar": "سؤال سريع عن عمليات [Company]",
        "en": "Quick question about [Company]'s operations",
    },
}

# ---------------------------------------------------------------------------
# Email body templates per sector
# ---------------------------------------------------------------------------

EMAIL_BODIES: dict[str, dict[str, str]] = {
    "legal": {
        "ar": (
            "السلام عليكم أستاذ/ة [Name]،\n"
            "لاحظت أن [Company] تعمل في مجال القانون وغالباً يكون لديكم مستندات ومراسلات كثيرة تحتاج مراجعة وتنظيم.\n"
            "نبني في Dealix أنظمة AI Workflow مصممة لمكاتب المحاماة تساعد على:\n"
            "• تنظيم ملفات القضايا وسهولة البحث\n"
            "• تتبع المراسلات مع العملاء تلقائياً\n"
            "• إعداد تقارير مرحلية بدون وقت إضافي\n"
            "النظام يعمل مع موافقة بشرية كاملة ولا يشارك أي بيانات خارج بيئتكم.\n"
            "حابب أرسل لكم نبذة مختصرة عن كيفية تطبيقه على workflow واحد في مكتبكم؟\n\n"
            "مع التحية،\nSami | Dealix"
        ),
        "en": (
            "Dear [Name],\n"
            "I noticed that [Company] operates in the legal sector, and law firms often deal with high volumes of documents and correspondence requiring review and organization.\n"
            "At Dealix, we build AI workflow systems designed for law firms that help with:\n"
            "• Organizing case files for easy search and retrieval\n"
            "• Automatically tracking client correspondence\n"
            "• Generating progress reports without additional time investment\n"
            "The system operates with full human oversight and does not share any data outside your environment.\n"
            "I would be happy to send a brief overview of how this applies to one workflow at your firm.\n\n"
            "Best regards,\nSami | Dealix"
        ),
    },
    "facilities_management": {
        "ar": (
            "السلام عليكم،\n"
            "في [Company]، غالباً تكون هناك تقارير SLA وبلاغات صيانة تحتاج متابعة يدوية مستمرة.\n"
            "Dealix يساعد فرق FM على تحويل هذه العمليات إلى workflows ذكية:\n"
            "• استلام البلاغ → تصنيف تلقائي → تعيين الفني → تتبع الإنجاز → إرسال تقرير SLA\n"
            "• توليد تقارير KPI أسبوعية بدون لصق بيانات يدوي\n"
            "• تنبيهات تلقائية للمسؤولين عند تجاوز الـ SLA\n"
            "الآن نقدم AI Workflow Audit مجاني على مسار واحد لتحديد أين يمكن تطبيقه بشكل فوري.\n"
            "هل تناسبكم 20 دقيقة لنرى كيف يطبق على عملياتكم؟\n\n"
            "مع التحية،\nSami | Dealix"
        ),
        "en": (
            "Hi [Name],\n"
            "Facilities management teams at companies like [Company] typically deal with SLA reports and maintenance tickets that require continuous manual follow-up.\n"
            "Dealix helps FM teams turn these operations into intelligent workflows:\n"
            "• Ticket intake → auto-classification → technician assignment → completion tracking → SLA report\n"
            "• Weekly KPI reports without manual data entry\n"
            "• Automatic alerts to managers when SLA thresholds are breached\n"
            "We are currently offering a free AI Workflow Audit on one process to identify immediate automation opportunities.\n"
            "Would 20 minutes work to see how this applies to your operations?\n\n"
            "Best regards,\nSami | Dealix"
        ),
    },
    "consulting": {
        "ar": (
            "السلام عليكم [Name]،\n"
            "شركات الاستشارات مثل [Company] كثيراً ما تقضي وقتاً كبيراً في كتابة المقترحات، تتبع العملاء، وإعداد التقارير.\n"
            "Dealix يساعد فرق الاستشارات على:\n"
            "• أتمتة هياكل المقترحات بناءً على متطلبات العميل\n"
            "• تتبع مراحل المشاريع ومتابعة المهام تلقائياً\n"
            "• بناء قاعدة معرفية داخلية قابلة للبحث بدون وقت إضافي\n"
            "هل يناسبكم أرسل نبذة عن كيف يمكن تطبيق هذا على workflow واحد في شركتكم؟\n\n"
            "مع التحية،\nSami | Dealix"
        ),
        "en": (
            "Hi [Name],\n"
            "Consulting firms like [Company] often invest significant time in proposal writing, client tracking, and reporting.\n"
            "Dealix helps consulting teams with:\n"
            "• Automating proposal structures based on client requirements\n"
            "• Tracking project milestones and task follow-up automatically\n"
            "• Building a searchable internal knowledge base without added overhead\n"
            "Would it be useful if I sent a brief overview of how this applies to one workflow at your firm?\n\n"
            "Best regards,\nSami | Dealix"
        ),
    },
    "real_estate": {
        "ar": (
            "السلام عليكم [Name]،\n"
            "في قطاع العقارات، متابعة العملاء المحتملين وتنسيق الوسطاء يمكن أن يستهلك وقتاً كبيراً.\n"
            "Dealix يساعد شركات العقارات مثل [Company] على:\n"
            "• أتمتة متابعة العملاء المحتملين من أول تواصل حتى الإغلاق\n"
            "• تنسيق الوسطاء والتحديثات تلقائياً\n"
            "• توليد تقارير المبيعات بدون لصق بيانات يدوي\n"
            "هل أرسل لكم نبذة مختصرة عن كيفية تطبيق هذا على مسار المبيعات لديكم؟\n\n"
            "مع التحية،\nSami | Dealix"
        ),
        "en": (
            "Hi [Name],\n"
            "In real estate, following up with leads and coordinating brokers can consume significant time and effort.\n"
            "Dealix helps real estate companies like [Company] with:\n"
            "• Automating lead nurture from first contact through closing\n"
            "• Coordinating brokers and sending automatic updates\n"
            "• Generating sales reports without manual data entry\n"
            "Would it be helpful if I sent a brief overview of how this applies to your sales pipeline?\n\n"
            "Best regards,\nSami | Dealix"
        ),
    },
    "healthcare": {
        "ar": (
            "السلام عليكم [Name]،\n"
            "المنشآت الصحية مثل [Company] تواجه تحديات إدارية كثيرة: جدولة المواعيد، الفواتير، وتتبع الامتثال.\n"
            "Dealix يساعد فرق إدارة المستشفيات على:\n"
            "• أتمتة جدولة المرضى وتذكيرات المواعيد\n"
            "• تقليل أخطاء الفواتير عبر مسارات مراجعة آلية\n"
            "• إعداد تقارير الامتثال بدون جهد إضافي\n"
            "النظام يعمل بموافقة بشرية كاملة ولا تتم مشاركة بيانات المرضى.\n"
            "هل أرسل نبذة مختصرة عن التطبيق المناسب لمنشأتكم؟\n\n"
            "مع التحية،\nSami | Dealix"
        ),
        "en": (
            "Hi [Name],\n"
            "Healthcare facilities like [Company] face significant administrative challenges: appointment scheduling, billing, and compliance tracking.\n"
            "Dealix helps healthcare operations teams with:\n"
            "• Automating patient scheduling and appointment reminders\n"
            "• Reducing billing errors through automated review workflows\n"
            "• Generating compliance reports without manual effort\n"
            "The system operates with full human approval and no patient data is shared.\n"
            "Would it be useful if I sent a brief overview of what would fit your facility?\n\n"
            "Best regards,\nSami | Dealix"
        ),
    },
    "education_training": {
        "ar": (
            "السلام عليكم [Name]،\n"
            "مراكز التدريب مثل [Company] تقضي وقتاً في إدارة التسجيل، إصدار الشهادات، وتتبع المتعلمين.\n"
            "Dealix يساعد فرق التدريب على:\n"
            "• أتمتة تسجيل المشاركين وإرسال تأكيدات البرامج\n"
            "• إصدار الشهادات تلقائياً عند الانتهاء من البرامج\n"
            "• تتبع مشاركة المتعلمين وإرسال تذكيرات ذكية\n"
            "هل أرسل لكم نبذة مختصرة عن كيفية تطبيق هذا على برامجكم؟\n\n"
            "مع التحية،\nSami | Dealix"
        ),
        "en": (
            "Hi [Name],\n"
            "Training centers like [Company] spend considerable time managing enrollment, issuing certificates, and tracking learner progress.\n"
            "Dealix helps training teams with:\n"
            "• Automating participant enrollment and program confirmation messages\n"
            "• Issuing certificates automatically upon program completion\n"
            "• Tracking learner engagement and sending intelligent reminders\n"
            "Would it be useful if I sent a brief overview of how this applies to your programs?\n\n"
            "Best regards,\nSami | Dealix"
        ),
    },
    "international_company": {
        "ar": (
            "السلام عليكم [Name]،\n"
            "الشركات الدولية التي تدخل السوق السعودي تواجه تحديات في التوطين والامتثال المحلي.\n"
            "Dealix يساعد الشركات الدولية على:\n"
            "• دخول السوق السعودي بسرعة مع الامتثال المحلي\n"
            "• بناء محتوى عربي عالي الجودة للسوق المحلي\n"
            "• ربط العمليات الدولية مع متطلبات السوق المحلي\n"
            "هل أرسل لكم نبذة مختصرة عن كيف نساعد شركات مثل [Company]؟\n\n"
            "مع التحية،\nSami | Dealix"
        ),
        "en": (
            "Hi [Name],\n"
            "International companies entering the GCC market often face challenges around localization, compliance, and building local operations.\n"
            "Dealix supports international companies like [Company] with:\n"
            "• Accelerating GCC market entry with local compliance support\n"
            "• Arabic content and localization workflows\n"
            "• Connecting international processes with local market requirements\n"
            "Would it be useful if I sent a brief overview of how we support companies like yours?\n\n"
            "Best regards,\nSami | Dealix"
        ),
    },
    "local_sme": {
        "ar": (
            "السلام عليكم [Name]،\n"
            "الشركات الصغيرة والمتوسطة مثل [Company] كثيراً ما تعمل بموارد محدودة وتحتاج كل دقيقة.\n"
            "Dealix يساعد الشركات الصغيرة على:\n"
            "• أتمتة المتابعة مع العملاء بدون موارد إضافية\n"
            "• تنظيم العمليات اليومية في مسارات واضحة\n"
            "• تحويل الوقت الضائع في التقارير اليدوية إلى وقت للعمل الفعلي\n"
            "نبدأ بـ sprint واحد على مسار واحد — تشخيص مجاني لمدة 7 أيام.\n"
            "هل يناسبكم نتكلم 15 دقيقة؟\n\n"
            "مع التحية،\nSami | Dealix"
        ),
        "en": (
            "Hi [Name],\n"
            "Small and medium businesses like [Company] often operate with limited resources where every minute counts.\n"
            "Dealix helps SMEs with:\n"
            "• Automating client follow-up without additional headcount\n"
            "• Organizing daily operations into clear workflows\n"
            "• Converting time spent on manual reports into productive work time\n"
            "We start with one sprint on one workflow — a free 7-day diagnostic.\n"
            "Would 15 minutes work to discuss this?\n\n"
            "Best regards,\nSami | Dealix"
        ),
    },
    "government_adjacent": {
        "ar": (
            "السلام عليكم [Name]،\n"
            "الشركات التي تتعامل مع الجهات الحكومية مثل [Company] تعاني من تعقيدات توثيق المناقصات والامتثال.\n"
            "Dealix يساعد على:\n"
            "• أتمتة إعداد وثائق المناقصات وملفات ETIMAD\n"
            "• تتبع متطلبات الامتثال الحكومي تلقائياً\n"
            "• توليد التقارير الدورية للجهات المختصة بدون جهد يدوي\n"
            "هل أرسل لكم نبذة عن كيفية التطبيق على عملياتكم؟\n\n"
            "مع التحية،\nSami | Dealix"
        ),
        "en": (
            "Hi [Name],\n"
            "Companies working with government entities like [Company] often face complexity around tender documentation and compliance requirements.\n"
            "Dealix helps with:\n"
            "• Automating tender document preparation and ETIMAD file management\n"
            "• Automatically tracking government compliance requirements\n"
            "• Generating periodic reports for relevant authorities without manual effort\n"
            "Would it be useful if I sent an overview of how this applies to your operations?\n\n"
            "Best regards,\nSami | Dealix"
        ),
    },
}

EMAIL_BODIES["default"] = {
    "ar": (
        "السلام عليكم [Name]،\n"
        "نبني في Dealix أنظمة AI Workflow للشركات التي تريد تحويل عملياتها المتكررة إلى مسارات منظمة.\n"
        "نبدأ بتشخيص مجاني على مسار واحد في شركتكم لتحديد أين يمكن تطبيق AI بشكل آمن وعملي.\n"
        "هل أرسل لكم نبذة مختصرة عن كيفية عمل النظام؟\n\n"
        "مع التحية،\nSami | Dealix"
    ),
    "en": (
        "Hi [Name],\n"
        "At Dealix, we build AI workflow systems for companies that want to turn repetitive operations into structured, automated processes.\n"
        "We start with a free diagnostic on one workflow to identify where AI can be applied safely and practically.\n"
        "Would it be useful if I sent a brief overview of how the system works?\n\n"
        "Best regards,\nSami | Dealix"
    ),
}


@dataclass
class OfferData:
    """Offer data passed into asset generation functions."""

    offer_name: str
    angle_ar: str
    angle_en: str
    lead_magnet_ar: str
    lead_magnet_en: str
    cta_ar: str
    cta_en: str
    tier: str


class EmailOS:
    """Generates bilingual sector-specific email drafts. DRAFT_ONLY."""

    _NO_AUTO_SEND = True

    def draft(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: OfferData,
    ) -> ChannelAsset:
        """Generate one email draft for the given company + persona + offer."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"

        sector_key = company.sector.value if company.sector != Sector.other else "default"
        lang = company.language

        subject = self._build_subject(sector_key, lang, company.name)
        body = self._build_body(sector_key, lang, company.name, persona, offer)
        cta = offer.cta_ar if lang == Language.arabic else offer.cta_en

        log.debug("email_os.draft company_id=%s sector=%s lang=%s", company.id, sector_key, lang.value)

        return ChannelAsset(
            company_id=company.id,
            asset_type=AssetType.email_draft,
            channel=ChannelType.email,
            language=lang,
            subject_or_hook=subject,
            body=body,
            cta=cta,
            is_auto_sendable=False,
            requires_founder_approval=True,
            risk_level=RiskLevel.medium,
            approval_status="approval_required",
            sector=company.sector.value,
            country=company.country.value,
        )

    def _build_subject(self, sector: str, language: Language, company_name: str) -> str:
        tmpl = SUBJECT_LINES.get(sector, SUBJECT_LINES["default"])
        key = "ar" if language == Language.arabic else "en"
        return tmpl[key].replace("[Company]", company_name)

    def _build_body(
        self,
        sector: str,
        language: Language,
        company_name: str,
        persona: BuyerPersona,
        offer: OfferData,
    ) -> str:
        bodies = EMAIL_BODIES.get(sector, EMAIL_BODIES["default"])
        key = "ar" if language == Language.arabic else "en"
        body = bodies[key]

        decision_maker = (
            persona.typical_titles[0] if persona.typical_titles else "المدير"
        )
        body = body.replace("[Company]", company_name)
        body = body.replace("[Name]", decision_maker)
        return body


__all__ = ["EmailOS", "OfferData"]
