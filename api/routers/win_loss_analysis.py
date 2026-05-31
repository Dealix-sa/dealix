"""
Win/loss analysis engine for Saudi B2B deals.

Provides weighted factor scoring, loss guidance lookup, and structured
debrief templates. Pure Python — no LLM calls, no external API calls.
Bilingual (EN/AR). All outputs carry a governance_decision field.

No guaranteed-outcome language. Results indicate tendencies, not certainties.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/win-loss-analysis", tags=["Analytics"])

# ---------------------------------------------------------------------------
# Win factor registry — 8 criteria, weights sum to 100
# ---------------------------------------------------------------------------

_WIN_FACTORS: dict[str, dict[str, Any]] = {
    "relationship_strength": {
        "label_en": "Relationship Strength",
        "label_ar": "قوة العلاقة",
        "description_en": "Strong champion, multiple stakeholder touches.",
        "score_range": "0-10",
        "weight": 25,
    },
    "roi_clarity": {
        "label_en": "ROI Clarity",
        "label_ar": "وضوح العائد",
        "description_en": "Clear SAR ROI, ZATCA savings articulated.",
        "score_range": "0-10",
        "weight": 20,
    },
    "pdpl_zatca_fit": {
        "label_en": "PDPL / ZATCA Compliance Fit",
        "label_ar": "ملاءمة الامتثال",
        "description_en": "Compliance angle matched to pain.",
        "score_range": "0-10",
        "weight": 15,
    },
    "decision_maker_access": {
        "label_en": "Decision Maker Access",
        "label_ar": "الوصول لصانع القرار",
        "description_en": "C-level or VP present in proposal.",
        "score_range": "0-10",
        "weight": 15,
    },
    "timing_alignment": {
        "label_en": "Timing Alignment",
        "label_ar": "توافق التوقيت",
        "description_en": "Q1 Jan or Q4 Oct budget cycles.",
        "score_range": "0-10",
        "weight": 10,
    },
    "vision_2030_narrative": {
        "label_en": "Vision 2030 Narrative",
        "label_ar": "سردية رؤية 2030",
        "description_en": "Saudization/digitization angle.",
        "score_range": "0-10",
        "weight": 8,
    },
    "competitive_differentiation": {
        "label_en": "Competitive Differentiation",
        "label_ar": "التميز التنافسي",
        "description_en": "Clear advantage vs. do-nothing or Big 4.",
        "score_range": "0-10",
        "weight": 4,
    },
    "proposal_quality": {
        "label_en": "Proposal Quality",
        "label_ar": "جودة العرض",
        "description_en": "Bilingual, well-formatted, correct pricing.",
        "score_range": "0-10",
        "weight": 3,
    },
}

# Verified at import: weights must sum to exactly 100.
_WIN_FACTOR_WEIGHT_TOTAL = sum(f["weight"] for f in _WIN_FACTORS.values())
assert _WIN_FACTOR_WEIGHT_TOTAL == 100, (
    f"Win factor weights must sum to 100, got {_WIN_FACTOR_WEIGHT_TOTAL}"
)

# ---------------------------------------------------------------------------
# Loss factor registry — 6 common loss reasons
# ---------------------------------------------------------------------------

_LOSS_FACTORS: dict[str, dict[str, str]] = {
    "budget_not_approved": {
        "label_en": "Budget Not Approved",
        "label_ar": "لم تتم الموافقة على الميزانية",
        "description_en": "Decision escalated, budget rejected.",
        "recovery_en": "Schedule Q1 re-engagement.",
        "recovery_ar": "جدول إعادة التواصل في الربع الأول.",
    },
    "competitor_won": {
        "label_en": "Competitor Won",
        "label_ar": "فاز منافس",
        "description_en": "Another vendor selected (generic CRM or Big 4).",
        "recovery_en": "Ask for a 30-day debrief meeting.",
        "recovery_ar": "اطلب اجتماع إحاطة خلال 30 يوماً.",
    },
    "internal_project_chosen": {
        "label_en": "Internal Project Chosen",
        "label_ar": "تم اختيار مشروع داخلي",
        "description_en": "IT team to build internally.",
        "recovery_en": "Document in friction log; revisit in 6 months.",
        "recovery_ar": "سجّل في سجل العقبات؛ راجع خلال 6 أشهر.",
    },
    "timing_mismatch": {
        "label_en": "Timing Mismatch",
        "label_ar": "عدم توافق التوقيت",
        "description_en": "Decision postponed to next fiscal year.",
        "recovery_en": "Nurture with quarterly insight emails.",
        "recovery_ar": "رعاية بإيميلات رؤى ربع سنوية.",
    },
    "champion_left": {
        "label_en": "Champion Left",
        "label_ar": "غادر البطل الداخلي",
        "description_en": "Internal champion changed jobs.",
        "recovery_en": "Identify successor; restart relationship.",
        "recovery_ar": "حدد الخلف؛ أعد بناء العلاقة.",
    },
    "no_decision": {
        "label_en": "No Decision",
        "label_ar": "لا قرار",
        "description_en": "Prospect couldn't drive internal alignment.",
        "recovery_en": "Offer free diagnostic to reset.",
        "recovery_ar": "قدّم تشخيصاً مجانياً لإعادة الضبط.",
    },
}

# ---------------------------------------------------------------------------
# Analysis template registry — 3 templates
# ---------------------------------------------------------------------------

_ANALYSIS_TEMPLATES: dict[str, dict[str, Any]] = {
    "quick_debrief": {
        "id": "quick_debrief",
        "name_en": "Quick Debrief",
        "name_ar": "إحاطة سريعة",
        "duration_minutes": 20,
        "questions": [
            {
                "order": 1,
                "question_en": "What was the primary factor in your decision?",
                "question_ar": "ما العامل الرئيسي في قرارك؟",
            },
            {
                "order": 2,
                "question_en": "Which part of our process worked best for you?",
                "question_ar": "أي جزء من عمليتنا كان الأفضل بالنسبة لك؟",
            },
            {
                "order": 3,
                "question_en": "What one thing would have changed the outcome?",
                "question_ar": "ما الشيء الوحيد الذي كان يمكن أن يغير النتيجة؟",
            },
            {
                "order": 4,
                "question_en": "Would you consider us again in the future?",
                "question_ar": "هل ستفكر في التعامل معنا مستقبلاً؟",
            },
        ],
    },
    "deep_analysis": {
        "id": "deep_analysis",
        "name_en": "Deep Analysis",
        "name_ar": "تحليل معمّق",
        "duration_minutes": 60,
        "questions": [
            {
                "order": 1,
                "question_en": "Walk me through your evaluation process from start to finish.",
                "question_ar": "أرشدني خلال عملية تقييمك من البداية إلى النهاية.",
            },
            {
                "order": 2,
                "question_en": "Who else was involved in the final decision?",
                "question_ar": "من شارك في القرار النهائي؟",
            },
            {
                "order": 3,
                "question_en": "How did we compare against the alternatives you evaluated?",
                "question_ar": "كيف قارنّا بالبدائل التي قيّمتها؟",
            },
            {
                "order": 4,
                "question_en": "Which of our capabilities resonated most?",
                "question_ar": "أي قدراتنا كان لها الأثر الأكبر؟",
            },
            {
                "order": 5,
                "question_en": "Where did we fall short of your expectations?",
                "question_ar": "أين لم نرقَ إلى مستوى توقعاتك؟",
            },
            {
                "order": 6,
                "question_en": "How did our pricing compare to the value you expected?",
                "question_ar": "كيف قارنت أسعارنا بالقيمة التي توقعتها؟",
            },
            {
                "order": 7,
                "question_en": "Was there a specific moment the deal shifted in direction?",
                "question_ar": "هل كانت هناك لحظة محددة تحوّل فيها مسار الصفقة؟",
            },
            {
                "order": 8,
                "question_en": "What advice would you give our team for future opportunities?",
                "question_ar": "ما النصيحة التي تقدمها لفريقنا للفرص المستقبلية؟",
            },
        ],
    },
    "pattern_report": {
        "id": "pattern_report",
        "name_en": "Pattern Report",
        "name_ar": "تقرير الأنماط",
        "min_deals_required": 10,
        "metrics": [
            {
                "metric_en": "Win rate by sector",
                "metric_ar": "معدل الفوز حسب القطاع",
            },
            {
                "metric_en": "Average weighted score for won vs. lost deals",
                "metric_ar": "متوسط الدرجة الموزونة للصفقات الرابحة مقابل الخاسرة",
            },
            {
                "metric_en": "Most common primary loss reason",
                "metric_ar": "السبب الرئيسي الأكثر شيوعاً للخسارة",
            },
            {
                "metric_en": "Average relationship_strength score in won deals",
                "metric_ar": "متوسط درجة قوة العلاقة في الصفقات الرابحة",
            },
            {
                "metric_en": "Correlation between decision_maker_access and win outcome",
                "metric_ar": "الارتباط بين الوصول لصانع القرار ونتيجة الفوز",
            },
            {
                "metric_en": "Average deal cycle length (days) won vs. lost",
                "metric_ar": "متوسط مدة دورة الصفقة (بالأيام) للفوز مقابل الخسارة",
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# Pydantic model
# ---------------------------------------------------------------------------

_VALID_LOSS_REASONS = set(_LOSS_FACTORS.keys())
_VALID_OUTCOMES = {"won", "lost"}


class WinLossInput(BaseModel):
    """Input for a single deal win/loss analysis."""

    deal_name: str = Field(..., min_length=1)
    outcome: str = Field(..., description="'won' or 'lost'")
    primary_loss_reason: str | None = Field(
        None,
        description="Required when outcome is 'lost'. One of the 6 loss factor keys.",
    )

    relationship_strength_score: float = Field(..., ge=0, le=10)
    roi_clarity_score: float = Field(..., ge=0, le=10)
    pdpl_zatca_fit_score: float = Field(..., ge=0, le=10)
    decision_maker_access_score: float = Field(..., ge=0, le=10)
    timing_alignment_score: float = Field(..., ge=0, le=10)
    vision_2030_narrative_score: float = Field(..., ge=0, le=10)
    competitive_differentiation_score: float = Field(..., ge=0, le=10)
    proposal_quality_score: float = Field(..., ge=0, le=10)


# ---------------------------------------------------------------------------
# Core business logic
# ---------------------------------------------------------------------------

_FACTOR_SCORE_FIELDS: dict[str, str] = {
    "relationship_strength": "relationship_strength_score",
    "roi_clarity": "roi_clarity_score",
    "pdpl_zatca_fit": "pdpl_zatca_fit_score",
    "decision_maker_access": "decision_maker_access_score",
    "timing_alignment": "timing_alignment_score",
    "vision_2030_narrative": "vision_2030_narrative_score",
    "competitive_differentiation": "competitive_differentiation_score",
    "proposal_quality": "proposal_quality_score",
}


def _analyze_deal(inp: WinLossInput) -> dict[str, Any]:
    """
    Compute a weighted 0-100 score for a closed deal and return diagnostics.

    Includes top 2 / bottom 2 factor contributions and, for lost deals with a
    supplied primary_loss_reason, structured recovery guidance.

    weighted_score = sum(score_i * weight_i / 10) for each factor.
    Max possible = sum of all weights = 100.
    """
    if inp.outcome not in _VALID_OUTCOMES:
        raise ValueError(f"outcome must be one of {_VALID_OUTCOMES}, got '{inp.outcome}'")

    if inp.primary_loss_reason is not None and inp.primary_loss_reason not in _VALID_LOSS_REASONS:
        raise ValueError(
            f"primary_loss_reason must be one of {sorted(_VALID_LOSS_REASONS)}, "
            f"got '{inp.primary_loss_reason}'"
        )

    contributions: list[dict[str, Any]] = []
    for factor_id, field_name in _FACTOR_SCORE_FIELDS.items():
        meta = _WIN_FACTORS[factor_id]
        raw_score: float = getattr(inp, field_name)
        weight: int = meta["weight"]
        contribution = round(raw_score * weight / 10, 2)
        contributions.append(
            {
                "factor": factor_id,
                "label_en": meta["label_en"],
                "label_ar": meta["label_ar"],
                "score": raw_score,
                "weight": weight,
                "weighted_contribution": contribution,
            }
        )

    weighted_score = round(sum(c["weighted_contribution"] for c in contributions), 2)

    sorted_by_contribution = sorted(
        contributions, key=lambda c: c["weighted_contribution"], reverse=True
    )
    strongest_factors = sorted_by_contribution[:2]
    weakest_factors = sorted_by_contribution[-2:]

    loss_guidance: dict[str, Any] | None = None
    if inp.outcome == "lost" and inp.primary_loss_reason:
        lf = _LOSS_FACTORS[inp.primary_loss_reason]
        loss_guidance = {
            "loss_reason": inp.primary_loss_reason,
            "label_en": lf["label_en"],
            "label_ar": lf["label_ar"],
            "description_en": lf["description_en"],
            "recovery_en": lf["recovery_en"],
            "recovery_ar": lf["recovery_ar"],
        }

    return {
        "deal_name": inp.deal_name,
        "outcome": inp.outcome,
        "weighted_score": weighted_score,
        "strongest_factors": strongest_factors,
        "weakest_factors": weakest_factors,
        "loss_guidance": loss_guidance,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/win-factors", summary="All 8 win factors with weights and bilingual labels")
async def get_win_factors() -> dict[str, Any]:
    return {
        "win_factors": _WIN_FACTORS,
        "total_weight": _WIN_FACTOR_WEIGHT_TOTAL,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/loss-factors", summary="All 6 loss factors with recovery guidance")
async def get_loss_factors() -> dict[str, Any]:
    return {
        "loss_factors": _LOSS_FACTORS,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/templates", summary="All 3 structured analysis templates")
async def get_analysis_templates() -> dict[str, Any]:
    return {
        "templates": _ANALYSIS_TEMPLATES,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/analyze", summary="Compute weighted win/loss analysis for a closed deal")
async def analyze_deal(inp: WinLossInput) -> dict[str, Any]:
    """
    Returned governance_decision is APPROVAL_FIRST.
    Review findings with the team before circulating externally.
    """
    if inp.outcome not in _VALID_OUTCOMES:
        raise HTTPException(
            status_code=422,
            detail=f"outcome must be one of {sorted(_VALID_OUTCOMES)}",
        )
    if inp.primary_loss_reason is not None and inp.primary_loss_reason not in _VALID_LOSS_REASONS:
        raise HTTPException(
            status_code=422,
            detail=f"primary_loss_reason must be one of {sorted(_VALID_LOSS_REASONS)}",
        )
    result = _analyze_deal(inp)
    result["governance_decision"] = "APPROVAL_FIRST"
    return result
