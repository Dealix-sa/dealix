"""Pipeline Operations API — sales pipeline management and forecasting.

Stages (in order):
  lead → qualified → diagnostic_sent → sprint_proposed
  → sprint_active → closed_won → closed_lost

Endpoints:
  GET  /api/v1/pipeline/overview      — stage counts, total/weighted pipeline value
  GET  /api/v1/pipeline/deals         — all deals, filterable by stage
  GET  /api/v1/pipeline/velocity      — avg days per stage, conversion rates, bottleneck
  POST /api/v1/pipeline/advance       — advance a deal to a new stage (APPROVAL_FIRST)
  GET  /api/v1/pipeline/forecast      — 30/60/90 day revenue forecast
  GET  /api/v1/pipeline/lost-analysis — closed_lost breakdown by reason and sector

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - governance_decision: ALLOW_WITH_REVIEW (except advance: APPROVAL_FIRST)
  - Bilingual ar/en labels
"""

from __future__ import annotations

import copy
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/pipeline",
    tags=["pipeline-ops"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"
_NOW = datetime.now(UTC)

# ---------------------------------------------------------------------------
# Stage ordering and constants
# ---------------------------------------------------------------------------

PIPELINE_STAGES: list[str] = [
    "lead",
    "qualified",
    "diagnostic_sent",
    "sprint_proposed",
    "sprint_active",
    "closed_won",
    "closed_lost",
]

ACTIVE_STAGES: list[str] = [s for s in PIPELINE_STAGES if not s.startswith("closed_")]

STAGE_LABELS: dict[str, dict[str, str]] = {
    "lead": {"ar": "عميل محتمل", "en": "Lead"},
    "qualified": {"ar": "مؤهَّل", "en": "Qualified"},
    "diagnostic_sent": {"ar": "تشخيص أُرسل", "en": "Diagnostic Sent"},
    "sprint_proposed": {"ar": "سبرنت مقترح", "en": "Sprint Proposed"},
    "sprint_active": {"ar": "سبرنت نشط", "en": "Sprint Active"},
    "closed_won": {"ar": "فاز", "en": "Closed Won"},
    "closed_lost": {"ar": "خسر", "en": "Closed Lost"},
}

# ---------------------------------------------------------------------------
# Demo pipeline — 12 deals, realistic Saudi B2B companies
# ---------------------------------------------------------------------------

_DEMO_DEALS: list[dict[str, Any]] = [
    {
        "deal_id": "DL-001",
        "company_name_ar": "شركة المنفعة للتجارة",
        "company_name_en": "Al Manfa'a Trading",
        "stage": "qualified",
        "value_sar": 4_500,
        "probability": 0.60,
        "days_in_stage": 4,
        "assigned_to": "founder",
        "sector": "retail",
        "city": "riyadh",
        "next_action_ar": "إرسال حزمة التشخيص المجاني",
        "next_action_en": "Send free diagnostic pack",
        "lost_reason": None,
    },
    {
        "deal_id": "DL-002",
        "company_name_ar": "شركة صفاء اللوجستية",
        "company_name_en": "Safaa Logistics",
        "stage": "sprint_proposed",
        "value_sar": 3_200,
        "probability": 0.50,
        "days_in_stage": 7,
        "assigned_to": "founder",
        "sector": "logistics",
        "city": "dammam",
        "next_action_ar": "متابعة الرد على العرض",
        "next_action_en": "Follow up on proposal response",
        "lost_reason": None,
    },
    {
        "deal_id": "DL-003",
        "company_name_ar": "شركة تمكين للرعاية الصحية",
        "company_name_en": "Tamkeen Health",
        "stage": "sprint_active",
        "value_sar": 5_500,
        "probability": 0.80,
        "days_in_stage": 3,
        "assigned_to": "founder",
        "sector": "healthcare",
        "city": "riyadh",
        "next_action_ar": "تسليم تقرير الأسبوع الأول",
        "next_action_en": "Deliver week-1 sprint report",
        "lost_reason": None,
    },
    {
        "deal_id": "DL-004",
        "company_name_ar": "مركز الرياض للتعليم",
        "company_name_en": "Riyadh Education Hub",
        "stage": "diagnostic_sent",
        "value_sar": 2_500,
        "probability": 0.40,
        "days_in_stage": 6,
        "assigned_to": "founder",
        "sector": "education",
        "city": "riyadh",
        "next_action_ar": "متابعة تقرير التشخيص",
        "next_action_en": "Follow up on diagnostic report",
        "lost_reason": None,
    },
    {
        "deal_id": "DL-005",
        "company_name_ar": "شركة الوافي للخدمات المالية",
        "company_name_en": "Al Wafi Financial",
        "stage": "sprint_active",
        "value_sar": 6_000,
        "probability": 0.75,
        "days_in_stage": 5,
        "assigned_to": "founder",
        "sector": "financial_services",
        "city": "riyadh",
        "next_action_ar": "مراجعة الأسبوع الثاني من السبرنت",
        "next_action_en": "Review sprint week 2 deliverables",
        "lost_reason": None,
    },
    {
        "deal_id": "DL-006",
        "company_name_ar": "شركة جازان للتصنيع",
        "company_name_en": "Jazan Manufacturing Co",
        "stage": "qualified",
        "value_sar": 3_800,
        "probability": 0.55,
        "days_in_stage": 9,
        "assigned_to": "founder",
        "sector": "manufacturing",
        "city": "jizan",
        "next_action_ar": "تأهيل عميق وتحديد أصحاب القرار",
        "next_action_en": "Deep qualification and stakeholder mapping",
        "lost_reason": None,
    },
    {
        "deal_id": "DL-007",
        "company_name_ar": "شركة نخيل العقارية",
        "company_name_en": "Nakheel Real Estate",
        "stage": "lead",
        "value_sar": 4_200,
        "probability": 0.20,
        "days_in_stage": 2,
        "assigned_to": "founder",
        "sector": "real_estate",
        "city": "jeddah",
        "next_action_ar": "الرد على الاستفسار الأولي",
        "next_action_en": "Respond to initial inquiry",
        "lost_reason": None,
    },
    {
        "deal_id": "DL-008",
        "company_name_ar": "شركة البصيرة للتقنية",
        "company_name_en": "Al Basira Tech",
        "stage": "lead",
        "value_sar": 4_500,
        "probability": 0.15,
        "days_in_stage": 1,
        "assigned_to": "founder",
        "sector": "technology",
        "city": "riyadh",
        "next_action_ar": "تأهيل أولي عبر مكالمة 15 دقيقة",
        "next_action_en": "Initial 15-minute qualification call",
        "lost_reason": None,
    },
    {
        "deal_id": "DL-009",
        "company_name_ar": "مجموعة الهلال التجارية",
        "company_name_en": "Al Hilal Commercial Group",
        "stage": "closed_won",
        "value_sar": 5_000,
        "probability": 1.0,
        "days_in_stage": 0,
        "assigned_to": "founder",
        "sector": "retail",
        "city": "riyadh",
        "next_action_ar": "بدء إعداد العميل",
        "next_action_en": "Begin client onboarding",
        "lost_reason": None,
    },
    {
        "deal_id": "DL-010",
        "company_name_ar": "شركة الأمانة للخدمات",
        "company_name_en": "Al Amanah Services",
        "stage": "closed_lost",
        "value_sar": 3_000,
        "probability": 0.0,
        "days_in_stage": 0,
        "assigned_to": "founder",
        "sector": "logistics",
        "city": "jeddah",
        "next_action_ar": "مراجعة سبب الخسارة وتحديث السجل",
        "next_action_en": "Review loss reason and update record",
        "lost_reason": "budget_constraints",
    },
    {
        "deal_id": "DL-011",
        "company_name_ar": "شركة إنجاز للتقنية",
        "company_name_en": "Injaz Technology",
        "stage": "diagnostic_sent",
        "value_sar": 4_500,
        "probability": 0.45,
        "days_in_stage": 11,
        "assigned_to": "founder",
        "sector": "technology",
        "city": "jeddah",
        "next_action_ar": "تذكير بموعد مراجعة التشخيص",
        "next_action_en": "Send diagnostic review reminder",
        "lost_reason": None,
    },
    {
        "deal_id": "DL-012",
        "company_name_ar": "شركة الفارابي للخدمات الصحية",
        "company_name_en": "Al Farabi Health Services",
        "stage": "closed_lost",
        "value_sar": 5_500,
        "probability": 0.0,
        "days_in_stage": 0,
        "assigned_to": "founder",
        "sector": "healthcare",
        "city": "riyadh",
        "next_action_ar": "مراجعة سبب الخسارة",
        "next_action_en": "Review loss reason",
        "lost_reason": "chose_competitor",
    },
]

# In-memory mutable store (reset on process restart; suitable for demo usage)
_pipeline: dict[str, dict[str, Any]] = {d["deal_id"]: copy.deepcopy(d) for d in _DEMO_DEALS}

# ---------------------------------------------------------------------------
# Lost-reason catalogue (bilingual)
# ---------------------------------------------------------------------------

_LOST_REASON_LABELS: dict[str, dict[str, str]] = {
    "budget_constraints": {"ar": "قيود الميزانية", "en": "Budget Constraints"},
    "chose_competitor": {"ar": "اختار منافساً", "en": "Chose Competitor"},
    "no_urgency": {"ar": "لا إلحاح", "en": "No Urgency"},
    "wrong_timing": {"ar": "توقيت غير مناسب", "en": "Wrong Timing"},
    "decision_maker_changed": {"ar": "تغيّر صاحب القرار", "en": "Decision-Maker Changed"},
    "unknown": {"ar": "غير محدد", "en": "Unknown"},
}

# ---------------------------------------------------------------------------
# Pure helper functions
# ---------------------------------------------------------------------------


def _all_deals() -> list[dict[str, Any]]:
    return list(_pipeline.values())


def _compute_weighted_value(deals: list[dict[str, Any]]) -> float:
    return sum(d["value_sar"] * d["probability"] for d in deals)


def _stage_counts() -> dict[str, int]:
    counts: dict[str, int] = {s: 0 for s in PIPELINE_STAGES}
    for deal in _pipeline.values():
        stage = deal.get("stage", "lead")
        if stage in counts:
            counts[stage] += 1
    return counts


def _active_deals() -> list[dict[str, Any]]:
    return [d for d in _pipeline.values() if d["stage"] in ACTIVE_STAGES]


def _compute_forecast(days: int) -> float:
    """Sum weighted value for deals likely to close within `days` days.

    Deals in sprint_active close within 14 days; sprint_proposed within 30;
    diagnostic_sent within 45; qualified within 60; lead within 90.
    """
    stage_close_days: dict[str, int] = {
        "sprint_active": 14,
        "sprint_proposed": 30,
        "diagnostic_sent": 45,
        "qualified": 60,
        "lead": 90,
    }
    total = 0.0
    for deal in _pipeline.values():
        if deal["stage"] in ("closed_won", "closed_lost"):
            continue
        expected_days = stage_close_days.get(deal["stage"], 90)
        if expected_days <= days:
            total += deal["value_sar"] * deal["probability"]
    return round(total, 2)


def _get_next_stage(current_stage: str) -> str | None:
    """Return the next stage in the pipeline or None if already terminal."""
    if current_stage in ("closed_won", "closed_lost"):
        return None
    idx = PIPELINE_STAGES.index(current_stage)
    if idx + 1 < len(PIPELINE_STAGES):
        return PIPELINE_STAGES[idx + 1]
    return None


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class AdvanceDealInput(BaseModel):
    deal_id: str = Field(..., min_length=1, description="Deal ID to advance")
    new_stage: str = Field(..., description="Target pipeline stage")
    reason: str = Field(..., min_length=1, description="Reason for stage advance")


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/overview")
async def get_overview() -> dict[str, Any]:
    """Return stage counts, total pipeline value, weighted pipeline, and avg days per stage."""
    all_d = _all_deals()
    active = [d for d in all_d if d["stage"] not in ("closed_won", "closed_lost")]
    counts = _stage_counts()
    total_value = sum(d["value_sar"] for d in active)
    weighted_value = round(_compute_weighted_value(active), 2)

    stage_avg_days: dict[str, Any] = {}
    for stage in PIPELINE_STAGES:
        stage_deals = [d for d in all_d if d["stage"] == stage]
        if stage_deals:
            avg = round(sum(d["days_in_stage"] for d in stage_deals) / len(stage_deals), 1)
        else:
            avg = 0.0
        stage_avg_days[stage] = {
            "count": counts[stage],
            "avg_days_in_stage": avg,
            "label": STAGE_LABELS.get(stage, {"ar": stage, "en": stage}),
        }

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_deals": len(all_d),
        "active_deals": len(active),
        "total_pipeline_value_sar": total_value,
        "weighted_pipeline_value_sar": weighted_value,
        "stages": stage_avg_days,
        "currency": "SAR",
    }


@router.get("/deals")
async def get_deals(
    stage: str | None = Query(default=None, description="Filter by pipeline stage"),
) -> dict[str, Any]:
    """Return all deals sorted by value descending, optionally filtered by stage."""
    if stage is not None and stage not in PIPELINE_STAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid stage. Must be one of: {PIPELINE_STAGES}",
        )

    deals = _all_deals()
    if stage:
        deals = [d for d in deals if d["stage"] == stage]

    deals_sorted = sorted(deals, key=lambda d: d["value_sar"], reverse=True)

    enriched = []
    for deal in deals_sorted:
        enriched_deal = dict(deal)
        enriched_deal["stage_label"] = STAGE_LABELS.get(
            deal["stage"], {"ar": deal["stage"], "en": deal["stage"]}
        )
        enriched_deal["weighted_value_sar"] = round(
            deal["value_sar"] * deal["probability"], 2
        )
        enriched.append(enriched_deal)

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total": len(enriched),
        "filter_stage": stage,
        "deals": enriched,
        "currency": "SAR",
    }


@router.get("/velocity")
async def get_velocity() -> dict[str, Any]:
    """Return avg days in each stage, conversion rates, and the identified bottleneck stage."""
    all_d = _all_deals()

    velocity: dict[str, Any] = {}
    for stage in ACTIVE_STAGES:
        stage_deals = [d for d in all_d if d["stage"] == stage]
        avg_days = (
            round(sum(d["days_in_stage"] for d in stage_deals) / len(stage_deals), 1)
            if stage_deals
            else 0.0
        )
        velocity[stage] = {
            "avg_days": avg_days,
            "deal_count": len(stage_deals),
            "label": STAGE_LABELS.get(stage, {"ar": stage, "en": stage}),
        }

    won = sum(1 for d in all_d if d["stage"] == "closed_won")
    lost = sum(1 for d in all_d if d["stage"] == "closed_lost")
    total_closed = won + lost
    overall_win_rate = round(won / total_closed, 3) if total_closed > 0 else 0.0

    active_stages_with_data = [
        s for s in ACTIVE_STAGES if velocity[s]["avg_days"] > 0
    ]
    bottleneck_stage: str | None = (
        max(active_stages_with_data, key=lambda s: velocity[s]["avg_days"])
        if active_stages_with_data
        else None
    )

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "stage_velocity": velocity,
        "overall_win_rate": overall_win_rate,
        "total_closed_won": won,
        "total_closed_lost": lost,
        "bottleneck_stage": bottleneck_stage,
        "bottleneck_label": STAGE_LABELS.get(bottleneck_stage, {"ar": "", "en": ""})
        if bottleneck_stage
        else None,
        "bottleneck_note_en": (
            "The bottleneck is the active stage with the highest avg days. "
            "Focus effort here to reduce sales cycle length."
        ),
        "bottleneck_note_ar": (
            "الاختناق هو المرحلة النشطة ذات أعلى متوسط أيام. "
            "ركّز الجهد هنا لتقليل طول دورة المبيعات."
        ),
    }


@router.post("/advance")
async def advance_deal(body: AdvanceDealInput) -> dict[str, Any]:
    """Advance a deal to a new pipeline stage.

    Every stage change requires founder sign-off (APPROVAL_FIRST).
    This endpoint records the intent; external approval must be obtained
    before downstream actions are triggered.
    """
    if body.deal_id not in _pipeline:
        raise HTTPException(status_code=404, detail=f"Deal {body.deal_id!r} not found")

    if body.new_stage not in PIPELINE_STAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid new_stage. Must be one of: {PIPELINE_STAGES}",
        )

    deal = _pipeline[body.deal_id]
    current_stage = deal["stage"]

    if current_stage == body.new_stage:
        raise HTTPException(
            status_code=400,
            detail=f"Deal is already in stage {body.new_stage!r}",
        )

    current_idx = PIPELINE_STAGES.index(current_stage)
    new_idx = PIPELINE_STAGES.index(body.new_stage)

    if new_idx <= current_idx and body.new_stage not in ("closed_lost",):
        raise HTTPException(
            status_code=400,
            detail="Stage regression is not allowed. Use closed_lost to mark deal as lost.",
        )

    _log.info(
        "pipeline_deal_advance_requested",
        deal_id=body.deal_id,
        from_stage=current_stage,
        to_stage=body.new_stage,
        reason=body.reason,
    )

    deal["stage"] = body.new_stage
    deal["days_in_stage"] = 0

    if body.new_stage == "closed_won":
        deal["probability"] = 1.0
    elif body.new_stage == "closed_lost":
        deal["probability"] = 0.0
    else:
        stage_probs: dict[str, float] = {
            "qualified": 0.55,
            "diagnostic_sent": 0.45,
            "sprint_proposed": 0.50,
            "sprint_active": 0.80,
        }
        deal["probability"] = stage_probs.get(body.new_stage, deal["probability"])

    updated = dict(deal)
    updated["stage_label"] = STAGE_LABELS.get(
        body.new_stage, {"ar": body.new_stage, "en": body.new_stage}
    )

    return {
        "governance_decision": _GOV_APPROVAL,
        "generated_at": _NOW.isoformat(),
        "deal": updated,
        "previous_stage": current_stage,
        "advance_reason": body.reason,
        "approval_note_en": (
            "Stage advance recorded. Founder approval is required before "
            "any downstream action (email, invoice, proposal) is triggered."
        ),
        "approval_note_ar": (
            "تم تسجيل تقدم المرحلة. موافقة المؤسس مطلوبة قبل "
            "تشغيل أي إجراء لاحق (بريد، فاتورة، عرض)."
        ),
        "currency": "SAR",
    }


@router.get("/forecast")
async def get_forecast() -> dict[str, Any]:
    """Return 30/60/90 day revenue forecast based on pipeline probabilities.

    Uses expected close-date heuristics per stage, not AI prediction.
    Figures are estimates and not guaranteed revenue.
    """
    forecast_30 = _compute_forecast(30)
    forecast_60 = _compute_forecast(60)
    forecast_90 = _compute_forecast(90)

    active = _active_deals()
    total_pipeline = sum(d["value_sar"] for d in active)
    total_weighted = round(_compute_weighted_value(active), 2)

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "forecast": {
            "30_day_sar": forecast_30,
            "60_day_sar": forecast_60,
            "90_day_sar": forecast_90,
        },
        "total_pipeline_sar": total_pipeline,
        "total_weighted_pipeline_sar": total_weighted,
        "methodology_en": (
            "Stage-based heuristic: sprint_active closes in <=14d, "
            "sprint_proposed <=30d, diagnostic_sent <=45d, "
            "qualified <=60d, lead <=90d. "
            "Weighted by deal probability."
        ),
        "methodology_ar": (
            "توقع مستند إلى المرحلة: سبرنت نشط يُغلق خلال 14 يوم، "
            "سبرنت مقترح 30 يوم، تشخيص أُرسل 45 يوم، "
            "مؤهَّل 60 يوم، عميل محتمل 90 يوم. مرجَّح باحتمالية الصفقة."
        ),
        "disclaimer_en": "Forecast is an estimate — not a guaranteed revenue projection",
        "disclaimer_ar": "التوقع تقديري — ليس توقع إيرادات مضموناً",
        "currency": "SAR",
    }


@router.get("/lost-analysis")
async def get_lost_analysis() -> dict[str, Any]:
    """Return breakdown of closed_lost deals by reason and sector patterns."""
    lost_deals = [d for d in _pipeline.values() if d["stage"] == "closed_lost"]

    reason_counts: dict[str, int] = {}
    sector_counts: dict[str, int] = {}

    for deal in lost_deals:
        reason = deal.get("lost_reason") or "unknown"
        reason_counts[reason] = reason_counts.get(reason, 0) + 1
        sector = deal.get("sector", "unknown")
        sector_counts[sector] = sector_counts.get(sector, 0) + 1

    reason_breakdown = []
    for reason, count in sorted(reason_counts.items(), key=lambda x: x[1], reverse=True):
        label = _LOST_REASON_LABELS.get(reason, {"ar": reason, "en": reason})
        reason_breakdown.append(
            {
                "reason": reason,
                "label": label,
                "count": count,
                "pct": round(count / len(lost_deals) * 100, 1) if lost_deals else 0.0,
            }
        )

    sector_breakdown = []
    for sector, count in sorted(sector_counts.items(), key=lambda x: x[1], reverse=True):
        sector_breakdown.append(
            {
                "sector": sector,
                "lost_deals": count,
            }
        )

    total_lost_value = sum(d["value_sar"] for d in lost_deals)

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_lost_deals": len(lost_deals),
        "total_lost_value_sar": total_lost_value,
        "reason_breakdown": reason_breakdown,
        "sector_patterns": sector_breakdown,
        "action_note_en": (
            "Use reason breakdown to adjust ICP targeting and objection handling. "
            "High budget_constraints rate suggests pricing friction."
        ),
        "action_note_ar": (
            "استخدم تحليل الأسباب لضبط استهداف ICP ومعالجة الاعتراضات. "
            "ارتفاع معدل قيود الميزانية يشير إلى احتكاك في التسعير."
        ),
        "currency": "SAR",
    }
