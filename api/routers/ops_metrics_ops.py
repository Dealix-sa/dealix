"""Operations Metrics — admin nerve center for Dealix operational health.

Aggregates KPIs from all operational modules into a single call.

Endpoints:
  GET  /api/v1/ops-metrics/snapshot        — full KPI snapshot with health score
  GET  /api/v1/ops-metrics/pulse           — quick 5-second pulse check
  GET  /api/v1/ops-metrics/weekly-summary  — formatted Monday morning review
  GET  /api/v1/ops-metrics/benchmarks      — KPIs vs. Dealix targets
  POST /api/v1/ops-metrics/flag-issue      — founder flags an operational issue

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return governance_decision field
  - Read-only: ALLOW_WITH_REVIEW
  - Mutating: APPROVAL_FIRST
  - Bilingual ar/en labels
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
    prefix="/api/v1/ops-metrics",
    tags=["ops-metrics"],
    dependencies=[Depends(require_admin_key)],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_MUTATE = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Demo KPI snapshot — current state of the business
# ---------------------------------------------------------------------------

_OPS_SNAPSHOT: dict[str, Any] = {
    # Revenue
    "mrr_sar": 68_000,
    "arr_sar": 816_000,
    "mrr_growth_pct": 8.5,
    "nrr_pct": 108,
    # Clients
    "active_clients": 12,
    "at_risk_clients": 4,
    "avg_health_score": 72,
    "avg_proof_score": 78,
    # Pipeline
    "pipeline_deals": 7,
    "pipeline_value_sar": 185_000,
    "deals_closing_30d": 2,
    # Operations
    "active_onboardings": 3,
    "pending_approvals": 2,
    "open_invoices": 3,
    "overdue_invoices": 2,
    # Proof Packs
    "proof_packs_delivered_30d": 5,
    "proof_packs_pending_delivery": 2,
    # Team
    "active_team_members": 4,
    "open_roles": 1,
    # Compliance
    "zatca_compliance_rate_pct": 92,
    "pdpl_readiness_score": 78,
}

# Valid issue types for flag-issue endpoint
VALID_ISSUE_TYPES: frozenset[str] = frozenset({
    "revenue",
    "client",
    "delivery",
    "compliance",
    "team",
    "other",
})

# Valid priority levels
VALID_PRIORITIES: frozenset[str] = frozenset({"high", "medium", "low"})

# In-memory store for flagged issues (keyed by issue_id)
_FLAGGED_ISSUES: dict[str, dict[str, Any]] = {}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class FlagIssueBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    issue_type: str = Field(
        ...,
        description="Category of the operational issue",
    )
    description: str = Field(
        ...,
        min_length=10,
        description="Description of the issue (minimum 10 characters)",
    )
    priority: str = Field(
        ...,
        description="Priority level: high, medium, or low",
    )


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(UTC).isoformat()


def _compute_health(snapshot: dict[str, Any]) -> tuple[float, str]:
    """Compute overall ops health score and band from a KPI snapshot.

    Weights:
      revenue_health  30%
      client_health   25%
      delivery_health 25%
      compliance_health 20%

    Returns (score: float 0-100, band: "green" | "amber" | "red").
    """
    mrr_growth = float(snapshot.get("mrr_growth_pct", 0))
    if mrr_growth >= 5:
        revenue_health: float = 100.0
    elif mrr_growth >= 0:
        revenue_health = 70.0
    else:
        revenue_health = 40.0

    client_health: float = float(snapshot.get("avg_health_score", 0))

    delivered = int(snapshot.get("proof_packs_delivered_30d", 0))
    pending_approvals = int(snapshot.get("pending_approvals", 0))
    if delivered > 3 and pending_approvals <= 3:
        delivery_health: float = 90.0
    else:
        delivery_health = 65.0

    zatca = float(snapshot.get("zatca_compliance_rate_pct", 0))
    pdpl = float(snapshot.get("pdpl_readiness_score", 0))
    compliance_health: float = (zatca + pdpl) / 2.0

    overall = (
        revenue_health * 0.30
        + client_health * 0.25
        + delivery_health * 0.25
        + compliance_health * 0.20
    )
    overall = max(0.0, min(100.0, overall))

    if overall >= 75:
        band = "green"
    elif overall >= 50:
        band = "amber"
    else:
        band = "red"

    return round(overall, 2), band


def _build_alerts(snapshot: dict[str, Any]) -> list[dict[str, str]]:
    """Generate up to 3 top operational alerts from the snapshot."""
    alerts: list[dict[str, str]] = []

    overdue = int(snapshot.get("overdue_invoices", 0))
    if overdue > 0:
        alerts.append({
            "type": "overdue_invoices",
            "message_ar": f"يوجد {overdue} فاتورة متأخرة تحتاج متابعة فورية",
            "message_en": f"{overdue} overdue invoice(s) require immediate follow-up",
            "severity": "high",
        })

    at_risk = int(snapshot.get("at_risk_clients", 0))
    if at_risk > 0:
        alerts.append({
            "type": "at_risk_clients",
            "message_ar": f"{at_risk} عملاء في منطقة الخطر — يجب مراجعتهم هذا الأسبوع",
            "message_en": f"{at_risk} client(s) at risk — review this week",
            "severity": "high",
        })

    pending = int(snapshot.get("pending_approvals", 0))
    if pending > 0:
        alerts.append({
            "type": "pending_approvals",
            "message_ar": f"يوجد {pending} طلب موافقة معلّق يستلزم قرار المؤسس",
            "message_en": f"{pending} pending approval(s) require founder decision",
            "severity": "medium",
        })

    return alerts[:3]


def _issue_type_label(issue_type: str) -> tuple[str, str]:
    """Return (label_ar, label_en) for a given issue_type."""
    labels: dict[str, tuple[str, str]] = {
        "revenue": ("إيرادات", "Revenue"),
        "client": ("عميل", "Client"),
        "delivery": ("تسليم", "Delivery"),
        "compliance": ("امتثال", "Compliance"),
        "team": ("فريق", "Team"),
        "other": ("أخرى", "Other"),
    }
    return labels.get(issue_type, ("أخرى", "Other"))


def _priority_label(priority: str) -> tuple[str, str]:
    """Return (label_ar, label_en) for a given priority."""
    labels: dict[str, tuple[str, str]] = {
        "high": ("عالية", "High"),
        "medium": ("متوسطة", "Medium"),
        "low": ("منخفضة", "Low"),
    }
    return labels.get(priority, ("متوسطة", "Medium"))


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/snapshot")
async def get_snapshot() -> dict[str, Any]:
    """Full ops KPI snapshot with computed overall health score."""
    overall_health, health_band = _compute_health(_OPS_SNAPSHOT)
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "overall_health_score": overall_health,
        "health_band": health_band,
        "kpis": dict(_OPS_SNAPSHOT),
    }


@router.get("/pulse")
async def get_pulse() -> dict[str, Any]:
    """Quick 5-second pulse check: health score, band, and top 3 alerts."""
    overall_health, health_band = _compute_health(_OPS_SNAPSHOT)
    alerts = _build_alerts(_OPS_SNAPSHOT)
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "overall_health_score": overall_health,
        "health_band": health_band,
        "top_alerts": alerts,
    }


@router.get("/weekly-summary")
async def get_weekly_summary() -> dict[str, Any]:
    """Formatted weekly summary suitable for a Monday morning review."""
    now = datetime.now(UTC)
    week_label = f"Week of {now.strftime('%B %d, %Y')}"

    key_wins: list[dict[str, str]] = [
        {
            "win_ar": f"تسليم {_OPS_SNAPSHOT['proof_packs_delivered_30d']} حزمة إثبات خلال 30 يوماً الماضية",
            "win_en": f"{_OPS_SNAPSHOT['proof_packs_delivered_30d']} Proof Packs delivered in the last 30 days",
        },
        {
            "win_ar": f"الإيرادات الشهرية المتكررة بلغت {_OPS_SNAPSHOT['mrr_sar']:,} ريال بنمو {_OPS_SNAPSHOT['mrr_growth_pct']}%",
            "win_en": f"MRR reached {_OPS_SNAPSHOT['mrr_sar']:,} SAR with {_OPS_SNAPSHOT['mrr_growth_pct']}% growth",
        },
        {
            "win_ar": f"الاحتفاظ الصافي بالإيرادات بلغ {_OPS_SNAPSHOT['nrr_pct']}% مما يشير إلى توسع حقيقي من العملاء الحاليين",
            "win_en": f"Net Revenue Retention at {_OPS_SNAPSHOT['nrr_pct']}% — indicating genuine expansion from existing clients",
        },
    ]

    focus_areas: list[dict[str, str]] = [
        {
            "area_ar": f"معالجة {_OPS_SNAPSHOT['at_risk_clients']} عملاء في منطقة الخطر خلال هذا الأسبوع",
            "area_en": f"Address {_OPS_SNAPSHOT['at_risk_clients']} at-risk clients this week",
        },
        {
            "area_ar": f"إغلاق {_OPS_SNAPSHOT['overdue_invoices']} فاتورة متأخرة ومتابعة {_OPS_SNAPSHOT['open_invoices']} فاتورة مفتوحة",
            "area_en": f"Close {_OPS_SNAPSHOT['overdue_invoices']} overdue invoice(s) and follow up on {_OPS_SNAPSHOT['open_invoices']} open invoice(s)",
        },
        {
            "area_ar": f"الإغلاق المتوقع لـ {_OPS_SNAPSHOT['deals_closing_30d']} صفقات خلال 30 يوماً — استعد للتفاوض",
            "area_en": f"{_OPS_SNAPSHOT['deals_closing_30d']} deal(s) closing in 30 days — prepare for negotiations",
        },
    ]

    kpi_highlights: list[dict[str, Any]] = [
        {"metric": "mrr_sar", "label_ar": "الإيرادات الشهرية المتكررة", "label_en": "MRR", "value": _OPS_SNAPSHOT["mrr_sar"], "unit": "SAR"},
        {"metric": "nrr_pct", "label_ar": "الاحتفاظ الصافي بالإيرادات", "label_en": "Net Revenue Retention", "value": _OPS_SNAPSHOT["nrr_pct"], "unit": "%"},
        {"metric": "active_clients", "label_ar": "العملاء النشطون", "label_en": "Active Clients", "value": _OPS_SNAPSHOT["active_clients"], "unit": "clients"},
        {"metric": "avg_health_score", "label_ar": "متوسط درجة الصحة", "label_en": "Avg Health Score", "value": _OPS_SNAPSHOT["avg_health_score"], "unit": "score"},
        {"metric": "pipeline_value_sar", "label_ar": "قيمة خط الأنابيب", "label_en": "Pipeline Value", "value": _OPS_SNAPSHOT["pipeline_value_sar"], "unit": "SAR"},
    ]

    action_items: list[dict[str, str]] = [
        {
            "governance_decision": _GOV_MUTATE,
            "action_ar": f"راجع ووافق على {_OPS_SNAPSHOT['pending_approvals']} طلب موافقة معلّق",
            "action_en": f"Review and approve {_OPS_SNAPSHOT['pending_approvals']} pending approval(s)",
        },
        {
            "governance_decision": _GOV_MUTATE,
            "action_ar": f"تواصل مع {_OPS_SNAPSHOT['at_risk_clients']} عملاء في منطقة الخطر وضع خطة تدخل",
            "action_en": f"Reach out to {_OPS_SNAPSHOT['at_risk_clients']} at-risk clients and create intervention plan",
        },
        {
            "governance_decision": _GOV_MUTATE,
            "action_ar": f"تابع {_OPS_SNAPSHOT['overdue_invoices']} فاتورة متأخرة وحدد موعد للسداد",
            "action_en": f"Follow up on {_OPS_SNAPSHOT['overdue_invoices']} overdue invoice(s) and set payment deadline",
        },
    ]

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "week_label": week_label,
        "key_wins": key_wins,
        "focus_areas": focus_areas,
        "kpi_highlights": kpi_highlights,
        "action_items": action_items,
    }


@router.get("/benchmarks")
async def get_benchmarks() -> dict[str, Any]:
    """Compare current KPIs against Dealix targets."""
    snap = _OPS_SNAPSHOT

    def _benchmark(
        metric_name_ar: str,
        metric_name_en: str,
        current_value: float,
        target_value: float,
        unit: str,
        *,
        lower_is_better: bool = False,
    ) -> dict[str, Any]:
        gap = round(current_value - target_value, 2)
        if lower_is_better:
            if current_value <= target_value:
                status = "on_track"
            elif current_value <= target_value * 1.5:
                status = "needs_attention"
            else:
                status = "critical"
        else:
            ratio = current_value / target_value if target_value else 0
            if ratio >= 0.95:
                status = "on_track"
            elif ratio >= 0.75:
                status = "needs_attention"
            else:
                status = "critical"
        return {
            "metric_name_ar": metric_name_ar,
            "metric_name_en": metric_name_en,
            "current_value": current_value,
            "target_value": target_value,
            "unit": unit,
            "status": status,
            "gap": gap,
        }

    churn_rate_pct = round(
        (snap["at_risk_clients"] / snap["active_clients"]) * 100, 2
    ) if snap["active_clients"] else 0.0

    benchmarks = [
        _benchmark("الإيرادات الشهرية المتكررة", "MRR", snap["mrr_sar"], 100_000, "SAR"),
        _benchmark("الاحتفاظ الصافي بالإيرادات", "NRR", snap["nrr_pct"], 110, "%"),
        _benchmark("متوسط درجة الصحة", "Avg Health Score", snap["avg_health_score"], 75, "score"),
        _benchmark("قيمة خط الأنابيب", "Pipeline Value", snap["pipeline_value_sar"], 250_000, "SAR"),
        _benchmark("نسبة الامتثال لزاتكا", "ZATCA Compliance Rate", snap["zatca_compliance_rate_pct"], 100, "%"),
        _benchmark("متوسط درجة الإثبات", "Avg Proof Score", snap["avg_proof_score"], 85, "score"),
        _benchmark("العملاء النشطون", "Active Clients", snap["active_clients"], 20, "clients"),
        _benchmark("معدل الإلغاء", "Churn Rate", churn_rate_pct, 5, "%", lower_is_better=True),
    ]

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "benchmarks": benchmarks,
    }


@router.post("/flag-issue")
async def flag_issue(body: FlagIssueBody) -> dict[str, Any]:
    """Founder flags an operational issue for tracking. APPROVAL_FIRST gated."""
    if body.issue_type not in VALID_ISSUE_TYPES:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=422,
            detail=f"issue_type must be one of: {sorted(VALID_ISSUE_TYPES)}",
        )
    if body.priority not in VALID_PRIORITIES:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=422,
            detail=f"priority must be one of: {sorted(VALID_PRIORITIES)}",
        )

    issue_id = f"ISSUE-{uuid.uuid4().hex[:8].upper()}"
    timestamp = _now_iso()

    type_label_ar, type_label_en = _issue_type_label(body.issue_type)
    priority_label_ar, priority_label_en = _priority_label(body.priority)

    record: dict[str, Any] = {
        "issue_id": issue_id,
        "created_at": timestamp,
        "issue_type": body.issue_type,
        "issue_type_label_ar": type_label_ar,
        "issue_type_label_en": type_label_en,
        "description": body.description,
        "priority": body.priority,
        "priority_label_ar": priority_label_ar,
        "priority_label_en": priority_label_en,
        "status": "open",
    }
    _FLAGGED_ISSUES[issue_id] = record

    _log.info(
        "ops_issue_flagged",
        issue_id=issue_id,
        issue_type=body.issue_type,
        priority=body.priority,
    )

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": timestamp,
        "status": "issue_flagged_pending_review",
        "issue_id": issue_id,
        "issue_type": body.issue_type,
        "issue_type_label_ar": type_label_ar,
        "issue_type_label_en": type_label_en,
        "description": body.description,
        "priority": body.priority,
        "priority_label_ar": priority_label_ar,
        "priority_label_en": priority_label_en,
        "acknowledgement_ar": "تم تسجيل المشكلة بنجاح — تحتاج إلى مراجعة وموافقة المؤسس قبل اتخاذ أي إجراء",
        "acknowledgement_en": "Issue flagged successfully — requires founder review and approval before action is taken",
    }
