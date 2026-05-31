"""Health Intelligence API — cross-client health scoring, trends, and benchmarks.

Endpoints:
  GET  /api/v1/health-intelligence/portfolio     — all clients' health portfolio
  GET  /api/v1/health-intelligence/trends        — health score trends (12 months)
  GET  /api/v1/health-intelligence/benchmarks    — sector benchmarks
  POST /api/v1/health-intelligence/compute       — compute health score for new data
  GET  /api/v1/health-intelligence/alerts        — active health alerts
  GET  /api/v1/health-intelligence/leaderboard   — top 5 healthiest clients

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - governance_decision: ALLOW_WITH_REVIEW
  - Bilingual ar/en labels
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, Literal

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/health-intelligence",
    tags=["health-intelligence"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"
_NOW = datetime.now(UTC)

# ---------------------------------------------------------------------------
# Health dimension definitions
# ---------------------------------------------------------------------------

DIMENSIONS: list[dict[str, Any]] = [
    {
        "id": "data_readiness",
        "label_ar": "جاهزية البيانات",
        "label_en": "Data Readiness",
        "description_ar": "جودة وجاهزية بيانات العميل للتحليل",
        "description_en": "Quality and readiness of client data for analysis",
        "weight": 0.20,
        "max_score": 100,
    },
    {
        "id": "onboarding_ops",
        "label_ar": "عمليات التأهيل",
        "label_en": "Onboarding Operations",
        "description_ar": "مدى اكتمال عملية تأهيل العميل ونجاحها",
        "description_en": "Completeness and success of client onboarding",
        "weight": 0.15,
        "max_score": 100,
    },
    {
        "id": "delivery_quality",
        "label_ar": "جودة التسليم",
        "label_en": "Delivery Quality",
        "description_ar": "جودة المخرجات والتسليمات للعميل",
        "description_en": "Quality of deliverables and outputs to the client",
        "weight": 0.20,
        "max_score": 100,
    },
    {
        "id": "zatca_compliance",
        "label_ar": "امتثال ZATCA",
        "label_en": "ZATCA Compliance",
        "description_ar": "مستوى الامتثال لمتطلبات هيئة الزكاة والضريبة",
        "description_en": "Compliance level with ZATCA requirements",
        "weight": 0.15,
        "max_score": 100,
    },
    {
        "id": "client_retention",
        "label_ar": "احتفاظ العملاء",
        "label_en": "Client Retention",
        "description_ar": "احتمالية استمرار العميل وتجديد اشتراكه",
        "description_en": "Probability of client continuation and renewal",
        "weight": 0.20,
        "max_score": 100,
    },
    {
        "id": "recurring_revenue",
        "label_ar": "الإيراد المتكرر",
        "label_en": "Recurring Revenue",
        "description_ar": "استقرار ونمو الإيرادات المتكررة من العميل",
        "description_en": "Stability and growth of recurring revenue from client",
        "weight": 0.10,
        "max_score": 100,
    },
]

# ---------------------------------------------------------------------------
# Mock portfolio — 8 clients with 6-dimension health scores
# ---------------------------------------------------------------------------

_PORTFOLIO: list[dict[str, Any]] = [
    {
        "client_id": "CLT-001",
        "company_ar": "شركة الأفق للتقنية",
        "company_en": "Horizon Technology",
        "sector": "technology",
        "tier": "professional",
        "dimensions": {
            "data_readiness": 88,
            "onboarding_ops": 75,
            "delivery_quality": 82,
            "zatca_compliance": 90,
            "client_retention": 85,
            "recurring_revenue": 78,
        },
        "trend_30d": +5,
    },
    {
        "client_id": "CLT-002",
        "company_ar": "مجموعة الريادة للاستشارات",
        "company_en": "Riyadah Consulting",
        "sector": "professional_services",
        "tier": "essential",
        "dimensions": {
            "data_readiness": 71,
            "onboarding_ops": 68,
            "delivery_quality": 74,
            "zatca_compliance": 65,
            "client_retention": 70,
            "recurring_revenue": 62,
        },
        "trend_30d": +2,
    },
    {
        "client_id": "CLT-003",
        "company_ar": "شركة النخبة الطبية",
        "company_en": "Elite Medical",
        "sector": "healthcare",
        "tier": "enterprise",
        "dimensions": {
            "data_readiness": 45,
            "onboarding_ops": 38,
            "delivery_quality": 52,
            "zatca_compliance": 40,
            "client_retention": 35,
            "recurring_revenue": 42,
        },
        "trend_30d": -8,
    },
    {
        "client_id": "CLT-004",
        "company_ar": "التوسع العقاري السعودي",
        "company_en": "Saudi RE Expansion",
        "sector": "real_estate",
        "tier": "professional",
        "dimensions": {
            "data_readiness": 85,
            "onboarding_ops": 80,
            "delivery_quality": 88,
            "zatca_compliance": 75,
            "client_retention": 88,
            "recurring_revenue": 82,
        },
        "trend_30d": +3,
    },
    {
        "client_id": "CLT-005",
        "company_ar": "أكاديمية المستقبل للتعليم",
        "company_en": "Future Academy",
        "sector": "education",
        "tier": "essential",
        "dimensions": {
            "data_readiness": 60,
            "onboarding_ops": 55,
            "delivery_quality": 58,
            "zatca_compliance": 50,
            "client_retention": 48,
            "recurring_revenue": 52,
        },
        "trend_30d": 0,
    },
    {
        "client_id": "CLT-006",
        "company_ar": "سلسلة المتاجر الذكية",
        "company_en": "Smart Retail Chain",
        "sector": "retail",
        "tier": "professional",
        "dimensions": {
            "data_readiness": 75,
            "onboarding_ops": 70,
            "delivery_quality": 72,
            "zatca_compliance": 68,
            "client_retention": 74,
            "recurring_revenue": 70,
        },
        "trend_30d": +1,
    },
    {
        "client_id": "CLT-007",
        "company_ar": "خدمات اللوجستيات المتقدمة",
        "company_en": "Advanced Logistics",
        "sector": "logistics",
        "tier": "essential",
        "dimensions": {
            "data_readiness": 68,
            "onboarding_ops": 65,
            "delivery_quality": 70,
            "zatca_compliance": 88,
            "client_retention": 65,
            "recurring_revenue": 60,
        },
        "trend_30d": +4,
    },
    {
        "client_id": "CLT-008",
        "company_ar": "مصنع الجودة العالية",
        "company_en": "High Quality Mfg",
        "sector": "manufacturing",
        "tier": "enterprise",
        "dimensions": {
            "data_readiness": 90,
            "onboarding_ops": 88,
            "delivery_quality": 92,
            "zatca_compliance": 85,
            "client_retention": 90,
            "recurring_revenue": 88,
        },
        "trend_30d": +2,
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _compute_weighted_score(dimensions: dict[str, int]) -> float:
    total = 0.0
    for dim in DIMENSIONS:
        score = dimensions.get(dim["id"], 0)
        total += score * dim["weight"]
    return round(total, 1)


def _health_tier(score: float) -> dict[str, str]:
    if score >= 75:
        return {"tier": "healthy", "ar": "بصحة جيدة", "en": "Healthy", "color": "green"}
    if score >= 55:
        return {"tier": "moderate", "ar": "معتدل", "en": "Moderate", "color": "amber"}
    if score >= 35:
        return {"tier": "at_risk", "ar": "في خطر", "en": "At Risk", "color": "orange"}
    return {"tier": "critical", "ar": "حرج", "en": "Critical", "color": "red"}


def _trend_label(trend_30d: int) -> dict[str, str]:
    if trend_30d > 5:
        return {"ar": "تحسن ملحوظ", "en": "Notable improvement"}
    if trend_30d > 0:
        return {"ar": "تحسن طفيف", "en": "Slight improvement"}
    if trend_30d == 0:
        return {"ar": "مستقر", "en": "Stable"}
    if trend_30d > -5:
        return {"ar": "تراجع طفيف", "en": "Slight decline"}
    return {"ar": "تراجع ملحوظ", "en": "Notable decline"}


def _enrich_client(client: dict[str, Any]) -> dict[str, Any]:
    score = _compute_weighted_score(client["dimensions"])
    tier_info = _health_tier(score)
    trend = client.get("trend_30d", 0)
    return {
        "client_id": client["client_id"],
        "company": {"ar": client["company_ar"], "en": client["company_en"]},
        "sector": client["sector"],
        "tier": client["tier"],
        "health_score": score,
        "health_tier": tier_info,
        "trend_30d": trend,
        "trend_label": _trend_label(trend),
        "dimensions": {
            dim["id"]: {
                "score": client["dimensions"].get(dim["id"], 0),
                "label": {"ar": dim["label_ar"], "en": dim["label_en"]},
                "weight_pct": round(dim["weight"] * 100),
            }
            for dim in DIMENSIONS
        },
        "weakest_dimension": min(
            DIMENSIONS, key=lambda d: client["dimensions"].get(d["id"], 0)
        )["id"],
    }


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class HealthComputeBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_name: str = Field(min_length=1, max_length=200)
    data_readiness: int = Field(ge=0, le=100, default=50)
    onboarding_ops: int = Field(ge=0, le=100, default=50)
    delivery_quality: int = Field(ge=0, le=100, default=50)
    zatca_compliance: int = Field(ge=0, le=100, default=50)
    client_retention: int = Field(ge=0, le=100, default=50)
    recurring_revenue: int = Field(ge=0, le=100, default=50)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/portfolio")
async def health_portfolio() -> dict[str, Any]:
    """Full portfolio view — all clients with health scores and trends."""
    enriched = [_enrich_client(c) for c in _PORTFOLIO]
    enriched.sort(key=lambda x: x["health_score"], reverse=True)

    scores = [c["health_score"] for c in enriched]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0
    at_risk = [c for c in enriched if c["health_score"] < 55]

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "portfolio_summary": {
            "total_clients": len(enriched),
            "avg_health_score": avg_score,
            "healthy_count": sum(1 for c in enriched if c["health_score"] >= 75),
            "at_risk_count": len(at_risk),
            "critical_count": sum(1 for c in enriched if c["health_score"] < 35),
        },
        "clients": enriched,
        "dimension_definitions": [
            {
                "id": d["id"],
                "label": {"ar": d["label_ar"], "en": d["label_en"]},
                "weight_pct": round(d["weight"] * 100),
            }
            for d in DIMENSIONS
        ],
    }


@router.get("/leaderboard")
async def health_leaderboard(top: int = 5) -> dict[str, Any]:
    """Top N healthiest clients with achievement badges."""
    enriched = [_enrich_client(c) for c in _PORTFOLIO]
    top_clients = sorted(enriched, key=lambda x: x["health_score"], reverse=True)[:top]

    for i, client in enumerate(top_clients):
        if i == 0:
            client["badge_ar"] = "الأفضل أداءً"
            client["badge_en"] = "Top Performer"
        elif i <= 2:
            client["badge_ar"] = "أداء ممتاز"
            client["badge_en"] = "Excellent"
        else:
            client["badge_ar"] = "أداء جيد"
            client["badge_en"] = "Strong"

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "leaderboard": top_clients,
        "note_ar": "يُشجَّع مشاركة هذه النتائج مع العملاء كدليل على جودة الخدمة",
        "note_en": "Consider sharing these results with clients as proof of service quality",
    }


@router.get("/alerts")
async def health_alerts() -> dict[str, Any]:
    """Active health alerts — clients needing immediate attention."""
    enriched = [_enrich_client(c) for c in _PORTFOLIO]
    alerts: list[dict[str, Any]] = []

    for client in enriched:
        score = client["health_score"]
        trend = client["trend_30d"]

        if score < 35:
            alerts.append({
                "severity": "critical",
                "client_id": client["client_id"],
                "company": client["company"],
                "health_score": score,
                "alert_ar": "درجة صحة حرجة — يتطلب تدخل فوري",
                "alert_en": "Critical health score — immediate intervention required",
                "recommended_action_ar": "اتصل بالعميل خلال 24 ساعة، عرض Sprint إنقاذ",
                "recommended_action_en": "Call client within 24 hours, offer rescue Sprint",
            })
        elif score < 55:
            alerts.append({
                "severity": "high",
                "client_id": client["client_id"],
                "company": client["company"],
                "health_score": score,
                "alert_ar": "درجة صحة منخفضة — يتطلب متابعة خلال 72 ساعة",
                "alert_en": "Low health score — follow-up required within 72 hours",
                "recommended_action_ar": "أرسل Proof Pack محدث، حدد موعد مراجعة",
                "recommended_action_en": "Send updated Proof Pack, schedule review call",
            })
        elif trend < -5:
            alerts.append({
                "severity": "medium",
                "client_id": client["client_id"],
                "company": client["company"],
                "health_score": score,
                "trend_30d": trend,
                "alert_ar": "تراجع ملحوظ في درجة الصحة — مراقبة مكثفة مطلوبة",
                "alert_en": "Notable health score decline — increased monitoring required",
                "recommended_action_ar": "افحص الأبعاد المتراجعة، ناقش مع العميل",
                "recommended_action_en": "Review declining dimensions, discuss with client",
            })

    alerts.sort(key=lambda a: {"critical": 0, "high": 1, "medium": 2}.get(a["severity"], 3))

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "alert_count": len(alerts),
        "critical_count": sum(1 for a in alerts if a["severity"] == "critical"),
        "high_count": sum(1 for a in alerts if a["severity"] == "high"),
        "alerts": alerts,
    }


@router.get("/benchmarks")
async def health_benchmarks() -> dict[str, Any]:
    """Sector benchmarks for health score dimensions."""
    benchmarks = {
        "technology": {
            "avg_overall": 74,
            "data_readiness": 78,
            "zatca_compliance": 82,
            "client_retention": 72,
        },
        "healthcare": {
            "avg_overall": 68,
            "data_readiness": 65,
            "zatca_compliance": 70,
            "client_retention": 75,
        },
        "real_estate": {
            "avg_overall": 71,
            "data_readiness": 70,
            "zatca_compliance": 68,
            "client_retention": 76,
        },
        "professional_services": {
            "avg_overall": 69,
            "data_readiness": 67,
            "zatca_compliance": 72,
            "client_retention": 70,
        },
        "all_sectors": {
            "avg_overall": 71,
            "data_readiness": 73,
            "zatca_compliance": 74,
            "client_retention": 72,
        },
    }

    portfolio_scores = [_compute_weighted_score(c["dimensions"]) for c in _PORTFOLIO]
    dealix_avg = round(sum(portfolio_scores) / len(portfolio_scores), 1)

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "dealix_portfolio_avg": dealix_avg,
        "saudi_b2b_benchmark": benchmarks["all_sectors"]["avg_overall"],
        "dealix_vs_benchmark": round(dealix_avg - benchmarks["all_sectors"]["avg_overall"], 1),
        "sector_benchmarks": benchmarks,
        "note_ar": "المعايير المرجعية مبنية على متوسطات السوق السعودي B2B 2026",
        "note_en": "Benchmarks based on Saudi B2B market averages 2026",
        "disclaimer_ar": "أرقام تقديرية للاسترشاد — ليست ضمانات.",
        "disclaimer_en": "Indicative figures for guidance — not guarantees.",
    }


@router.get("/trends")
async def health_trends(months: int = 6) -> dict[str, Any]:
    """Portfolio health score trends over the past N months."""
    base_score = 68.0
    trend_data: list[dict[str, Any]] = []
    for i in range(months, 0, -1):
        month_dt = _NOW - timedelta(days=30 * i)
        # Simulate gradual improvement with slight variability
        offset = (months - i) * 0.8
        noise = ((i * 7) % 3) - 1  # deterministic noise: -1, 0, or 1
        score = round(base_score + offset + noise, 1)
        at_risk_count = max(0, 3 - (months - i) // 2)
        trend_data.append({
            "month": month_dt.strftime("%Y-%m"),
            "avg_score": score,
            "at_risk_clients": at_risk_count,
            "healthy_clients": max(0, len(_PORTFOLIO) - at_risk_count - 1),
        })

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "months": months,
        "trend": trend_data,
        "current_avg": _compute_weighted_score(
            {d["id"]: sum(c["dimensions"].get(d["id"], 0) for c in _PORTFOLIO) // len(_PORTFOLIO)
             for d in DIMENSIONS}
        ),
        "trend_direction": "improving" if len(trend_data) > 1 and trend_data[-1]["avg_score"] > trend_data[0]["avg_score"] else "stable",
    }


@router.post("/compute")
async def compute_health_score(body: HealthComputeBody = Body(...)) -> dict[str, Any]:
    """Compute a weighted health score for a new or hypothetical client."""
    dimensions = {
        "data_readiness": body.data_readiness,
        "onboarding_ops": body.onboarding_ops,
        "delivery_quality": body.delivery_quality,
        "zatca_compliance": body.zatca_compliance,
        "client_retention": body.client_retention,
        "recurring_revenue": body.recurring_revenue,
    }
    score = _compute_weighted_score(dimensions)
    tier_info = _health_tier(score)

    weakest_dim = min(DIMENSIONS, key=lambda d: dimensions.get(d["id"], 0))
    strongest_dim = max(DIMENSIONS, key=lambda d: dimensions.get(d["id"], 0))

    # Benchmarking
    saudi_b2b_avg = 71.0
    vs_benchmark = round(score - saudi_b2b_avg, 1)

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "company": body.company_name,
        "health_score": score,
        "health_tier": tier_info,
        "dimension_scores": dimensions,
        "weakest_dimension": {
            "id": weakest_dim["id"],
            "label": {"ar": weakest_dim["label_ar"], "en": weakest_dim["label_en"]},
            "score": dimensions[weakest_dim["id"]],
            "improvement_tip_ar": "ركّز على تحسين هذا البُعد للحصول على أكبر تأثير",
            "improvement_tip_en": "Focus on improving this dimension for maximum impact",
        },
        "strongest_dimension": {
            "id": strongest_dim["id"],
            "label": {"ar": strongest_dim["label_ar"], "en": strongest_dim["label_en"]},
            "score": dimensions[strongest_dim["id"]],
        },
        "vs_saudi_b2b_benchmark": {
            "benchmark": saudi_b2b_avg,
            "delta": vs_benchmark,
            "label_ar": "مقارنة بمتوسط السوق السعودي B2B",
            "label_en": "vs Saudi B2B market average",
        },
        "recommended_tier_ar": (
            "Custom AI" if score >= 80
            else ("Managed Ops" if score >= 65 else ("Sprint 499 SAR" if score >= 40 else "Free Diagnostic"))
        ),
        "recommended_tier_en": (
            "Custom AI" if score >= 80
            else ("Managed Ops" if score >= 65 else ("Sprint 499 SAR" if score >= 40 else "Free Diagnostic"))
        ),
    }
