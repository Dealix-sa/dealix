"""
Saudi SME accelerator intelligence — Vision 2030 SME programs, funding
readiness scoring, and high-growth sector guidance.

Data sourced from public Monsha'at / SMEF / Kafalah program documentation.
No funding guarantees; scores are indicative only.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/sme-accelerator", tags=["Saudi Market"])

# ---------------------------------------------------------------------------
# Saudi SME program database
# ---------------------------------------------------------------------------

_PROGRAMS: dict[str, dict[str, Any]] = {
    "monshaat_advisory": {
        "id": "monshaat_advisory",
        "name_ar": "الاستشارات المجانية — منشآت",
        "name_en": "Monsha'at Free Advisory Services",
        "provider_ar": "الهيئة العامة للمنشآت الصغيرة والمتوسطة",
        "provider_en": "General Authority for Small and Medium Enterprises (Monsha'at)",
        "type": "advisory",
        "funding_range_sar": None,
        "eligibility_criteria": [
            "Saudi-registered entity (CR required)",
            "At least 1 Saudi employee",
            "Annual revenue under SAR 200M",
        ],
        "benefits_en": [
            "Free business advisory sessions",
            "Access to certified business advisors",
            "Strategic planning workshops",
            "Market entry guidance",
        ],
        "benefits_ar": [
            "جلسات استشارية مجانية",
            "وصول إلى مستشارين أعمال معتمدين",
            "ورش تخطيط استراتيجي",
            "توجيه دخول الأسواق",
        ],
        "vision2030_pillar": "Thriving Economy",
        "url_ref": "https://www.monshaat.gov.sa",
    },
    "kafalah": {
        "id": "kafalah",
        "name_ar": "برنامج كفالة",
        "name_en": "Kafalah SME Loan Guarantee Program",
        "provider_ar": "الصندوق السعودي للتنمية الصناعية",
        "provider_en": "Saudi Industrial Development Fund (SIDF) / Kafalah",
        "type": "loan_guarantee",
        "funding_range_sar": {"min": 50_000, "max": 5_000_000},
        "eligibility_criteria": [
            "Saudi-registered LLC or sole proprietorship",
            "Minimum 2 years of operation",
            "Positive cash flow for latest 12 months",
            "No active NPL in SAMA records",
            "Saudization rate ≥ minimum Nitaqat band (Green)",
        ],
        "benefits_en": [
            "Loan guarantee up to 80% of principal",
            "Access to participating Saudi banks",
            "Reduced collateral requirements",
        ],
        "benefits_ar": [
            "ضمان قرض حتى 80% من المبلغ الأصلي",
            "وصول لبنوك سعودية مشاركة",
            "متطلبات ضمانات مخفضة",
        ],
        "vision2030_pillar": "Thriving Economy",
        "url_ref": "https://www.kafalah.com.sa",
    },
    "smef": {
        "id": "smef",
        "name_ar": "صندوق المنشآت الصغيرة والمتوسطة",
        "name_en": "Small and Medium Enterprises Fund (SMEF)",
        "provider_ar": "صندوق المنشآت الصغيرة والمتوسطة",
        "provider_en": "SMEF",
        "type": "equity_investment",
        "funding_range_sar": {"min": 500_000, "max": 50_000_000},
        "eligibility_criteria": [
            "Saudi entity with ≥ 51% Saudi ownership",
            "Scalable business model with clear market fit",
            "Experienced founding team",
            "Financial statements for ≥ 1 year",
        ],
        "benefits_en": [
            "Equity investment (minority stake)",
            "Board advisory support",
            "Network introductions to Saudi corporates",
        ],
        "benefits_ar": [
            "استثمار حقوق ملكية (حصة أقلية)",
            "دعم مجلس استشاري",
            "مقدمات شبكة للشركات السعودية",
        ],
        "vision2030_pillar": "Thriving Economy",
        "url_ref": "https://www.smef.com.sa",
    },
    "badir": {
        "id": "badir",
        "name_ar": "برنامج بادر للتقنية والحاضنات",
        "name_en": "Badir Technology Incubator Program",
        "provider_ar": "مدينة الملك عبدالعزيز للعلوم والتقنية",
        "provider_en": "King Abdulaziz City for Science and Technology (KACST)",
        "type": "incubator",
        "funding_range_sar": {"min": 100_000, "max": 2_000_000},
        "eligibility_criteria": [
            "Tech-focused startup at idea or MVP stage",
            "Saudi founder or ≥ 51% Saudi team",
            "Innovative solution with IP potential",
        ],
        "benefits_en": [
            "Office space and lab access",
            "Pre-seed funding (grant/convertible)",
            "IP protection support",
            "KACST research collaboration",
        ],
        "benefits_ar": [
            "مساحة مكتبية ومختبرات",
            "تمويل أولي (منحة/قابل للتحويل)",
            "دعم حماية الملكية الفكرية",
            "تعاون بحثي مع كاكست",
        ],
        "vision2030_pillar": "Thriving Economy",
        "url_ref": "https://www.badir.com.sa",
    },
    "misk_innovation": {
        "id": "misk_innovation",
        "name_ar": "مركز مسك للابتكار",
        "name_en": "Misk Innovation Center",
        "provider_ar": "مؤسسة مسك الخيرية",
        "provider_en": "Misk Foundation",
        "type": "innovation_hub",
        "funding_range_sar": None,
        "eligibility_criteria": [
            "Saudi youth (18–35) or Saudi startup",
            "Focus on education, tech, or entrepreneurship",
        ],
        "benefits_en": [
            "Mentorship from global entrepreneurs",
            "Access to Misk 500 accelerator",
            "Investor networking events",
            "Training bootcamps",
        ],
        "benefits_ar": [
            "إرشاد من رواد أعمال عالميين",
            "وصول لمسرّع مسك 500",
            "فعاليات شبكة المستثمرين",
            "معسكرات تدريب",
        ],
        "vision2030_pillar": "Vibrant Society",
        "url_ref": "https://miskinnovation.com",
    },
    "vision_realization_programs": {
        "id": "vision_realization_programs",
        "name_ar": "برامج تحقيق رؤية 2030 للتوطين التقني",
        "name_en": "Vision Realization Programs — Tech Localization",
        "provider_ar": "وزارة الاتصالات وتقنية المعلومات",
        "provider_en": "Ministry of Communications and Information Technology (MCIT)",
        "type": "subsidy",
        "funding_range_sar": {"min": 200_000, "max": 10_000_000},
        "eligibility_criteria": [
            "Saudi-licensed tech company or startup",
            "Solution addresses Vision 2030 priority sector",
            "Saudi employment percentage ≥ 25%",
        ],
        "benefits_en": [
            "Government contract fast-track access",
            "Subsidy for qualified Saudi tech talent hiring",
            "Digital infrastructure credits",
        ],
        "benefits_ar": [
            "وصول سريع لعقود حكومية",
            "إعانة لتوظيف الكوادر التقنية السعودية",
            "اعتمادات بنية تحتية رقمية",
        ],
        "vision2030_pillar": "Thriving Economy",
        "url_ref": "https://www.mcit.gov.sa",
    },
}

# ---------------------------------------------------------------------------
# High-growth SME sectors
# ---------------------------------------------------------------------------

_SECTORS: list[dict[str, Any]] = [
    {
        "sector": "ai_software",
        "name_ar": "الذكاء الاصطناعي والبرمجيات",
        "name_en": "AI & Software",
        "growth_outlook": "very_high",
        "vision2030_priority": True,
        "key_programs": ["badir", "vision_realization_programs", "misk_innovation"],
        "typical_funding_stage": "seed_to_series_a",
        "market_size_note_en": "SAR 45B+ digital economy target by 2030.",
        "market_size_note_ar": "هدف اقتصاد رقمي يتجاوز 45 مليار ريال بحلول 2030.",
    },
    {
        "sector": "healthcare_tech",
        "name_ar": "التقنية الصحية",
        "name_en": "Health Tech",
        "growth_outlook": "very_high",
        "vision2030_priority": True,
        "key_programs": ["smef", "kafalah", "monshaat_advisory"],
        "typical_funding_stage": "pre_seed_to_series_b",
        "market_size_note_en": "Saudi Vision 2030 healthcare privatization creates large SME market.",
        "market_size_note_ar": "خصخصة القطاع الصحي في رؤية 2030 تخلق سوقاً ضخماً للمنشآت.",
    },
    {
        "sector": "fintech",
        "name_ar": "التقنية المالية",
        "name_en": "FinTech",
        "growth_outlook": "high",
        "vision2030_priority": True,
        "key_programs": ["smef", "kafalah"],
        "typical_funding_stage": "seed_to_series_b",
        "market_size_note_en": "SAMA sandbox enables rapid FinTech licensing.",
        "market_size_note_ar": "بيئة ساما التجريبية تتيح ترخيص التقنية المالية بسرعة.",
    },
    {
        "sector": "logistics",
        "name_ar": "اللوجستيات وسلاسل التوريد",
        "name_en": "Logistics & Supply Chain",
        "growth_outlook": "high",
        "vision2030_priority": True,
        "key_programs": ["kafalah", "smef", "monshaat_advisory"],
        "typical_funding_stage": "seed_to_series_a",
        "market_size_note_en": "NEOM and Red Sea projects drive massive logistics demand.",
        "market_size_note_ar": "مشاريع نيوم والبحر الأحمر تخلق طلباً هائلاً على اللوجستيات.",
    },
    {
        "sector": "edtech",
        "name_ar": "تقنية التعليم",
        "name_en": "EdTech",
        "growth_outlook": "high",
        "vision2030_priority": True,
        "key_programs": ["misk_innovation", "badir", "monshaat_advisory"],
        "typical_funding_stage": "pre_seed_to_series_a",
        "market_size_note_en": "65% of population under 35; massive digital learning demand.",
        "market_size_note_ar": "65% من السكان دون 35 عاماً؛ طلب ضخم على التعلم الرقمي.",
    },
    {
        "sector": "real_estate_proptech",
        "name_ar": "تقنية العقارات",
        "name_en": "PropTech / Real Estate Tech",
        "growth_outlook": "high",
        "vision2030_priority": False,
        "key_programs": ["kafalah", "smef"],
        "typical_funding_stage": "seed_to_series_a",
        "market_size_note_en": "Vision 2030 housing targets: 70% homeownership by 2030.",
        "market_size_note_ar": "هدف رؤية 2030: 70% تملّك المساكن بحلول 2030.",
    },
    {
        "sector": "tourism_hospitality",
        "name_ar": "السياحة والضيافة",
        "name_en": "Tourism & Hospitality",
        "growth_outlook": "very_high",
        "vision2030_priority": True,
        "key_programs": ["smef", "kafalah", "monshaat_advisory"],
        "typical_funding_stage": "seed_to_series_b",
        "market_size_note_en": "100M tourist target by 2030 via Diriyah, AlUla, NEOM.",
        "market_size_note_ar": "هدف 100 مليون سائح بحلول 2030 عبر الدرعية والعُلا ونيوم.",
    },
]


# ---------------------------------------------------------------------------
# Funding readiness scoring
# ---------------------------------------------------------------------------

class ReadinessInput(BaseModel):
    annual_revenue_sar: float = Field(..., ge=0, description="Latest 12-month revenue in SAR")
    months_operating: int = Field(..., ge=0, description="Months the business has been operating")
    saudi_employee_count: int = Field(..., ge=0, description="Number of Saudi employees")
    total_employee_count: int = Field(..., ge=1, description="Total headcount")
    has_audited_financials: bool = Field(..., description="Audited financial statements available")
    has_registered_cr: bool = Field(..., description="Active Saudi Commercial Registration")
    sector: str = Field(..., description="One of the sector IDs from GET /sectors")
    seeking_type: str = Field(
        "loan_guarantee",
        description="loan_guarantee | equity_investment | incubator | advisory",
    )


def _score_readiness(inp: ReadinessInput) -> dict[str, Any]:
    score = 0
    max_score = 100
    factors: list[dict[str, str]] = []

    # CR (hard prerequisite)
    if inp.has_registered_cr:
        score += 20
        factors.append({"factor": "Commercial Registration", "status": "pass",
                         "points": 20, "note_en": "Active CR confirmed."})
    else:
        factors.append({"factor": "Commercial Registration", "status": "fail",
                         "points": 0, "note_en": "CR required for all programs."})

    # Operating history
    if inp.months_operating >= 24:
        score += 20
        factors.append({"factor": "Operating history (≥2 years)", "status": "pass",
                         "points": 20, "note_en": f"{inp.months_operating} months meets Kafalah requirement."})
    elif inp.months_operating >= 12:
        score += 12
        factors.append({"factor": "Operating history (1–2 years)", "status": "partial",
                         "points": 12, "note_en": "Qualifies for incubators/advisors, not Kafalah."})
    elif inp.months_operating >= 6:
        score += 6
        factors.append({"factor": "Operating history (6–12 months)", "status": "partial",
                         "points": 6, "note_en": "Early stage — Badir/Misk programs most relevant."})
    else:
        factors.append({"factor": "Operating history (<6 months)", "status": "fail",
                         "points": 0, "note_en": "Too early for most programs."})

    # Revenue
    if inp.annual_revenue_sar >= 1_000_000:
        score += 20
        factors.append({"factor": "Revenue (≥ SAR 1M)", "status": "pass",
                         "points": 20, "note_en": "Strong revenue signal for debt/equity programs."})
    elif inp.annual_revenue_sar >= 300_000:
        score += 12
        factors.append({"factor": "Revenue (SAR 300K–1M)", "status": "partial",
                         "points": 12, "note_en": "Moderate — suitable for early-stage programs."})
    elif inp.annual_revenue_sar > 0:
        score += 5
        factors.append({"factor": "Revenue (>0, <300K SAR)", "status": "partial",
                         "points": 5, "note_en": "Pre-revenue or very early — incubator focus."})
    else:
        factors.append({"factor": "Revenue (zero)", "status": "fail",
                         "points": 0, "note_en": "Pre-revenue — only incubator programs apply."})

    # Audited financials
    if inp.has_audited_financials:
        score += 15
        factors.append({"factor": "Audited financials", "status": "pass",
                         "points": 15, "note_en": "Required for Kafalah and SMEF."})
    else:
        factors.append({"factor": "Audited financials", "status": "fail",
                         "points": 0, "note_en": "Obtain audited statements before applying."})

    # Saudization
    if inp.total_employee_count > 0:
        saudi_pct = inp.saudi_employee_count / inp.total_employee_count * 100
        if saudi_pct >= 50:
            score += 15
            factors.append({"factor": f"Saudization ({saudi_pct:.0f}%)", "status": "pass",
                             "points": 15, "note_en": "Exceeds typical program thresholds."})
        elif saudi_pct >= 25:
            score += 8
            factors.append({"factor": f"Saudization ({saudi_pct:.0f}%)", "status": "partial",
                             "points": 8, "note_en": "Meets basic threshold but below preferred."})
        else:
            factors.append({"factor": f"Saudization ({saudi_pct:.0f}%)", "status": "fail",
                             "points": 0, "note_en": "Below minimum 25% for most programs."})

    # Sector bonus
    sector_match = next((s for s in _SECTORS if s["sector"] == inp.sector), None)
    if sector_match and sector_match["vision2030_priority"]:
        score += 10
        factors.append({"factor": f"Vision 2030 priority sector ({inp.sector})", "status": "pass",
                         "points": 10, "note_en": "Preferred sector increases program match rate."})

    # Determine eligible programs
    eligible: list[str] = []
    if score >= 70 and inp.has_registered_cr and inp.months_operating >= 24 and inp.has_audited_financials:
        if inp.seeking_type in ("loan_guarantee",):
            eligible.append("kafalah")
        if inp.seeking_type in ("equity_investment",):
            eligible.append("smef")
    if score >= 40:
        eligible.append("monshaat_advisory")
    if inp.sector in ("ai_software", "healthcare_tech") and inp.months_operating <= 36:
        eligible.append("badir")
    if inp.months_operating <= 48:
        eligible.append("misk_innovation")
    if sector_match and "vision_realization_programs" in (sector_match.get("key_programs") or []):
        eligible.append("vision_realization_programs")

    eligible = list(dict.fromkeys(eligible))  # deduplicate, preserve order

    band = (
        "Excellent (≥80)" if score >= 80
        else "Good (60–79)" if score >= 60
        else "Fair (40–59)" if score >= 40
        else "Early-stage (<40)"
    )

    return {
        "readiness_score": score,
        "max_score": max_score,
        "readiness_band": band,
        "scoring_factors": factors,
        "eligible_programs": eligible,
        "recommended_next_steps_en": _next_steps(score, inp),
        "recommended_next_steps_ar": _next_steps_ar(score, inp),
    }


def _next_steps(score: int, inp: ReadinessInput) -> list[str]:
    steps = []
    if not inp.has_registered_cr:
        steps.append("Register a Saudi Commercial Registration (CR) before applying.")
    if not inp.has_audited_financials and inp.months_operating >= 12:
        steps.append("Obtain audited financial statements from a SOCPA-licensed auditor.")
    if inp.saudi_employee_count / max(inp.total_employee_count, 1) < 0.25:
        steps.append("Increase Saudi hiring to ≥25% of headcount to unlock more programs.")
    if score >= 60:
        steps.append("Apply to Monsha'at advisory first for no-cost support before funding applications.")
    if score < 40:
        steps.append("Focus on 6–12 months of revenue generation before approaching Kafalah or SMEF.")
    return steps or ["Your profile is strong — proceed to program applications."]


def _next_steps_ar(score: int, inp: ReadinessInput) -> list[str]:
    steps = []
    if not inp.has_registered_cr:
        steps.append("سجّل سجلاً تجارياً سعودياً قبل التقديم.")
    if not inp.has_audited_financials and inp.months_operating >= 12:
        steps.append("احصل على قوائم مالية مراجعة من مراجع حسابات مرخّص من هيئة المحاسبين السعوديين.")
    if inp.saudi_employee_count / max(inp.total_employee_count, 1) < 0.25:
        steps.append("زد التوظيف السعودي إلى ≥25% من الموظفين لفتح برامج إضافية.")
    if score >= 60:
        steps.append("تقدّم لخدمات استشارات منشآت المجانية أولاً قبل طلبات التمويل.")
    if score < 40:
        steps.append("ركّز على 6–12 شهراً من توليد الإيرادات قبل التقدم لكفالة أو صندوق المنشآت.")
    return steps or ["ملفك قوي — تقدّم للبرامج مباشرة."]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/programs", summary="Saudi SME funding and support programs")
async def list_programs() -> dict[str, Any]:
    return {
        "total": len(_PROGRAMS),
        "programs": list(_PROGRAMS.values()),
        "disclaimer_en": (
            "Program details based on publicly available information. "
            "Eligibility and terms change — verify directly with the program provider."
        ),
        "disclaimer_ar": (
            "تفاصيل البرامج مستندة إلى معلومات متاحة للعموم. "
            "تتغير الشروط والأهلية — تحقق مباشرة مع مزود البرنامج."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/programs/{program_id}", summary="Details for a specific SME program")
async def get_program(program_id: str) -> dict[str, Any]:
    prog = _PROGRAMS.get(program_id)
    if not prog:
        raise HTTPException(
            status_code=404,
            detail=f"Program '{program_id}' not found. Use GET /api/v1/sme-accelerator/programs.",
        )
    return {
        "program": prog,
        "disclaimer_en": "Verify current eligibility terms directly with the program provider.",
        "disclaimer_ar": "تحقق من شروط الأهلية الحالية مباشرة مع مزود البرنامج.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/sectors", summary="High-growth Saudi SME sectors with Vision 2030 alignment")
async def list_sectors() -> dict[str, Any]:
    return {
        "sectors": _SECTORS,
        "note_en": "Growth outlook based on Vision 2030 targets and MCIT sector reports.",
        "note_ar": "توقعات النمو مستندة إلى أهداف رؤية 2030 وتقارير وزارة الاتصالات.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/readiness-score", summary="SME funding readiness assessment")
async def score_readiness(body: ReadinessInput) -> dict[str, Any]:
    if body.total_employee_count < body.saudi_employee_count:
        raise HTTPException(
            status_code=422,
            detail="saudi_employee_count cannot exceed total_employee_count.",
        )
    result = _score_readiness(body)
    return {
        **result,
        "disclaimer_en": (
            "This score is indicative only. It does not guarantee program approval. "
            "Consult a Monsha'at-certified advisor for a formal assessment."
        ),
        "disclaimer_ar": (
            "هذه الدرجة استرشادية فقط. لا تضمن قبول أي برنامج. "
            "استشر مستشاراً معتمداً من منشآت للتقييم الرسمي."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
