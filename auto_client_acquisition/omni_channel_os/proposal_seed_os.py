"""Proposal Seed OS — generates 1-page opportunity memos for Tier A prospects. FOUNDER APPROVED."""
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
)

log = logging.getLogger(__name__)

_NO_AUTO_SEND = True

_OBSERVED_CHALLENGES: dict[str, dict[str, str]] = {
    "legal": {
        "ar": "حجم كبير من المستندات والمراسلات التي تحتاج تنظيماً ومتابعة",
        "en": "high volumes of documents and correspondence requiring organization and follow-up",
    },
    "facilities_management": {
        "ar": "تقارير SLA وبلاغات صيانة تحتاج متابعة يدوية مستمرة",
        "en": "SLA reports and maintenance tickets requiring continuous manual follow-up",
    },
    "consulting": {
        "ar": "وقت كبير في كتابة المقترحات، تتبع العملاء، وإعداد التقارير",
        "en": "significant time spent on proposal writing, client tracking, and reporting",
    },
    "real_estate": {
        "ar": "متابعة مستمرة مع العملاء المحتملين والوسطاء",
        "en": "continuous follow-up with leads and brokers",
    },
    "healthcare": {
        "ar": "أعباء إدارية في الجدولة والفواتير والامتثال",
        "en": "administrative burdens around scheduling, billing, and compliance",
    },
    "education_training": {
        "ar": "إدارة التسجيل، إصدار الشهادات، وتتبع المتعلمين",
        "en": "managing enrollment, certificate issuance, and learner tracking",
    },
    "government_adjacent": {
        "ar": "تعقيدات توثيق المناقصات ومتطلبات الامتثال الحكومي",
        "en": "tender documentation complexity and government compliance requirements",
    },
    "local_sme": {
        "ar": "ضغط العمل بموارد محدودة مع متطلبات متابعة متعددة",
        "en": "working under resource constraints with multiple follow-up requirements",
    },
    "international_company": {
        "ar": "تحديات التوطين والامتثال المحلي عند دخول السوق الخليجي",
        "en": "localization and local compliance challenges when entering the GCC market",
    },
    "default": {
        "ar": "عمليات تشغيلية متكررة تستهلك وقتاً كبيراً من الفريق",
        "en": "repetitive operational processes consuming significant team time",
    },
}

_LIKELY_WORKFLOWS: dict[str, dict[str, str]] = {
    "legal": {
        "ar": "تصنيف المستندات، البحث في ملفات القضايا، تتبع المراسلات مع العملاء",
        "en": "Document classification, case file search, client correspondence tracking",
    },
    "facilities_management": {
        "ar": "استلام البلاغ، تصنيفه، تعيين الفني، تتبع الإنجاز، إصدار تقرير SLA",
        "en": "Ticket intake, classification, technician assignment, completion tracking, SLA report issuance",
    },
    "consulting": {
        "ar": "هيكلة المقترحات، تتبع مراحل المشاريع، بناء قاعدة معرفية داخلية",
        "en": "Proposal structuring, project milestone tracking, internal knowledge base building",
    },
    "real_estate": {
        "ar": "متابعة العملاء المحتملين، تنسيق الوسطاء، توليد تقارير المبيعات",
        "en": "Lead follow-up, broker coordination, sales report generation",
    },
    "healthcare": {
        "ar": "جدولة المرضى، مراجعة الفواتير، إعداد تقارير الامتثال",
        "en": "Patient scheduling, billing review, compliance report preparation",
    },
    "default": {
        "ar": "العمليات المتكررة التي يمكن توثيقها وأتمتتها مع موافقة بشرية",
        "en": "Repetitive processes that can be documented and automated with human approval",
    },
}

_PILOT_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "legal": {
        "ar": "نظام تصنيف مستندات يعمل على مسار واحد في المكتب — مع موافقة كاملة من الفريق",
        "en": "A document classification system on one office workflow — with full team approval",
    },
    "facilities_management": {
        "ar": "أتمتة مسار بلاغ واحد من الاستلام حتى إصدار تقرير SLA — مع موافقة المسؤول",
        "en": "Automating one ticket workflow from intake to SLA report — with manager approval",
    },
    "consulting": {
        "ar": "أتمتة هيكل مقترح واحد بناءً على متطلبات العميل — مع مراجعة بشرية كاملة",
        "en": "Automating one proposal structure based on client requirements — with full human review",
    },
    "default": {
        "ar": "تطبيق AI Workflow على مسار واحد تختاره الشركة — بدون مخاطرة على البيانات",
        "en": "Applying AI Workflow to one company-selected process — without data risk",
    },
}


class ProposalSeedOS:
    """Generates 1-page opportunity memos for Tier A prospects."""

    _NO_AUTO_SEND = True

    def generate_memo(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: object,
        observed_workflow: str = "",
    ) -> ChannelAsset:
        """Generate 1-page opportunity memo. High-touch, Tier A only."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"

        lang = company.language
        sector = company.sector.value

        what_noticed = self._what_we_noticed(company, sector, lang)
        likely_wf = self._likely_workflow(sector, lang)
        recommended = self._recommended_audit(offer, lang)
        pilot = self._possible_pilot(sector, lang)
        needed = self._what_we_need(lang)

        wf_display = observed_workflow or likely_wf

        if lang == Language.arabic:
            body = (
                f"مذكرة فرصة — {company.name}\n\n"
                f"ما لاحظناه:\n{what_noticed}\n\n"
                f"Workflow محتمل للأتمتة:\n{wf_display}\n\n"
                f"التشخيص المقترح:\n{recommended}\n\n"
                f"Pilot محتمل خلال 30 يوم:\n{pilot}\n\n"
                f"ما نحتاجه من {company.name}:\n{needed}"
            )
            hook = f"مذكرة فرصة — {company.name}"
            cta = "جلسة اكتشاف 30 دقيقة"
        else:
            body = (
                f"Opportunity Memo — {company.name}\n\n"
                f"What we noticed:\n{what_noticed}\n\n"
                f"Likely automation workflow:\n{wf_display}\n\n"
                f"Recommended diagnostic:\n{recommended}\n\n"
                f"Possible pilot within 30 days:\n{pilot}\n\n"
                f"What we need from {company.name}:\n{needed}"
            )
            hook = f"Opportunity memo — {company.name}"
            cta = "30-minute discovery call"

        log.debug(
            "proposal_seed_os.generate_memo company_id=%s sector=%s lang=%s",
            company.id,
            sector,
            lang.value,
        )

        return ChannelAsset(
            company_id=company.id,
            asset_type=AssetType.proposal_seed,
            channel=ChannelType.email,
            language=lang,
            subject_or_hook=hook,
            body=body,
            cta=cta,
            is_auto_sendable=False,
            requires_founder_approval=True,
            risk_level=RiskLevel.low,
            approval_status="approval_required",
            sector=company.sector.value,
            country=company.country.value,
        )

    def _what_we_noticed(
        self, company: Company, sector: str, language: Language
    ) -> str:
        challenges = _OBSERVED_CHALLENGES.get(sector, _OBSERVED_CHALLENGES["default"])
        key = "ar" if language == Language.arabic else "en"
        challenge = challenges[key]
        if language == Language.arabic:
            return f"{company.name} تعمل في مجال {sector} وغالباً يكون لديهم {challenge}."
        return f"{company.name} operates in the {sector} space and typically has {challenge}."

    def _likely_workflow(self, sector: str, language: Language) -> str:
        workflows = _LIKELY_WORKFLOWS.get(sector, _LIKELY_WORKFLOWS["default"])
        key = "ar" if language == Language.arabic else "en"
        return workflows[key]

    def _recommended_audit(self, offer: object, language: Language) -> str:
        offer_name = getattr(offer, "offer_name", "AI Workflow Audit")
        if language == Language.arabic:
            return (
                f"{offer_name} على مسار واحد — 7 أيام، بدون مخاطرة على البيانات."
            )
        return f"{offer_name} on one workflow — 7 days, without data risk."

    def _possible_pilot(self, sector: str, language: Language) -> str:
        pilots = _PILOT_DESCRIPTIONS.get(sector, _PILOT_DESCRIPTIONS["default"])
        key = "ar" if language == Language.arabic else "en"
        return pilots[key]

    def _what_we_need(self, language: Language) -> str:
        if language == Language.arabic:
            return (
                "• وصف قصير للـ workflow الحالي\n"
                "• نماذج من البيانات (بدون PII)\n"
                "• 30 دقيقة discovery call"
            )
        return (
            "• Short description of the current workflow\n"
            "• Sample data (without PII)\n"
            "• 30-minute discovery call"
        )


__all__ = ["ProposalSeedOS"]
