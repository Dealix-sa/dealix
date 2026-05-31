"""Maps Company sector to the best offer, angle, lead magnet, and CTA for GCC outreach."""
from __future__ import annotations

import logging

from auto_client_acquisition.omni_channel_os.schemas import (
    BuyerPersona,
    Company,
    Language,
)

log = logging.getLogger(__name__)

_NO_AUTO_SEND = True

OFFER_MAP: dict[str, dict] = {
    "legal": {
        "offer": "Legal Knowledge OS",
        "tier": "sprint_499",
        "angle_ar": "ذكاء اصطناعي لمستندات المكتب بدون مخاطرة بسرية العميل",
        "angle_en": "AI document intelligence without risking client confidentiality",
        "lead_magnet_ar": "قائمة فحص AI لـ workflows مكتب المحاماة",
        "lead_magnet_en": "Legal AI Workflow Audit Checklist",
        "cta_ar": "احصل على تشخيص مجاني",
        "cta_en": "Get your free workflow diagnostic",
    },
    "facilities_management": {
        "offer": "Maintenance SLA AI",
        "tier": "sprint_499",
        "angle_ar": "تقارير SLA تلقائية وإشعارات الفنيين بدون متابعة يدوية",
        "angle_en": "Automated SLA reports and technician alerts without manual follow-up",
        "lead_magnet_ar": "خريطة فرص AI للصيانة",
        "lead_magnet_en": "Maintenance SLA AI Opportunity Map",
        "cta_ar": "شوف كيف يشتغل على عملياتكم",
        "cta_en": "See how it fits your operations",
    },
    "consulting": {
        "offer": "Consulting Ops AI",
        "tier": "sprint_499",
        "angle_ar": "أتمتة كتابة المقترحات وتتبع العملاء بدون موارد إضافية",
        "angle_en": "Automate proposal writing and client tracking without extra headcount",
        "lead_magnet_ar": "قالب AI لمقترحات الاستشارات",
        "lead_magnet_en": "AI Consulting Proposal Template Pack",
        "cta_ar": "جرب النموذج مجاناً",
        "cta_en": "Try the template free",
    },
    "real_estate": {
        "offer": "Real Estate Lead OS",
        "tier": "sprint_499",
        "angle_ar": "متابعة تلقائية للعملاء المحتملين مع تنسيق الوسطاء",
        "angle_en": "Automated lead nurture with broker coordination in one system",
        "lead_magnet_ar": "خريطة AI لتحويل العملاء المحتملين في العقارات",
        "lead_magnet_en": "Real Estate Lead Conversion AI Map",
        "cta_ar": "شوف كيف يشتغل النظام",
        "cta_en": "See the system in action",
    },
    "healthcare": {
        "offer": "Healthcare Admin AI",
        "tier": "sprint_499",
        "angle_ar": "أتمتة جدولة المرضى والفواتير بدون أخطاء امتثال",
        "angle_en": "Automate patient scheduling and billing without compliance risk",
        "lead_magnet_ar": "قائمة فحص الامتثال الرقمي للمستشفيات",
        "lead_magnet_en": "Hospital Digital Compliance Checklist",
        "cta_ar": "احصل على تقييم مجاني",
        "cta_en": "Get a free compliance assessment",
    },
    "education_training": {
        "offer": "Training Ops AI",
        "tier": "sprint_499",
        "angle_ar": "أتمتة التسجيل وإصدار الشهادات وتتبع المتعلمين",
        "angle_en": "Automate enrollment, certificates, and learner tracking",
        "lead_magnet_ar": "دليل أتمتة عمليات التدريب",
        "lead_magnet_en": "Training Operations Automation Playbook",
        "cta_ar": "ابدأ بتشخيص مجاني",
        "cta_en": "Start with a free diagnostic",
    },
    "international_company": {
        "offer": "GCC Market Entry AI",
        "tier": "sprint_999",
        "angle_ar": "دخول سوق الخليج بسرعة مع الامتثال المحلي والتوطين",
        "angle_en": "Enter GCC markets fast with local compliance and Arabic localization",
        "lead_magnet_ar": "دليل دخول السوق السعودي للشركات الدولية",
        "lead_magnet_en": "Saudi Market Entry Guide for International Companies",
        "cta_ar": "احصل على خريطة دخول السوق",
        "cta_en": "Get your market entry map",
    },
    "local_sme": {
        "offer": "SME Growth OS",
        "tier": "sprint_299",
        "angle_ar": "أتمتة المتابعة اليدوية وإدارة العملاء في سبرنت واحد",
        "angle_en": "Automate manual follow-up and client management in one sprint",
        "lead_magnet_ar": "تشخيص مجاني لعمليات الأعمال الصغيرة",
        "lead_magnet_en": "Free SME Operations Diagnostic",
        "cta_ar": "جرب التشخيص المجاني",
        "cta_en": "Try the free diagnostic",
    },
    "government_adjacent": {
        "offer": "Gov Procurement AI",
        "tier": "sprint_999",
        "angle_ar": "أتمتة توثيق المناقصات والامتثال الحكومي",
        "angle_en": "Automate tender documentation and government compliance workflows",
        "lead_magnet_ar": "قائمة فحص مناقصات ETIMAD",
        "lead_magnet_en": "ETIMAD Tender Compliance Checklist",
        "cta_ar": "احصل على تقييم المناقصات",
        "cta_en": "Get your tender readiness assessment",
    },
    "technology": {
        "offer": "Tech Revenue OS",
        "tier": "sprint_499",
        "angle_ar": "أتمتة onboarding العملاء وخفض معدل الاستنزاف",
        "angle_en": "Automate customer onboarding and reduce churn with AI",
        "lead_magnet_ar": "نموذج أتمتة customer success للشركات التقنية",
        "lead_magnet_en": "Tech Customer Success Automation Playbook",
        "cta_ar": "شوف النموذج مجاناً",
        "cta_en": "See the playbook free",
    },
    "manufacturing": {
        "offer": "Manufacturing Ops AI",
        "tier": "sprint_499",
        "angle_ar": "أتمتة جدولة الإنتاج وتنسيق الموردين",
        "angle_en": "Automate production scheduling and supplier coordination",
        "lead_magnet_ar": "خريطة فرص AI لعمليات التصنيع",
        "lead_magnet_en": "Manufacturing Operations AI Opportunity Map",
        "cta_ar": "احصل على خريطة الفرص",
        "cta_en": "Get your opportunity map",
    },
    "retail": {
        "offer": "Retail Intelligence OS",
        "tier": "sprint_499",
        "angle_ar": "توقع الطلب وأتمتة برامج الولاء بدون تعقيد",
        "angle_en": "Demand forecasting and loyalty automation without the complexity",
        "lead_magnet_ar": "تقرير AI لتحسين المخزون وولاء العملاء",
        "lead_magnet_en": "Retail AI Inventory and Loyalty Optimization Report",
        "cta_ar": "احصل على التقرير المجاني",
        "cta_en": "Get the free report",
    },
    "financial_services": {
        "offer": "FinOps AI",
        "tier": "sprint_999",
        "angle_ar": "أتمتة KYC والتقارير التنظيمية بدون مخاطر امتثال",
        "angle_en": "Automate KYC and regulatory reporting without compliance risk",
        "lead_magnet_ar": "قائمة فحص الامتثال التنظيمي للخدمات المالية",
        "lead_magnet_en": "Financial Services Regulatory Compliance Checklist",
        "cta_ar": "احصل على تقييم الامتثال",
        "cta_en": "Get your compliance assessment",
    },
    "default": {
        "offer": "Free AI Workflow Diagnostic",
        "tier": "free_diagnostic",
        "angle_ar": "اكتشف أين يمكن تطبيق AI في workflow واحد خلال 7 أيام",
        "angle_en": "Discover where AI fits your operations in 7 days",
        "lead_magnet_ar": "تشخيص AI Workflow مجاني",
        "lead_magnet_en": "Free AI Workflow Diagnostic",
        "cta_ar": "ابدأ تشخيصك المجاني",
        "cta_en": "Start your free diagnostic",
    },
}


class OfferRouter:
    _NO_AUTO_SEND = True

    def route(self, company: Company, persona: BuyerPersona) -> tuple[str, str]:
        sector = company.sector.value
        data = OFFER_MAP.get(sector, OFFER_MAP["default"])
        offer = data["offer"]
        if company.language == Language.arabic:
            angle = data["angle_ar"]
        else:
            angle = data["angle_en"]
        log.debug("offer_router.route company_id=%s offer=%s", company.id, offer)
        return offer, angle

    def get_lead_magnet(self, sector: str, language: Language) -> str:
        data = OFFER_MAP.get(sector, OFFER_MAP["default"])
        if language == Language.arabic:
            return data["lead_magnet_ar"]
        return data["lead_magnet_en"]

    def get_cta(self, offer: str, language: Language) -> str:
        for data in OFFER_MAP.values():
            if data["offer"] == offer:
                if language == Language.arabic:
                    return data["cta_ar"]
                return data["cta_en"]
        default = OFFER_MAP["default"]
        if language == Language.arabic:
            return default["cta_ar"]
        return default["cta_en"]

    def get_tier(self, sector: str) -> str:
        data = OFFER_MAP.get(sector, OFFER_MAP["default"])
        return data["tier"]

    def get_full_offer_data(self, sector: str, language: Language) -> dict:
        data = OFFER_MAP.get(sector, OFFER_MAP["default"])
        return {
            "offer": data["offer"],
            "tier": data["tier"],
            "angle": data["angle_ar"] if language == Language.arabic else data["angle_en"],
            "lead_magnet": data["lead_magnet_ar"] if language == Language.arabic else data["lead_magnet_en"],
            "cta": data["cta_ar"] if language == Language.arabic else data["cta_en"],
        }


__all__ = ["OFFER_MAP", "OfferRouter"]
