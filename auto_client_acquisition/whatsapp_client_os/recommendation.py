"""WhatsApp Client OS — service recommendation.

Maps readiness signals to a single best next offer from the canonical
``service_catalog`` registry (no invented offers, no invented prices). Every
recommendation is tied to the product catalog and an evidence level, per the
non-negotiables. Recommendations are estimates, never guarantees.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.service_catalog import get_offering
from auto_client_acquisition.whatsapp_client_os.schemas import EvidenceLevel

# Canonical offer ids (must exist in service_catalog.registry).
OFFER_FREE_DIAGNOSTIC = "free_mini_diagnostic"
OFFER_SPRINT = "revenue_proof_sprint_499"
OFFER_DATA_PACK = "data_to_revenue_pack_1500"
OFFER_GROWTH_OPS = "growth_ops_monthly_2999"


@dataclass(frozen=True, slots=True)
class OfferRecommendation:
    offer_id: str
    name_ar: str
    name_en: str
    reason_ar: str
    reason_en: str
    plan_steps_ar: tuple[str, ...]
    evidence_level: str


def _offer_names(offer_id: str) -> tuple[str, str]:
    offering = get_offering(offer_id)
    if offering is None:  # defensive — keeps the layer honest if a id drifts
        return (offer_id, offer_id)
    return (offering.name_ar, offering.name_en)


def recommend_offer(
    *,
    axis_scores: dict[str, int],
    risk: str = "medium",
) -> OfferRecommendation:
    """Pick the single best starting offer from readiness axis scores.

    Decision order (first match wins):
    1. Very low lead flow / unknown footing -> Free Mini Diagnostic.
    2. Leads exist but follow-up is weak -> 499 Revenue Proof Sprint.
    3. Leads exist but data is messy -> Data-to-Revenue Pack.
    4. Ready for an ongoing operating system -> Growth Ops Monthly.
    5. Default -> Free Mini Diagnostic.
    """
    lead_flow = int(axis_scores.get("lead_flow", 0))
    follow_up = int(axis_scores.get("follow_up_maturity", 0))
    data_readiness = int(axis_scores.get("data_readiness", 0))
    automation = int(axis_scores.get("automation_readiness", 0))
    budget = int(axis_scores.get("budget_fit", 0))

    if lead_flow < 40:
        offer_id = OFFER_FREE_DIAGNOSTIC
        reason_ar = "تدفّق الاستفسارات غير واضح بعد — نبدأ بتشخيص مجاني يحدد نقطة الانطلاق."
        reason_en = "Lead flow is still unclear — start with a free diagnostic to set the baseline."
        plan = (
            "تشخيص مجاني خلال ٢٤ ساعة",
            "توصية بأفضل بداية",
            "قرار الخطوة التالية",
        )
        evidence = EvidenceLevel.L1.value
    elif follow_up < 50:
        offer_id = OFFER_SPRINT
        reason_ar = "عندكم استفسارات لكن المتابعة ضعيفة — سبرنت ٧ أيام يثبت القيمة باسترجاع الفرص."
        reason_en = "You have leads but weak follow-up — a 7-day sprint proves value by recovering opportunities."
        plan = (
            "خريطة تسرّب الفرص",
            "أول workflow متابعة",
            "Draft Pack عربي",
            "Proof Pack",
        )
        evidence = EvidenceLevel.L2.value
    elif data_readiness < 50:
        offer_id = OFFER_DATA_PACK
        reason_ar = "البيانات مبعثرة — حزمة من البيانات إلى الإيراد تنظّف وتصنّف وتستخرج الفرص."
        reason_en = "Data is scattered — the Data-to-Revenue Pack cleans, scores, and surfaces opportunities."
        plan = (
            "لوحة Leads نظيفة",
            "تقرير تكرارات ومصادر",
            "أعلى ٢٠ فرصة مُقيّمة",
            "مسودات عربية",
        )
        evidence = EvidenceLevel.L2.value
    elif automation >= 50 and budget >= 50:
        offer_id = OFFER_GROWTH_OPS
        reason_ar = "جاهزون لنظام تشغيل مستمر — عمليات نمو شهرية بتقارير proof متكررة."
        reason_en = (
            "Ready for an ongoing system — monthly growth ops with recurring proof reporting."
        )
        plan = (
            "تدقيق pipeline أسبوعي",
            "قائمة موافقات يومية",
            "Draft Pack شهري",
            "Proof Pack شهري",
        )
        evidence = EvidenceLevel.L2.value
    else:
        offer_id = OFFER_FREE_DIAGNOSTIC
        reason_ar = "أفضل بداية آمنة هي تشخيص مجاني يحدّد الأولوية قبل أي التزام."
        reason_en = (
            "The safest start is a free diagnostic that sets priority before any commitment."
        )
        plan = (
            "تشخيص مجاني",
            "توصية بأفضل بداية",
            "قرار الخطوة التالية",
        )
        evidence = EvidenceLevel.L1.value

    name_ar, name_en = _offer_names(offer_id)
    if risk == "high":
        reason_ar += " (حساسية بيانات مرتفعة — نبدأ بنطاق محدود وموافقات واضحة.)"
        reason_en += " (High data sensitivity — start with a narrow scope and explicit approvals.)"

    return OfferRecommendation(
        offer_id=offer_id,
        name_ar=name_ar,
        name_en=name_en,
        reason_ar=reason_ar,
        reason_en=reason_en,
        plan_steps_ar=plan,
        evidence_level=evidence,
    )


__all__ = [
    "OFFER_DATA_PACK",
    "OFFER_FREE_DIAGNOSTIC",
    "OFFER_GROWTH_OPS",
    "OFFER_SPRINT",
    "OfferRecommendation",
    "recommend_offer",
]
