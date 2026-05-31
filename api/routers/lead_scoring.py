"""
Lead scoring router — AI-powered prioritisation of Saudi B2B prospects.

Scores a prospect against 8 weighted criteria (max 100 pts), derives a
grade band, and returns recommended actions and SLA follow-up targets.

Endpoints
---------
GET  /api/v1/lead-scoring/criteria        — scoring criteria + weights
GET  /api/v1/lead-scoring/grade-bands     — band definitions
POST /api/v1/lead-scoring/score           — score a single prospect
GET  /api/v1/lead-scoring/quick-guide     — field-filling reference

All data is static; no LLM or external API calls.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/lead-scoring", tags=["Sales"])

# ---------------------------------------------------------------------------
# Scoring criteria
# ---------------------------------------------------------------------------

_SCORING_CRITERIA: dict[str, dict[str, Any]] = {
    "sector_fit": {
        "weight": 20,
        "description_en": (
            "Is the prospect's sector in Dealix's primary sweet spot? "
            "Target sectors: AI software, fintech, healthcare tech, logistics."
        ),
        "description_ar": (
            "هل قطاع العميل المحتمل ضمن النطاق المستهدف لـ Dealix؟ "
            "القطاعات المستهدفة: برمجيات الذكاء الاصطناعي، التقنية المالية، التقنية الصحية، اللوجستيات."
        ),
    },
    "company_size_fit": {
        "weight": 15,
        "description_en": (
            "50–500 employees is the ideal range for managed ops packages; "
            ">500 employees suits custom AI engagements."
        ),
        "description_ar": (
            "50–500 موظف هو النطاق المثالي لباقات الإدارة التشغيلية؛ "
            "أكثر من 500 موظف يناسب مشاريع الذكاء الاصطناعي المخصصة."
        ),
    },
    "pain_clarity": {
        "weight": 15,
        "description_en": (
            "Does the prospect have explicit, articulated pain around reporting, "
            "ZATCA compliance, Nitaqat, or pipeline visibility?"
        ),
        "description_ar": (
            "هل لدى العميل المحتمل ألم واضح ومُعبَّر عنه في التقارير، "
            "أو الامتثال لهيئة الزكاة والضريبة، أو نطاقات، أو رؤية الخط الوظيفي؟"
        ),
    },
    "budget_signal": {
        "weight": 15,
        "description_en": (
            "Has the prospect asked about price, scope, or ROI? "
            "Is there a confirmed or likely allocated budget?"
        ),
        "description_ar": (
            "هل سأل العميل المحتمل عن السعر أو النطاق أو العائد على الاستثمار؟ "
            "هل هناك ميزانية مخصصة مؤكدة أو محتملة؟"
        ),
    },
    "champion_quality": {
        "weight": 10,
        "description_en": (
            "Is there a mid-level or senior internal champion who has access "
            "to — or is — the economic buyer?"
        ),
        "description_ar": (
            "هل يوجد بطل داخلي في مستوى متوسط أو عليا، "
            "يملك وصولاً إلى متخذ القرار المالي أو هو نفسه متخذ القرار؟"
        ),
    },
    "timing_signal": {
        "weight": 10,
        "description_en": (
            "Are there timing catalysts? Q1/Q4 budget cycles, post-Eid acceleration, "
            "post-LEAP momentum, or ZATCA deadline pressure."
        ),
        "description_ar": (
            "هل توجد محفزات توقيت؟ دورات ميزانية الربع الأول/الرابع، "
            "التسارع بعد العيد، زخم ما بعد ليب، أو ضغط مواعيد هيئة الزكاة والضريبة."
        ),
    },
    "competitor_dissatisfaction": {
        "weight": 8,
        "description_en": (
            "Is the prospect actively unhappy with their current CRM, "
            "analytics tool, or BI platform?"
        ),
        "description_ar": (
            "هل العميل المحتمل غير راضٍ بشكل فعلي عن CRM الحالي، "
            "أو أداة التحليلات، أو منصة BI؟"
        ),
    },
    "vision_2030_alignment": {
        "weight": 7,
        "description_en": (
            "Does the prospect's industry or stated strategic goals map clearly "
            "to Vision 2030 programs (NEOM, Tourism, Giga-projects, Financial Sector Dev)?"
        ),
        "description_ar": (
            "هل يرتبط قطاع العميل المحتمل أو أهدافه الاستراتيجية المُعلنة "
            "بوضوح ببرامج رؤية 2030 (نيوم، السياحة، المشاريع العملاقة، تطوير القطاع المالي)؟"
        ),
    },
}

# ---------------------------------------------------------------------------
# Grade bands
# ---------------------------------------------------------------------------

_GRADE_BANDS: list[dict[str, Any]] = [
    {
        "grade": "A+",
        "min_score": 85,
        "label_en": "Exceptional Fit",
        "label_ar": "ملاءمة استثنائية",
        "recommended_action_en": "Assign immediately to senior rep; personalised outreach within 4 hours.",
        "recommended_action_ar": "تعيين فوري لمندوب كبير؛ تواصل شخصي خلال 4 ساعات.",
        "sla_hours": 4,
    },
    {
        "grade": "A",
        "min_score": 70,
        "label_en": "Strong Fit",
        "label_ar": "ملاءمة قوية",
        "recommended_action_en": "Prioritise in next outreach sequence; follow up within 24 hours.",
        "recommended_action_ar": "أولوية في تسلسل التواصل التالي؛ متابعة خلال 24 ساعة.",
        "sla_hours": 24,
    },
    {
        "grade": "B",
        "min_score": 55,
        "label_en": "Moderate Fit",
        "label_ar": "ملاءمة متوسطة",
        "recommended_action_en": "Nurture cadence; follow up within 48 hours; build context first.",
        "recommended_action_ar": "برنامج رعاية؛ متابعة خلال 48 ساعة؛ بناء السياق أولاً.",
        "sla_hours": 48,
    },
    {
        "grade": "C",
        "min_score": 40,
        "label_en": "Weak Fit",
        "label_ar": "ملاءمة ضعيفة",
        "recommended_action_en": "Low-touch nurture only; revisit in 72 hours after research.",
        "recommended_action_ar": "رعاية محدودة فقط؛ مراجعة خلال 72 ساعة بعد البحث.",
        "sla_hours": 72,
    },
    {
        "grade": "D",
        "min_score": 0,
        "label_en": "Poor Fit",
        "label_ar": "ملاءمة ضعيفة جداً",
        "recommended_action_en": "Deprioritise; consider disqualification or long-cycle nurture (168 h+).",
        "recommended_action_ar": "تخفيض الأولوية؛ النظر في الاستبعاد أو رعاية طويلة الأمد (+168 ساعة).",
        "sla_hours": 168,
    },
]

# ---------------------------------------------------------------------------
# Pydantic model
# ---------------------------------------------------------------------------


class LeadScoringInput(BaseModel):
    prospect_name: str = Field(..., description="Full name of the primary contact.")
    prospect_company: str = Field(..., description="Company or organisation name.")
    sector: str = Field(..., description="Sector label for context (free text).")
    company_size_employees: int = Field(..., ge=1, description="Headcount.")
    sector_fit_score: float = Field(..., ge=0, le=20, description="Sector fit (0–20).")
    company_size_fit_score: float = Field(..., ge=0, le=15, description="Size fit (0–15).")
    pain_clarity_score: float = Field(..., ge=0, le=15, description="Pain clarity (0–15).")
    budget_signal_score: float = Field(..., ge=0, le=15, description="Budget signal (0–15).")
    champion_quality_score: float = Field(..., ge=0, le=10, description="Champion quality (0–10).")
    timing_signal_score: float = Field(..., ge=0, le=10, description="Timing signal (0–10).")
    competitor_dissatisfaction_score: float = Field(
        ..., ge=0, le=8, description="Competitor dissatisfaction (0–8)."
    )
    vision_2030_alignment_score: float = Field(
        ..., ge=0, le=7, description="Vision 2030 alignment (0–7)."
    )
    notes: str = ""


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------

_CRITERION_SCORE_MAP = {
    "sector_fit": ("sector_fit_score", 20),
    "company_size_fit": ("company_size_fit_score", 15),
    "pain_clarity": ("pain_clarity_score", 15),
    "budget_signal": ("budget_signal_score", 15),
    "champion_quality": ("champion_quality_score", 10),
    "timing_signal": ("timing_signal_score", 10),
    "competitor_dissatisfaction": ("competitor_dissatisfaction_score", 8),
    "vision_2030_alignment": ("vision_2030_alignment_score", 7),
}


def _score_lead(inp: LeadScoringInput) -> dict[str, Any]:
    """Compute a lead score, grade, strengths, gaps, and next steps.

    Parameters
    ----------
    inp:
        Validated ``LeadScoringInput`` from the request body.

    Returns
    -------
    dict[str, Any]
        Scoring result with grade, labels, SLA, strengths, gaps, and
        recommended next steps.
    """
    total_score = (
        inp.sector_fit_score
        + inp.company_size_fit_score
        + inp.pain_clarity_score
        + inp.budget_signal_score
        + inp.champion_quality_score
        + inp.timing_signal_score
        + inp.competitor_dissatisfaction_score
        + inp.vision_2030_alignment_score
    )

    band = next(b for b in _GRADE_BANDS if total_score >= b["min_score"])

    top_strengths: list[str] = []
    gaps: list[str] = []
    for criterion, (field_name, weight) in _CRITERION_SCORE_MAP.items():
        raw = getattr(inp, field_name)
        ratio = raw / weight if weight > 0 else 0.0
        if ratio >= 0.70:
            top_strengths.append(criterion)
        elif ratio < 0.30:
            gaps.append(criterion)

    next_steps_en: list[str]
    grade = band["grade"]
    if grade == "A+":
        next_steps_en = [
            "Book a discovery call within 4 hours.",
            "Prepare a tailored proof pack referencing their sector pain points.",
            "Loop in a senior decision-maker on the first call.",
            "Send a pre-meeting personalised brief the night before.",
        ]
    elif grade == "A":
        next_steps_en = [
            "Send a personalised LinkedIn connection or warm email within 24 hours.",
            "Attach a one-page sector case study relevant to their vertical.",
            "Qualify budget and timeline on the first touchpoint.",
            "Schedule a 30-minute scoping call this week.",
        ]
    elif grade == "B":
        next_steps_en = [
            "Add to a bi-weekly nurture sequence.",
            "Share relevant sector content (ZATCA/Nitaqat) to build trust.",
            "Identify and qualify the budget holder before pushing for a call.",
            "Revisit score in 2 weeks based on any new signals.",
        ]
    elif grade == "C":
        next_steps_en = [
            "Monitor for trigger events (funding, leadership change, ZATCA deadlines).",
            "Light-touch check-in in 72 hours — no hard sell.",
            "Research missing criteria to identify upgrade path.",
            "Consider a peer referral intro if a mutual contact exists.",
        ]
    else:
        next_steps_en = [
            "Place in low-priority pipeline segment.",
            "Do not invest significant outreach resources at this stage.",
            "Set a 30-day reminder to reassess if conditions change.",
            "Explore if a referral or partnership angle is more appropriate.",
        ]

    return {
        "prospect_name": inp.prospect_name,
        "prospect_company": inp.prospect_company,
        "sector": inp.sector,
        "company_size_employees": inp.company_size_employees,
        "total_score": round(total_score, 2),
        "grade": band["grade"],
        "label_en": band["label_en"],
        "label_ar": band["label_ar"],
        "recommended_action_en": band["recommended_action_en"],
        "recommended_action_ar": band["recommended_action_ar"],
        "sla_hours": band["sla_hours"],
        "top_strengths": top_strengths,
        "gaps": gaps,
        "next_steps_en": next_steps_en,
        "score_breakdown": {
            criterion: round(getattr(inp, field_name), 2)
            for criterion, (field_name, _) in _CRITERION_SCORE_MAP.items()
        },
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/criteria", summary="Scoring criteria with weights and descriptions")
async def get_criteria() -> dict[str, Any]:
    """Return all 8 scoring criteria with weights and bilingual descriptions."""
    return {
        "criteria": [
            {"criterion": k, **v}
            for k, v in _SCORING_CRITERIA.items()
        ],
        "total_possible_score": 100,
        "note_en": "Assign each criterion a score within its stated maximum weight.",
        "note_ar": "امنح كل معيار درجة ضمن الحد الأقصى للوزن المحدد.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/grade-bands", summary="Grade band definitions and SLA targets")
async def get_grade_bands() -> dict[str, Any]:
    """Return grade band definitions, minimum scores, labels, and SLA hours."""
    return {
        "grade_bands": _GRADE_BANDS,
        "note_en": "Bands are applied by comparing total_score to min_score in descending order.",
        "note_ar": "تُطبَّق الفئات بمقارنة الدرجة الإجمالية بالحد الأدنى تنازلياً.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/score", summary="Score a Saudi B2B prospect")
async def score_lead(body: LeadScoringInput) -> dict[str, Any]:
    """Accept a ``LeadScoringInput`` and return a full scored lead record."""
    result = _score_lead(body)
    return {
        **result,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/quick-guide", summary="Quick reference guide for filling score fields")
async def quick_guide() -> dict[str, Any]:
    """Return a reference guide explaining how to assign values to each score field."""
    return {
        "title_en": "Lead Scoring Field Guide",
        "title_ar": "دليل حقول تقييم الفرص",
        "guidance": [
            {
                "field": "sector_fit_score",
                "max": 20,
                "scoring_guide_en": (
                    "20 = core sector (AI software, fintech, healthcare tech, logistics). "
                    "15 = adjacent sector (e-commerce, PropTech, EdTech). "
                    "8 = tangential (government, FMCG). "
                    "0 = out-of-scope sector."
                ),
                "scoring_guide_ar": (
                    "20 = قطاع أساسي (برمجيات الذكاء الاصطناعي، التقنية المالية، التقنية الصحية، اللوجستيات). "
                    "15 = قطاع مجاور (التجارة الإلكترونية، PropTech، EdTech). "
                    "8 = قطاع هامشي (حكومي، FMCG). "
                    "0 = قطاع خارج النطاق."
                ),
            },
            {
                "field": "company_size_fit_score",
                "max": 15,
                "scoring_guide_en": (
                    "15 = 50–500 employees (managed ops sweet spot). "
                    "12 = >500 employees (custom AI viable). "
                    "7 = 20–49 employees (starter tier possible). "
                    "3 = <20 employees (low priority). "
                    "0 = sole trader / micro."
                ),
                "scoring_guide_ar": (
                    "15 = 50–500 موظف (النطاق المثالي للإدارة التشغيلية). "
                    "12 = أكثر من 500 موظف (مناسب للذكاء الاصطناعي المخصص). "
                    "7 = 20–49 موظفاً (الباقة التجريبية ممكنة). "
                    "3 = أقل من 20 موظفاً (أولوية منخفضة). "
                    "0 = فرد/مشروع صغير جداً."
                ),
            },
            {
                "field": "pain_clarity_score",
                "max": 15,
                "scoring_guide_en": (
                    "15 = explicit documented pain (ZATCA/Nitaqat/reporting mentioned). "
                    "10 = implied pain from tech stack or sector context. "
                    "5 = generic frustration expressed. "
                    "0 = no pain signal."
                ),
                "scoring_guide_ar": (
                    "15 = ألم موثّق صريح (ذُكر ZATCA/نطاقات/التقارير). "
                    "10 = ألم ضمني من مجموعة التقنيات أو سياق القطاع. "
                    "5 = إحباط عام معبَّر عنه. "
                    "0 = لا إشارة ألم."
                ),
            },
            {
                "field": "budget_signal_score",
                "max": 15,
                "scoring_guide_en": (
                    "15 = confirmed budget + asked about price/ROI. "
                    "10 = budget likely allocated (fiscal year timing, recent funding). "
                    "5 = indirect signal (asked about scope or timeline). "
                    "0 = no budget signal."
                ),
                "scoring_guide_ar": (
                    "15 = ميزانية مؤكدة + سأل عن السعر/العائد على الاستثمار. "
                    "10 = ميزانية محتملة مخصصة (توقيت السنة المالية، تمويل حديث). "
                    "5 = إشارة غير مباشرة (سأل عن النطاق أو الجدول الزمني). "
                    "0 = لا إشارة ميزانية."
                ),
            },
            {
                "field": "champion_quality_score",
                "max": 10,
                "scoring_guide_en": (
                    "10 = champion IS the economic buyer (CEO/CFO/COO). "
                    "7 = champion has direct access to economic buyer. "
                    "4 = mid-level champion, indirect access. "
                    "0 = contact is junior / no access."
                ),
                "scoring_guide_ar": (
                    "10 = البطل هو نفسه متخذ القرار المالي (CEO/CFO/COO). "
                    "7 = للبطل وصول مباشر لمتخذ القرار المالي. "
                    "4 = بطل متوسط المستوى، وصول غير مباشر. "
                    "0 = الاتصال في مستوى جونيور / لا وصول."
                ),
            },
            {
                "field": "timing_signal_score",
                "max": 10,
                "scoring_guide_en": (
                    "10 = immediate catalyst (ZATCA deadline this quarter, LEAP momentum). "
                    "7 = seasonal catalyst (Q1/Q4 budget, post-Eid). "
                    "4 = soft timing window (6-month horizon). "
                    "0 = no timing signal."
                ),
                "scoring_guide_ar": (
                    "10 = محفّز فوري (موعد ZATCA هذا الربع، زخم ليب). "
                    "7 = محفّز موسمي (ميزانية الربع الأول/الرابع، ما بعد العيد). "
                    "4 = نافزة زمنية ناعمة (أفق 6 أشهر). "
                    "0 = لا إشارة توقيت."
                ),
            },
            {
                "field": "competitor_dissatisfaction_score",
                "max": 8,
                "scoring_guide_en": (
                    "8 = actively seeking replacement (mentioned competitor by name with complaint). "
                    "5 = hinted at frustration with current tools. "
                    "2 = using legacy/basic tools (Excel, manual processes). "
                    "0 = satisfied with current stack."
                ),
                "scoring_guide_ar": (
                    "8 = يبحث فعلياً عن بديل (ذكر المنافس باسمه مع شكوى). "
                    "5 = أشار إلى إحباط من الأدوات الحالية. "
                    "2 = يستخدم أدوات قديمة/أساسية (Excel، عمليات يدوية). "
                    "0 = راضٍ عن مجموعة الأدوات الحالية."
                ),
            },
            {
                "field": "vision_2030_alignment_score",
                "max": 7,
                "scoring_guide_en": (
                    "7 = directly funded or mandated by a Vision 2030 program. "
                    "5 = sector explicitly named in Vision 2030 strategy. "
                    "2 = indirect alignment (general digital transformation). "
                    "0 = no alignment."
                ),
                "scoring_guide_ar": (
                    "7 = ممول أو مفوَّض مباشرةً بموجب برنامج رؤية 2030. "
                    "5 = القطاع مذكور صراحةً في استراتيجية رؤية 2030. "
                    "2 = توافق غير مباشر (تحول رقمي عام). "
                    "0 = لا توافق."
                ),
            },
        ],
        "tip_en": "Fill each field independently. Do not anchor later scores to earlier ones.",
        "tip_ar": "امنح كل حقل درجة باستقلالية. لا تستند درجات لاحقة إلى سابقة.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
