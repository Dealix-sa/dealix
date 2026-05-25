"""V12 Sales OS — thin wrapper exposing CRM + reply_classifier as V12.

NO guarantee claims. NO pressure manipulation. NO fake scarcity.
Every external messaging output is `draft_only` or `approval_required`.

Qualification is delegated to ``auto_client_acquisition.sales_os.qualification``
(same path as ``POST /api/v1/service-setup/qualify``).
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/api/v1/sales-os", tags=["sales-os"])


_HARD_GATES = {
    "no_live_send": True,
    "no_guaranteed_claims": True,
    "no_pressure_manipulation": True,
    "approval_required_for_external_actions": True,
}


class _QualifyRequest(BaseModel):
    """V12 discovery flags; mapped to canonical ``qualify()`` inputs."""

    model_config = ConfigDict(extra="forbid")

    has_warm_intro: bool = False
    sector: str = "b2b_services"
    pain_described: bool = False
    budget_signal: bool = False
    authority_signal: bool = False
    urgency_signal: bool = False
    accepts_governance: bool = True
    data_available: bool = False
    raw_request_text: str = ""


class _ObjectionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    objection_text: str
    language: str = "ar"


class _MeetingPrepRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_handle: str = "Slot-A"
    sector: str = "b2b_services"
    duration_min: int = 30


def _map_v12_to_qualify(req: _QualifyRequest) -> dict[str, Any]:
    return {
        "pain_clear": req.pain_described,
        "owner_present": req.has_warm_intro or req.authority_signal,
        "data_available": req.data_available or req.pain_described,
        "accepts_governance": req.accepts_governance,
        "has_budget": req.budget_signal,
        "wants_safe_methods": True,
        "proof_path_visible": req.urgency_signal or req.budget_signal,
        "retainer_path_visible": req.has_warm_intro,
        "raw_request_text": req.raw_request_text,
        "sector": req.sector,
        "city": "",
    }


def _legacy_next_step(decision: str, score: int, recommended_offer: str) -> tuple[str, str, str]:
    """Map canonical verdict to V12 ``next_step`` + bilingual recommendation."""
    if decision == "reject":
        return (
            "nurture_only",
            "غير مؤهَّل حاليّاً — لا تواصل بارد",
            "Not qualified yet — no cold outreach",
        )
    if decision == "accept" or score >= 85:
        if recommended_offer == "revenue_intelligence_sprint":
            return (
                "offer_sprint_9500",
                "مؤهَّل — قدّم Lead Intelligence Sprint (9,500 ريال)",
                "Qualified — offer Lead Intelligence Sprint (9,500 SAR)",
            )
        return (
            "offer_pilot",
            "مؤهَّل — قدّم Pilot 499 ريال",
            "Qualified — offer 499 SAR Pilot",
        )
    if decision in ("diagnostic_only", "reframe") or score >= 45:
        return (
            "offer_diagnostic",
            "نصف مؤهَّل — قدّم Mini Diagnostic مجاني",
            "Half-qualified — offer free Mini Diagnostic",
        )
    return (
        "nurture_only",
        "غير مؤهَّل حاليّاً — لا تواصل بارد",
        "Not qualified yet — no cold outreach",
    )


@router.get("/status")
async def sales_os_status() -> dict[str, Any]:
    return {
        "service": "sales_os",
        "module": "sales_os.qualification (canonical)",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "checks": {"qualification": "ok", "deal_score": "ok", "reply_classifier": "ok"},
        "hard_gates": _HARD_GATES,
        "canonical_qualify_endpoint": "POST /api/v1/service-setup/qualify",
        "next_action_ar": "استخدم /qualify ثم /meeting-prep",
        "next_action_en": "Use /qualify then /meeting-prep.",
    }


@router.post("/qualify")
async def sales_qualify(req: _QualifyRequest) -> dict[str, Any]:
    """Deterministic qualification — same engine as service-setup/qualify."""
    from auto_client_acquisition.sales_os.qualification import qualify

    result = qualify(**_map_v12_to_qualify(req))
    payload = result.to_dict()
    next_step, rec_ar, rec_en = _legacy_next_step(
        payload["decision"], payload["score"], payload["recommended_offer"]
    )
    return {
        "score": payload["score"],
        "decision": payload["decision"],
        "recommended_offer": payload["recommended_offer"],
        "reasons": payload.get("reasons", []),
        "doctrine_violations": payload.get("doctrine_violations", []),
        "recommendation_ar": rec_ar,
        "recommendation_en": rec_en,
        "next_step": next_step,
        "action_mode": "suggest_only",
        "hard_gates": _HARD_GATES,
        "canonical": True,
        "is_estimate": True,
    }


@router.post("/objection-response")
async def sales_objection_response(req: _ObjectionRequest) -> dict[str, Any]:
    """Returns a draft response to a sales objection, no guarantees."""
    o = req.objection_text.lower()
    if "guarantee" in o or "نضمن" in req.objection_text or "تضمنون" in req.objection_text:
        return {
            "action_mode": "blocked",
            "blocked_reason_ar": (
                "العميل يطلب ضمانات — Dealix لا يضمن نتائج مبيعات. "
                "صعّد للمؤسس لتقديم ردّ صادق."
            ),
            "blocked_reason_en": (
                "Customer demands guarantees — Dealix does NOT guarantee "
                "sales results. Escalate to founder for honest framing."
            ),
            "hard_gates": _HARD_GATES,
        }
    if "expensive" in o or "غالي" in req.objection_text or "مكلف" in req.objection_text:
        return {
            "action_mode": "draft_only",
            "draft_ar": (
                "أتفهّم. الـ Pilot 499 ريال لمدّة 7 أيّام مع استرجاع كامل لو "
                "ما طابق التسليم المواصفات. هل نبدأ بـ Mini Diagnostic مجاني "
                "أولاً؟"
            ),
            "draft_en": (
                "I understand. The 499 SAR Pilot runs 7 days with a full refund "
                "if delivery misses agreed criteria. Shall we start with a free "
                "Mini Diagnostic?"
            ),
            "hard_gates": _HARD_GATES,
        }
    return {
        "action_mode": "draft_only",
        "draft_ar": "شكراً على السؤال — سأراجع مع الفريق وأعود بمسودة مخصّصة.",
        "draft_en": "Thanks for the question — I'll review with the team and return a tailored draft.",
        "hard_gates": _HARD_GATES,
    }


@router.post("/meeting-prep")
async def sales_meeting_prep(req: _MeetingPrepRequest) -> dict[str, Any]:
    return {
        "customer_handle": req.customer_handle,
        "duration_min": req.duration_min,
        "agenda_ar": [
            "5 د — تعريف Dealix والوضع الحالي",
            "10 د — ما الفرص الـ 3 التي ترى أنها تستحق؟",
            "10 د — Diagnostic أو Sprint (499 / 9,500) — ما هو، وما ليس",
            "5 د — الخطوة التالية + اعتماد المسوّدة",
        ],
        "agenda_en": [
            "5 min — Dealix intro + current state",
            "10 min — Which 3 opportunities feel worth pursuing?",
            "10 min — Diagnostic or Sprint (499 / 9,500 SAR) — what it is, what it isn't",
            "5 min — Next step + draft approval",
        ],
        "must_avoid_ar": [
            "ادّعاء عوائد محدّدة",
            "مقارنة مباشرة بالمنافسين بدون مصدر عام",
            "وعد بإرسال آلي",
        ],
        "must_avoid_en": [
            "Claiming specific revenue numbers",
            "Direct competitor comparison without public source",
            "Promising automated sends",
        ],
        "action_mode": "suggest_only",
        "hard_gates": _HARD_GATES,
    }
