"""Master Cockpit API — single-call founder intelligence aggregator.

Aggregates health, pipeline, retainer, growth, alerts, and ZATCA/PDPL signals
into one structured response. This is the "God view" for the Dealix founder.

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return governance_decision: "ALLOW_WITH_REVIEW"
  - Bilingual ar/en labels
  - Never expose PII; no scraping; no cold outreach triggers
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/cockpit",
    tags=["master-cockpit"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


# ---------------------------------------------------------------------------
# Demo data: aggregated platform state (realistic 2026 figures)
# ---------------------------------------------------------------------------

_PORTFOLIO_STATE = {
    "total_clients": 12,
    "healthy_count": 5,
    "moderate_count": 4,
    "at_risk_count": 2,
    "critical_count": 1,
    "avg_health_score": 67.3,
    "mrr_sar": 42_800,
    "arr_sar": 513_600,
    "clients_at_renewal_30d": 3,
}

_PIPELINE_STATE = {
    "total_deals": 18,
    "qualified_count": 6,
    "diagnostic_sent_count": 4,
    "sprint_proposed_count": 3,
    "sprint_active_count": 2,
    "pipeline_value_sar": 187_500,
    "weighted_pipeline_sar": 94_200,
    "avg_deal_size_sar": 10_417,
    "stalled_deals_7d": 2,
}

_REVENUE_STATE = {
    "mrr_sar": 42_800,
    "mrr_growth_mom_pct": 8.2,
    "arr_sar": 513_600,
    "nrr_pct": 108,
    "churn_rate_monthly_pct": 3.2,
    "avg_contract_value_sar": 3_567,
    "total_ltv_portfolio_sar": 427_800,
}

_COMPLIANCE_STATE = {
    "clients_zatca_compliant": 9,
    "clients_zatca_at_risk": 3,
    "clients_pdpl_aligned": 8,
    "clients_pdpl_at_risk": 4,
    "avg_zatca_score": 72,
    "avg_pdpl_score": 68,
    "next_zatca_wave_deadline": "2026-08-31",
    "next_zatca_wave_number": 8,
}

_ACTIVE_ALERTS: list[dict[str, Any]] = [
    {
        "alert_id": "ALT-001",
        "severity": "critical",
        "client_id": "CLT-003",
        "company_ar": "شركة الرياض للتقنية",
        "company_en": "Riyadh Tech Co",
        "issue_ar": "نقاط صحة المحفظة أقل من 35 — خطر إلغاء وشيك",
        "issue_en": "Portfolio health score below 35 — imminent churn risk",
        "action_ar": "جلسة طوارئ مع مدير الحساب خلال 48 ساعة",
        "action_en": "Emergency account manager session within 48 hours",
        "days_in_alert": 4,
    },
    {
        "alert_id": "ALT-002",
        "severity": "high",
        "client_id": "CLT-007",
        "company_ar": "مجموعة الخليج للخدمات المالية",
        "company_en": "Gulf Financial Services Group",
        "issue_ar": "موعد تجديد العقد خلال 21 يوماً — لم يُرسل Proof Pack بعد",
        "issue_en": "Contract renewal in 21 days — Proof Pack not yet sent",
        "action_ar": "تجهيز Proof Pack وعرض التجديد",
        "action_en": "Prepare Proof Pack and send renewal proposal",
        "days_in_alert": 2,
    },
    {
        "alert_id": "ALT-003",
        "severity": "high",
        "client_id": "CLT-011",
        "company_ar": "شركة سفا للخدمات اللوجستية",
        "company_en": "Safa Logistics Co",
        "issue_ar": "درجة ZATCA انخفضت 12 نقطة هذا الشهر",
        "issue_en": "ZATCA score dropped 12 points this month",
        "action_ar": "مراجعة حالة تكامل Fatoora API",
        "action_en": "Review Fatoora API integration status",
        "days_in_alert": 1,
    },
    {
        "alert_id": "ALT-004",
        "severity": "medium",
        "client_id": "CLT-005",
        "company_ar": "شركة تمكين الصحية",
        "company_en": "Tamkeen Health Co",
        "issue_ar": "3 فواتير معلقة لم تُعالج منذ 7 أيام",
        "issue_en": "3 invoices pending unprocessed for 7 days",
        "action_ar": "تتبع حالة معالجة الفواتير مع الفريق التقني",
        "action_en": "Track invoice processing status with technical team",
        "days_in_alert": 7,
    },
]

_PENDING_APPROVALS: list[dict[str, Any]] = [
    {
        "approval_id": "APV-001",
        "type": "proposal_send",
        "type_ar": "إرسال عرض سعر",
        "client_id": "PROSPECT-042",
        "company_ar": "شركة المنفعة التجارية",
        "company_en": "Al Manfaa Trading",
        "value_sar": 14_999,
        "tier": "managed_ops",
        "created_at": "2026-05-30T09:15:00Z",
        "urgency": "normal",
    },
    {
        "approval_id": "APV-002",
        "type": "retainer_upgrade",
        "type_ar": "ترقية عقد الاحتفاظ",
        "client_id": "CLT-009",
        "company_ar": "شركة الوافي المالية",
        "company_en": "Al Wafi Financial",
        "value_sar": 4_999,
        "tier": "enterprise",
        "created_at": "2026-05-30T11:42:00Z",
        "urgency": "high",
    },
]

_WEEKLY_KPIS: list[dict[str, Any]] = [
    {
        "kpi_id": "KPI-DIALS-01",
        "name_ar": "الإيراد الشهري المتكرر",
        "name_en": "Monthly Recurring Revenue",
        "value": 42_800,
        "unit": "SAR",
        "change_pct": +8.2,
        "trend": "up",
        "target": 50_000,
        "target_date": "2026-08-31",
    },
    {
        "kpi_id": "KPI-DIALS-02",
        "name_ar": "عدد العملاء النشطين",
        "name_en": "Active Client Count",
        "value": 12,
        "unit": "clients",
        "change_pct": +20.0,
        "trend": "up",
        "target": 20,
        "target_date": "2026-12-31",
    },
    {
        "kpi_id": "KPI-DIALS-03",
        "name_ar": "متوسط درجة صحة المحفظة",
        "name_en": "Avg Portfolio Health Score",
        "value": 67.3,
        "unit": "points",
        "change_pct": +2.1,
        "trend": "up",
        "target": 75.0,
        "target_date": "2026-12-31",
    },
    {
        "kpi_id": "KPI-DIALS-04",
        "name_ar": "معدل الاحتفاظ بالإيراد الصافي",
        "name_en": "Net Revenue Retention",
        "value": 108,
        "unit": "%",
        "change_pct": +3.0,
        "trend": "up",
        "target": 115,
        "target_date": "2026-12-31",
    },
    {
        "kpi_id": "KPI-DIALS-05",
        "name_ar": "خط أنابيب المبيعات المرجح",
        "name_en": "Weighted Sales Pipeline",
        "value": 94_200,
        "unit": "SAR",
        "change_pct": +15.3,
        "trend": "up",
        "target": 200_000,
        "target_date": "2026-09-30",
    },
    {
        "kpi_id": "KPI-DIALS-06",
        "name_ar": "الموافقات المعلقة",
        "name_en": "Pending Approvals",
        "value": len(_PENDING_APPROVALS),
        "unit": "actions",
        "change_pct": 0.0,
        "trend": "stable",
        "target": 0,
        "target_date": "rolling",
    },
]

_GROWTH_SIGNALS_SUMMARY: list[dict[str, Any]] = [
    {
        "signal_id": "SIG-SUM-01",
        "urgency": "HIGH",
        "signal_ar": "موعد ZATCA الموجة 8 — أغسطس 2026 — 3,200 شركة غير متوافقة",
        "signal_en": "ZATCA Wave 8 deadline Aug 2026 — 3,200 non-compliant SMBs",
        "opportunity_sar": 28_800_000,
        "sector": "cross-sector",
    },
    {
        "signal_id": "SIG-SUM-02",
        "urgency": "HIGH",
        "signal_ar": "تطبيق لوائح PDPL Q3 — تدقيق مكثف على قطاع الصحة والتمويل",
        "signal_en": "PDPL enforcement Q3 — heightened audits in healthcare and finance",
        "opportunity_sar": 15_400_000,
        "sector": "healthcare, financial_services",
    },
    {
        "signal_id": "SIG-SUM-03",
        "urgency": "MEDIUM",
        "signal_ar": "برنامج رؤية 2030 — 450 شركة تقنية جديدة مقررة 2026",
        "signal_en": "Vision 2030 — 450 new tech companies planned in 2026",
        "opportunity_sar": 9_000_000,
        "sector": "technology",
    },
]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/pulse")
async def get_pulse() -> dict[str, Any]:
    """One-call founder pulse check — all critical metrics in a single response.

    Returns portfolio health, revenue state, active alerts, pending approvals,
    pipeline overview, compliance state, and top growth signals.
    Designed for the founder's morning review — under 2 seconds.
    """
    critical_alerts = [a for a in _ACTIVE_ALERTS if a["severity"] == "critical"]
    high_alerts = [a for a in _ACTIVE_ALERTS if a["severity"] == "high"]

    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        "overall_status_ar": "يحتاج انتباهاً" if critical_alerts else "وضع مستقر",
        "overall_status_en": "Needs Attention" if critical_alerts else "Stable",
        "portfolio": _PORTFOLIO_STATE,
        "revenue": _REVENUE_STATE,
        "pipeline": _PIPELINE_STATE,
        "compliance": _COMPLIANCE_STATE,
        "alerts": {
            "total": len(_ACTIVE_ALERTS),
            "critical": len(critical_alerts),
            "high": len(high_alerts),
            "items": sorted(_ACTIVE_ALERTS, key=lambda a: {"critical": 0, "high": 1, "medium": 2}.get(a["severity"], 3)),
        },
        "pending_approvals": {
            "total": len(_PENDING_APPROVALS),
            "items": _PENDING_APPROVALS,
        },
        "top_growth_signals": _GROWTH_SIGNALS_SUMMARY[:3],
        "disclaimer_ar": "البيانات لأغراض التشغيل الداخلي فقط — لا تُشارَك مع أطراف خارجية دون موافقة",
        "disclaimer_en": "Data for internal operations only — do not share externally without approval",
    }


@router.get("/kpis")
async def get_kpis() -> dict[str, Any]:
    """Weekly KPI snapshot — 6 top-level metrics with trend and targets.

    Returns current value, % change WoW, trend direction, and target for
    each of Dealix's 6 key performance indicators.
    """
    on_track = [k for k in _WEEKLY_KPIS if k["trend"] == "up"]
    at_risk_kpis = [k for k in _WEEKLY_KPIS if k["trend"] == "down"]

    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        "kpi_count": len(_WEEKLY_KPIS),
        "on_track_count": len(on_track),
        "at_risk_count": len(at_risk_kpis),
        "kpis": _WEEKLY_KPIS,
        "summary_ar": f"{len(on_track)} من {len(_WEEKLY_KPIS)} مؤشرات أداء في المسار الصحيح",
        "summary_en": f"{len(on_track)} of {len(_WEEKLY_KPIS)} KPIs on track",
    }


@router.get("/alerts")
async def get_cockpit_alerts() -> dict[str, Any]:
    """All active alerts sorted by severity — critical first.

    Each alert includes: client, issue (bilingual), recommended action,
    and days the alert has been open.
    """
    sorted_alerts = sorted(
        _ACTIVE_ALERTS,
        key=lambda a: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(a["severity"], 9),
    )
    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        "alert_count": len(sorted_alerts),
        "critical_count": sum(1 for a in sorted_alerts if a["severity"] == "critical"),
        "high_count": sum(1 for a in sorted_alerts if a["severity"] == "high"),
        "alerts": sorted_alerts,
    }


@router.get("/approvals")
async def get_pending_approvals() -> dict[str, Any]:
    """All actions awaiting founder approval — APPROVAL_FIRST gate.

    Returns pending proposals, upgrades, and outreach items that require
    explicit founder sign-off before execution.
    """
    high_urgency = [a for a in _PENDING_APPROVALS if a.get("urgency") == "high"]

    return {
        "governance_decision": "APPROVAL_FIRST",
        "generated_at": _now_iso(),
        "total_pending": len(_PENDING_APPROVALS),
        "high_urgency_count": len(high_urgency),
        "approvals": _PENDING_APPROVALS,
        "note_ar": "كل هذه الإجراءات تتطلب موافقة المؤسس قبل التنفيذ — APPROVAL_FIRST",
        "note_en": "All these actions require founder approval before execution — APPROVAL_FIRST",
    }


@router.get("/revenue-summary")
async def get_revenue_summary() -> dict[str, Any]:
    """Revenue metrics snapshot — MRR, ARR, NRR, churn, and LTV.

    Returns current month revenue state with comparison to targets.
    All figures are operational data, not audited financials.
    """
    mrr = _REVENUE_STATE["mrr_sar"]
    target_mrr = 50_000
    gap_to_target = target_mrr - mrr

    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        "mrr_sar": mrr,
        "arr_sar": _REVENUE_STATE["arr_sar"],
        "mrr_growth_mom_pct": _REVENUE_STATE["mrr_growth_mom_pct"],
        "nrr_pct": _REVENUE_STATE["nrr_pct"],
        "churn_rate_monthly_pct": _REVENUE_STATE["churn_rate_monthly_pct"],
        "avg_contract_value_sar": _REVENUE_STATE["avg_contract_value_sar"],
        "total_ltv_portfolio_sar": _REVENUE_STATE["total_ltv_portfolio_sar"],
        "target_mrr_sar": target_mrr,
        "gap_to_target_sar": max(gap_to_target, 0),
        "pct_to_target": round(mrr / target_mrr * 100, 1),
        "renewal_clients_30d": _PORTFOLIO_STATE["clients_at_renewal_30d"],
        "disclaimer_ar": "أرقام تشغيلية — ليست بيانات مالية مدققة",
        "disclaimer_en": "Operational figures — not audited financial statements",
    }


@router.get("/compliance-overview")
async def get_compliance_overview() -> dict[str, Any]:
    """ZATCA + PDPL compliance state across the full client portfolio.

    Shows compliance distribution, next wave deadline, and clients needing
    immediate attention.
    """
    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        "zatca": {
            "compliant_clients": _COMPLIANCE_STATE["clients_zatca_compliant"],
            "at_risk_clients": _COMPLIANCE_STATE["clients_zatca_at_risk"],
            "avg_score": _COMPLIANCE_STATE["avg_zatca_score"],
            "next_wave": _COMPLIANCE_STATE["next_zatca_wave_number"],
            "next_deadline": _COMPLIANCE_STATE["next_zatca_wave_deadline"],
            "compliance_rate_pct": round(
                _COMPLIANCE_STATE["clients_zatca_compliant"]
                / _PORTFOLIO_STATE["total_clients"]
                * 100,
                1,
            ),
        },
        "pdpl": {
            "aligned_clients": _COMPLIANCE_STATE["clients_pdpl_aligned"],
            "at_risk_clients": _COMPLIANCE_STATE["clients_pdpl_at_risk"],
            "avg_score": _COMPLIANCE_STATE["avg_pdpl_score"],
            "alignment_rate_pct": round(
                _COMPLIANCE_STATE["clients_pdpl_aligned"]
                / _PORTFOLIO_STATE["total_clients"]
                * 100,
                1,
            ),
        },
        "disclaimer_ar": "درجات الامتثال تقديرية بناءً على بيانات التقييم الذاتي",
        "disclaimer_en": "Compliance scores are estimates based on self-assessment data",
    }
