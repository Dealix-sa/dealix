"""Maps a Company to its GCC buyer persona based on sector, country, and language."""
from __future__ import annotations

import logging

from auto_client_acquisition.omni_channel_os.schemas import (
    BuyerPersona,
    ChannelType,
    Company,
    Language,
)

log = logging.getLogger(__name__)

_NO_AUTO_SEND = True


class BuyerMapper:
    _NO_AUTO_SEND = True

    PERSONA_MAP: dict[str, BuyerPersona] = {
        "legal": BuyerPersona(
            sector="legal",
            typical_titles=[
                "Managing Partner",
                "Senior Partner",
                "رئيس الشركة",
                "شريك إداري",
                "مدير العمليات",
            ],
            pain_points=[
                "manual document review",
                "case file chaos",
                "client follow-up tracking",
                "time billing accuracy",
                "مراجعة المستندات يدوياً",
                "تتبع ملفات القضايا",
            ],
            preferred_channels=[
                ChannelType.website_form,
                ChannelType.email,
                ChannelType.linkedin,
                ChannelType.webinar,
            ],
            offer_fit="Legal Knowledge OS — confidential document intelligence",
            language_preference=Language.arabic,
            decision_style="relationship_first",
        ),
        "facilities_management": BuyerPersona(
            sector="facilities_management",
            typical_titles=[
                "Operations Manager",
                "FM Director",
                "مدير العمليات",
                "مدير الصيانة",
                "VP Operations",
            ],
            pain_points=[
                "manual SLA reports",
                "technician dispatch",
                "maintenance ticket overload",
                "KPI reporting",
                "تقارير SLA اليدوية",
                "جدولة الفنيين",
            ],
            preferred_channels=[
                ChannelType.email,
                ChannelType.phone_call,
                ChannelType.linkedin,
                ChannelType.website_form,
            ],
            offer_fit="Maintenance SLA AI — automated technician workflow and KPI reporting",
            language_preference=Language.bilingual,
            decision_style="roi_first",
        ),
        "consulting": BuyerPersona(
            sector="consulting",
            typical_titles=[
                "Managing Director",
                "Practice Lead",
                "مدير عام",
                "رئيس القسم",
                "Partner",
            ],
            pain_points=[
                "proposal writing time",
                "client onboarding bottlenecks",
                "knowledge management",
                "utilization tracking",
                "كتابة المقترحات يدوياً",
                "متابعة العملاء",
            ],
            preferred_channels=[
                ChannelType.linkedin,
                ChannelType.email,
                ChannelType.webinar,
                ChannelType.partnership,
            ],
            offer_fit="Consulting Ops AI — proposal automation and client intelligence",
            language_preference=Language.bilingual,
            decision_style="roi_first",
        ),
        "real_estate": BuyerPersona(
            sector="real_estate",
            typical_titles=[
                "Sales Director",
                "مدير المبيعات",
                "مدير التسويق",
                "CEO",
                "مدير تطوير الأعمال",
            ],
            pain_points=[
                "lead follow-up delays",
                "manual CRM updates",
                "broker coordination",
                "listing management",
                "متابعة العملاء المحتملين",
                "تحديث CRM يدوياً",
            ],
            preferred_channels=[
                ChannelType.meta_lead_ads,
                ChannelType.website_form,
                ChannelType.phone_call,
                ChannelType.whatsapp_optin,
            ],
            offer_fit="Real Estate Lead OS — automated lead nurture and broker coordination",
            language_preference=Language.arabic,
            decision_style="roi_first",
        ),
        "healthcare": BuyerPersona(
            sector="healthcare",
            typical_titles=[
                "Hospital Administrator",
                "مدير المستشفى",
                "Director of Operations",
                "مدير الخدمات الطبية",
                "Chief Medical Officer",
            ],
            pain_points=[
                "patient scheduling backlog",
                "billing errors",
                "staff shift coordination",
                "compliance documentation",
                "جدولة المرضى",
                "أخطاء الفواتير الطبية",
            ],
            preferred_channels=[
                ChannelType.website_form,
                ChannelType.email,
                ChannelType.webinar,
                ChannelType.phone_call,
            ],
            offer_fit="Healthcare Admin AI — scheduling, billing, and compliance automation",
            language_preference=Language.arabic,
            decision_style="compliance_first",
        ),
        "education_training": BuyerPersona(
            sector="education_training",
            typical_titles=[
                "Training Manager",
                "مدير التدريب",
                "Head of L&D",
                "مدير الموارد البشرية",
                "Academic Director",
            ],
            pain_points=[
                "course enrollment tracking",
                "trainer coordination",
                "certificate issuance",
                "learner engagement",
                "تتبع التسجيل في الدورات",
                "إصدار الشهادات يدوياً",
            ],
            preferred_channels=[
                ChannelType.email,
                ChannelType.linkedin,
                ChannelType.webinar,
                ChannelType.website_form,
            ],
            offer_fit="Training Ops AI — enrollment automation and learner engagement",
            language_preference=Language.bilingual,
            decision_style="roi_first",
        ),
        "international_company": BuyerPersona(
            sector="international_company",
            typical_titles=[
                "Country Manager",
                "Regional Director",
                "Business Development Manager",
                "VP Growth",
                "Head of Sales MENA",
            ],
            pain_points=[
                "GCC market entry complexity",
                "localization gaps",
                "local partner vetting",
                "regulatory compliance",
                "Arabic content production",
            ],
            preferred_channels=[
                ChannelType.linkedin,
                ChannelType.email,
                ChannelType.linkedin_lead_gen,
                ChannelType.webinar,
            ],
            offer_fit="GCC Market Entry AI — localization, partner matching, and compliance",
            language_preference=Language.english,
            decision_style="roi_first",
        ),
        "local_sme": BuyerPersona(
            sector="local_sme",
            typical_titles=[
                "صاحب العمل",
                "المدير العام",
                "Owner",
                "مدير",
                "الرئيس التنفيذي",
            ],
            pain_points=[
                "limited staff bandwidth",
                "manual invoicing",
                "customer follow-up",
                "social media management",
                "نقص الموارد",
                "المتابعة اليدوية مع العملاء",
            ],
            preferred_channels=[
                ChannelType.website_form,
                ChannelType.phone_call,
                ChannelType.meta_lead_ads,
                ChannelType.whatsapp_optin,
            ],
            offer_fit="SME Growth OS — automate admin, follow-up, and social in one sprint",
            language_preference=Language.arabic,
            decision_style="roi_first",
        ),
        "government_adjacent": BuyerPersona(
            sector="government_adjacent",
            typical_titles=[
                "مدير المشاريع",
                "مسؤول المشتريات",
                "Project Director",
                "Procurement Manager",
                "مدير التطوير",
            ],
            pain_points=[
                "ETIMAD/Bids procurement process",
                "manual tender documentation",
                "vendor qualification",
                "compliance reporting",
                "توثيق المناقصات يدوياً",
                "متطلبات الامتثال الحكومي",
            ],
            preferred_channels=[
                ChannelType.partnership,
                ChannelType.email,
                ChannelType.procurement_portal,
                ChannelType.webinar,
            ],
            offer_fit="Gov Procurement AI — tender documentation and vendor compliance automation",
            language_preference=Language.arabic,
            decision_style="compliance_first",
        ),
        "technology": BuyerPersona(
            sector="technology",
            typical_titles=[
                "CTO",
                "VP Engineering",
                "Head of Product",
                "مدير التقنية",
                "Product Manager",
            ],
            pain_points=[
                "customer onboarding friction",
                "support ticket volume",
                "churn detection",
                "sales-engineering handoff",
                "احتكاك في onboarding العملاء",
                "حجم تذاكر الدعم",
            ],
            preferred_channels=[
                ChannelType.linkedin,
                ChannelType.email,
                ChannelType.community,
                ChannelType.webinar,
            ],
            offer_fit="Tech Revenue OS — customer success and sales automation for SaaS/tech",
            language_preference=Language.bilingual,
            decision_style="roi_first",
        ),
        "manufacturing": BuyerPersona(
            sector="manufacturing",
            typical_titles=[
                "Plant Manager",
                "مدير المصنع",
                "Operations Director",
                "مدير الإنتاج",
                "Supply Chain Manager",
            ],
            pain_points=[
                "production scheduling",
                "procurement delays",
                "quality control reporting",
                "supplier coordination",
                "جدولة الإنتاج اليدوية",
                "تقارير الجودة",
            ],
            preferred_channels=[
                ChannelType.email,
                ChannelType.phone_call,
                ChannelType.partnership,
                ChannelType.website_form,
            ],
            offer_fit="Manufacturing Ops AI — production scheduling and supplier coordination",
            language_preference=Language.bilingual,
            decision_style="roi_first",
        ),
        "retail": BuyerPersona(
            sector="retail",
            typical_titles=[
                "Retail Director",
                "مدير التجزئة",
                "Head of E-commerce",
                "مدير التسويق",
                "Operations Manager",
            ],
            pain_points=[
                "inventory management",
                "customer retention",
                "seasonal demand forecasting",
                "loyalty program complexity",
                "إدارة المخزون",
                "الاحتفاظ بالعملاء",
            ],
            preferred_channels=[
                ChannelType.meta_lead_ads,
                ChannelType.retargeting,
                ChannelType.email,
                ChannelType.website_form,
            ],
            offer_fit="Retail Intelligence OS — demand forecasting and loyalty automation",
            language_preference=Language.arabic,
            decision_style="roi_first",
        ),
        "financial_services": BuyerPersona(
            sector="financial_services",
            typical_titles=[
                "Head of Operations",
                "مدير العمليات",
                "CFO",
                "Risk Manager",
                "مدير المخاطر",
            ],
            pain_points=[
                "KYC/AML manual processing",
                "regulatory reporting",
                "client onboarding delays",
                "audit trail gaps",
                "معالجة KYC يدوياً",
                "التقارير التنظيمية",
            ],
            preferred_channels=[
                ChannelType.email,
                ChannelType.linkedin,
                ChannelType.webinar,
                ChannelType.partnership,
            ],
            offer_fit="FinOps AI — compliance automation and client onboarding acceleration",
            language_preference=Language.bilingual,
            decision_style="compliance_first",
        ),
    }

    def map(self, company: Company) -> BuyerPersona:
        persona = self.PERSONA_MAP.get(company.sector.value)
        if persona is None:
            log.debug("buyer_mapper.no_persona sector=%s using default", company.sector.value)
            return self._default_persona()
        return persona

    def get_offer_fit(self, sector: str) -> str:
        persona = self.PERSONA_MAP.get(sector)
        if persona is None:
            return self._default_persona().offer_fit
        return persona.offer_fit

    def get_angle(self, sector: str, company: Company) -> str:
        persona = self.PERSONA_MAP.get(sector)
        if persona is None:
            return f"AI workflow automation for {company.name}"
        # Construct a short angle from pain points + offer fit
        pain = persona.pain_points[0] if persona.pain_points else "manual processes"
        return f"{persona.offer_fit} — eliminate {pain}"

    def get_decision_maker_title(self, sector: str, language: Language) -> str:
        persona = self.PERSONA_MAP.get(sector)
        if persona is None:
            return "مدير" if language == Language.arabic else "Manager"
        titles = persona.typical_titles
        if not titles:
            return "مدير" if language == Language.arabic else "Manager"
        # Arabic titles contain Arabic characters; English titles do not
        if language == Language.arabic:
            arabic_titles = [t for t in titles if any("؀" <= c <= "ۿ" for c in t)]
            return arabic_titles[0] if arabic_titles else titles[0]
        english_titles = [t for t in titles if not any("؀" <= c <= "ۿ" for c in t)]
        return english_titles[0] if english_titles else titles[0]

    def _default_persona(self) -> BuyerPersona:
        return BuyerPersona(
            sector="other",
            typical_titles=["مدير", "CEO", "Managing Director"],
            pain_points=["manual workflows", "operational inefficiency", "العمليات اليدوية"],
            preferred_channels=[
                ChannelType.email,
                ChannelType.website_form,
                ChannelType.linkedin,
            ],
            offer_fit="Free AI Workflow Diagnostic",
            language_preference=Language.arabic,
            decision_style="relationship_first",
        )


__all__ = ["BuyerMapper"]
