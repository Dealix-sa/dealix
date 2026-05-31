"""
Saudi B2B deal scoring engine (adapted MEDDPICC for the Saudi market).

Scores open deals 0–100 based on Metrics, Economic Buyer access,
Decision Criteria, Decision Process, Paper Process, Identified Pain,
Champion strength, Competition, and Saudi-specific cultural factors.

No external calls. Pure Python. Used for pipeline health reviews.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/deal-scoring", tags=["Analytics"])

# ---------------------------------------------------------------------------
# Scoring factors and weights
# ---------------------------------------------------------------------------

_FACTORS = {
    "metrics": {
        "label_en": "Metrics (M)",
        "label_ar": "المقاييس",
        "weight": 12,
        "description_en": "Prospect has quantified the business impact (ROI, cost, time).",
        "description_ar": "المحتمل حدّد الأثر التجاري كمياً (عائد الاستثمار، التكلفة، الوقت).",
        "levels": {
            0: "No quantification discussed",
            4: "Vague qualitative impact stated",
            8: "Some numbers discussed, not agreed",
            12: "Agreed quantified impact with prospect sign-off",
        },
    },
    "economic_buyer": {
        "label_en": "Economic Buyer (E)",
        "label_ar": "المشتري الاقتصادي",
        "weight": 16,
        "description_en": "Access to the person who controls the budget.",
        "description_ar": "الوصول إلى الشخص الذي يتحكم في الميزانية.",
        "levels": {
            0: "Economic buyer not identified",
            4: "Identified but no meeting",
            8: "Met once; receptive",
            16: "Active sponsor; confirms budget availability",
        },
    },
    "decision_criteria": {
        "label_en": "Decision Criteria (D)",
        "label_ar": "معايير القرار",
        "weight": 10,
        "description_en": "Understanding of how they will evaluate and decide.",
        "description_ar": "فهم كيفية التقييم واتخاذ القرار.",
        "levels": {
            0: "Unknown",
            3: "Informal list mentioned",
            7: "Formal criteria shared",
            10: "We meet all criteria; documented",
        },
    },
    "decision_process": {
        "label_en": "Decision Process (D)",
        "label_ar": "عملية القرار",
        "weight": 10,
        "description_en": "Steps, approvals, and timeline to get a signed contract.",
        "description_ar": "الخطوات والموافقات والجدول الزمني للحصول على عقد موقّع.",
        "levels": {
            0: "Unknown",
            3: "High-level steps known",
            7: "All approvals mapped; timeline agreed",
            10: "Legal/procurement engaged; closing date confirmed",
        },
    },
    "paper_process": {
        "label_en": "Paper Process (P)",
        "label_ar": "عملية التعاقد",
        "weight": 8,
        "description_en": "Saudi-specific legal/procurement requirements (CR, ZATCA docs, PDPL DPA).",
        "description_ar": "متطلبات قانونية/مشتريات سعودية خاصة (السجل التجاري، وثائق هيئة الزكاة، اتفاقية معالجة البيانات).",
        "levels": {
            0: "Not started",
            2: "Requirements collected",
            5: "Draft contract under review",
            8: "Final contract; awaiting signature",
        },
    },
    "identified_pain": {
        "label_en": "Identified Pain (I)",
        "label_ar": "الألم المحدد",
        "weight": 14,
        "description_en": "Specific business pain clearly articulated and acknowledged by prospect.",
        "description_ar": "ألم تجاري محدد مُعبَّر عنه بوضوح ومعترف به من قِبل المحتمل.",
        "levels": {
            0: "No pain identified",
            5: "Implied pain; not stated",
            10: "Stated pain; no urgency",
            14: "Compelling event driving urgency (ZATCA deadline, Eid, board review)",
        },
    },
    "champion": {
        "label_en": "Champion (C)",
        "label_ar": "البطل الداخلي",
        "weight": 16,
        "description_en": "Internal advocate who will fight for you in the buying committee.",
        "description_ar": "مناصر داخلي سيدافع عنك في لجنة الشراء.",
        "levels": {
            0: "No champion identified",
            4: "Possible champion; not tested",
            10: "Champion identified; moderate influence",
            16: "Strong champion; has direct access to economic buyer",
        },
    },
    "competition": {
        "label_en": "Competition (C)",
        "label_ar": "المنافسة",
        "weight": 8,
        "description_en": "Awareness of competitive situation and our differentiated position.",
        "description_ar": "الوعي بالوضع التنافسي وموقفنا المتميز.",
        "levels": {
            0: "Competitors unknown",
            2: "Competitors identified",
            5: "Our differentiation clear to prospect",
            8: "Prospect prefers us; documented",
        },
    },
    "saudi_cultural_fit": {
        "label_en": "Saudi Cultural & Relationship Fit",
        "label_ar": "الملاءمة الثقافية والعلائقية السعودية",
        "weight": 6,
        "description_en": "Relationship strength, wasta, and cultural alignment in the Saudi context.",
        "description_ar": "قوة العلاقة والواسطة والتوافق الثقافي في السياق السعودي.",
        "levels": {
            0: "No relationship; cold outreach only",
            2: "Warm intro; first meeting done",
            4: "Multiple meetings; personal rapport established",
            6: "Strong relationship; mutual trust; reference from shared network",
        },
    },
}

# ---------------------------------------------------------------------------
# Input model
# ---------------------------------------------------------------------------

class DealScoreInput(BaseModel):
    deal_name: str = Field(..., max_length=120)
    sector: str = Field(..., max_length=80)
    deal_size_sar: float = Field(..., gt=0)

    # MEDDPICC scores (each must match a valid level)
    metrics_score: int = Field(..., ge=0, le=12)
    economic_buyer_score: int = Field(..., ge=0, le=16)
    decision_criteria_score: int = Field(..., ge=0, le=10)
    decision_process_score: int = Field(..., ge=0, le=10)
    paper_process_score: int = Field(..., ge=0, le=8)
    identified_pain_score: int = Field(..., ge=0, le=14)
    champion_score: int = Field(..., ge=0, le=16)
    competition_score: int = Field(..., ge=0, le=8)
    saudi_cultural_fit_score: int = Field(..., ge=0, le=6)


def _score_deal(inp: DealScoreInput) -> dict[str, Any]:
    max_total = sum(f["weight"] for f in _FACTORS.values())
    raw_score = (
        inp.metrics_score
        + inp.economic_buyer_score
        + inp.decision_criteria_score
        + inp.decision_process_score
        + inp.paper_process_score
        + inp.identified_pain_score
        + inp.champion_score
        + inp.competition_score
        + inp.saudi_cultural_fit_score
    )
    score_pct = round(raw_score / max_total * 100, 1)

    factor_details = [
        {
            "factor": fid,
            "label_en": fmeta["label_en"],
            "label_ar": fmeta["label_ar"],
            "score": getattr(inp, f"{fid}_score"),
            "max": fmeta["weight"],
            "pct": round(getattr(inp, f"{fid}_score") / fmeta["weight"] * 100),
        }
        for fid, fmeta in _FACTORS.items()
    ]

    # Identify weakest factors (bottom 3 by pct)
    sorted_factors = sorted(factor_details, key=lambda x: x["pct"])
    weakest = sorted_factors[:3]

    stage = (
        "Close" if score_pct >= 80
        else "Commit" if score_pct >= 65
        else "Validate" if score_pct >= 45
        else "Qualify" if score_pct >= 25
        else "Prospect"
    )

    # Generate action items for weak factors
    actions_en = []
    actions_ar = []
    for wf in weakest:
        fid = wf["factor"]
        if wf["pct"] < 50:
            if fid == "economic_buyer":
                actions_en.append("Get a meeting with the Economic Buyer this week.")
                actions_ar.append("احصل على اجتماع مع المشتري الاقتصادي هذا الأسبوع.")
            elif fid == "champion":
                actions_en.append("Identify and test your internal champion with a difficult question.")
                actions_ar.append("حدد بطلك الداخلي واختبره بسؤال صعب.")
            elif fid == "identified_pain":
                actions_en.append("Anchor to a compelling event (ZATCA deadline, budget cycle, Eid).")
                actions_ar.append("ارتكز على حدث ملزم (موعد هيئة الزكاة، دورة الميزانية، العيد).")
            elif fid == "metrics":
                actions_en.append("Co-create the ROI model with the prospect in the next meeting.")
                actions_ar.append("أنشئ نموذج العائد على الاستثمار مع المحتمل في الاجتماع القادم.")
            elif fid == "paper_process":
                actions_en.append("Get procurement requirements and Saudi CR/tax docs checklist.")
                actions_ar.append("احصل على متطلبات المشتريات وقائمة وثائق السجل التجاري/الضريبة السعودية.")

    return {
        "deal_name": inp.deal_name,
        "sector": inp.sector,
        "deal_size_sar": inp.deal_size_sar,
        "total_score": raw_score,
        "max_possible": max_total,
        "score_pct": score_pct,
        "recommended_stage": stage,
        "factor_details": factor_details,
        "weakest_factors": weakest,
        "recommended_actions_en": actions_en or ["Deal looks strong — focus on closing."],
        "recommended_actions_ar": actions_ar or ["الصفقة تبدو قوية — ركّز على الإغلاق."],
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/methodology", summary="MEDDPICC scoring methodology for Saudi B2B")
async def get_methodology() -> dict[str, Any]:
    return {
        "methodology": "MEDDPICC adapted for Saudi B2B",
        "total_points": sum(f["weight"] for f in _FACTORS.values()),
        "factors": [
            {"id": fid, **{k: v for k, v in fmeta.items() if k != "levels"}}
            for fid, fmeta in _FACTORS.items()
        ],
        "stages": [
            {"stage": "Prospect", "score_range": "0–24%", "note": "Qualification not started"},
            {"stage": "Qualify", "score_range": "25–44%", "note": "Initial MEDDPICC discovery"},
            {"stage": "Validate", "score_range": "45–64%", "note": "Solution fit confirmed"},
            {"stage": "Commit", "score_range": "65–79%", "note": "Champion + EB aligned"},
            {"stage": "Close", "score_range": "80–100%", "note": "Paper process underway"},
        ],
        "saudi_context_en": (
            "Saudi B2B deals weight relationships (wasta) and C-level access heavily. "
            "An Economic Buyer score of 0 = stalled deal regardless of other factors."
        ),
        "saudi_context_ar": (
            "صفقات B2B السعودية تُعطي وزناً كبيراً للعلاقات والوصول لمستوى C. "
            "درجة المشتري الاقتصادي = 0 تعني صفقة متوقفة بصرف النظر عن العوامل الأخرى."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/score", summary="Score an open B2B deal using MEDDPICC")
async def score_deal(body: DealScoreInput) -> dict[str, Any]:
    result = _score_deal(body)
    return {
        **result,
        "disclaimer_en": "Deal score is a management aid, not a forecast. Human judgment required.",
        "disclaimer_ar": "درجة الصفقة أداة إدارية وليست توقعاً. يلزم الحكم البشري.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/scoring-guide", summary="How to score each MEDDPICC factor")
async def get_scoring_guide() -> dict[str, Any]:
    return {
        "factors": [
            {
                "id": fid,
                "label_en": fmeta["label_en"],
                "label_ar": fmeta["label_ar"],
                "weight": fmeta["weight"],
                "description_en": fmeta["description_en"],
                "description_ar": fmeta["description_ar"],
                "scoring_levels": [
                    {"points": pts, "description": desc}
                    for pts, desc in fmeta["levels"].items()
                ],
            }
            for fid, fmeta in _FACTORS.items()
        ],
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
