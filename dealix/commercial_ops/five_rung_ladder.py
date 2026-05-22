"""
Five-Rung Commercial Ladder — Dealix's core service offer management.
Maps each rung to pricing, deliverables, qualification gates, and upgrade paths.
SAR pricing anchored to Saudi SME market; no guaranteed-outcome language.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

OfferTier = Literal["free_diagnostic", "sprint_499", "data_pack_1500", "managed_ops", "custom_ai"]

OFFER_LADDER: list[dict] = [
    {
        "rung": 0,
        "tier": "free_diagnostic",
        "name_ar": "تشخيص مجاني",
        "name_en": "Free Diagnostic",
        "price_sar": 0,
        "price_display": "مجاناً",
        "duration": "45 دقيقة",
        "deliverables_ar": [
            "تقرير DQ Score (0-100)",
            "خريطة فجوات البيانات",
            "توصيات أولوية (3 نقاط)",
            "تقييم جاهزية الذكاء الاصطناعي",
        ],
        "deliverables_en": [
            "DQ Score report (0-100)",
            "Data gap map",
            "Priority recommendations (3 points)",
            "AI readiness assessment",
        ],
        "qualification_gates": ["company_exists", "owner_reachable"],
        "upgrade_to": "sprint_499",
        "upgrade_trigger": "DQ score < 70 or owner expresses pain",
        "ltv_weight": 0.0,
        "conversion_rate_target": 0.40,
    },
    {
        "rung": 1,
        "tier": "sprint_499",
        "name_ar": "سبرنت ذكاء الإيرادات",
        "name_en": "Revenue Intelligence Sprint",
        "price_sar": 499,
        "price_display": "499 ريال",
        "duration": "7 أيام",
        "deliverables_ar": [
            "Source Passport كامل",
            "تقرير جودة البيانات المفصل",
            "تسجيل 5 أصول معرفية",
            "حزمة الدليل (Proof Pack) أولية",
            "خطة تشغيل 30 يوم",
        ],
        "deliverables_en": [
            "Full Source Passport",
            "Detailed DQ report",
            "5 knowledge asset registrations",
            "Initial Proof Pack",
            "30-day ops plan",
        ],
        "qualification_gates": [
            "company_has_data",
            "owner_committed_7_days",
            "moyasar_payment_confirmed",
        ],
        "upgrade_to": "data_pack_1500",
        "upgrade_trigger": "Sprint complete + owner sees value + data volume > 500 records",
        "ltv_weight": 0.05,
        "conversion_rate_target": 0.60,
    },
    {
        "rung": 2,
        "tier": "data_pack_1500",
        "name_ar": "حزمة البيانات والأتمتة",
        "name_en": "Data & Automation Pack",
        "price_sar": 1500,
        "price_display": "1,500 ريال",
        "duration": "14 يوم",
        "deliverables_ar": [
            "تنظيف وتحويل البيانات الكامل",
            "لوحة تحكم تفاعلية مخصصة",
            "3 تدفقات أتمتة مُهيأة",
            "تقرير رأس المال البياني",
            "نقل المعرفة (جلستان)",
        ],
        "deliverables_en": [
            "Full data cleaning & transformation",
            "Custom interactive dashboard",
            "3 configured automation flows",
            "Data capital report",
            "Knowledge transfer (2 sessions)",
        ],
        "qualification_gates": [
            "sprint_499_completed",
            "data_volume_sufficient",
            "owner_has_use_case",
            "moyasar_payment_confirmed",
        ],
        "upgrade_to": "managed_ops",
        "upgrade_trigger": "Owner wants ongoing support or automation expansion",
        "ltv_weight": 0.10,
        "conversion_rate_target": 0.50,
    },
    {
        "rung": 3,
        "tier": "managed_ops",
        "name_ar": "العمليات المُدارة شهرياً",
        "name_en": "Managed Monthly Ops",
        "price_sar_min": 2999,
        "price_sar_max": 4999,
        "price_display": "2,999 – 4,999 ريال / شهر",
        "duration": "شهري (التزام 3 أشهر كحد أدنى)",
        "deliverables_ar": [
            "مدير عمليات ذكاء اصطناعي مخصص",
            "تقارير أسبوعية تلقائية",
            "مراقبة البيانات على مدار الساعة",
            "4 اجتماعات استراتيجية / شهر",
            "أولوية دعم فني (SLA 24 ساعة)",
            "تطوير مستمر للأتمتة",
        ],
        "deliverables_en": [
            "Dedicated AI operations manager",
            "Automated weekly reports",
            "24/7 data monitoring",
            "4 strategy sessions/month",
            "Priority support (24h SLA)",
            "Continuous automation development",
        ],
        "qualification_gates": [
            "data_pack_completed_or_equivalent",
            "monthly_budget_confirmed",
            "3_month_commitment_signed",
            "moyasar_subscription_active",
        ],
        "upgrade_to": "custom_ai",
        "upgrade_trigger": "Company revenue > 5M SAR/year or needs custom AI model",
        "ltv_weight": 0.35,
        "conversion_rate_target": 0.40,
    },
    {
        "rung": 4,
        "tier": "custom_ai",
        "name_ar": "الذكاء الاصطناعي المخصص",
        "name_en": "Custom AI Build",
        "price_sar_min": 5000,
        "price_sar_max": 25000,
        "price_display": "5,000 – 25,000 ريال",
        "duration": "4-12 أسبوع (حسب النطاق)",
        "deliverables_ar": [
            "نموذج ذكاء اصطناعي مُدرَّب على بيانات الشركة",
            "واجهة برمجية (API) خاصة",
            "توثيق فني كامل",
            "تدريب الفريق (حتى 5 مستخدمين)",
            "ضمان صيانة 6 أشهر",
            "شهادة SOC 2 جاهزة (إن طُلب)",
        ],
        "deliverables_en": [
            "AI model trained on company data",
            "Private API integration",
            "Complete technical documentation",
            "Team training (up to 5 users)",
            "6-month maintenance warranty",
            "SOC 2-ready audit trail (if requested)",
        ],
        "qualification_gates": [
            "managed_ops_6_months_or_strong_brief",
            "technical_poc_approved",
            "budget_5k_plus_confirmed",
            "nda_signed",
            "scoping_doc_approved",
        ],
        "upgrade_to": None,
        "upgrade_trigger": None,
        "ltv_weight": 0.50,
        "conversion_rate_target": 0.25,
    },
]


@dataclass
class LadderContext:
    current_tier: OfferTier
    months_active: int
    total_paid_sar: float
    data_volume_records: int = 0
    nps_score: int | None = None
    support_tickets_open: int = 0
    last_interaction_days: int = 0


def get_offer(tier: OfferTier) -> dict:
    for offer in OFFER_LADDER:
        if offer["tier"] == tier:
            return offer
    raise KeyError(f"Unknown tier: {tier}")


def recommend_upgrade(ctx: LadderContext) -> dict:
    """Return upgrade recommendation and readiness score (0-100)."""
    current = get_offer(ctx.current_tier)
    next_tier = current.get("upgrade_to")
    if not next_tier:
        return {"recommended": False, "reason": "Already at highest tier"}

    next_offer = get_offer(next_tier)
    readiness = 0
    blockers: list[str] = []
    accelerators: list[str] = []

    # Base readiness from time active
    if ctx.months_active >= 1:
        readiness += 20
    if ctx.months_active >= 3:
        readiness += 15
        accelerators.append("Established relationship (3+ months)")

    # NPS signal
    if ctx.nps_score is not None:
        if ctx.nps_score >= 8:
            readiness += 25
            accelerators.append("High NPS — strong satisfaction signal")
        elif ctx.nps_score >= 6:
            readiness += 10
        else:
            blockers.append("Low NPS — address concerns before upgrade pitch")

    # Engagement signal
    if ctx.last_interaction_days <= 7:
        readiness += 15
        accelerators.append("Active engagement this week")
    elif ctx.last_interaction_days > 30:
        blockers.append("No interaction in 30+ days — re-engage first")
        readiness -= 10

    # Data volume (relevant for data pack upgrades)
    if ctx.data_volume_records >= 500:
        readiness += 15
        accelerators.append(f"Data volume ready ({ctx.data_volume_records:,} records)")

    # Support ticket health
    if ctx.support_tickets_open == 0:
        readiness += 10
    elif ctx.support_tickets_open >= 3:
        blockers.append("Open support tickets — resolve before upgrade")
        readiness -= 15

    readiness = max(0, min(100, readiness))
    ready = readiness >= 65 and len(blockers) == 0

    return {
        "recommended": ready,
        "readiness_score": readiness,
        "current_tier": ctx.current_tier,
        "next_tier": next_tier,
        "next_offer_name_ar": next_offer["name_ar"],
        "next_price_display": next_offer.get("price_display", ""),
        "accelerators": accelerators,
        "blockers": blockers,
        "trigger": current.get("upgrade_trigger", ""),
    }


def calculate_pipeline_value(active_clients_by_tier: dict[OfferTier, int]) -> dict:
    """Calculate total pipeline value and LTV breakdown."""
    total_mrr = 0.0
    total_ltv = 0.0
    breakdown: list[dict] = []

    for tier, count in active_clients_by_tier.items():
        offer = get_offer(tier)
        price = offer.get("price_sar") or offer.get("price_sar_min", 0)
        mrr = price * count
        # Estimated 24-month LTV
        ltv = price * 24 * offer["ltv_weight"] * count
        total_mrr += mrr
        total_ltv += ltv
        breakdown.append({
            "tier": tier,
            "name_ar": offer["name_ar"],
            "count": count,
            "mrr_sar": mrr,
            "ltv_24m_sar": ltv,
        })

    return {
        "total_mrr_sar": total_mrr,
        "total_arr_sar": total_mrr * 12,
        "total_ltv_24m_sar": total_ltv,
        "breakdown": breakdown,
    }


def get_upgrade_path_for_all() -> list[dict]:
    """Return the full upgrade path visualization for the ladder."""
    path = []
    for offer in OFFER_LADDER:
        path.append({
            "rung": offer["rung"],
            "tier": offer["tier"],
            "name_ar": offer["name_ar"],
            "name_en": offer["name_en"],
            "price_display": offer.get("price_display", ""),
            "conversion_rate_target": offer["conversion_rate_target"],
            "upgrade_to": offer.get("upgrade_to"),
        })
    return path
