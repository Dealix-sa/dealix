"""Revenue Intelligence Ops — MRR/ARR trends, leakage detection, forecasting.

Endpoints (prefix: /api/v1/revenue-intelligence/ops):
  GET  /mrr-breakdown       — current MRR breakdown + 6-month history
  GET  /leakage-analysis    — revenue leakage signals and estimates
  GET  /growth-forecast     — 3-month MRR growth forecast
  GET  /cohort-analysis     — simplified cohort retention analysis
  POST /revenue-alert       — create a founder revenue alert
  GET  /nrr-analysis        — Net Revenue Retention analysis

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return governance_decision field
  - Bilingual ar/en labels
  - Mutating actions: APPROVAL_FIRST
  - Read-only actions: ALLOW_WITH_REVIEW
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/revenue-intelligence/ops",
    tags=["revenue-intelligence-ops"],
    dependencies=[Depends(require_admin_key)],
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_MUTATE = "APPROVAL_FIRST"

_FORECAST_DISCLAIMER = (
    "جميع التوقعات تقديرية وليست ضمانات / "
    "All forecasts are estimates, not guarantees"
)

_VALID_ALERT_TYPES = frozenset({
    "mrr_drop",
    "churn_spike",
    "leakage_identified",
    "expansion_opportunity",
    "invoice_overdue",
})

_VALID_URGENCY = frozenset({"high", "medium", "low"})

# ---------------------------------------------------------------------------
# Demo MRR history (6 months Jan–Jun 2026)
# ---------------------------------------------------------------------------

_MRR_HISTORY: list[dict[str, Any]] = [
    {
        "month": "Jan 2026",
        "month_ar": "يناير 2026",
        "total_mrr": 35_000,
        "new_mrr": 10_000,
        "expansion_mrr": 2_000,
        "churned_mrr": 0,
        "contracted_mrr": 0,
    },
    {
        "month": "Feb 2026",
        "month_ar": "فبراير 2026",
        "total_mrr": 42_000,
        "new_mrr": 8_000,
        "expansion_mrr": 1_500,
        "churned_mrr": -2_500,
        "contracted_mrr": 0,
    },
    {
        "month": "Mar 2026",
        "month_ar": "مارس 2026",
        "total_mrr": 48_500,
        "new_mrr": 7_500,
        "expansion_mrr": 2_000,
        "churned_mrr": -3_000,
        "contracted_mrr": 0,
    },
    {
        "month": "Apr 2026",
        "month_ar": "أبريل 2026",
        "total_mrr": 55_000,
        "new_mrr": 8_500,
        "expansion_mrr": 2_000,
        "churned_mrr": -4_000,
        "contracted_mrr": -1_000,
    },
    {
        "month": "May 2026",
        "month_ar": "مايو 2026",
        "total_mrr": 61_000,
        "new_mrr": 9_000,
        "expansion_mrr": 2_500,
        "churned_mrr": -5_500,
        "contracted_mrr": 0,
    },
    {
        "month": "Jun 2026",
        "month_ar": "يونيو 2026",
        "total_mrr": 68_000,
        "new_mrr": 10_000,
        "expansion_mrr": 3_000,
        "churned_mrr": -6_000,
        "contracted_mrr": 0,
    },
]

# ---------------------------------------------------------------------------
# Demo leakage signals
# ---------------------------------------------------------------------------

_LEAKAGE_SIGNALS: list[dict[str, Any]] = [
    {
        "id": "LEAK-001",
        "type": "invoice_overdue",
        "description_ar": "3 فواتير متأخرة أكثر من 30 يوماً",
        "description_en": "3 invoices overdue more than 30 days",
        "estimated_amount_sar": 8_500,
        "action_ar": "متابعة فورية مع العملاء المتأخرين",
        "action_en": "Immediate follow-up with overdue clients",
        "priority": "high",
    },
    {
        "id": "LEAK-002",
        "type": "stalled_expansion",
        "description_ar": "عميلان بدرجة صحة 80+ لم يُعرض عليهم ترقية منذ أكثر من 90 يوماً",
        "description_en": "2 clients with health >= 80 not offered upgrade in 90+ days",
        "estimated_amount_sar": 4_000,
        "action_ar": "ابدأ محادثة التوسع مع هؤلاء العملاء",
        "action_en": "Initiate expansion conversation with these clients",
        "priority": "high",
    },
    {
        "id": "LEAK-003",
        "type": "missing_proof_pack",
        "description_ar": "عميل واحد دون تسليم Proof Pack منذ أكثر من 60 يوماً (خطر التجديد)",
        "description_en": "1 client without Proof Pack delivery in 60+ days (renewal risk)",
        "estimated_amount_sar": 3_999,
        "action_ar": "أرسل Proof Pack محدّثاً فوراً",
        "action_en": "Send updated Proof Pack immediately",
        "priority": "high",
    },
    {
        "id": "LEAK-004",
        "type": "underpriced_tier",
        "description_ar": "عميل واحد يستخدم سير عمل مخصصة تتجاوز حد الباقة",
        "description_en": "1 client using custom workflows above their tier limit",
        "estimated_amount_sar": 2_000,
        "action_ar": "اقترح ترقية الباقة لاستيعاب الاستخدام الفعلي",
        "action_en": "Propose tier upgrade to accommodate actual usage",
        "priority": "medium",
    },
    {
        "id": "LEAK-005",
        "type": "unreferenced_referral",
        "description_ar": "إحالة مؤهلة واحدة لم تتم متابعتها منذ 30 يوماً",
        "description_en": "1 qualified referral not followed up in 30 days",
        "estimated_amount_sar": 1_500,
        "action_ar": "تابع مع المُحيل وابدأ التأهيل",
        "action_en": "Follow up with referrer and begin qualification",
        "priority": "medium",
    },
]

_TOTAL_LEAKAGE_SAR = sum(s["estimated_amount_sar"] for s in _LEAKAGE_SIGNALS)

# ---------------------------------------------------------------------------
# Demo cohort data
# ---------------------------------------------------------------------------

_COHORTS: list[dict[str, Any]] = [
    {
        "cohort_month": "Jan 2026",
        "cohort_month_ar": "يناير 2026",
        "initial_clients": 3,
        "retained_at_3m": 3,
        "retained_at_6m": 3,
        "avg_ltv_sar_estimate": 18_000,
    },
    {
        "cohort_month": "Feb 2026",
        "cohort_month_ar": "فبراير 2026",
        "initial_clients": 2,
        "retained_at_3m": 2,
        "retained_at_6m": 2,
        "avg_ltv_sar_estimate": 15_000,
    },
    {
        "cohort_month": "Mar 2026",
        "cohort_month_ar": "مارس 2026",
        "initial_clients": 2,
        "retained_at_3m": 2,
        "retained_at_6m": None,
        "avg_ltv_sar_estimate": 12_000,
    },
    {
        "cohort_month": "Apr 2026",
        "cohort_month_ar": "أبريل 2026",
        "initial_clients": 2,
        "retained_at_3m": 2,
        "retained_at_6m": None,
        "avg_ltv_sar_estimate": 10_000,
    },
    {
        "cohort_month": "May 2026",
        "cohort_month_ar": "مايو 2026",
        "initial_clients": 2,
        "retained_at_3m": None,
        "retained_at_6m": None,
        "avg_ltv_sar_estimate": 8_000,
    },
    {
        "cohort_month": "Jun 2026",
        "cohort_month_ar": "يونيو 2026",
        "initial_clients": 2,
        "retained_at_3m": None,
        "retained_at_6m": None,
        "avg_ltv_sar_estimate": 6_000,
    },
]

# ---------------------------------------------------------------------------
# In-memory alert store
# ---------------------------------------------------------------------------

_ALERTS: list[dict[str, Any]] = []

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.now(UTC).isoformat()


def _compute_nrr(history: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute Net Revenue Retention metrics from MRR history.

    NRR = (Starting MRR + Expansion - Churn - Contraction) / Starting MRR * 100
    Uses the first month as the starting base and sums expansion/churn/contraction
    across all subsequent months to arrive at a trailing NRR estimate.

    Returns a dict with nrr_pct, gross_revenue_retention_pct, expansion_revenue_pct,
    churn_rate_pct keys plus bilingual interpretation strings.
    """
    if not history or len(history) < 2:
        return {
            "nrr_pct": 0.0,
            "gross_revenue_retention_pct": 0.0,
            "expansion_revenue_pct": 0.0,
            "churn_rate_pct": 0.0,
        }

    starting_mrr = float(history[0]["total_mrr"])
    if starting_mrr <= 0:
        return {
            "nrr_pct": 0.0,
            "gross_revenue_retention_pct": 0.0,
            "expansion_revenue_pct": 0.0,
            "churn_rate_pct": 0.0,
        }

    total_expansion = sum(float(m.get("expansion_mrr", 0)) for m in history[1:])
    total_churned = sum(abs(float(m.get("churned_mrr", 0))) for m in history[1:])
    total_contracted = sum(abs(float(m.get("contracted_mrr", 0))) for m in history[1:])

    ending_mrr = starting_mrr + total_expansion - total_churned - total_contracted
    nrr_pct = round((ending_mrr / starting_mrr) * 100.0, 2)

    gross_retained = starting_mrr - total_churned - total_contracted
    grr_pct = round(max(0.0, gross_retained / starting_mrr) * 100.0, 2)

    expansion_pct = round((total_expansion / starting_mrr) * 100.0, 2)
    churn_rate_pct = round((total_churned / starting_mrr) * 100.0, 2)

    if nrr_pct >= 120:
        interpretation_ar = "حافظة إيرادات استثنائية — توسع العملاء يتجاوز الإلغاءات بفارق كبير"
        interpretation_en = "Exceptional revenue retention — client expansion far outpaces churn"
    elif nrr_pct >= 110:
        interpretation_ar = "حافظة إيرادات ممتازة — تتجاوز معيار 110% المستهدف"
        interpretation_en = "Excellent revenue retention — surpasses the 110% target benchmark"
    elif nrr_pct >= 100:
        interpretation_ar = "حافظة إيرادات جيدة — النمو إيجابي لكنه دون المعيار المستهدف"
        interpretation_en = "Good revenue retention — growth positive but below target benchmark"
    else:
        interpretation_ar = "حافظة إيرادات دون المعيار — يستلزم معالجة الإلغاءات وزيادة التوسع"
        interpretation_en = "Below-benchmark revenue retention — churn must be addressed and expansion increased"

    return {
        "nrr_pct": nrr_pct,
        "gross_revenue_retention_pct": grr_pct,
        "expansion_revenue_pct": expansion_pct,
        "churn_rate_pct": churn_rate_pct,
        "interpretation_ar": interpretation_ar,
        "interpretation_en": interpretation_en,
    }


def _compute_growth_forecast(history: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute a 3-month MRR growth forecast from trailing 3-month average growth.

    Uses the last 3 months of history to compute an average month-on-month
    growth rate, then applies optimistic (+20% of rate), base, and pessimistic
    (-20% of rate) scenarios for the next 3 months.
    """
    if len(history) < 2:
        return {"trailing_3m_growth_rate_pct": 0.0, "forecast": []}

    trailing = history[-3:] if len(history) >= 3 else history
    growth_rates: list[float] = []
    for i in range(1, len(trailing)):
        prev = float(trailing[i - 1]["total_mrr"])
        curr = float(trailing[i]["total_mrr"])
        if prev > 0:
            growth_rates.append((curr - prev) / prev * 100.0)

    avg_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0.0

    _FORECAST_MONTHS = [
        ("Jul 2026", "يوليو 2026"),
        ("Aug 2026", "أغسطس 2026"),
        ("Sep 2026", "سبتمبر 2026"),
    ]

    current_mrr = float(history[-1]["total_mrr"])
    forecast: list[dict[str, Any]] = []
    base_mrr = current_mrr
    for month_en, month_ar in _FORECAST_MONTHS:
        opt_rate = avg_rate * 1.2
        pess_rate = avg_rate * 0.8

        base_mrr_next = round(base_mrr * (1 + avg_rate / 100), 0)
        opt_mrr = round(base_mrr * (1 + opt_rate / 100), 0)
        pess_mrr = round(base_mrr * (1 + pess_rate / 100), 0)

        forecast.append({
            "month": month_en,
            "month_ar": month_ar,
            "base_mrr": base_mrr_next,
            "optimistic_mrr": opt_mrr,
            "pessimistic_mrr": pess_mrr,
        })
        base_mrr = base_mrr_next

    return {
        "trailing_3m_growth_rate_pct": round(avg_rate, 4),
        "forecast": forecast,
    }


# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------


class RevenueAlertBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    alert_type: str = Field(
        description=(
            "One of: mrr_drop, churn_spike, leakage_identified, "
            "expansion_opportunity, invoice_overdue"
        ),
    )
    description: str = Field(min_length=10, max_length=2000)
    estimated_impact_sar: float = Field(ge=0)
    urgency: str = Field(
        description="One of: high, medium, low",
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/mrr-breakdown")
async def get_mrr_breakdown() -> dict[str, Any]:
    """Current MRR breakdown and 6-month history."""
    latest = _MRR_HISTORY[-1]
    current_mrr = latest["total_mrr"]

    # Net new MRR = new + expansion + churn + contraction (churn/contraction are negative)
    net_new_mrr = (
        latest["new_mrr"]
        + latest["expansion_mrr"]
        + latest["churned_mrr"]
        + latest["contracted_mrr"]
    )

    _log.info("mrr_breakdown_fetched", current_mrr=current_mrr)

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "label_ar": "تفصيل الإيراد الشهري المتكرر",
        "label_en": "MRR Breakdown",
        "new_mrr": latest["new_mrr"],
        "expansion_mrr": latest["expansion_mrr"],
        "churned_mrr": latest["churned_mrr"],
        "contracted_mrr": latest["contracted_mrr"],
        "net_new_mrr": net_new_mrr,
        "total_mrr": current_mrr,
        "arr_run_rate": current_mrr * 12,
        "currency": "SAR",
        "history": _MRR_HISTORY,
    }


@router.get("/leakage-analysis")
async def get_leakage_analysis() -> dict[str, Any]:
    """Revenue leakage signals and total estimated leakage."""
    _log.info("leakage_analysis_fetched", total_leakage=_TOTAL_LEAKAGE_SAR)

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "label_ar": "تحليل تسرب الإيراد",
        "label_en": "Revenue Leakage Analysis",
        "total_leakage_estimate_sar": _TOTAL_LEAKAGE_SAR,
        "signal_count": len(_LEAKAGE_SIGNALS),
        "signals": _LEAKAGE_SIGNALS,
        "priority_action_ar": "عالج الفواتير المتأخرة ومرشحي التوسع أولاً — هذا وحده يفتح 12,500 ريال شهرياً",
        "priority_action_en": (
            "Address overdue invoices and expansion candidates first — "
            "this alone unlocks SAR 12,500/month"
        ),
        "currency": "SAR",
    }


@router.get("/growth-forecast")
async def get_growth_forecast() -> dict[str, Any]:
    """3-month MRR growth forecast based on trailing 3-month average growth rate."""
    forecast_data = _compute_growth_forecast(_MRR_HISTORY)

    _log.info(
        "growth_forecast_fetched",
        trailing_rate=forecast_data["trailing_3m_growth_rate_pct"],
    )

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "label_ar": "توقعات النمو للأشهر الثلاثة القادمة",
        "label_en": "3-Month Growth Forecast",
        "trailing_3m_growth_rate_pct": forecast_data["trailing_3m_growth_rate_pct"],
        "forecast": forecast_data["forecast"],
        "disclaimer": _FORECAST_DISCLAIMER,
        "currency": "SAR",
        "basis_ar": "يستند إلى متوسط معدل النمو الشهري للأشهر الثلاثة الأخيرة",
        "basis_en": "Based on trailing 3-month average month-on-month growth rate",
    }


@router.get("/cohort-analysis")
async def get_cohort_analysis() -> dict[str, Any]:
    """Simplified cohort retention analysis by acquisition month."""
    _log.info("cohort_analysis_fetched", cohort_count=len(_COHORTS))

    total_initial = sum(c["initial_clients"] for c in _COHORTS)
    avg_ltv = round(
        sum(c["avg_ltv_sar_estimate"] for c in _COHORTS) / len(_COHORTS), 2
    ) if _COHORTS else 0.0

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "label_ar": "تحليل المجموعات حسب شهر الاستحواذ",
        "label_en": "Cohort Analysis by Acquisition Month",
        "cohort_count": len(_COHORTS),
        "total_initial_clients": total_initial,
        "avg_ltv_sar_estimate": avg_ltv,
        "cohorts": _COHORTS,
        "note_ar": "القيم الفارغة تعني أن الفترة لم تمر بعد على هذا المجموعة",
        "note_en": "Null values indicate the period has not yet elapsed for that cohort",
        "currency": "SAR",
    }


@router.post("/revenue-alert")
async def create_revenue_alert(body: RevenueAlertBody) -> dict[str, Any]:
    """Create a revenue alert for the founder. Requires APPROVAL_FIRST."""
    if body.alert_type not in _VALID_ALERT_TYPES:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=422,
            detail={
                "ar": f"نوع التنبيه '{body.alert_type}' غير صالح",
                "en": f"Invalid alert_type '{body.alert_type}'",
                "valid_types": sorted(_VALID_ALERT_TYPES),
            },
        )

    if body.urgency not in _VALID_URGENCY:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=422,
            detail={
                "ar": f"مستوى الاستعجال '{body.urgency}' غير صالح",
                "en": f"Invalid urgency '{body.urgency}'",
                "valid_urgency": sorted(_VALID_URGENCY),
            },
        )

    alert_id = f"RALERT-{uuid.uuid4().hex[:8].upper()}"
    timestamp = _now_iso()

    _ALERT_TYPE_LABELS: dict[str, tuple[str, str]] = {
        "mrr_drop": ("انخفاض الإيراد الشهري", "MRR Drop"),
        "churn_spike": ("ارتفاع معدل الإلغاء", "Churn Spike"),
        "leakage_identified": ("تسرب إيراد مُكتشف", "Leakage Identified"),
        "expansion_opportunity": ("فرصة توسع", "Expansion Opportunity"),
        "invoice_overdue": ("فاتورة متأخرة", "Invoice Overdue"),
    }
    _URGENCY_LABELS: dict[str, tuple[str, str]] = {
        "high": ("عالي", "High"),
        "medium": ("متوسط", "Medium"),
        "low": ("منخفض", "Low"),
    }

    type_label_ar, type_label_en = _ALERT_TYPE_LABELS[body.alert_type]
    urgency_label_ar, urgency_label_en = _URGENCY_LABELS[body.urgency]

    alert_record = {
        "id": alert_id,
        "alert_type": body.alert_type,
        "alert_type_label_ar": type_label_ar,
        "alert_type_label_en": type_label_en,
        "description": body.description,
        "estimated_impact_sar": body.estimated_impact_sar,
        "urgency": body.urgency,
        "urgency_label_ar": urgency_label_ar,
        "urgency_label_en": urgency_label_en,
        "created_at": timestamp,
        "status": "pending_approval",
    }
    _ALERTS.append(alert_record)

    _log.info(
        "revenue_alert_created",
        alert_id=alert_id,
        alert_type=body.alert_type,
        urgency=body.urgency,
        estimated_impact_sar=body.estimated_impact_sar,
    )

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": timestamp,
        "status": "alert_logged_pending_approval",
        "alert_id": alert_id,
        "alert_type": body.alert_type,
        "alert_type_label_ar": type_label_ar,
        "alert_type_label_en": type_label_en,
        "description": body.description,
        "estimated_impact_sar": body.estimated_impact_sar,
        "urgency": body.urgency,
        "urgency_label_ar": urgency_label_ar,
        "urgency_label_en": urgency_label_en,
        "message_ar": "التنبيه مُسجَّل وينتظر مراجعة المؤسس والموافقة",
        "message_en": "Alert logged and awaiting founder review and approval",
        "currency": "SAR",
    }


@router.get("/nrr-analysis")
async def get_nrr_analysis() -> dict[str, Any]:
    """Net Revenue Retention analysis computed from demo MRR history."""
    nrr_data = _compute_nrr(_MRR_HISTORY)

    _log.info("nrr_analysis_fetched", nrr_pct=nrr_data.get("nrr_pct"))

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "label_ar": "تحليل صافي الاحتفاظ بالإيراد",
        "label_en": "Net Revenue Retention Analysis",
        "nrr_pct": nrr_data["nrr_pct"],
        "gross_revenue_retention_pct": nrr_data["gross_revenue_retention_pct"],
        "expansion_revenue_pct": nrr_data["expansion_revenue_pct"],
        "churn_rate_pct": nrr_data["churn_rate_pct"],
        "target_nrr_pct": 110.0,
        "interpretation_ar": nrr_data.get("interpretation_ar", ""),
        "interpretation_en": nrr_data.get("interpretation_en", ""),
        "currency": "SAR",
        "basis_ar": "يُحسب من بيانات التاريخ الشهري: (إيراد البداية + توسع - إلغاء - انكماش) / إيراد البداية",
        "basis_en": "Computed from monthly history: (starting MRR + expansion - churn - contraction) / starting MRR",
    }
