"""
Saudi B2B prospect intelligence library for Dealix.

Provides ICP (Ideal Customer Profile) definitions, trigger event monitoring
frameworks, and prospect qualification scoring — all based on Saudi market
context. No scraping, no automation, no cold outreach automation.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, model_validator

router = APIRouter(prefix="/api/v1/prospect-intelligence", tags=["Sales"])

# ---------------------------------------------------------------------------
# Ideal Customer Profiles
# ---------------------------------------------------------------------------

_ICP_PROFILES: dict[str, Any] = {
    "saudi_sme_growth": {
        "profile_name_en": "Saudi SME — Growth Stage",
        "profile_name_ar": "المنشآت الصغيرة والمتوسطة السعودية — مرحلة النمو",
        "description_en": (
            "50–300 employees, SAR 5M–50M annual revenue, "
            "experiencing manual reporting pain, "
            "Saudization pressure (Yellow/Low Green Nitaqat band), "
            "ZATCA Phase 2 recently triggered."
        ),
        "description_ar": (
            "50–300 موظف، إيرادات سنوية 5–50 مليون ريال، "
            "يعاني من ألم التقارير اليدوية، "
            "ضغط السعودة (نطاق أصفر / أخضر منخفض)، "
            "اكتسب مؤخراً المرحلة الثانية من هيئة الزكاة."
        ),
        "firmographic_criteria": {
            "employees_min": 50,
            "employees_max": 300,
            "annual_revenue_sar_min": 5_000_000,
            "annual_revenue_sar_max": 50_000_000,
            "company_age_years_min": 3,
            "geography": "Saudi Arabia",
        },
        "trigger_events_en": [
            "Recently triggered ZATCA Phase 2 (company size milestone)",
            "Hired a new CFO or COO in last 6 months",
            "Recently received VC or Series A funding",
            "Joined Monsha'at / Badir accelerator cohort",
            "Nitaqat band dropped to Yellow",
        ],
        "disqualifiers_en": [
            "Less than 3 years old (unlikely to have budget stability)",
            "Operating in sunset industries without Vision 2030 alignment",
            "No identified champion with C-suite access",
        ],
        "best_entry_product": "sprint",
        "avg_deal_size_sar": 2_999,
        "sales_cycle_days": 21,
    },
    "saudi_enterprise": {
        "profile_name_en": "Saudi Enterprise — Digital Transformation",
        "profile_name_ar": "المؤسسات السعودية الكبيرة — التحول الرقمي",
        "description_en": (
            "300–5,000 employees, SAR 50M–2B annual revenue, "
            "running digital transformation programs, "
            "Vision 2030 reporting requirements, "
            "complex multi-stakeholder decisions."
        ),
        "description_ar": (
            "300–5,000 موظف، إيرادات سنوية 50 مليون–2 مليار ريال، "
            "يتبنى برامج تحول رقمي، "
            "متطلبات تقارير رؤية 2030، "
            "قرارات معقدة متعددة أصحاب المصلحة."
        ),
        "firmographic_criteria": {
            "employees_min": 300,
            "employees_max": 5_000,
            "annual_revenue_sar_min": 50_000_000,
            "annual_revenue_sar_max": 2_000_000_000,
            "company_age_years_min": 5,
            "geography": "Saudi Arabia",
        },
        "trigger_events_en": [
            "Digital transformation budget allocated (typically Q1 or post-National Day)",
            "New CTO, CDO, or Chief AI Officer hired",
            "LEAP conference presentation or participation",
            "Partnership with NEOM, PIF portfolio company",
            "Board mandate for AI adoption / Vision 2030 KPI reporting",
        ],
        "disqualifiers_en": [
            "Fully locked to SAP/Oracle with zero appetite for AI layering",
            "Government procurement process taking >18 months",
            "No internal champion willing to sponsor a pilot",
        ],
        "best_entry_product": "custom_ai",
        "avg_deal_size_sar": 25_000,
        "sales_cycle_days": 90,
    },
    "sama_regulated_fintech": {
        "profile_name_en": "SAMA-Regulated FinTech",
        "profile_name_ar": "شركات التقنية المالية المرخصة من ساما",
        "description_en": (
            "10–200 employees, SAR 2M–20M revenue, "
            "SAMA sandbox license, Islamic finance compliance, "
            "high regulatory reporting burden, "
            "need for automated compliance + revenue analytics."
        ),
        "description_ar": (
            "10–200 موظف، إيرادات 2–20 مليون ريال، "
            "رخصة بيئة اختبار ساما، امتثال التمويل الإسلامي، "
            "عبء تقارير تنظيمية عالية، "
            "حاجة لأتمتة الامتثال + تحليلات الإيرادات."
        ),
        "firmographic_criteria": {
            "employees_min": 10,
            "employees_max": 200,
            "annual_revenue_sar_min": 2_000_000,
            "annual_revenue_sar_max": 20_000_000,
            "company_age_years_min": 1,
            "geography": "Saudi Arabia",
        },
        "trigger_events_en": [
            "SAMA license upgrade or new product approval",
            "Post-Series A looking to scale B2B revenue operations",
            "Compliance team growing (new Head of Compliance hire)",
            "Saudi FinTech Forum attendance",
        ],
        "disqualifiers_en": [
            "B2C only — no B2B revenue stream",
            "SAMA license pending — too early stage",
        ],
        "best_entry_product": "data_pack",
        "avg_deal_size_sar": 8_000,
        "sales_cycle_days": 30,
    },
}

# ---------------------------------------------------------------------------
# Trigger event framework
# ---------------------------------------------------------------------------

_TRIGGER_EVENT_CATEGORIES: list[dict[str, Any]] = [
    {
        "category": "leadership_change",
        "name_en": "Leadership Change",
        "name_ar": "تغيير القيادة",
        "description_en": "New C-suite or VP hire creates a 90-day window to influence strategy.",
        "examples_en": ["New CFO", "New CTO", "New Chief Digital Officer", "New CEO"],
        "sales_implication_en": "New leaders often want to make their mark — ideal window for new vendor introductions.",
        "urgency": "high",
    },
    {
        "category": "compliance_deadline",
        "name_en": "Compliance Deadline",
        "name_ar": "موعد الامتثال",
        "description_en": "ZATCA phase triggers, Nitaqat band changes, PDPL enforcement dates.",
        "examples_en": ["ZATCA Phase 2 triggered", "Nitaqat band dropped to Yellow", "PDPL deadline approaching"],
        "sales_implication_en": "Compliance deadlines create urgency without you needing to manufacture it.",
        "urgency": "critical",
    },
    {
        "category": "funding_event",
        "name_en": "Funding Event",
        "name_ar": "حدث تمويل",
        "description_en": "Series A/B/C, PIF investment, or government grant creates budget signal.",
        "examples_en": ["Series A closed", "PIF co-investment", "Monsha'at grant received"],
        "sales_implication_en": "Post-funding companies are actively investing in operations — budget is available.",
        "urgency": "high",
    },
    {
        "category": "expansion_signal",
        "name_en": "Expansion Signal",
        "name_ar": "إشارة التوسع",
        "description_en": "Hiring surges, new office openings, market entry announcements.",
        "examples_en": ["50+ new job postings", "New Riyadh office opened", "Regional expansion announced"],
        "sales_implication_en": "Rapid growth strains existing systems — ideal Dealix entry point.",
        "urgency": "medium",
    },
    {
        "category": "tech_change",
        "name_en": "Technology Change",
        "name_ar": "تغيير تقني",
        "description_en": "CRM migration, ERP upgrade, cloud migration project.",
        "examples_en": ["Migrating from Zoho to Salesforce", "SAP upgrade in progress", "Moving to cloud"],
        "sales_implication_en": "System transitions create openings for adjacent tools like Dealix.",
        "urgency": "medium",
    },
]

# ---------------------------------------------------------------------------
# ICP qualification model
# ---------------------------------------------------------------------------


class ICPQualificationInput(BaseModel):
    company_name: str = Field(..., min_length=2)
    sector: str
    employee_count: int = Field(..., ge=1)
    annual_revenue_sar: float = Field(..., ge=0)
    has_zatca_phase2: bool = False
    has_identified_champion: bool = False
    has_budget_signal: bool = False
    has_trigger_event: bool = False
    nitaqat_band: str = "unknown"
    months_since_last_funding: int = Field(default=999, ge=0)


def _qualify_prospect(inp: ICPQualificationInput) -> dict[str, Any]:
    score = 0
    signals: list[str] = []
    gaps: list[str] = []

    # Size fit (25 pts)
    if 50 <= inp.employee_count <= 5000:
        score += 25
        signals.append(f"Employee count {inp.employee_count} within ICP range")
    elif inp.employee_count < 50:
        score += 10
        gaps.append("Below 50 employees — may lack budget; consider free diagnostic only")
    else:
        score += 20

    # Revenue fit (20 pts)
    if inp.annual_revenue_sar >= 5_000_000:
        score += 20
        signals.append("Revenue above SAR 5M minimum threshold")
    elif inp.annual_revenue_sar >= 1_000_000:
        score += 10
        gaps.append("Revenue below SAR 5M — managed ops may be stretch; sprint is right fit")

    # Trigger events (20 pts)
    if inp.has_zatca_phase2:
        score += 10
        signals.append("ZATCA Phase 2 is an active compliance trigger")
    if inp.has_trigger_event:
        score += 10
        signals.append("Active trigger event increases urgency")

    # Sales readiness (20 pts)
    if inp.has_identified_champion:
        score += 10
        signals.append("Internal champion identified")
    else:
        gaps.append("No champion identified — discovery required before advancing")
    if inp.has_budget_signal:
        score += 10
        signals.append("Budget signal confirmed")
    else:
        gaps.append("No budget signal — use free diagnostic to qualify budget")

    # Recent funding (15 pts)
    if inp.months_since_last_funding <= 12:
        score += 15
        signals.append(f"Funded {inp.months_since_last_funding} months ago — budget available")
    elif inp.months_since_last_funding <= 24:
        score += 8

    qual_level = (
        "Strong ICP" if score >= 70
        else "Moderate ICP" if score >= 45
        else "Weak ICP"
    )

    recommended_action = (
        "Book discovery call this week"
        if score >= 70
        else "Run free diagnostic to build case and qualify budget"
        if score >= 45
        else "Nurture with content; revisit in 30–60 days"
    )

    return {
        "company_name": inp.company_name,
        "qualification_score": score,
        "qualification_level_en": qual_level,
        "recommended_action_en": recommended_action,
        "signals": signals,
        "gaps": gaps,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/icp-profiles", summary="Ideal Customer Profile definitions")
async def get_icp_profiles() -> dict[str, Any]:
    return {
        "profiles": {
            k: {
                "profile_name_en": v["profile_name_en"],
                "profile_name_ar": v["profile_name_ar"],
                "description_en": v["description_en"],
                "best_entry_product": v["best_entry_product"],
                "avg_deal_size_sar": v["avg_deal_size_sar"],
                "sales_cycle_days": v["sales_cycle_days"],
            }
            for k, v in _ICP_PROFILES.items()
        },
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/icp-profiles/{profile_id}", summary="Full ICP profile detail")
async def get_icp_profile(profile_id: str) -> dict[str, Any]:
    profile = _ICP_PROFILES.get(profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail=f"ICP profile '{profile_id}' not found.")
    return {**profile, "profile_id": profile_id, "governance_decision": "ALLOW_WITH_REVIEW"}


@router.get("/trigger-events", summary="Saudi B2B trigger event categories")
async def get_trigger_events(
    urgency: str | None = Query(None, description="Filter by urgency: critical | high | medium"),
) -> dict[str, Any]:
    events = _TRIGGER_EVENT_CATEGORIES
    if urgency is not None:
        events = [e for e in _TRIGGER_EVENT_CATEGORIES if e.get("urgency") == urgency]
    return {
        "trigger_events": events,
        "total": len(events),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/qualify", summary="Qualify a prospect against Dealix ICP")
async def qualify_prospect(inp: ICPQualificationInput) -> dict[str, Any]:
    return _qualify_prospect(inp)
