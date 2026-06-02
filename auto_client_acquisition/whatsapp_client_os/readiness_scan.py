"""WhatsApp Client OS — Company Readiness Scan.

Two depths:
- ``QUICK_TRIAGE_QUESTIONS`` (4 questions) powers the "ما أعرف — اقترح علي"
  path: a fast read that maps directly to a recommended starting offer.
- ``READINESS_AXES`` (10 axes) powers the full Revenue & Follow-up Readiness
  Scan, producing a scored :class:`ClientAssessment`.

All axis options are scored 0-100 where higher = healthier (more ready,
lower risk). Scoring is deterministic; no LLM. Scores are estimates.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.governance_os import GovernanceDecision
from auto_client_acquisition.whatsapp_client_os.recommendation import recommend_offer
from auto_client_acquisition.whatsapp_client_os.schemas import (
    ClientAssessment,
    EvidenceLevel,
)


@dataclass(frozen=True, slots=True)
class ScanOption:
    value: str
    label_ar: str
    score: int  # 0-100, higher = healthier


@dataclass(frozen=True, slots=True)
class ScanAxis:
    id: str
    title_ar: str
    title_en: str
    question_ar: str
    options: tuple[ScanOption, ...]


# --- Quick triage (the "ما أعرف — اقترح علي" path) -------------------------

QUICK_TRIAGE_QUESTIONS: tuple[dict[str, object], ...] = (
    {
        "id": "has_leads",
        "question_ar": "هل عندكم استفسارات أو leads شهريًا؟",
        "options": ("نعم", "لا", "غير متأكد"),
    },
    {
        "id": "lead_source",
        "question_ar": "أين تأتي الاستفسارات غالبًا؟",
        "options": ("واتساب", "إيميل", "نموذج", "إعلانات", "فريق مبيعات", "ما أعرف"),
    },
    {
        "id": "biggest_problem",
        "question_ar": "ما أكبر مشكلة؟",
        "options": ("المتابعة", "التقارير", "الحجوزات", "العروض", "تشتت الفريق", "ما أعرف"),
    },
    {
        "id": "nearest_goal",
        "question_ar": "ما هدفك الأقرب؟",
        "options": (
            "زيادة الردود",
            "حجز مواعيد",
            "تقليل ضياع الفرص",
            "تقرير للإدارة",
            "بدء نظام كامل",
        ),
    },
)


# --- Full 10-axis scan ------------------------------------------------------


def _opts(*pairs: tuple[str, str, int]) -> tuple[ScanOption, ...]:
    return tuple(ScanOption(value=v, label_ar=lbl, score=s) for v, lbl, s in pairs)


READINESS_AXES: tuple[ScanAxis, ...] = (
    ScanAxis(
        "lead_flow",
        "تدفّق الاستفسارات",
        "Lead Flow",
        "كم استفسار/lead يصلكم شهريًا تقريبًا؟",
        _opts(
            ("none", "لا شيء تقريبًا", 15),
            ("few", "أقل من ٢٠", 50),
            ("steady", "٢٠–١٠٠", 80),
            ("high", "أكثر من ١٠٠", 95),
        ),
    ),
    ScanAxis(
        "follow_up_maturity",
        "نضج المتابعة",
        "Follow-up Maturity",
        "كيف تتابعون الاستفسارات حاليًا؟",
        _opts(
            ("none", "بدون متابعة منظمة", 15),
            ("manual", "يدوي ومتقطّع", 45),
            ("partial", "قوالب بدون تتبّع", 70),
            ("system", "نظام متابعة واضح", 95),
        ),
    ),
    ScanAxis(
        "sales_process",
        "عملية المبيعات",
        "Sales Process",
        "هل لديكم خطوات مبيعات واضحة؟",
        _opts(
            ("adhoc", "عشوائي", 25),
            ("informal", "غير موثّق", 55),
            ("documented", "موثّق جزئيًا", 75),
            ("mature", "ناضج ومُقاس", 95),
        ),
    ),
    ScanAxis(
        "data_readiness",
        "جاهزية البيانات",
        "CRM / Data Readiness",
        "أين تُحفظ بيانات العملاء؟",
        _opts(
            ("scattered", "مبعثرة/ورق/واتساب", 20),
            ("sheets", "جداول", 55),
            ("crm_basic", "CRM أساسي", 80),
            ("crm_clean", "CRM نظيف ومنظّم", 95),
        ),
    ),
    ScanAxis(
        "automation_readiness",
        "جاهزية الأتمتة",
        "Automation Readiness",
        "ما مدى استخدامكم للأتمتة اليوم؟",
        _opts(
            ("none", "لا شيء", 20),
            ("basic", "تذكيرات بسيطة", 55),
            ("some", "تكاملات محدودة", 75),
            ("advanced", "تدفقات آلية", 95),
        ),
    ),
    ScanAxis(
        "reporting_maturity",
        "نضج التقارير",
        "Reporting Maturity",
        "كيف ترفعون التقارير للإدارة؟",
        _opts(
            ("none", "لا تقارير", 20),
            ("manual", "يدوي عند الطلب", 50),
            ("periodic", "تقارير دورية", 78),
            ("dashboard", "لوحات حيّة", 95),
        ),
    ),
    ScanAxis(
        "compliance_sensitivity",
        "حساسية الامتثال",
        "Compliance Sensitivity",
        "ما مستوى ضوابط الخصوصية لديكم؟",
        _opts(
            ("none", "بيانات حساسة بدون ضوابط", 25),
            ("basic", "ضوابط أساسية", 55),
            ("clear", "ضوابط وموافقات واضحة", 85),
            ("strict", "حوكمة كاملة", 95),
        ),
    ),
    ScanAxis(
        "urgency",
        "الإلحاح",
        "Urgency",
        "ما مدى إلحاح تحسين المبيعات الآن؟",
        _opts(
            ("low", "لا يوجد إلحاح", 35),
            ("medium", "خلال أشهر", 65),
            ("high", "خلال أسابيع", 85),
            ("critical", "عاجل جدًا", 95),
        ),
    ),
    ScanAxis(
        "budget_fit",
        "ملاءمة الميزانية",
        "Budget Fit",
        "هل توجد ميزانية مخصّصة للتحسين؟",
        _opts(
            ("none", "لا توجد", 25),
            ("small", "محدودة", 55),
            ("ready", "جاهزة للبدء", 80),
            ("flexible", "مرنة", 95),
        ),
    ),
    ScanAxis(
        "decision_access",
        "الوصول لصاحب القرار",
        "Decision Access",
        "هل أنت صاحب القرار أو قريب منه؟",
        _opts(
            ("none", "لا", 30),
            ("influencer", "مؤثّر", 60),
            ("close", "قريب من القرار", 80),
            ("owner", "صاحب القرار", 95),
        ),
    ),
)

_AXIS_BY_ID: dict[str, ScanAxis] = {a.id: a for a in READINESS_AXES}


def axis_score(axis_id: str, option_value: str) -> int:
    """Look up the 0-100 score for a chosen option; 0 if unknown."""
    axis = _AXIS_BY_ID.get(axis_id)
    if axis is None:
        return 0
    for opt in axis.options:
        if opt.value == option_value:
            return opt.score
    return 0


def _risk_band(revenue_readiness: int, data_readiness: int, compliance: int) -> str:
    if data_readiness < 40 or compliance < 40 or revenue_readiness < 45:
        return "high"
    if revenue_readiness >= 70 and compliance >= 60:
        return "low"
    return "medium"


def score_assessment(
    *,
    answers: dict[str, str],
    company: str = "",
    session_id: str = "",
) -> ClientAssessment:
    """Score a full scan into a :class:`ClientAssessment` with a recommendation.

    ``answers`` maps axis id -> chosen option value. Missing axes score 0.
    """
    axis_scores: dict[str, int] = {
        axis.id: axis_score(axis.id, answers.get(axis.id, "")) for axis in READINESS_AXES
    }
    revenue_readiness = round(sum(axis_scores.values()) / max(len(axis_scores), 1))
    follow_up = axis_scores.get("follow_up_maturity", 0)
    automation = axis_scores.get("automation_readiness", 0)
    data_readiness = axis_scores.get("data_readiness", 0)
    compliance = axis_scores.get("compliance_sensitivity", 0)
    risk = _risk_band(revenue_readiness, data_readiness, compliance)

    rec = recommend_offer(axis_scores=axis_scores, risk=risk)

    return ClientAssessment(
        session_id=session_id,
        company=company,
        axis_scores=axis_scores,
        revenue_readiness=revenue_readiness,
        follow_up_maturity=follow_up,
        automation_readiness=automation,
        risk=risk,
        recommended_offer_id=rec.offer_id,
        recommendation_reason_ar=rec.reason_ar,
        recommendation_reason_en=rec.reason_en,
        plan_steps_ar=rec.plan_steps_ar,
        evidence_level=EvidenceLevel.L1.value,
        governance_decision=GovernanceDecision.ALLOW.value,
    )


def quick_triage(answers: dict[str, str]) -> ClientAssessment:
    """Light read from the 4 quick-triage answers, reusing the scan engine.

    Maps quick answers onto representative axis scores so the same offer
    engine drives the "ما أعرف — اقترح علي" recommendation.
    """
    has_leads = answers.get("has_leads", "")
    problem = answers.get("biggest_problem", "")
    goal = answers.get("nearest_goal", "")

    lead_flow = 80 if has_leads == "نعم" else (35 if has_leads == "غير متأكد" else 15)
    follow_up = 30 if problem == "المتابعة" else 60
    data_readiness = 35 if problem in {"التقارير", "تشتت الفريق"} else 60
    automation = 60 if goal == "بدء نظام كامل" else 40
    budget = 60 if goal == "بدء نظام كامل" else 45

    axis_scores = {
        "lead_flow": lead_flow,
        "follow_up_maturity": follow_up,
        "data_readiness": data_readiness,
        "automation_readiness": automation,
        "budget_fit": budget,
    }
    risk = _risk_band(round(sum(axis_scores.values()) / len(axis_scores)), data_readiness, 70)
    rec = recommend_offer(axis_scores=axis_scores, risk=risk)
    return ClientAssessment(
        axis_scores=axis_scores,
        revenue_readiness=round(sum(axis_scores.values()) / len(axis_scores)),
        follow_up_maturity=follow_up,
        automation_readiness=automation,
        risk=risk,
        recommended_offer_id=rec.offer_id,
        recommendation_reason_ar=rec.reason_ar,
        recommendation_reason_en=rec.reason_en,
        plan_steps_ar=rec.plan_steps_ar,
        evidence_level=EvidenceLevel.L1.value,
        governance_decision=GovernanceDecision.ALLOW.value,
    )


__all__ = [
    "QUICK_TRIAGE_QUESTIONS",
    "READINESS_AXES",
    "ScanAxis",
    "ScanOption",
    "axis_score",
    "quick_triage",
    "score_assessment",
]
