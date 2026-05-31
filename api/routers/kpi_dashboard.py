"""KPI Dashboard API — comprehensive company KPIs with bilingual labels.

Endpoints:
  GET /api/v1/kpi/summary      — overall KPIs (MRR, ARR, leads, conversion)
  GET /api/v1/kpi/commercial   — commercial pipeline metrics
  GET /api/v1/kpi/cohort       — customer cohort retention analysis
  GET /api/v1/kpi/nps          — NPS trend over time
  GET /api/v1/kpi/health-score — AI-calculated company health score (0-100)

All endpoints:
  - Require admin auth (X-Admin-API-Key header)
  - Return bilingual ar/en labels
  - Use realistic mock data when live DB is unavailable
  - Include a governance_decision field per platform convention
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/kpi",
    tags=["kpi-dashboard"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"

# ---------------------------------------------------------------------------
# Bilingual label helpers
# ---------------------------------------------------------------------------

_LABELS_AR: dict[str, str] = {
    "mrr": "الإيراد الشهري المتكرر",
    "arr": "الإيراد السنوي المتوقع",
    "leads_total": "إجمالي العملاء المحتملين",
    "conversion_rate": "معدل التحويل",
    "churn_rate": "معدل الإلغاء",
    "arpa": "متوسط الإيراد لكل حساب",
    "nps": "صافي نقاط المروّجين",
    "health_score": "درجة صحة الشركة",
    "pipeline_value": "قيمة خط الأنابيب",
    "deals_open": "الصفقات المفتوحة",
    "deals_won": "الصفقات المُغلقة",
    "avg_deal_size": "متوسط حجم الصفقة",
    "sales_cycle_days": "أيام دورة المبيعات",
    "retention_rate": "معدل الاحتفاظ",
}

_LABELS_EN: dict[str, str] = {
    "mrr": "Monthly Recurring Revenue",
    "arr": "Annual Run-Rate",
    "leads_total": "Total Leads",
    "conversion_rate": "Conversion Rate",
    "churn_rate": "Churn Rate",
    "arpa": "Avg Revenue per Account",
    "nps": "Net Promoter Score",
    "health_score": "Company Health Score",
    "pipeline_value": "Pipeline Value",
    "deals_open": "Open Deals",
    "deals_won": "Deals Won",
    "avg_deal_size": "Avg Deal Size",
    "sales_cycle_days": "Sales Cycle Days",
    "retention_rate": "Retention Rate",
}


def _label(key: str) -> dict[str, str]:
    return {"ar": _LABELS_AR.get(key, key), "en": _LABELS_EN.get(key, key)}


# ---------------------------------------------------------------------------
# Mock data builders (replace with DB queries when available)
# ---------------------------------------------------------------------------

_NOW = datetime.now(UTC)


def _mock_mrr_history(months: int = 12) -> list[dict[str, Any]]:
    base_mrr = 18_000
    result: list[dict[str, Any]] = []
    for i in range(months, 0, -1):
        month_dt = _NOW - timedelta(days=30 * i)
        growth = 1.0 + (months - i) * 0.05
        mrr = round(base_mrr * growth)
        result.append(
            {
                "month": month_dt.strftime("%Y-%m"),
                "mrr_sar": mrr,
                "arr_sar": mrr * 12,
            }
        )
    return result


def _mock_cohort(cohort_month: str) -> dict[str, Any]:
    """Simulate retention curve for a cohort month."""
    months_retained = [100, 88, 79, 74, 70, 67, 65, 63, 61, 60, 59, 58]
    return {
        "cohort_month": cohort_month,
        "starting_customers": 8,
        "retention_by_month": [
            {"month_offset": i, "pct": r} for i, r in enumerate(months_retained)
        ],
    }


def _mock_nps_trend(periods: int = 6) -> list[dict[str, Any]]:
    nps_vals = [42, 45, 48, 44, 52, 55]
    result: list[dict[str, Any]] = []
    for i in range(periods):
        month_dt = _NOW - timedelta(days=30 * (periods - i - 1))
        result.append(
            {
                "period": month_dt.strftime("%Y-%m"),
                "nps": nps_vals[i],
                "promoters_pct": 60 + i * 2,
                "passives_pct": 25 - i,
                "detractors_pct": 15 - i,
                "responses": 20 + i * 3,
            }
        )
    return result


async def _get_mrr_history(
    db_session: AsyncSession | None, months: int = 12
) -> list[dict[str, Any]]:
    """
    Query PaymentRecordDB grouped by month for managed_ops and custom_ai tiers.

    Falls back to mock data if the DB session is unavailable or the query fails.
    """
    if db_session is None:
        return _mock_mrr_history(months)
    try:
        from db.repositories.wave17_repos import PaymentRepository

        repo = PaymentRepository(db_session)
        rows = await repo.get_mrr_by_month(tiers=["managed_ops", "custom_ai"])
        if rows:
            # Return the last N months from live data
            return rows[-months:]
        # No live data yet — fall back to mock so the dashboard is always populated
        return _mock_mrr_history(months)
    except Exception as exc:
        _log.warning("kpi_mrr_history_db_failed", error=str(exc))
        return _mock_mrr_history(months)


async def _get_nps_trend(
    db_session: AsyncSession | None, periods: int = 6
) -> list[dict[str, Any]]:
    """
    Query HealthSnapshotRecord grouped by month, averaging satisfaction_score.

    Falls back to mock data if the DB session is unavailable or the query fails.
    """
    if db_session is None:
        return _mock_nps_trend(periods)
    try:
        from db.models import HealthSnapshotRecord
        from sqlalchemy import select

        since = _NOW - timedelta(days=30 * periods)
        stmt = (
            select(HealthSnapshotRecord)
            .where(HealthSnapshotRecord.computed_at >= since)
            .order_by(HealthSnapshotRecord.computed_at.asc())
        )
        result = await db_session.execute(stmt)
        rows = result.scalars().all()

        if not rows:
            return _mock_nps_trend(periods)

        # Group by month and average satisfaction_score (used as proxy NPS)
        monthly: dict[str, list[float]] = {}
        for r in rows:
            key = r.computed_at.strftime("%Y-%m") if r.computed_at else "unknown"
            monthly.setdefault(key, []).append(r.satisfaction_score)

        trend: list[dict[str, Any]] = []
        for month_key in sorted(monthly.keys())[-periods:]:
            scores = monthly[month_key]
            avg_score = sum(scores) / len(scores) if scores else 0.0
            # Convert 0-100 satisfaction score to approximate NPS scale (-100 to 100)
            nps_approx = round((avg_score - 50) * 2)
            trend.append(
                {
                    "period": month_key,
                    "nps": nps_approx,
                    "promoters_pct": round(avg_score * 0.6),
                    "passives_pct": round(avg_score * 0.25),
                    "detractors_pct": max(0, 100 - round(avg_score * 0.85)),
                    "responses": len(scores),
                    "source": "db",
                }
            )
        return trend if trend else _mock_nps_trend(periods)
    except Exception as exc:
        _log.warning("kpi_nps_trend_db_failed", error=str(exc))
        return _mock_nps_trend(periods)


def _compute_health_score(
    mrr_growth_pct: float,
    churn_rate: float,
    nps: int,
    pipeline_coverage: float,
    proof_score: float,
) -> dict[str, Any]:
    """AI-calculated health score from weighted KPI signals (0-100)."""
    growth_pts = min(25, max(0, mrr_growth_pct / 2))
    churn_pts = max(0, 20 - churn_rate * 200)
    nps_pts = min(20, max(0, (nps + 20) / 4))
    pipeline_pts = min(20, max(0, pipeline_coverage * 10))
    proof_pts = min(15, max(0, proof_score / 100 * 15))
    total = round(growth_pts + churn_pts + nps_pts + pipeline_pts + proof_pts, 1)
    if total >= 75:
        tier = "healthy"
        tier_ar = "بصحة جيدة"
    elif total >= 55:
        tier = "moderate"
        tier_ar = "معتدل"
    elif total >= 35:
        tier = "at_risk"
        tier_ar = "في خطر"
    else:
        tier = "critical"
        tier_ar = "حرج"
    return {
        "score": total,
        "tier": tier,
        "tier_ar": tier_ar,
        "components": {
            "mrr_growth": round(growth_pts, 1),
            "low_churn": round(churn_pts, 1),
            "nps": round(nps_pts, 1),
            "pipeline_coverage": round(pipeline_pts, 1),
            "proof_strength": round(proof_pts, 1),
        },
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/summary")
async def kpi_summary() -> dict[str, Any]:
    """Overall company KPIs: MRR, ARR, leads, conversion rates.

    Returns bilingual labels and a governance_decision field.
    Tries live DB first; falls back to mock data when unavailable.
    """
    db_session: AsyncSession | None = None
    try:
        from db.session import async_session_factory
        db_session = async_session_factory()()
    except Exception:
        db_session = None

    try:
        history = await _get_mrr_history(db_session, months=12)
    finally:
        if db_session is not None:
            try:
                await db_session.close()
            except Exception:
                pass

    current = history[-1]
    previous = history[-2] if len(history) > 1 else current
    prev_mrr = previous["mrr_sar"] or 1
    mrr_growth_pct = round((current["mrr_sar"] - prev_mrr) / prev_mrr * 100, 1)

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "metrics": {
            "mrr": {
                "value_sar": current["mrr_sar"],
                "mom_growth_pct": mrr_growth_pct,
                "label": _label("mrr"),
            },
            "arr": {
                "value_sar": current["arr_sar"],
                "label": _label("arr"),
            },
            "leads_total": {
                "value": 84,
                "qualified": 31,
                "label": _label("leads_total"),
            },
            "conversion_rate": {
                "value_pct": 18.4,
                "label": _label("conversion_rate"),
            },
            "churn_rate": {
                "value_pct": 3.2,
                "label": _label("churn_rate"),
            },
            "arpa": {
                "value_sar": 2_200,
                "label": _label("arpa"),
            },
            "customer_count": {
                "active": 12,
                "churned_ytd": 2,
            },
        },
        "mrr_history": history[-6:],
    }


@router.get("/commercial")
async def kpi_commercial() -> dict[str, Any]:
    """Commercial pipeline metrics: pipeline value, deals, cycle times."""
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "metrics": {
            "pipeline_value": {
                "value_sar": 148_500,
                "label": _label("pipeline_value"),
                "stages": {
                    "diagnostic": {"count": 6, "value_sar": 12_000},
                    "proposal_sent": {"count": 5, "value_sar": 45_000},
                    "negotiation": {"count": 3, "value_sar": 38_000},
                    "closing": {"count": 2, "value_sar": 53_500},
                },
            },
            "deals_open": {
                "value": 16,
                "label": _label("deals_open"),
            },
            "deals_won_mtd": {
                "value": 3,
                "value_sar": 24_000,
                "label": _label("deals_won"),
            },
            "avg_deal_size": {
                "value_sar": 8_000,
                "label": _label("avg_deal_size"),
            },
            "sales_cycle_days": {
                "value": 21,
                "label": _label("sales_cycle_days"),
            },
            "sprint_offers_sent": 14,
            "sprint_accepted": 8,
            "sprint_conversion_pct": 57.1,
        },
    }


@router.get("/cohort")
async def kpi_cohort(
    cohort_month: str = Query(default="", description="YYYY-MM format. Empty = current month."),
) -> dict[str, Any]:
    """Customer cohort retention analysis by month."""
    if not cohort_month:
        cohort_month = _NOW.strftime("%Y-%m")
    cohort = _mock_cohort(cohort_month)
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "cohort": cohort,
        "labels": {
            "retention_rate": _label("retention_rate"),
        },
        "note_ar": "البيانات تقديرية بناءً على متوسطات السوق لحين توفر البيانات الفعلية.",
        "note_en": "Data is estimated from market averages pending live DB integration.",
    }


@router.get("/nps")
async def kpi_nps(periods: int = Query(default=6, ge=1, le=24)) -> dict[str, Any]:
    """NPS trend over time. Tries live DB first; falls back to mock."""
    db_session: AsyncSession | None = None
    try:
        from db.session import async_session_factory
        db_session = async_session_factory()()
    except Exception:
        db_session = None

    try:
        trend = await _get_nps_trend(db_session, periods=periods)
    finally:
        if db_session is not None:
            try:
                await db_session.close()
            except Exception:
                pass

    latest_nps = trend[-1]["nps"] if trend else 0
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "current_nps": latest_nps,
        "label": _label("nps"),
        "trend": trend,
        "benchmark": {
            "b2b_saas_median": 40,
            "dealix_target": 60,
        },
    }


@router.get("/health-score")
async def kpi_health_score() -> dict[str, Any]:
    """AI-calculated company health score (0-100) from weighted KPI signals."""
    history = _mock_mrr_history(2)
    current_mrr = history[-1]["mrr_sar"]
    prev_mrr = history[-2]["mrr_sar"] if len(history) > 1 else current_mrr
    mrr_growth_pct = round((current_mrr - prev_mrr) / prev_mrr * 100, 1) if prev_mrr else 0

    health = _compute_health_score(
        mrr_growth_pct=mrr_growth_pct,
        churn_rate=0.032,
        nps=52,
        pipeline_coverage=4.2,
        proof_score=68.0,
    )

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "health_score": health["score"],
        "tier": health["tier"],
        "tier_ar": health["tier_ar"],
        "label": _label("health_score"),
        "components": health["components"],
        "interpretation_ar": (
            "درجة صحة الشركة تقيس نمو الإيراد والاحتفاظ بالعملاء وجودة خط الأنابيب."
        ),
        "interpretation_en": (
            "Company health score measures revenue growth, retention, "
            "pipeline quality, NPS, and proof strength."
        ),
    }


# ===========================================================================
# /api/v1/kpi-dashboard — snapshot router (pure Python, no DB, no auth)
# ===========================================================================

from pydantic import BaseModel, Field as _Field  # noqa: E402

# ---------------------------------------------------------------------------
# Static data: KPI definitions
# ---------------------------------------------------------------------------

_KPI_DEFINITIONS: dict[str, dict[str, Any]] = {
    "mrr_growth": {
        "kpi_id": "mrr_growth",
        "name_en": "MRR Growth Rate",
        "name_ar": "معدل نمو الإيراد الشهري المتكرر",
        "description_en": "Month-over-month percentage growth in monthly recurring revenue.",
        "unit": "%",
        "direction": "up_is_good",
        "target_source_en": "Company revenue target set by founder.",
    },
    "nrr": {
        "kpi_id": "nrr",
        "name_en": "Net Revenue Retention",
        "name_ar": "صافي الاحتفاظ بالإيرادات",
        "description_en": "Percentage of recurring revenue retained from existing customers including expansion.",
        "unit": "%",
        "direction": "up_is_good",
        "target_source_en": "SaaS industry benchmark (world-class >= 120%).",
    },
    "churn_rate": {
        "kpi_id": "churn_rate",
        "name_en": "Churn Rate",
        "name_ar": "معدل الإلغاء",
        "description_en": "Percentage of customers or revenue lost per month.",
        "unit": "%",
        "direction": "down_is_good",
        "target_source_en": "SaaS benchmark (world-class < 2% monthly).",
    },
    "data_quality_score": {
        "kpi_id": "data_quality_score",
        "name_en": "Data Quality Score",
        "name_ar": "درجة جودة البيانات",
        "description_en": "Composite score measuring completeness, accuracy, and freshness of client data.",
        "unit": "score",
        "direction": "up_is_good",
        "target_source_en": "Dealix internal standard (target >= 80).",
    },
    "pipeline_velocity_days": {
        "kpi_id": "pipeline_velocity_days",
        "name_en": "Pipeline Velocity (Days)",
        "name_ar": "سرعة خط الأنابيب (أيام)",
        "description_en": "Average number of days a deal spends moving through the full pipeline.",
        "unit": "days",
        "direction": "down_is_good",
        "target_source_en": "Saudi B2B benchmark (world-class <= 30 days).",
    },
    "customer_health_score": {
        "kpi_id": "customer_health_score",
        "name_en": "Customer Health Score",
        "name_ar": "درجة صحة العميل",
        "description_en": "Composite score measuring engagement, satisfaction, and expansion likelihood.",
        "unit": "score",
        "direction": "up_is_good",
        "target_source_en": "Dealix internal standard (target >= 75).",
    },
    "saudization_pct": {
        "kpi_id": "saudization_pct",
        "name_en": "Saudization Percentage",
        "name_ar": "نسبة السعودة",
        "description_en": "Percentage of Saudi nationals in the workforce relative to Vision 2030 targets.",
        "unit": "%",
        "direction": "up_is_good",
        "target_source_en": "Vision 2030 and Nitaqat compliance requirements.",
    },
    "zatca_compliance_pct": {
        "kpi_id": "zatca_compliance_pct",
        "name_en": "ZATCA Compliance Rate",
        "name_ar": "معدل الامتثال للزكاة",
        "description_en": "Percentage of transactions and invoices fully compliant with ZATCA e-invoicing rules.",
        "unit": "%",
        "direction": "up_is_good",
        "target_source_en": "ZATCA Phase 2 mandate (target 100%).",
    },
}

# ---------------------------------------------------------------------------
# Static data: dashboard views
# ---------------------------------------------------------------------------

_DASHBOARD_VIEWS: list[dict[str, Any]] = [
    {
        "view_id": "executive",
        "name_en": "Executive View",
        "name_ar": "العرض التنفيذي",
        "kpi_ids": ["mrr_growth", "nrr", "churn_rate", "saudization_pct"],
        "audience_en": "C-level executives and board members.",
        "audience_ar": "المسؤولون التنفيذيون وأعضاء مجلس الإدارة.",
    },
    {
        "view_id": "operations",
        "name_en": "Operations View",
        "name_ar": "العرض التشغيلي",
        "kpi_ids": ["data_quality_score", "pipeline_velocity_days", "zatca_compliance_pct"],
        "audience_en": "Operations leads and delivery managers.",
        "audience_ar": "مسؤولو العمليات ومديرو التسليم.",
    },
    {
        "view_id": "customer_success",
        "name_en": "Customer Success View",
        "name_ar": "عرض نجاح العملاء",
        "kpi_ids": ["customer_health_score", "nrr", "churn_rate", "data_quality_score"],
        "audience_en": "Customer success managers and account owners.",
        "audience_ar": "مديرو نجاح العملاء وأصحاب الحسابات.",
    },
]

# ---------------------------------------------------------------------------
# Static data: Saudi KPI benchmarks
# ---------------------------------------------------------------------------

_SAUDI_KPI_BENCHMARKS: dict[str, dict[str, Any]] = {
    "mrr_growth": {"world_class": 20.0, "saudi_median": 8.0, "unit": "%"},
    "nrr": {"world_class": 120.0, "saudi_median": 100.0, "unit": "%"},
    "churn_rate": {"world_class": 1.0, "saudi_median": 4.0, "unit": "%"},
    "data_quality_score": {"world_class": 90.0, "saudi_median": 65.0, "unit": "score"},
    "pipeline_velocity_days": {"world_class": 30.0, "saudi_median": 55.0, "unit": "days"},
    "customer_health_score": {"world_class": 85.0, "saudi_median": 68.0, "unit": "score"},
    "saudization_pct": {"world_class": 80.0, "saudi_median": 55.0, "unit": "%"},
    "zatca_compliance_pct": {"world_class": 100.0, "saudi_median": 85.0, "unit": "%"},
}

_SNAPSHOT_DISCLAIMER_EN = (
    "KPI snapshot values are self-reported and unaudited. "
    "All benchmarks are estimates. Review before sharing externally."
)
_SNAPSHOT_DISCLAIMER_AR = (
    "قيم لقطة KPI مُبلَّغ عنها ذاتيًا وغير مدققة. "
    "جميع المعايير تقديرية. راجع قبل المشاركة الخارجية."
)

# ---------------------------------------------------------------------------
# Pydantic model for snapshot
# ---------------------------------------------------------------------------


class KPISnapshotInput(BaseModel):
    company_name: str
    period_label_en: str
    mrr_growth_pct: float
    nrr_pct: float
    churn_rate_pct: float
    data_quality_score: float = _Field(..., ge=0, le=100)
    pipeline_velocity_days: float = _Field(..., ge=0)
    customer_health_score: float = _Field(..., ge=0, le=100)
    saudization_pct: float = _Field(..., ge=0, le=100)
    zatca_compliance_pct: float = _Field(..., ge=0, le=100)


# ---------------------------------------------------------------------------
# Pure-function core: build KPI snapshot
# ---------------------------------------------------------------------------

_KPI_INPUT_MAP: dict[str, str] = {
    "mrr_growth": "mrr_growth_pct",
    "nrr": "nrr_pct",
    "churn_rate": "churn_rate_pct",
    "data_quality_score": "data_quality_score",
    "pipeline_velocity_days": "pipeline_velocity_days",
    "customer_health_score": "customer_health_score",
    "saudization_pct": "saudization_pct",
    "zatca_compliance_pct": "zatca_compliance_pct",
}


def _build_kpi_snapshot(inp: KPISnapshotInput) -> dict[str, Any]:
    """Compute a KPI snapshot with benchmark comparison for a given company period.

    Returns a structured dict with kpi_scores, top_performers, needs_attention,
    overall_grade, and disclaimers.
    """
    kpi_scores: list[dict[str, Any]] = []
    above_count = 0

    for kpi_id, field_name in _KPI_INPUT_MAP.items():
        value = getattr(inp, field_name)
        definition = _KPI_DEFINITIONS[kpi_id]
        benchmark = _SAUDI_KPI_BENCHMARKS[kpi_id]
        median = benchmark["saudi_median"]
        direction = definition["direction"]

        if direction == "up_is_good":
            if value > median:
                vs_benchmark = "above_median"
                above_count += 1
            elif value == median:
                vs_benchmark = "at_median"
            else:
                vs_benchmark = "below_median"
        else:  # down_is_good
            if value < median:
                vs_benchmark = "above_median"
                above_count += 1
            elif value == median:
                vs_benchmark = "at_median"
            else:
                vs_benchmark = "below_median"

        kpi_scores.append(
            {
                "kpi_id": kpi_id,
                "value": value,
                "vs_benchmark": vs_benchmark,
                "unit": benchmark["unit"],
            }
        )

    top_performers = [
        s["kpi_id"] for s in kpi_scores if s["vs_benchmark"] == "above_median"
    ][:3]
    needs_attention = [
        s["kpi_id"] for s in kpi_scores if s["vs_benchmark"] == "below_median"
    ][:3]

    if above_count >= 6:
        overall_grade = "A"
    elif above_count >= 4:
        overall_grade = "B"
    elif above_count >= 2:
        overall_grade = "C"
    else:
        overall_grade = "D"

    return {
        "company_name": inp.company_name,
        "period_label_en": inp.period_label_en,
        "kpi_scores": kpi_scores,
        "top_performers": top_performers,
        "needs_attention": needs_attention,
        "overall_grade": overall_grade,
        "governance_decision": "ALLOW_WITH_REVIEW",
        "disclaimer_en": _SNAPSHOT_DISCLAIMER_EN,
        "disclaimer_ar": _SNAPSHOT_DISCLAIMER_AR,
    }


# ---------------------------------------------------------------------------
# Second router: /api/v1/kpi-dashboard (pure Python, no auth, no DB)
# ---------------------------------------------------------------------------

router_v2 = APIRouter(
    prefix="/api/v1/kpi-dashboard",
    tags=["Analytics"],
)


@router_v2.get("/definitions", summary="All 8 KPI definitions")
def get_kpi_definitions() -> dict[str, Any]:
    """Return all KPI definitions with bilingual labels, units, and direction."""
    return {
        "definitions": list(_KPI_DEFINITIONS.values()),
        "total_kpis": len(_KPI_DEFINITIONS),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router_v2.get("/views", summary="All 3 dashboard views")
def get_dashboard_views() -> dict[str, Any]:
    """Return all dashboard views with bilingual labels and KPI groupings."""
    return {
        "views": _DASHBOARD_VIEWS,
        "total_views": len(_DASHBOARD_VIEWS),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router_v2.post("/snapshot", summary="Generate a KPI snapshot with benchmark comparison")
def create_kpi_snapshot(body: KPISnapshotInput) -> dict[str, Any]:
    """Accept company KPI values and return a structured benchmark comparison.

    Governance decision: ALLOW_WITH_REVIEW.
    """
    return _build_kpi_snapshot(body)
