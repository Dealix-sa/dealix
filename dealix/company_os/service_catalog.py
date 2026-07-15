"""Canonical founder-facing Dealix service catalog and deterministic matcher."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class ServiceOffer:
    id: str
    name_ar: str
    department: str
    stage: str
    price_guidance_sar: str
    ideal_for: tuple[str, ...]
    pain_keywords: tuple[str, ...]
    value_outcomes: tuple[str, ...]
    proof_required: tuple[str, ...]
    forbidden_claims: tuple[str, ...] = (
        "guaranteed_revenue",
        "guaranteed_cost_reduction",
        "government_access_claim",
        "employee_replacement_claim_without_scope_evidence",
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


SERVICE_CATALOG: tuple[ServiceOffer, ...] = (
    ServiceOffer(
        id="saudi_opportunity_snapshot",
        name_ar="Saudi Opportunity Snapshot",
        department="market_access",
        stage="entry",
        price_guidance_sar="499-1500",
        ideal_for=("foreign_company", "new_segment", "market_validation"),
        pain_keywords=("سوق", "توسع", "السعودية", "شريك", "دخول", "market", "saudi", "mena"),
        value_outcomes=("خريطة فرص أولية", "قائمة حسابات بحثية", "قرار دخول أولي"),
        proof_required=("مصادر عامة موثقة", "افتراضات معلنة", "لا ادعاء طلب غير مثبت"),
    ),
    ServiceOffer(
        id="revenue_proof_sprint",
        name_ar="Revenue Proof Sprint",
        department="sales",
        stage="entry",
        price_guidance_sar="499",
        ideal_for=("warm_lead", "first_paid_proof", "small_business"),
        pain_keywords=("متابعة", "عملاء", "عرض", "مبيعات", "تحويل", "follow-up", "sales", "leads"),
        value_outcomes=("تشخيص تسرب فرصة واحدة", "خطوة إغلاق يدوية", "Proof Pack محدود"),
        proof_required=("خط أساس متفق عليه", "حدث دفع حقيقي قبل تسجيل الإيراد", "دليل تسليم"),
    ),
    ServiceOffer(
        id="revenue_command_pilot",
        name_ar="Revenue Command Pilot",
        department="sales",
        stage="pilot",
        price_guidance_sar="2500-7500",
        ideal_for=("saudi_b2b", "clinic", "training_center", "professional_services"),
        pain_keywords=("استفسارات", "واتساب", "متابعة", "عروض", "صفقات", "pipeline", "crm", "leads"),
        value_outcomes=("Company Brain", "فرص مصنفة", "رسائل وعروض للموافقة", "تقرير يومي"),
        proof_required=("مصدر لكل فرصة", "موافقة قبل التواصل", "مقاييس قبل وبعد"),
    ),
    ServiceOffer(
        id="revenue_command_room",
        name_ar="Revenue Command Room",
        department="sales",
        stage="retainer",
        price_guidance_sar="5000-20000_monthly",
        ideal_for=("b2b_team", "multi_channel_sales", "recurring_pipeline"),
        pain_keywords=("فريق مبيعات", "تحصيل", "توقعات", "تقارير", "متابعة", "forecast", "pipeline"),
        value_outcomes=("غرفة قيادة يومية", "Next-best actions", "Forecast قائم على الدليل", "Proof Pack أسبوعي"),
        proof_required=("ربط CRM أو سجل أحداث", "تعريف مراحل موحد", "دليل دفع وتسليم"),
    ),
    ServiceOffer(
        id="saudi_market_access_sprint",
        name_ar="Saudi Market Access Sprint",
        department="market_access",
        stage="sprint",
        price_guidance_sar="8000-35000",
        ideal_for=("foreign_b2b", "saas", "industrial_supplier", "regional_expansion"),
        pain_keywords=("سعودي", "دخول", "موزع", "شريك", "pilot", "market entry", "riyadh", "ksa"),
        value_outcomes=("حسابات سعودية مؤهلة بحثيًا", "خريطة شركاء", "عرض موطّن", "قرار حركة تجارية"),
        proof_required=("مصادر السوق", "سبب اختيار كل حساب", "لا وعد باجتماعات أو عقود"),
    ),
    ServiceOffer(
        id="partner_distributor_desk",
        name_ar="Partner & Distributor Desk",
        department="partnerships",
        stage="sprint_or_retainer",
        price_guidance_sar="5000-15000_plus_success_fee",
        ideal_for=("vendor", "foreign_supplier", "technology_company", "saudi_distributor"),
        pain_keywords=("شريك", "موزع", "وكيل", "تكامل", "قناة", "partner", "distributor", "reseller"),
        value_outcomes=("Shortlist شركاء", "معايير توافق", "مسودات تقديم", "متابعة شراكة"),
        proof_required=("تعارف موثق", "لا عمولة غير موثقة", "لا ادعاء صفة رسمية"),
    ),
    ServiceOffer(
        id="b2g_readiness_sprint",
        name_ar="B2G Readiness Sprint",
        department="b2g_readiness",
        stage="sprint",
        price_guidance_sar="10000-50000",
        ideal_for=("supplier", "contractor", "enterprise_vendor", "foreign_company"),
        pain_keywords=("مناقصة", "حكومي", "تأهيل", "توريد", "اعتماد", "tender", "government", "vendor"),
        value_outcomes=("Capability Statement", "Readiness gaps", "Partner mapping", "Proposal checklist"),
        proof_required=("متطلبات عامة موثقة", "لا وعد فوز", "لا ادعاء علاقات حكومية"),
    ),
    ServiceOffer(
        id="ai_company_os_setup",
        name_ar="AI Company OS Setup",
        department="operations",
        stage="implementation",
        price_guidance_sar="5000-25000_plus_retainer",
        ideal_for=("multi_department_company", "manual_operations", "knowledge_heavy_team"),
        pain_keywords=("يدوي", "موظفين", "تقارير", "عمليات", "ذكاء", "automation", "manual", "operations"),
        value_outcomes=("Company Brain", "Action Queue", "Approval Center", "Proof & Learning Loop"),
        proof_required=("نطاق وظائف محدد", "صلاحيات موثقة", "اختبار عدم التنفيذ الخارجي"),
    ),
    ServiceOffer(
        id="executive_command_center",
        name_ar="Executive Command Center",
        department="executive",
        stage="implementation_or_retainer",
        price_guidance_sar="7500_plus",
        ideal_for=("project_company", "multi_site_operations", "leadership_team"),
        pain_keywords=("مشاريع", "مخاطر", "تسليم", "مؤشرات", "إدارة", "executive", "projects", "risk"),
        value_outcomes=("أولويات تنفيذية", "مخاطر وقرارات", "تقارير موحدة", "سجل إثبات"),
        proof_required=("مصدر لكل مؤشر", "مسؤول لكل إجراء", "لا أرقام مختلقة"),
    ),
    ServiceOffer(
        id="operations_automation_os",
        name_ar="Operations Automation OS",
        department="operations",
        stage="implementation",
        price_guidance_sar="scope_based",
        ideal_for=("manufacturing", "logistics", "contracting", "field_service"),
        pain_keywords=("صناعة", "مصنع", "نقل", "شحن", "مقاول", "صيانة", "مخزون", "logistics", "factory"),
        value_outcomes=("مسار استثناءات", "متابعة تنفيذ", "تقارير تشغيل", "أتمتة خاضعة للموافقة"),
        proof_required=("خريطة عملية", "خط أساس زمن/تكلفة", "اختبار استثناءات"),
    ),
    ServiceOffer(
        id="customer_experience_os",
        name_ar="Customer Experience & Inbox OS",
        department="customer_success",
        stage="pilot_or_retainer",
        price_guidance_sar="3000-15000_monthly",
        ideal_for=("clinic", "retail", "hospitality", "service_business"),
        pain_keywords=("عميل", "استفسار", "شكوى", "موعد", "حجز", "مريض", "customer", "support", "booking"),
        value_outcomes=("تصنيف الوارد", "ردود للموافقة", "تصعيد", "تقارير تجربة العميل"),
        proof_required=("سياسة خصوصية", "SLA حقيقي", "إشراف بشري للحالات الحساسة"),
    ),
    ServiceOffer(
        id="offer_negotiation_os",
        name_ar="Proposal & Negotiation OS",
        department="sales",
        stage="add_on",
        price_guidance_sar="scope_based",
        ideal_for=("complex_sales", "proposal_heavy_business", "enterprise_sales"),
        pain_keywords=("عرض", "خصم", "تفاوض", "اعتراض", "عقد", "proposal", "discount", "negotiation"),
        value_outcomes=("One-page offer", "Objection plan", "Give-get ladder", "Approval questions"),
        proof_required=("أسعار وحدود معتمدة", "مصادر العميل", "لا التزام خارجي تلقائي"),
    ),
)


def catalog_by_id(offer_id: str) -> ServiceOffer:
    for offer in SERVICE_CATALOG:
        if offer.id == offer_id:
            return offer
    raise KeyError(f"unknown_service_offer:{offer_id}")


def _normalise_text(parts: Iterable[str]) -> str:
    return " ".join(str(part).casefold().strip() for part in parts if str(part).strip())


def match_services(
    *,
    activity: str,
    city: str = "",
    company_name: str = "",
    signals: Iterable[str] = (),
    limit: int = 4,
) -> tuple[dict[str, Any], ...]:
    text = _normalise_text((company_name, city, activity, *signals))
    scored: list[tuple[int, ServiceOffer, tuple[str, ...]]] = []
    for offer in SERVICE_CATALOG:
        matched = tuple(keyword for keyword in offer.pain_keywords if keyword.casefold() in text)
        score = 30 + min(len(matched) * 12, 48)
        if offer.stage == "entry":
            score += 4
        if city and "الرياض" in city and offer.department in {"market_access", "partnerships"}:
            score += 4
        if not matched:
            score = 24 if offer.id in {"revenue_proof_sprint", "ai_company_os_setup"} else 10
        scored.append((min(score, 100), offer, matched))
    selected = sorted(scored, key=lambda item: (-item[0], item[1].id))[: max(1, min(limit, 8))]
    return tuple(
        {
            "offer_id": offer.id,
            "name_ar": offer.name_ar,
            "department": offer.department,
            "stage": offer.stage,
            "score": score,
            "matched_signals": matched,
            "value_outcomes": offer.value_outcomes,
            "proof_required": offer.proof_required,
            "price_guidance_sar": offer.price_guidance_sar,
        }
        for score, offer, matched in selected
    )


def service_catalog_summary() -> dict[str, Any]:
    return {
        "count": len(SERVICE_CATALOG),
        "departments": sorted({offer.department for offer in SERVICE_CATALOG}),
        "offers": [offer.to_dict() for offer in SERVICE_CATALOG],
        "global_positioning": (
            "Dealix works above existing systems to research, prioritise, draft, coordinate, "
            "measure, and learn across departments; it does not claim to replace every employee "
            "or guarantee outcomes."
        ),
    }
