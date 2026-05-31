"""Analytics Ops — admin-gated read-only business performance metrics.

Aggregates feature adoption, content performance, sprint delivery, sales
funnel, sector breakdown, and monthly report for the founder.

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return governance_decision field
  - Read-only: ALLOW_WITH_REVIEW
  - Bilingual ar/en labels
  - Estimate figures clearly labeled
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["analytics-ops"],
    dependencies=[Depends(require_admin_key)],
)

# ---------------------------------------------------------------------------
# Governance constant
# ---------------------------------------------------------------------------

_GOV_READ = "ALLOW_WITH_REVIEW"

# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------

# Weekly active users by feature — last 4 weeks
_WEEKLY_FEATURE_USAGE: list[dict[str, Any]] = [
    {
        "week": "W-4",
        "dashboard": 12,
        "pipeline": 8,
        "health": 10,
        "subscriptions": 7,
        "invoices": 5,
        "proof_packs": 9,
        "cockpit": 6,
    },
    {
        "week": "W-3",
        "dashboard": 14,
        "pipeline": 9,
        "health": 11,
        "subscriptions": 8,
        "invoices": 6,
        "proof_packs": 10,
        "cockpit": 7,
    },
    {
        "week": "W-2",
        "dashboard": 15,
        "pipeline": 11,
        "health": 13,
        "subscriptions": 10,
        "invoices": 8,
        "proof_packs": 11,
        "cockpit": 9,
    },
    {
        "week": "W-1",
        "dashboard": 16,
        "pipeline": 12,
        "health": 14,
        "subscriptions": 11,
        "invoices": 9,
        "proof_packs": 13,
        "cockpit": 11,
    },
]

_FEATURE_NAMES: list[str] = [
    "dashboard",
    "pipeline",
    "health",
    "subscriptions",
    "invoices",
    "proof_packs",
    "cockpit",
]

# LinkedIn content performance — last 5 posts
_CONTENT_POSTS: list[dict[str, Any]] = [
    {
        "post_id": "LI-001",
        "topic_ar": "كيف تحسّن إدارة بيانات الزاتكا عائد الاستثمار",
        "topic_en": "How ZATCA Data Management Improves ROI",
        "published_date": "2026-05-02",
        "impressions_estimate": 3200,
        "engagements_estimate": 180,
        "leads_generated_estimate": 4,
        "is_estimate": True,
    },
    {
        "post_id": "LI-002",
        "topic_ar": "ثلاثة أخطاء شائعة في بيانات العملاء بالسعودية",
        "topic_en": "Three Common Customer Data Mistakes in Saudi Arabia",
        "published_date": "2026-05-09",
        "impressions_estimate": 4800,
        "engagements_estimate": 310,
        "leads_generated_estimate": 7,
        "is_estimate": True,
    },
    {
        "post_id": "LI-003",
        "topic_ar": "دراسة حالة: تحسين دقة البيانات لشركة لوجستية",
        "topic_en": "Case Study: Improving Data Quality for a Logistics Company",
        "published_date": "2026-05-16",
        "impressions_estimate": 5600,
        "engagements_estimate": 420,
        "leads_generated_estimate": 11,
        "is_estimate": True,
    },
    {
        "post_id": "LI-004",
        "topic_ar": "لماذا تفشل مشاريع الذكاء الاصطناعي في المملكة؟",
        "topic_en": "Why AI Projects Fail in Saudi Arabia?",
        "published_date": "2026-05-23",
        "impressions_estimate": 7100,
        "engagements_estimate": 560,
        "leads_generated_estimate": 14,
        "is_estimate": True,
    },
    {
        "post_id": "LI-005",
        "topic_ar": "الفرق بين البيانات النظيفة والقرارات الصحيحة",
        "topic_en": "The Difference Between Clean Data and Sound Decisions",
        "published_date": "2026-05-30",
        "impressions_estimate": 4200,
        "engagements_estimate": 280,
        "leads_generated_estimate": 6,
        "is_estimate": True,
    },
]

# Sprint performance — last 6 sprints
_SPRINTS: list[dict[str, Any]] = [
    {
        "sprint_id": "SP-2025-11-001",
        "client_id": "client_alpha",
        "duration_days": 7,
        "dq_score_improvement": 12,
        "zatca_compliance_achieved": True,
        "on_time": True,
        "nps_score": 9,
        "month": "2025-11",
    },
    {
        "sprint_id": "SP-2025-12-001",
        "client_id": "client_beta",
        "duration_days": 9,
        "dq_score_improvement": 8,
        "zatca_compliance_achieved": False,
        "on_time": False,
        "nps_score": 7,
        "month": "2025-12",
    },
    {
        "sprint_id": "SP-2026-01-001",
        "client_id": "client_gamma",
        "duration_days": 6,
        "dq_score_improvement": 15,
        "zatca_compliance_achieved": True,
        "on_time": True,
        "nps_score": 10,
        "month": "2026-01",
    },
    {
        "sprint_id": "SP-2026-02-001",
        "client_id": "client_delta",
        "duration_days": 8,
        "dq_score_improvement": 10,
        "zatca_compliance_achieved": True,
        "on_time": True,
        "nps_score": 8,
        "month": "2026-02",
    },
    {
        "sprint_id": "SP-2026-03-001",
        "client_id": "client_epsilon",
        "duration_days": 5,
        "dq_score_improvement": 18,
        "zatca_compliance_achieved": True,
        "on_time": True,
        "nps_score": 9,
        "month": "2026-03",
    },
    {
        "sprint_id": "SP-2026-04-001",
        "client_id": "client_zeta",
        "duration_days": 7,
        "dq_score_improvement": 11,
        "zatca_compliance_achieved": False,
        "on_time": False,
        "nps_score": 7,
        "month": "2026-04",
    },
]

# Conversion funnel — current month estimates
_FUNNEL_STAGES: list[dict[str, Any]] = [
    {
        "stage_name_ar": "العملاء المحتملون",
        "stage_name_en": "Leads In",
        "count": 42,
        "is_estimate": True,
    },
    {
        "stage_name_ar": "العملاء المؤهلون",
        "stage_name_en": "Qualified",
        "count": 28,
        "is_estimate": True,
    },
    {
        "stage_name_ar": "تم إرسال التشخيص",
        "stage_name_en": "Diagnostic Sent",
        "count": 18,
        "is_estimate": True,
    },
    {
        "stage_name_ar": "تم اقتراح السبرينت",
        "stage_name_en": "Sprint Proposed",
        "count": 12,
        "is_estimate": True,
    },
    {
        "stage_name_ar": "السبرينت نشط",
        "stage_name_en": "Sprint Active",
        "count": 8,
        "is_estimate": True,
    },
    {
        "stage_name_ar": "مغلق",
        "stage_name_en": "Closed",
        "count": 6,
        "is_estimate": True,
    },
]

# Sector breakdown — demo data
_SECTORS: list[dict[str, Any]] = [
    {
        "sector_ar": "اللوجستيات",
        "sector_en": "Logistics",
        "client_count": 3,
        "mrr_sar_estimate": 18000,
        "avg_health_score": 74,
        "is_estimate": True,
    },
    {
        "sector_ar": "الرعاية الصحية",
        "sector_en": "Healthcare",
        "client_count": 2,
        "mrr_sar_estimate": 14000,
        "avg_health_score": 71,
        "is_estimate": True,
    },
    {
        "sector_ar": "المالية",
        "sector_en": "Finance",
        "client_count": 2,
        "mrr_sar_estimate": 16000,
        "avg_health_score": 78,
        "is_estimate": True,
    },
    {
        "sector_ar": "التصنيع",
        "sector_en": "Manufacturing",
        "client_count": 2,
        "mrr_sar_estimate": 12000,
        "avg_health_score": 69,
        "is_estimate": True,
    },
    {
        "sector_ar": "التجزئة",
        "sector_en": "Retail",
        "client_count": 1,
        "mrr_sar_estimate": 5000,
        "avg_health_score": 65,
        "is_estimate": True,
    },
    {
        "sector_ar": "أخرى",
        "sector_en": "Other",
        "client_count": 2,
        "mrr_sar_estimate": 8000,
        "avg_health_score": 66,
        "is_estimate": True,
    },
]

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(UTC).isoformat()


def _compute_most_used_feature(weeks: list[dict[str, Any]]) -> str:
    """Return the feature name with the highest average weekly active users."""
    if not weeks:
        return ""
    totals: dict[str, int] = {f: 0 for f in _FEATURE_NAMES}
    for week in weeks:
        for feature in _FEATURE_NAMES:
            totals[feature] += int(week.get(feature, 0))
    return max(totals, key=lambda f: totals[f])


def _compute_fastest_growing_feature(weeks: list[dict[str, Any]]) -> str:
    """Return the feature with the largest absolute growth from W-4 to W-1.

    Growth is computed as (W-1 value) - (W-4 value). When weeks contains
    fewer than 2 entries the first available feature is returned.
    """
    if len(weeks) < 2:
        return _FEATURE_NAMES[0] if _FEATURE_NAMES else ""
    first = weeks[0]
    last = weeks[-1]
    growth: dict[str, int] = {}
    for feature in _FEATURE_NAMES:
        growth[feature] = int(last.get(feature, 0)) - int(first.get(feature, 0))
    return max(growth, key=lambda f: growth[f])


def _build_usage_trend(weeks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return per-week total active users across all features."""
    trend: list[dict[str, Any]] = []
    for week in weeks:
        total = sum(int(week.get(f, 0)) for f in _FEATURE_NAMES)
        trend.append({"week": week.get("week", ""), "total_active_users": total})
    return trend


def _compute_sprint_rates(sprints: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute aggregate rates from a list of sprint records."""
    if not sprints:
        return {
            "total_sprints": 0,
            "on_time_rate_pct": 0.0,
            "avg_dq_improvement": 0.0,
            "avg_nps": 0.0,
            "zatca_compliance_rate_pct": 0.0,
        }
    total = len(sprints)
    on_time_count = sum(1 for s in sprints if s.get("on_time"))
    zatca_count = sum(1 for s in sprints if s.get("zatca_compliance_achieved"))
    avg_dq = sum(float(s.get("dq_score_improvement", 0)) for s in sprints) / total
    avg_nps = sum(float(s.get("nps_score", 0)) for s in sprints) / total
    return {
        "total_sprints": total,
        "on_time_rate_pct": round(on_time_count / total * 100, 1),
        "avg_dq_improvement": round(avg_dq, 1),
        "avg_nps": round(avg_nps, 2),
        "zatca_compliance_rate_pct": round(zatca_count / total * 100, 1),
    }


def _build_funnel_with_rates(stages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Annotate funnel stages with conversion_rate_pct from previous stage."""
    result: list[dict[str, Any]] = []
    for i, stage in enumerate(stages):
        entry = dict(stage)
        if i == 0:
            entry["conversion_rate_pct"] = 100.0
        else:
            prev_count = int(stages[i - 1].get("count", 0))
            curr_count = int(stage.get("count", 0))
            if prev_count > 0:
                entry["conversion_rate_pct"] = round(curr_count / prev_count * 100, 1)
            else:
                entry["conversion_rate_pct"] = 0.0
        result.append(entry)
    return result


def _compute_overall_conversion_pct(stages: list[dict[str, Any]]) -> float:
    """Return leads-in to closed conversion percentage."""
    if not stages:
        return 0.0
    first_count = int(stages[0].get("count", 0))
    last_count = int(stages[-1].get("count", 0))
    if first_count == 0:
        return 0.0
    return round(last_count / first_count * 100, 1)


def _build_key_metrics() -> dict[str, Any]:
    """Return the 8 KPIs for the monthly report."""
    sprint_rates = _compute_sprint_rates(_SPRINTS)
    total_clients = sum(s["client_count"] for s in _SECTORS)
    total_mrr = sum(s["mrr_sar_estimate"] for s in _SECTORS)
    total_impressions = sum(p["impressions_estimate"] for p in _CONTENT_POSTS)
    total_leads_content = sum(p["leads_generated_estimate"] for p in _CONTENT_POSTS)
    funnel_conversion = _compute_overall_conversion_pct(_FUNNEL_STAGES)
    return {
        "total_active_clients": total_clients,
        "mrr_sar_estimate": total_mrr,
        "sprints_delivered": sprint_rates["total_sprints"],
        "on_time_delivery_rate_pct": sprint_rates["on_time_rate_pct"],
        "avg_nps_score": sprint_rates["avg_nps"],
        "content_impressions_estimate": total_impressions,
        "content_leads_estimate": total_leads_content,
        "funnel_overall_conversion_pct": funnel_conversion,
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/feature-adoption")
async def get_feature_adoption() -> dict[str, Any]:
    """Weekly feature usage stats for the last 4 weeks."""
    most_used = _compute_most_used_feature(_WEEKLY_FEATURE_USAGE)
    fastest_growing = _compute_fastest_growing_feature(_WEEKLY_FEATURE_USAGE)
    usage_trend = _build_usage_trend(_WEEKLY_FEATURE_USAGE)
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "weeks_count": len(_WEEKLY_FEATURE_USAGE),
        "data": _WEEKLY_FEATURE_USAGE,
        "most_used_feature": most_used,
        "fastest_growing_feature": fastest_growing,
        "usage_trend": usage_trend,
        "is_estimate": True,
    }


@router.get("/content-performance")
async def get_content_performance() -> dict[str, Any]:
    """LinkedIn content performance for the last 5 posts."""
    total_impressions = sum(p["impressions_estimate"] for p in _CONTENT_POSTS)
    total_leads = sum(p["leads_generated_estimate"] for p in _CONTENT_POSTS)
    best_post = max(_CONTENT_POSTS, key=lambda p: p["leads_generated_estimate"])
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "posts": _CONTENT_POSTS,
        "total_impressions_estimate": total_impressions,
        "total_leads_estimate": total_leads,
        "best_performing_post_topic": best_post["topic_en"],
        "best_performing_post_topic_ar": best_post["topic_ar"],
        "best_performing_post_id": best_post["post_id"],
        "disclaimer": (
            "جميع أرقام LinkedIn تقديرية / All LinkedIn figures are estimates"
        ),
        "is_estimate": True,
    }


@router.get("/sprint-performance")
async def get_sprint_performance() -> dict[str, Any]:
    """Sprint delivery analytics for the last 6 sprints."""
    rates = _compute_sprint_rates(_SPRINTS)
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "total_sprints": rates["total_sprints"],
        "on_time_rate_pct": rates["on_time_rate_pct"],
        "avg_dq_improvement": rates["avg_dq_improvement"],
        "avg_nps": rates["avg_nps"],
        "zatca_compliance_rate_pct": rates["zatca_compliance_rate_pct"],
        "sprints": _SPRINTS,
        "is_estimate": False,
    }


@router.get("/conversion-funnel")
async def get_conversion_funnel() -> dict[str, Any]:
    """Sales conversion funnel for the current month."""
    stages_with_rates = _build_funnel_with_rates(_FUNNEL_STAGES)
    overall_conversion = _compute_overall_conversion_pct(_FUNNEL_STAGES)
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "stages": stages_with_rates,
        "overall_conversion_pct": overall_conversion,
        "disclaimer": (
            "جميع أرقام القمع تقديرية للشهر الحالي / "
            "All funnel figures are estimates for the current month"
        ),
        "is_estimate": True,
    }


@router.get("/sector-breakdown")
async def get_sector_breakdown() -> dict[str, Any]:
    """Clients and revenue breakdown by sector."""
    total_clients = sum(s["client_count"] for s in _SECTORS)
    total_mrr = sum(s["mrr_sar_estimate"] for s in _SECTORS)
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "sectors": _SECTORS,
        "total_clients": total_clients,
        "total_mrr_sar_estimate": total_mrr,
        "sector_count": len(_SECTORS),
        "is_estimate": True,
    }


@router.get("/monthly-report")
async def get_monthly_report() -> dict[str, Any]:
    """Structured monthly business report for the founder."""
    now = datetime.now(UTC)
    report_month = now.strftime("%Y-%m")
    key_metrics = _build_key_metrics()
    sprint_rates = _compute_sprint_rates(_SPRINTS)
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "report_month": report_month,
        "executive_summary_ar": (
            "حققت ديليكس في هذا الشهر أداءً قوياً عبر جميع المحاور الرئيسية: "
            "الاستحواذ على العملاء، وتسليم السبرينتات، والامتثال. "
            "سجّلت قمع المبيعات تحويلاً إجمالياً مع نمو ملحوظ في عدد العملاء المحتملين."
        ),
        "executive_summary_en": (
            "Dealix delivered strong performance across all key pillars this month: "
            "client acquisition, sprint delivery, and compliance. "
            "The sales funnel recorded solid overall conversion with notable growth "
            "in qualified leads."
        ),
        "top_3_wins_ar": [
            f"تسليم {sprint_rates['total_sprints']} سبرينتات مكتملة بمعدل التزام بالموعد {sprint_rates['on_time_rate_pct']}%",
            "تحسين درجة جودة البيانات بمتوسط "
            f"{sprint_rates['avg_dq_improvement']} نقطة لكل عميل",
            f"متوسط مؤشر صافي الترويج {sprint_rates['avg_nps']} — يشير إلى رضا العملاء",
        ],
        "top_3_wins_en": [
            f"{sprint_rates['total_sprints']} sprints completed with "
            f"{sprint_rates['on_time_rate_pct']}% on-time delivery rate",
            f"Data quality score improved by an average of "
            f"{sprint_rates['avg_dq_improvement']} points per client",
            f"Net Promoter Score averaged {sprint_rates['avg_nps']} — "
            "indicating strong client satisfaction",
        ],
        "top_3_challenges_ar": [
            "ضرورة تحسين معدل تحويل مرحلة اقتراح السبرينت",
            "بعض السبرينتات لم تحقق الامتثال لزاتكا — يستلزم مراجعة المنهجية",
            "قناة LinkedIn تحتاج إلى محتوى أكثر استهدافاً لتحسين معدل التحويل",
        ],
        "top_3_challenges_en": [
            "Sprint proposal conversion rate needs improvement",
            "Some sprints did not achieve ZATCA compliance — methodology review required",
            "LinkedIn channel requires more targeted content to improve conversion rate",
        ],
        "key_metrics": key_metrics,
        "next_month_priorities_ar": [
            "مضاعفة جهود الاستحواذ على العملاء في قطاع الرعاية الصحية والتمويل",
            "اطلاق برنامج تحسين الامتثال لزاتكا لجميع العملاء الجدد",
            "نشر ثلاث دراسات حالة موثّقة لتقوية حزمة الإثبات",
        ],
        "next_month_priorities_en": [
            "Double client acquisition efforts in the healthcare and finance sectors",
            "Launch ZATCA compliance improvement programme for all new clients",
            "Publish three documented case studies to strengthen the proof pack",
        ],
        "is_estimate": True,
    }
