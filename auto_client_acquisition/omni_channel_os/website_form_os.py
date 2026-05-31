"""Website Form OS — drafts contact form messages. DRAFT ONLY, human submits."""
from __future__ import annotations

import logging

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

_SECTOR_OPENERS: dict[str, dict[str, str]] = {
    "legal": {
        "ar": "لاحظنا أن طبيعة عمل مكاتب المحاماة تشمل حجماً كبيراً من المستندات والمراسلات التي تحتاج تنظيماً.",
        "en": "We noticed that law firms typically handle large volumes of documents and correspondence requiring systematic organization.",
    },
    "facilities_management": {
        "ar": "لاحظنا أن شركات FM غالباً لديها تقارير SLA وبلاغات صيانة تحتاج متابعة يدوية مستمرة.",
        "en": "We noticed that FM companies typically manage SLA reports and maintenance tickets requiring continuous manual follow-up.",
    },
    "consulting": {
        "ar": "لاحظنا أن شركات الاستشارات تقضي وقتاً كبيراً في كتابة المقترحات وإعداد التقارير.",
        "en": "We noticed that consulting firms invest significant time in proposal writing and reporting.",
    },
    "real_estate": {
        "ar": "لاحظنا أن شركات العقارات تحتاج متابعة مستمرة مع العملاء المحتملين والوسطاء.",
        "en": "We noticed that real estate companies require continuous follow-up with leads and brokers.",
    },
    "healthcare": {
        "ar": "لاحظنا أن المنشآت الصحية تواجه أعباءً إدارية كبيرة في الجدولة والفواتير والامتثال.",
        "en": "We noticed that healthcare facilities face significant administrative burdens around scheduling, billing, and compliance.",
    },
    "education_training": {
        "ar": "لاحظنا أن مراكز التدريب تقضي وقتاً في إدارة التسجيل وإصدار الشهادات.",
        "en": "We noticed that training centers spend considerable time managing enrollment and certificate issuance.",
    },
    "international_company": {
        "ar": "لاحظنا أن الشركات الدولية التي تدخل السوق السعودي تواجه تحديات في التوطين والامتثال.",
        "en": "We noticed that international companies entering the GCC market face localization and compliance challenges.",
    },
    "local_sme": {
        "ar": "لاحظنا أن الشركات الصغيرة والمتوسطة تعمل بموارد محدودة وتحتاج كل دقيقة.",
        "en": "We noticed that small and medium businesses operate with limited resources where every minute counts.",
    },
    "government_adjacent": {
        "ar": "لاحظنا أن الشركات العاملة مع الجهات الحكومية تواجه تعقيدات في توثيق المناقصات.",
        "en": "We noticed that companies working with government entities face complexity around tender documentation.",
    },
    "default": {
        "ar": "لاحظنا أن طبيعة عمل شركتكم قد تستفيد من تحسين بعض العمليات التشغيلية.",
        "en": "We noticed that your company's operations may benefit from improving certain operational processes.",
    },
}

_BODY_TEMPLATES: dict[str, dict[str, str]] = {
    "ar": (
        "السلام عليكم،\n"
        "معكم Sami من Dealix.\n"
        "نبني أنظمة Agentic AI تساعد المنشآت على تحويل workflows المتكررة — "
        "التقارير، المستندات، المتابعة، خدمة العملاء — إلى مسارات منظمة مع موافقة بشرية.\n"
        "لاحظت أن طبيعة عمل {company_name} في {sector} قد تستفيد من AI Workflow Audit قصير "
        "على مسار واحد لتحديد أين يمكن تطبيق AI بشكل آمن وعملي.\n"
        "يسعدني إرسال نبذة مختصرة إذا كان الموضوع مناسبًا.\n"
        "مع أطيب التحيات،\nSami | Dealix"
    ),
    "en": (
        "Hello,\n"
        "I'm Sami, founder of Dealix.\n"
        "We build controlled Agentic AI workflows for GCC businesses — turning repetitive operations "
        "like reporting, document handling, follow-up, and customer service into structured, "
        "human-approved automation.\n"
        "I noticed {company_name}'s work in {sector} might benefit from a short AI Workflow Audit "
        "on one process to identify where AI can be applied safely.\n"
        "Happy to send a brief overview if relevant.\n"
        "Best regards,\nSami | Dealix"
    ),
}


class WebsiteFormOS:
    """Drafts contact form messages. Human submits — never auto-submitted."""

    _NO_AUTO_SEND = True

    def draft_message(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: object,
    ) -> ChannelAsset:
        """Drafts the contact form message. Human submits."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"

        lang = company.language
        sector_key = company.sector.value if company.sector != Sector.other else "default"

        opener = self._sector_opener(sector_key, lang)
        body = self._body_template(sector_key, lang, company.name)

        if lang == Language.arabic:
            hook = f"استفسار عن AI Workflow Audit — {company.name}"
            cta = "إرسال الرسالة"
        else:
            hook = f"Inquiry about AI Workflow Audit — {company.name}"
            cta = "Submit message"

        full_body = f"{opener}\n\n{body}"

        log.debug(
            "website_form_os.draft company_id=%s sector=%s lang=%s",
            company.id,
            sector_key,
            lang.value,
        )

        return ChannelAsset(
            company_id=company.id,
            asset_type=AssetType.website_form_message,
            channel=ChannelType.website_form,
            language=lang,
            subject_or_hook=hook,
            body=full_body,
            cta=cta,
            is_auto_sendable=False,
            requires_founder_approval=True,
            risk_level=RiskLevel.medium,
            approval_status="approval_required",
            sector=company.sector.value,
            country=company.country.value,
        )

    def _sector_opener(self, sector: str, language: Language) -> str:
        openers = _SECTOR_OPENERS.get(sector, _SECTOR_OPENERS["default"])
        return openers["ar"] if language == Language.arabic else openers["en"]

    def _body_template(
        self, sector: str, language: Language, company_name: str
    ) -> str:
        key = "ar" if language == Language.arabic else "en"
        template = _BODY_TEMPLATES[key]
        return template.format(company_name=company_name, sector=sector.replace("_", " "))


__all__ = ["WebsiteFormOS"]
