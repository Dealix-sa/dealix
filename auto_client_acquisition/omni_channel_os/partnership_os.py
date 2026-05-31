"""Partnership OS — drafts partner intro messages and referral agreements. DRAFT ONLY."""
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

_NO_AUTO_SEND = True

PARTNER_TYPES: dict[str, dict[str, str]] = {
    "it_firm": {
        "ar": "شركات تقنية المعلومات",
        "en": "IT companies",
        "value_prop_ar": "نكمل خدماتكم التقنية بطبقة AI Workflow على العمليات التشغيلية",
        "value_prop_en": "We complement your technical services with an AI workflow layer on operational processes",
    },
    "consulting": {
        "ar": "شركات الاستشارات",
        "en": "consulting firms",
        "value_prop_ar": "نساعد عملاءكم على تنفيذ توصيات التحول الرقمي بأنظمة workflow عملية",
        "value_prop_en": "We help your clients implement digital transformation recommendations with practical workflow systems",
    },
    "accounting": {
        "ar": "شركات المحاسبة والمراجعة",
        "en": "accounting and audit firms",
        "value_prop_ar": "نتيح لعملاءكم أتمتة التقارير المالية والامتثال بدون تعقيد",
        "value_prop_en": "We enable your clients to automate financial reporting and compliance without complexity",
    },
    "erp_implementer": {
        "ar": "شركات تطبيق ERP",
        "en": "ERP implementers",
        "value_prop_ar": "نضيف طبقة AI فوق ERP الحالي لأتمتة العمليات التي يتركها النظام بدون حل",
        "value_prop_en": "We add an AI layer on top of the existing ERP to automate processes it leaves unsolved",
    },
    "digital_agency": {
        "ar": "وكالات التسويق الرقمي",
        "en": "digital agencies",
        "value_prop_ar": "نحول leads عملاءكم إلى مسارات متابعة ذكية بدون جهد يدوي",
        "value_prop_en": "We turn your clients' leads into intelligent follow-up workflows without manual effort",
    },
    "training_company": {
        "ar": "شركات التدريب",
        "en": "training companies",
        "value_prop_ar": "نساعد في أتمتة التسجيل والشهادات وتتبع المتعلمين لبرامجكم",
        "value_prop_en": "We automate enrollment, certificates, and learner tracking for your programs",
    },
    "crm_implementer": {
        "ar": "شركات تطبيق CRM",
        "en": "CRM implementers",
        "value_prop_ar": "نضيف AI workflows فوق CRM عملاءكم لأتمتة متابعة العملاء والتقارير",
        "value_prop_en": "We add AI workflows on top of your clients' CRM to automate follow-up and reporting",
    },
    "legal_tech": {
        "ar": "شركات التقنية القانونية",
        "en": "legal tech companies",
        "value_prop_ar": "نتكامل مع أنظمتكم لأتمتة إدارة المستندات ومتابعة القضايا",
        "value_prop_en": "We integrate with your systems to automate document management and case tracking",
    },
}

_REFERRAL_TERMS: dict[str, str] = {
    "ar": (
        "نموذج الشراكة — Dealix\n"
        "================\n\n"
        "النموذج:\n"
        "• الشريك يُحيل عميلاً يحتاج AI Workflow Audit أو pilot\n"
        "• Dealix ينفذ التشخيص والـ pilot\n"
        "• عمولة إحالة: [REFERRAL_FEE]% من قيمة أول عقد\n"
        "• العلاقة شفافة مع العميل من البداية\n\n"
        "الالتزامات:\n"
        "• الشريك: إحالة مؤهلة (decision maker + احتياج واضح)\n"
        "• Dealix: استجابة خلال 48 ساعة + تقرير نتيجة للشريك\n\n"
        "هذا نموذج مبسط — التفاصيل تُناقش في جلسة قصيرة."
    ),
    "en": (
        "Partnership Model — Dealix\n"
        "==========================\n\n"
        "The model:\n"
        "• Partner refers a client who needs an AI Workflow Audit or pilot\n"
        "• Dealix delivers the diagnostic and pilot\n"
        "• Referral commission: [REFERRAL_FEE]% of first contract value\n"
        "• Relationship is transparent with the client from the start\n\n"
        "Commitments:\n"
        "• Partner: qualified referral (decision maker + clear need)\n"
        "• Dealix: response within 48 hours + outcome report to partner\n\n"
        "This is a simplified model — details discussed in a short session."
    ),
}


class PartnershipOS:
    """Drafts partnership intro messages and referral agreement summaries."""

    _NO_AUTO_SEND = True

    def draft_intro(
        self,
        partner_company: str,
        partner_type: str,
        contact_name: str,
        language: Language,
    ) -> ChannelAsset:
        """Draft initial partnership introduction message."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"

        pt = PARTNER_TYPES.get(partner_type, PARTNER_TYPES["consulting"])

        if language == Language.arabic:
            sector_label = pt["ar"]
            value_prop = pt["value_prop_ar"]
            body = (
                f"السلام عليكم {contact_name},\n"
                f"لاحظت أنكم تخدمون شركات في {sector_label}.\n"
                "أنا أبني Dealix كـ AI workflow delivery partner للشركات التي تحتاج تحويل "
                "العمليات اليدوية والتقارير والمتابعات إلى workflows مدعومة بالذكاء الاصطناعي.\n"
                f"الفكرة ليست منافسة لخدماتكم — بل شراكة: {value_prop}.\n"
                "إذا عندكم عميل يحتاج AI pilot أو automation assessment، نقدر ندخل كـ "
                "delivery partner والعلاقة واضحة من البداية.\n"
                "هل يناسبك أرسل لكم نموذج الشراكة المختصر؟"
            )
            cta = "إرسال نموذج الشراكة"
            hook = f"فرصة شراكة — Dealix × {partner_company}"
        else:
            sector_label = pt["en"]
            value_prop = pt["value_prop_en"]
            body = (
                f"Hi {contact_name},\n"
                f"I noticed you work with companies in {sector_label}.\n"
                "I am building Dealix as an AI workflow delivery partner for companies that need "
                "to turn manual operations, reporting, and follow-up into AI-supported workflows.\n"
                f"This is not a competing service — it is a partnership: {value_prop}.\n"
                "If you have a client who needs an AI pilot or automation assessment, we can enter "
                "as the delivery partner with a transparent arrangement from the start.\n"
                "Would it be useful if I sent you the brief partnership model?"
            )
            cta = "Send partnership model"
            hook = f"Partnership opportunity — Dealix x {partner_company}"

        log.debug(
            "partnership_os.draft_intro partner=%s type=%s lang=%s",
            partner_company,
            partner_type,
            language.value,
        )

        return ChannelAsset(
            company_id=partner_company,
            asset_type=AssetType.partner_intro,
            channel=ChannelType.partnership,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
            is_auto_sendable=False,
            requires_founder_approval=True,
            risk_level=RiskLevel.low,
            approval_status="approval_required",
            sector=partner_type,
            country="",
        )

    def draft_referral_terms(
        self,
        partner_type: str,
        language: Language,
    ) -> ChannelAsset:
        """Draft referral agreement summary."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"

        key = "ar" if language == Language.arabic else "en"
        body = _REFERRAL_TERMS[key]

        if language == Language.arabic:
            cta = "مناقشة التفاصيل"
            hook = "ملخص نموذج الإحالة"
        else:
            cta = "Discuss details"
            hook = "Referral model summary"

        return ChannelAsset(
            company_id="generic",
            asset_type=AssetType.partner_intro,
            channel=ChannelType.partnership,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
            is_auto_sendable=False,
            requires_founder_approval=True,
            risk_level=RiskLevel.low,
            approval_status="approval_required",
            sector=partner_type,
            country="",
        )

    def followup_sequence(
        self,
        partner_type: str,
        language: Language,
    ) -> list[ChannelAsset]:
        """3-touch follow-up sequence for partnership outreach."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"

        pt = PARTNER_TYPES.get(partner_type, PARTNER_TYPES["consulting"])
        assets: list[ChannelAsset] = []

        for i, (subj_ar, subj_en, body_ar, body_en) in enumerate(
            [
                (
                    "متابعة: نموذج الشراكة",
                    "Follow-up: partnership model",
                    (
                        "السلام عليكم،\nأرسلت لكم رسالة قبل أيام عن شراكة Dealix.\n"
                        "فقط أتأكد أنها وصلت — هل راجعتموها؟"
                    ),
                    (
                        "Hi,\nI sent you a note a few days ago about the Dealix partnership.\n"
                        "Just checking it reached you — did you get a chance to review it?"
                    ),
                ),
                (
                    f"قيمة مباشرة لشركاء {pt['ar']}",
                    f"Direct value for {pt['en']} partners",
                    (
                        f"السلام عليكم،\nشاركت مؤخراً مقالاً عن كيف يستفيد {pt['ar']} "
                        "من نموذج الشراكة مع Dealix.\n"
                        "إذا كان عندكم عميل يفكر في AI pilot — أنا هنا."
                    ),
                    (
                        f"Hi,\nI recently shared an article about how {pt['en']} "
                        "partners benefit from the Dealix model.\n"
                        "If you have a client considering an AI pilot — I am here."
                    ),
                ),
                (
                    "آخر تواصل — شراكة Dealix",
                    "Final note — Dealix partnership",
                    (
                        "السلام عليكم،\nهذه آخر رسالة بخصوص الشراكة.\n"
                        "إذا تغير الوقت في المستقبل — يسعدني التواصل.\n"
                        "أتمنى لكم التوفيق."
                    ),
                    (
                        "Hi,\nThis is my last note about the partnership.\n"
                        "If timing changes in the future — happy to reconnect.\n"
                        "Wishing you continued success."
                    ),
                ),
            ],
            start=1,
        ):
            if language == Language.arabic:
                body = body_ar
                subject = subj_ar
                cta = "رد" if i < 3 else "للمستقبل"
            else:
                body = body_en
                subject = subj_en
                cta = "Reply" if i < 3 else "Future reference"

            assets.append(
                ChannelAsset(
                    company_id="generic",
                    asset_type=AssetType.partner_intro,
                    channel=ChannelType.partnership,
                    language=language,
                    subject_or_hook=f"Touch {i}: {subject}",
                    body=body,
                    cta=cta,
                    is_auto_sendable=False,
                    requires_founder_approval=True,
                    risk_level=RiskLevel.low,
                    approval_status="approval_required",
                    sector=partner_type,
                    country="",
                )
            )
        return assets


__all__ = ["PARTNER_TYPES", "PartnershipOS"]
