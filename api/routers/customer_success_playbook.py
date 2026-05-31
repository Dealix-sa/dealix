"""
Customer success playbooks for Dealix managed service clients.

Provides structured playbooks for different client lifecycle stages
(onboarding, value realization, expansion, renewal, churn risk)
with Saudi-specific cultural considerations.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/customer-success", tags=["Analytics"])

# ---------------------------------------------------------------------------
# Lifecycle stages and playbooks
# ---------------------------------------------------------------------------

_PLAYBOOKS: dict[str, dict[str, Any]] = {
    "onboarding": {
        "stage": "onboarding",
        "name_ar": "الإعداد والتأهيل",
        "name_en": "Onboarding",
        "duration": "Days 1–30",
        "goal_en": "Ensure technical deployment, data access, and first value milestone.",
        "goal_ar": "ضمان النشر التقني والوصول للبيانات وتحقيق أول معلم للقيمة.",
        "success_metrics": [
            {"metric": "Time to first dashboard", "target": "≤ 7 business days", "kpi_type": "speed"},
            {"metric": "Data source connections", "target": "≥ 80% of agreed sources", "kpi_type": "coverage"},
            {"metric": "Stakeholder training completion", "target": "100% of named users", "kpi_type": "adoption"},
            {"metric": "First quick win delivered", "target": "By day 30", "kpi_type": "value"},
        ],
        "weekly_actions": [
            {
                "week": 1,
                "actions_en": [
                    "Kick-off call with all stakeholders (CR + technical contact + economic buyer)",
                    "Collect data access credentials and system documentation",
                    "Sign DPA (Data Processing Agreement) per PDPL requirements",
                    "Configure ZATCA webhook if applicable",
                ],
                "actions_ar": [
                    "اجتماع انطلاق مع جميع أصحاب المصلحة (اتصال CR + فني + مشتري اقتصادي)",
                    "جمع بيانات الوصول والوثائق التقنية للأنظمة",
                    "توقيع اتفاقية معالجة البيانات وفق PDPL",
                    "تهيئة webhook هيئة الزكاة إن انطبق",
                ],
            },
            {
                "week": 2,
                "actions_en": [
                    "Complete data pipeline setup and quality assessment",
                    "Deliver preliminary data quality score",
                    "Identify quick win #1 and start execution",
                    "Schedule weekly check-in cadence (avoid prayer times)",
                ],
                "actions_ar": [
                    "إكمال إعداد خط البيانات وتقييم الجودة",
                    "تسليم درجة جودة البيانات الأولية",
                    "تحديد المكسب السريع الأول والبدء في التنفيذ",
                    "جدولة إيقاع الاجتماعات الأسبوعية (تجنب أوقات الصلاة)",
                ],
            },
            {
                "week": 3,
                "actions_en": [
                    "Present first revenue intelligence insights",
                    "Train users on dashboard and key metrics",
                    "Document baseline KPIs for ROI measurement",
                    "Confirm Month 2 roadmap",
                ],
                "actions_ar": [
                    "تقديم أولى رؤى ذكاء الإيرادات",
                    "تدريب المستخدمين على لوحة التحكم والمقاييس الرئيسية",
                    "توثيق KPIs الأساسية لقياس العائد على الاستثمار",
                    "تأكيد خارطة طريق الشهر الثاني",
                ],
            },
            {
                "week": 4,
                "actions_en": [
                    "Deliver Month 1 impact report",
                    "Document first quick win results vs. baseline",
                    "NPS pulse survey (1 question)",
                    "Identify Month 2 expansion opportunity",
                ],
                "actions_ar": [
                    "تسليم تقرير أثر الشهر الأول",
                    "توثيق نتائج المكسب السريع الأول مقارنة بالأساس",
                    "استطلاع NPS السريع (سؤال واحد)",
                    "تحديد فرصة توسع الشهر الثاني",
                ],
            },
        ],
        "saudi_context_en": (
            "Ramadan onboardings: compress weeks 2-3, avoid Eid overlap. "
            "All documentation must be available in Arabic. "
            "Named contacts should have direct WhatsApp line for urgent queries (business hours only)."
        ),
        "saudi_context_ar": (
            "إعداد رمضان: اضغط الأسبوع 2-3، تجنب التداخل مع العيد. "
            "يجب توفير جميع الوثائق بالعربية. "
            "جهات الاتصال المسمّاة يجب أن تمتلك خط واتساب مباشر للاستفسارات العاجلة (ساعات العمل فقط)."
        ),
        "churn_warning_signs": [
            "No login in 7+ days during active onboarding",
            "Key contact changed without notification",
            "Data access not granted by end of week 1",
        ],
    },
    "value_realization": {
        "stage": "value_realization",
        "name_ar": "تحقيق القيمة",
        "name_en": "Value Realization (Months 2–6)",
        "duration": "Days 31–180",
        "goal_en": "Deliver measurable ROI and build executive-level advocacy.",
        "goal_ar": "تحقيق عائد استثمار قابل للقياس وبناء دعم تنفيذي.",
        "success_metrics": [
            {"metric": "Monthly ROI report shared", "target": "100% of months", "kpi_type": "consistency"},
            {"metric": "NPS score", "target": "≥ 8/10", "kpi_type": "satisfaction"},
            {"metric": "Executive sponsor engagement", "target": "Monthly touchpoint", "kpi_type": "relationship"},
            {"metric": "Quick wins documented", "target": "≥ 1 per month", "kpi_type": "value"},
        ],
        "monthly_cadence": [
            "Monthly ROI report (share with CFO/sponsor)",
            "30-minute strategy call with champion",
            "Dashboard refresh and new insight delivery",
            "ZATCA compliance status update",
        ],
        "monthly_cadence_ar": [
            "تقرير العائد الشهري (مشاركة مع المدير المالي/الراعي)",
            "مكالمة استراتيجية 30 دقيقة مع البطل",
            "تحديث لوحة التحكم وتسليم رؤى جديدة",
            "تحديث حالة امتثال هيئة الزكاة",
        ],
        "churn_warning_signs": [
            "ROI report rejected or unread",
            "Champion leaves company",
            "Missed 2+ check-in calls",
            "Negative NPS or formal complaint",
            "Budget holder changed without notice",
        ],
    },
    "expansion": {
        "stage": "expansion",
        "name_ar": "التوسع",
        "name_en": "Expansion",
        "duration": "Month 4+ (whenever ROI > 100%)",
        "goal_en": "Upsell additional use cases or upgrade tier when ROI is demonstrated.",
        "goal_ar": "بيع حالات استخدام إضافية أو ترقية المستوى عند إثبات العائد.",
        "expansion_triggers": [
            "ROI report shows > 150% return",
            "Client adds new business unit or acquires a company",
            "Vision 2030 program win requires new compliance module",
            "Approaching Eid / year-end: budget spend-down window",
        ],
        "expansion_triggers_ar": [
            "تقرير العائد يُظهر > 150% عائد",
            "العميل يضيف وحدة عمل جديدة أو يستحوذ على شركة",
            "فوز ببرنامج رؤية 2030 يتطلب وحدة امتثال جديدة",
            "قرب العيد / نهاية السنة: نافذة استنفاد الميزانية",
        ],
        "upsell_paths": [
            {"from": "sprint", "to": "data_pack", "trigger": "Needs market intelligence"},
            {"from": "sprint", "to": "managed_ops", "trigger": "Wants ongoing support"},
            {"from": "data_pack", "to": "managed_ops", "trigger": "Needs automation, not just data"},
            {"from": "managed_ops", "to": "custom_ai", "trigger": "Ready for bespoke AI build"},
        ],
        "churn_warning_signs": [
            "Client building internal team to replace Dealix",
            "Competitor proposal being evaluated",
            "New CTO/CFO unfamiliar with Dealix value",
        ],
    },
    "renewal": {
        "stage": "renewal",
        "name_ar": "التجديد",
        "name_en": "Renewal",
        "duration": "30–60 days before contract end",
        "goal_en": "Renew before contract expiry with price protection or expansion.",
        "goal_ar": "التجديد قبل انتهاء العقد مع حماية السعر أو التوسع.",
        "renewal_playbook": [
            "60 days out: Send renewal ROI summary — total value delivered YTD",
            "45 days out: Renewal call with economic buyer (not just champion)",
            "30 days out: Share new-year roadmap + Saudi seasonal campaign calendar",
            "14 days out: Final proposal with multi-year discount option",
            "7 days out: Executive sponsor letter from Dealix founder",
        ],
        "renewal_playbook_ar": [
            "60 يوماً: أرسل ملخص العائد للتجديد — إجمالي القيمة المقدمة خلال العام",
            "45 يوماً: مكالمة تجديد مع المشتري الاقتصادي (ليس البطل فحسب)",
            "30 يوماً: مشاركة خارطة طريق السنة الجديدة + تقويم الحملات الموسمية السعودية",
            "14 يوماً: مقترح نهائي مع خيار خصم متعدد السنوات",
            "7 أيام: رسالة من مؤسس ديليكس لراعي التنفيذ",
        ],
        "saudi_timing_en": (
            "Avoid renewal conversations in Ramadan (weeks 1-3) and 2 weeks pre-Eid. "
            "Best renewal window: September–November (post-National Day budget cycle) "
            "and January–February (post-Founding Day, new FY budgets)."
        ),
        "saudi_timing_ar": (
            "تجنب محادثات التجديد في رمضان (الأسبوع 1-3) وأسبوعين قبل العيد. "
            "أفضل نوافذ التجديد: سبتمبر–نوفمبر (دورة ميزانية ما بعد اليوم الوطني) "
            "ويناير–فبراير (ما بعد يوم التأسيس، ميزانيات السنة المالية الجديدة)."
        ),
        "churn_warning_signs": [
            "No renewal conversation started by day 45",
            "Procurement putting deal to re-tender",
            "Economic buyer unavailable for renewal meeting",
        ],
    },
    "churn_risk": {
        "stage": "churn_risk",
        "name_ar": "مخاطر الإلغاء",
        "name_en": "Churn Risk Mitigation",
        "duration": "Activated when 2+ warning signs present",
        "goal_en": "Identify churn risk early and execute recovery plan within 30 days.",
        "goal_ar": "الكشف المبكر عن مخاطر الإلغاء وتنفيذ خطة الاسترداد خلال 30 يوماً.",
        "risk_signals": [
            {"signal": "Login frequency drops >50%", "urgency": "high"},
            {"signal": "Champion leaves company", "urgency": "critical"},
            {"signal": "Missed 2 check-in calls", "urgency": "medium"},
            {"signal": "Complaint escalated to founder", "urgency": "critical"},
            {"signal": "No ROI report engagement for 30 days", "urgency": "medium"},
            {"signal": "New competitor POC running", "urgency": "high"},
            {"signal": "Budget frozen / company restructuring", "urgency": "high"},
        ],
        "recovery_actions": [
            "Immediate executive sponsor call (Dealix founder to EB directly)",
            "Deliver surprise quick win within 7 days",
            "Identify new internal champion if old one left",
            "Offer a 30-day pause (not cancellation) for budget issues",
            "Schedule on-site visit if relationship at risk",
        ],
        "recovery_actions_ar": [
            "مكالمة فورية مع راعي التنفيذ (مؤسس ديليكس مباشرة للمشتري الاقتصادي)",
            "تسليم مكسب سريع مفاجئ خلال 7 أيام",
            "تحديد بطل داخلي جديد إذا غادر القديم",
            "تقديم إيقاف مؤقت لمدة 30 يوماً (وليس إلغاء) لمشاكل الميزانية",
            "جدولة زيارة ميدانية إذا كانت العلاقة في خطر",
        ],
        "churn_warning_signs": [],
    },
}


# ---------------------------------------------------------------------------
# Health scoring
# ---------------------------------------------------------------------------

class AccountHealthInput(BaseModel):
    account_name: str = Field(..., max_length=100)
    months_active: int = Field(..., ge=1)
    last_login_days_ago: int = Field(..., ge=0)
    nps_score: float = Field(..., ge=0, le=10)
    roi_reports_opened_pct: float = Field(..., ge=0, le=100)
    check_ins_missed_last_30d: int = Field(..., ge=0)
    champion_active: bool = Field(...)
    competitor_poc_running: bool = Field(False)


def _health_score(inp: AccountHealthInput) -> dict[str, Any]:
    score = 100
    risks: list[str] = []

    if inp.last_login_days_ago > 14:
        score -= 25
        risks.append("No login in 14+ days")
    elif inp.last_login_days_ago > 7:
        score -= 10
        risks.append("No login in 7-14 days")

    if inp.nps_score < 7:
        score -= 20
        risks.append(f"Low NPS ({inp.nps_score:.1f}/10)")
    elif inp.nps_score < 8:
        score -= 5

    if inp.roi_reports_opened_pct < 50:
        score -= 15
        risks.append(f"Low report engagement ({inp.roi_reports_opened_pct:.0f}%)")

    if inp.check_ins_missed_last_30d >= 2:
        score -= 20
        risks.append(f"{inp.check_ins_missed_last_30d} missed check-ins in 30 days")

    if not inp.champion_active:
        score -= 20
        risks.append("Champion no longer active")

    if inp.competitor_poc_running:
        score -= 15
        risks.append("Competitor POC in progress")

    score = max(score, 0)

    band = (
        "Healthy" if score >= 80
        else "At Risk" if score >= 60
        else "Critical" if score >= 40
        else "Churning"
    )

    recommended_stage = "churn_risk" if score < 60 else ("expansion" if score >= 85 else "value_realization")

    return {
        "account_name": inp.account_name,
        "health_score": score,
        "health_band": band,
        "risk_factors": risks,
        "recommended_playbook_stage": recommended_stage,
        "immediate_action_needed": score < 60,
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/stages", summary="Customer success lifecycle stages")
async def list_stages() -> dict[str, Any]:
    return {
        "stages": [
            {
                "stage": k,
                "name_ar": v["name_ar"],
                "name_en": v["name_en"],
                "duration": v["duration"],
                "goal_en": v["goal_en"],
                "goal_ar": v["goal_ar"],
            }
            for k, v in _PLAYBOOKS.items()
        ],
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/playbook/{stage}", summary="Full playbook for a lifecycle stage")
async def get_playbook(stage: str) -> dict[str, Any]:
    playbook = _PLAYBOOKS.get(stage)
    if not playbook:
        raise HTTPException(
            status_code=404,
            detail=f"Stage '{stage}' not found. Valid: {list(_PLAYBOOKS.keys())}",
        )
    return {
        **playbook,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/health-score", summary="Score account health and identify churn risk")
async def score_account_health(body: AccountHealthInput) -> dict[str, Any]:
    result = _health_score(body)
    playbook = _PLAYBOOKS.get(result["recommended_playbook_stage"])
    return {
        **result,
        "playbook_name_en": playbook["name_en"] if playbook else None,
        "playbook_name_ar": playbook["name_ar"] if playbook else None,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
