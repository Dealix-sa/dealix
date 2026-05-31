"""Client Portal Operations — self-service account and deliverable views.

Endpoints (prefix /api/v1/client-portal):
  GET  /accounts                         — list all client portal accounts
  GET  /accounts/{client_id}             — single client account detail
  GET  /accounts/{client_id}/deliverables — deliverables for a client
  GET  /summary                          — portfolio-level summary
  POST /accounts/{client_id}/request-review — request a business review
  GET  /upgrade-paths                    — tier upgrade recommendations

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return governance_decision field on every response
  - PDPL-compliant: no guaranteed outcome claims
  - Bilingual ar/en content where applicable
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/client-portal",
    tags=["Client Portal"],
    dependencies=[Depends(require_admin_key)],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_ACTION = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Tier pricing map (canonical SAR MRR per tier)
# ---------------------------------------------------------------------------

_TIER_MRR: dict[str, float] = {
    "sprint": 499.0,
    "data_pack": 1500.0,
    "managed_ops": 2999.0,
    "custom_ai": 8999.0,
}

# Ordered tier progression
_TIER_ORDER: list[str] = ["sprint", "data_pack", "managed_ops", "custom_ai"]

# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------

CLIENT_PORTALS: dict[str, dict[str, Any]] = {
    "CP-001": {
        "client_id": "CP-001",
        "company_name": "مجموعة الصحة الوطنية",
        "company_name_en": "National Health Group",
        "contact_name": "أحمد الزهراني",
        "contact_email": "a.zahrani@nhg.sa",
        "tier": "managed_ops",
        "mrr_sar": 4500.0,
        "contract_start": "2026-01-01",
        "contract_end": "2026-12-31",
        "health_score": 87,
        "sprints_completed": 8,
        "sprints_remaining": 4,
        "active_deliverables": ["AI Dashboard", "Revenue Intelligence", "ZATCA Integration"],
        "next_review_date": "2026-06-15",
        "satisfaction_score": 4.5,
        "nps": 9,
        "last_login": "2026-05-30T10:30:00Z",
    },
    "CP-002": {
        "client_id": "CP-002",
        "company_name": "شركة التجزئة الذكية",
        "company_name_en": "Smart Retail Co",
        "contact_name": "منى الحربي",
        "contact_email": "m.harbi@smartretail.sa",
        "tier": "data_pack",
        "mrr_sar": 1500.0,
        "contract_start": "2026-02-01",
        "contract_end": "2026-07-31",
        "health_score": 73,
        "sprints_completed": 3,
        "sprints_remaining": 0,
        "active_deliverables": ["Data Passport", "Customer Segmentation"],
        "next_review_date": "2026-06-01",
        "satisfaction_score": 4.0,
        "nps": 7,
        "last_login": "2026-05-28T14:00:00Z",
    },
    "CP-003": {
        "client_id": "CP-003",
        "company_name": "مجموعة العقارات الحديثة",
        "company_name_en": "Modern Properties Group",
        "contact_name": "فيصل الدوسري",
        "contact_email": "f.dosari@mpg.sa",
        "tier": "custom_ai",
        "mrr_sar": 8999.0,
        "contract_start": "2025-10-01",
        "contract_end": "2026-09-30",
        "health_score": 92,
        "sprints_completed": 15,
        "sprints_remaining": 6,
        "active_deliverables": [
            "Custom NLP Engine",
            "Market Intelligence",
            "Investment Scoring",
            "Automated Reports",
        ],
        "next_review_date": "2026-06-30",
        "satisfaction_score": 4.8,
        "nps": 10,
        "last_login": "2026-05-31T08:00:00Z",
    },
    "CP-004": {
        "client_id": "CP-004",
        "company_name": "شركة الاستشارات الرقمية",
        "company_name_en": "Digital Consulting Co",
        "contact_name": "ليلى القحطاني",
        "contact_email": "l.qahtani@dcc.sa",
        "tier": "sprint",
        "mrr_sar": 499.0,
        "contract_start": "2026-04-01",
        "contract_end": "2026-04-30",
        "health_score": 58,
        "sprints_completed": 1,
        "sprints_remaining": 0,
        "active_deliverables": ["Free Diagnostic Report"],
        "next_review_date": "2026-06-01",
        "satisfaction_score": 3.5,
        "nps": 6,
        "last_login": "2026-04-30T16:00:00Z",
    },
    "CP-005": {
        "client_id": "CP-005",
        "company_name": "مركز التدريب التقني",
        "company_name_en": "Technical Training Center",
        "contact_name": "عبدالله المطيري",
        "contact_email": "a.mutairi@ttc.sa",
        "tier": "managed_ops",
        "mrr_sar": 2999.0,
        "contract_start": "2026-03-01",
        "contract_end": "2027-02-28",
        "health_score": 81,
        "sprints_completed": 5,
        "sprints_remaining": 7,
        "active_deliverables": ["Operations Dashboard", "Compliance Tracker"],
        "next_review_date": "2026-07-01",
        "satisfaction_score": 4.2,
        "nps": 8,
        "last_login": "2026-05-29T11:00:00Z",
    },
}

DELIVERABLES: dict[str, dict[str, Any]] = {
    "DLV-001": {
        "id": "DLV-001",
        "client_id": "CP-001",
        "name": "AI Dashboard",
        "status": "delivered",
        "due_date": "2026-02-28",
        "delivered_date": "2026-02-25",
        "quality_score": 94,
        "notes": "Delivered 3 days early",
    },
    "DLV-002": {
        "id": "DLV-002",
        "client_id": "CP-001",
        "name": "Revenue Intelligence",
        "status": "in_progress",
        "due_date": "2026-06-30",
        "delivered_date": None,
        "quality_score": None,
        "notes": "On track — 65% complete",
    },
    "DLV-003": {
        "id": "DLV-003",
        "client_id": "CP-001",
        "name": "ZATCA Integration",
        "status": "planned",
        "due_date": "2026-08-31",
        "delivered_date": None,
        "quality_score": None,
        "notes": "Scheduled for Q3 2026",
    },
    "DLV-004": {
        "id": "DLV-004",
        "client_id": "CP-003",
        "name": "Custom NLP Engine",
        "status": "delivered",
        "due_date": "2026-02-15",
        "delivered_date": "2026-02-14",
        "quality_score": 98,
        "notes": "Exceptional quality",
    },
    "DLV-005": {
        "id": "DLV-005",
        "client_id": "CP-003",
        "name": "Market Intelligence",
        "status": "delivered",
        "due_date": "2026-04-01",
        "delivered_date": "2026-04-01",
        "quality_score": 95,
        "notes": "On time",
    },
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(UTC).isoformat()


def _client_or_404(client_id: str) -> dict[str, Any]:
    """Return the client record or raise HTTP 404.

    Lookup is case-sensitive; client IDs are always uppercase (CP-NNN).
    """
    record = CLIENT_PORTALS.get(client_id)
    if record is None:
        raise HTTPException(
            status_code=404,
            detail={
                "ar": f"الحساب '{client_id}' غير موجود",
                "en": f"Client account '{client_id}' not found",
            },
        )
    return record


def _filter_accounts(
    accounts: list[dict[str, Any]],
    tier: str | None,
    min_health: int | None,
) -> list[dict[str, Any]]:
    """Apply optional tier and min_health filters to a list of account records."""
    result = accounts
    if tier is not None:
        result = [a for a in result if a["tier"] == tier]
    if min_health is not None:
        result = [a for a in result if a["health_score"] >= min_health]
    return result


def _compute_by_tier(accounts: list[dict[str, Any]]) -> dict[str, int]:
    """Return a count of accounts per tier."""
    counts: dict[str, int] = {}
    for account in accounts:
        t = account["tier"]
        counts[t] = counts.get(t, 0) + 1
    return counts


def _compute_portfolio_summary(accounts: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute aggregate portfolio statistics from a list of account records."""
    total = len(accounts)
    if total == 0:
        return {
            "total_clients": 0,
            "by_tier": {},
            "avg_health_score": 0.0,
            "total_mrr_sar": 0.0,
            "avg_satisfaction": 0.0,
            "avg_nps": 0.0,
            "active_deliverables_count": 0,
            "high_health_clients": 0,
            "at_risk_clients": 0,
        }

    by_tier = _compute_by_tier(accounts)
    avg_health = round(sum(a["health_score"] for a in accounts) / total, 2)
    total_mrr = sum(a["mrr_sar"] for a in accounts)
    avg_satisfaction = round(sum(a["satisfaction_score"] for a in accounts) / total, 2)
    avg_nps = round(sum(a["nps"] for a in accounts) / total, 2)
    active_deliverables_count = sum(len(a["active_deliverables"]) for a in accounts)
    high_health_clients = sum(1 for a in accounts if a["health_score"] >= 80)
    at_risk_clients = sum(1 for a in accounts if a["health_score"] < 65)

    return {
        "total_clients": total,
        "by_tier": by_tier,
        "avg_health_score": avg_health,
        "total_mrr_sar": total_mrr,
        "avg_satisfaction": avg_satisfaction,
        "avg_nps": avg_nps,
        "active_deliverables_count": active_deliverables_count,
        "high_health_clients": high_health_clients,
        "at_risk_clients": at_risk_clients,
    }


def _next_tier(current_tier: str) -> str | None:
    """Return the next tier in the upgrade path, or None if already at the top."""
    try:
        idx = _TIER_ORDER.index(current_tier)
    except ValueError:
        return None
    next_idx = idx + 1
    if next_idx >= len(_TIER_ORDER):
        return None
    return _TIER_ORDER[next_idx]


_UPGRADE_REASON: dict[tuple[str, str], str] = {
    ("sprint", "data_pack"): "Ready for structured data ops",
    ("data_pack", "managed_ops"): "Strong data foundation — upgrade to managed AI",
    ("managed_ops", "custom_ai"): "Complex workflows warrant custom AI build",
}


def _build_upgrade_paths(accounts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build upgrade path recommendations for eligible accounts.

    Only includes accounts with health_score >= 70 that are not already on
    the custom_ai tier.  Returns empty list when no accounts qualify.
    """
    paths: list[dict[str, Any]] = []
    for account in accounts:
        current_tier = account["tier"]
        if current_tier == "custom_ai":
            continue
        if account["health_score"] < 70:
            continue
        next_t = _next_tier(current_tier)
        if next_t is None:
            continue
        current_mrr = _TIER_MRR.get(current_tier, account["mrr_sar"])
        recommended_mrr = _TIER_MRR.get(next_t, 0.0)
        reason = _UPGRADE_REASON.get((current_tier, next_t), "Consider upgrading to next tier")
        paths.append({
            "client_id": account["client_id"],
            "company_name": account["company_name_en"],
            "current_tier": current_tier,
            "recommended_tier": next_t,
            "current_mrr_sar": current_mrr,
            "recommended_mrr_sar": recommended_mrr,
            "revenue_uplift_sar": round(recommended_mrr - current_mrr, 2),
            "reason": reason,
        })
    return paths


# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------


class RequestReviewBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requested_date: str = Field(
        description="Preferred date for the review session (ISO 8601, YYYY-MM-DD).",
    )
    topics: list[str] = Field(
        min_length=1,
        description="List of topics the client wants to discuss.",
    )


# ---------------------------------------------------------------------------
# Endpoints — fixed paths first, then parameterised
# ---------------------------------------------------------------------------


@router.get("/accounts")
async def list_accounts(
    tier: str | None = Query(default=None, description="Filter by tier slug"),
    min_health: int | None = Query(default=None, ge=0, le=100, description="Minimum health score"),
) -> dict[str, Any]:
    """List all client portal accounts with optional filtering."""
    all_accounts = list(CLIENT_PORTALS.values())
    filtered = _filter_accounts(all_accounts, tier=tier, min_health=min_health)

    _log.info(
        "client_portal_accounts_listed",
        total=len(all_accounts),
        returned=len(filtered),
        filter_tier=tier,
        filter_min_health=min_health,
    )

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "total": len(filtered),
        "accounts": filtered,
    }


@router.get("/summary")
async def get_portfolio_summary() -> dict[str, Any]:
    """Aggregate portfolio summary across all client portal accounts."""
    all_accounts = list(CLIENT_PORTALS.values())
    summary = _compute_portfolio_summary(all_accounts)

    _log.info("client_portal_summary_fetched", total_clients=summary["total_clients"])

    return {
        "governance_decision": _GOV_READ,
        **summary,
    }


@router.get("/upgrade-paths")
async def get_upgrade_paths() -> dict[str, Any]:
    """Upgrade path recommendations for clients eligible to move to the next tier.

    Only clients with health_score >= 70 and not on the custom_ai tier are
    included.  Revenue uplift figures are indicative and not guaranteed.
    """
    all_accounts = list(CLIENT_PORTALS.values())
    upgrade_paths = _build_upgrade_paths(all_accounts)

    _log.info("upgrade_paths_generated", count=len(upgrade_paths))

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "disclaimer": (
            "Revenue uplift figures are indicative only and do not constitute "
            "a guarantee of results. Actual outcomes depend on client engagement "
            "and implementation quality."
        ),
        "upgrade_paths": upgrade_paths,
    }


@router.get("/accounts/{client_id}")
async def get_account(client_id: str) -> dict[str, Any]:
    """Return the full account record for a single client portal account."""
    record = _client_or_404(client_id)

    _log.info("client_portal_account_fetched", client_id=client_id)

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        **record,
    }


@router.get("/accounts/{client_id}/deliverables")
async def get_client_deliverables(client_id: str) -> dict[str, Any]:
    """Return all deliverables associated with the given client account."""
    _client_or_404(client_id)  # raises 404 if client not found

    client_deliverables = [
        dlv for dlv in DELIVERABLES.values() if dlv["client_id"] == client_id
    ]

    delivered_count = sum(1 for d in client_deliverables if d["status"] == "delivered")
    in_progress_count = sum(1 for d in client_deliverables if d["status"] == "in_progress")
    planned_count = sum(1 for d in client_deliverables if d["status"] == "planned")

    _log.info(
        "client_portal_deliverables_fetched",
        client_id=client_id,
        total=len(client_deliverables),
    )

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "client_id": client_id,
        "total": len(client_deliverables),
        "delivered_count": delivered_count,
        "in_progress_count": in_progress_count,
        "planned_count": planned_count,
        "deliverables": client_deliverables,
    }


@router.post("/accounts/{client_id}/request-review")
async def request_review(client_id: str, body: RequestReviewBody) -> dict[str, Any]:
    """Submit a business review request on behalf of a client.

    The request is queued for human approval before scheduling.
    No outcome is guaranteed by accepting this request.
    """
    record = _client_or_404(client_id)

    _log.info(
        "client_portal_review_requested",
        client_id=client_id,
        requested_date=body.requested_date,
        topics_count=len(body.topics),
    )

    return {
        "governance_decision": _GOV_ACTION,
        "generated_at": _now_iso(),
        "status": "review_request_received_pending_approval",
        "client_id": client_id,
        "company_name": record["company_name_en"],
        "requested_date": body.requested_date,
        "topics": body.topics,
        "message_ar": (
            "تم استلام طلب المراجعة — سيتم تأكيد الموعد بعد موافقة الفريق"
        ),
        "message_en": (
            "Review request received — appointment will be confirmed after team approval"
        ),
    }
