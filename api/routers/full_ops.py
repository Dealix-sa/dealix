"""V12 — Full-Ops umbrella router.

Single ``GET /api/v1/full-ops/daily-command-center`` returning all 5
active OS queues + top-3 decisions + blocked actions + hard gates.

Read-only. No external calls. Returns 200 always; degraded sections
are reported in ``degraded_sections`` rather than raising 5xx.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from api.security.auth_deps import get_current_user
from auto_client_acquisition.full_ops import (
    WorkItem,
    get_default_queue,
    prioritize,
)
from dealix.company_os.workload_router import (
    CompanyWorkloadRequest,
    capability_map,
    route_company_workload,
)

router = APIRouter(prefix="/api/v1/full-ops", tags=["full-ops"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_scraping": True,
    "no_cold_outreach": True,
    "no_linkedin_automation": True,
    "no_fake_proof": True,
    "approval_required_for_external_actions": True,
}


class RouteWorkloadBody(BaseModel):
    """PII-light request for the company-wide operating router."""

    model_config = ConfigDict(extra="forbid")

    customer_id: str | None = Field(default=None, max_length=120)
    title: str = Field(min_length=1, max_length=500)
    description: str = Field(default="", max_length=5_000)
    objective: str = Field(default="", max_length=1_000)
    urgency: Literal["low", "normal", "high", "critical"] = "normal"
    sensitivity: Literal["public", "internal", "confidential", "restricted"] = "internal"
    external_action_requested: bool = False
    requested_channel: str | None = Field(default=None, max_length=50)
    recipient_opted_in: bool | None = None
    evidence_ids: list[str] = Field(default_factory=list, max_length=100)

    def to_request(self, *, tenant_id: str) -> CompanyWorkloadRequest:
        return CompanyWorkloadRequest(
            tenant_id=tenant_id,
            customer_id=self.customer_id,
            title=self.title,
            description=self.description,
            objective=self.objective,
            urgency=self.urgency,
            sensitivity=self.sensitivity,
            external_action_requested=self.external_action_requested,
            requested_channel=self.requested_channel,
            recipient_opted_in=self.recipient_opted_in,
            evidence_ids=tuple(self.evidence_ids),
        )


def _authenticated_tenant_id(current_user: Any) -> str:
    """Derive queue scope only from the authenticated identity."""
    tenant_id = getattr(current_user, "tenant_id", None)
    if not tenant_id:
        raise HTTPException(403, "authenticated_tenant_required")
    return str(tenant_id)


def _safe(name: str, fn, default, degraded: list[str]) -> Any:
    try:
        return fn()
    except BaseException as exc:
        degraded.append(name)
        return {
            "_error": True,
            "_type": type(exc).__name__,
            "_default": default,
        }


def _growth_queue(tenant_id: str = "dealix") -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("growth", tenant_id=tenant_id)
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _sales_queue(tenant_id: str = "dealix") -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("sales", tenant_id=tenant_id)
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _support_queue(tenant_id: str = "dealix") -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("support", tenant_id=tenant_id)
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _cs_queue(tenant_id: str = "dealix") -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("customer_success", tenant_id=tenant_id)
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _delivery_queue(tenant_id: str = "dealix") -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("delivery", tenant_id=tenant_id)
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _compliance_alerts(tenant_id: str = "dealix") -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("compliance", tenant_id=tenant_id)
    escalated = [it for it in items if it.status == "escalated"]
    return {
        "count": len(items),
        "escalated": len(escalated),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _executive_summary(tenant_id: str = "dealix") -> dict[str, Any]:
    queue = get_default_queue()
    all_items = queue.list_all(tenant_id=tenant_id)
    by_priority = {
        p: len(queue.list_by_priority(p, tenant_id=tenant_id))
        for p in ("p0", "p1", "p2", "p3")
    }
    return {
        "total_items": len(all_items),
        "by_priority": by_priority,
    }


def _blocked_actions(tenant_id: str = "dealix") -> dict[str, Any]:
    queue = get_default_queue()
    blocked = queue.list_by_status("blocked", tenant_id=tenant_id)
    return {
        "count": len(blocked),
        "first_3": [b.model_dump(mode="json") for b in prioritize(blocked)[:3]],
    }


def _today_top_3(tenant_id: str = "dealix") -> list[dict[str, Any]]:
    queue = get_default_queue()
    items = queue.list_all(tenant_id=tenant_id)
    return [it.model_dump(mode="json") for it in prioritize(items)[:3]]


def _revenue_truth_summary() -> dict[str, Any]:
    """RX — single revenue-truth snapshot for the founder.

    Imported lazily so the daily-command-center stays operational
    even if revenue_pipeline ships with a bug.
    """
    from auto_client_acquisition.revenue_pipeline import snapshot_revenue_truth
    from auto_client_acquisition.revenue_pipeline.pipeline import get_default_pipeline
    from auto_client_acquisition.revenue_pipeline.revenue_truth import to_dict
    from auto_client_acquisition.runtime_paths import resolve_proof_events_dir

    pipeline = get_default_pipeline()
    p_summary = pipeline.summary()

    proof_dir = resolve_proof_events_dir()
    if proof_dir.exists():
        count = sum(
            1 for f in proof_dir.iterdir()
            if f.is_file()
            and f.suffix.lower() in (".json", ".jsonl", ".md")
            and not any(s in f.name.lower() for s in (
                ".gitkeep", "readme", "schema.example", ".example.", "template",
            ))
        )
    else:
        count = 0

    truth = snapshot_revenue_truth(
        pipeline_summary=p_summary,
        proof_event_files_count=count,
    )
    return to_dict(truth)


def _revenue_execution_next_step() -> dict[str, str]:
    """RX — single string telling the founder the next revenue action."""
    truth = _revenue_truth_summary()
    return {
        "ar": truth["next_action_ar"],
        "en": truth["next_action_en"],
    }


@router.get("/status")
async def full_ops_status() -> dict[str, Any]:
    return {
        "service": "full_ops",
        "module": "full_ops",
        "status": "operational",
        "version": "v12",
        "company_workload_router_version": "v1",
        "degraded": False,
        "checks": {"work_queue": "ok"},
        "hard_gates": _HARD_GATES,
        "next_action_ar": "افتح /daily-command-center للحصول على القرارات اليومية",
        "next_action_en": "Open /daily-command-center for today's decisions.",
    }


@router.get("/capability-map")
async def company_capability_map() -> dict[str, Any]:
    """The 16 business functions Dealix can diagnose and orchestrate."""
    capabilities = capability_map()
    return {
        "schema_version": 1,
        "count": len(capabilities),
        "capabilities": capabilities,
        "operating_model": "one_router_existing_catalog_one_queue",
        "hard_gates": _HARD_GATES,
    }


@router.post("/route-workload")
async def route_workload(
    body: RouteWorkloadBody,
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    """Plan a company workload without mutating queues or calling connectors."""
    tenant_id = _authenticated_tenant_id(current_user)
    route = route_company_workload(body.to_request(tenant_id=tenant_id))
    return {
        "mode": "plan_only",
        "external_side_effect": False,
        "route": route.to_dict(),
        "hard_gates": _HARD_GATES,
    }


@router.post("/workloads")
async def enqueue_workload(
    body: RouteWorkloadBody,
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    """Route and idempotently enqueue one internal work item.

    This endpoint never sends a message, charges a customer, changes a contract,
    or calls a third-party connector.  Such work remains blocked or approval-gated.
    """
    tenant_id = _authenticated_tenant_id(current_user)
    route = route_company_workload(body.to_request(tenant_id=tenant_id))
    item = get_default_queue().add(route.to_work_item())
    tenant_depth = len(get_default_queue().list_all(tenant_id=tenant_id))
    return {
        "mode": "internal_enqueue",
        "external_side_effect": False,
        "idempotent": True,
        "work_item": item.model_dump(mode="json"),
        "route": route.to_dict(),
        "tenant_queue_depth": tenant_depth,
        "hard_gates": _HARD_GATES,
    }


@router.get("/daily-command-center")
async def daily_command_center(
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    """Single bilingual snapshot across all 9 OSes.

    Read-only. 200 always. Degraded sections reported in
    ``degraded_sections`` rather than 5xx.
    """
    tenant_id = _authenticated_tenant_id(current_user)
    degraded: list[str] = []
    growth = _safe(
        "growth_queue",
        lambda: _growth_queue(tenant_id),
        {"count": 0, "top_3": []},
        degraded,
    )
    sales = _safe(
        "sales_queue",
        lambda: _sales_queue(tenant_id),
        {"count": 0, "top_3": []},
        degraded,
    )
    support = _safe(
        "support_queue",
        lambda: _support_queue(tenant_id),
        {"count": 0, "top_3": []},
        degraded,
    )
    cs = _safe(
        "cs_queue",
        lambda: _cs_queue(tenant_id),
        {"count": 0, "top_3": []},
        degraded,
    )
    delivery = _safe(
        "delivery_queue",
        lambda: _delivery_queue(tenant_id),
        {"count": 0, "top_3": []},
        degraded,
    )
    compliance = _safe(
        "compliance_alerts",
        lambda: _compliance_alerts(tenant_id),
        {"count": 0, "escalated": 0, "top_3": []},
        degraded,
    )
    executive = _safe(
        "executive_summary",
        lambda: _executive_summary(tenant_id),
        {"total_items": 0, "by_priority": {}},
        degraded,
    )
    blocked = _safe(
        "blocked_actions",
        lambda: _blocked_actions(tenant_id),
        {"count": 0, "first_3": []},
        degraded,
    )
    top_3 = _safe("today_top_3", lambda: _today_top_3(tenant_id), [], degraded)
    if tenant_id == "dealix":
        revenue_truth = _safe(
            "revenue_truth",
            _revenue_truth_summary,
            {
                "revenue_live": False,
                "v12_1_unlocked": False,
                "blockers": ["unavailable"],
            },
            degraded,
        )
        revenue_next_step = _safe(
            "revenue_execution_next_step",
            _revenue_execution_next_step,
            {
                "ar": "نفّذ 14_DAY_FIRST_REVENUE_PLAYBOOK",
                "en": "Run 14_DAY_FIRST_REVENUE_PLAYBOOK",
            },
            degraded,
        )
    else:
        revenue_truth = {
            "tenant_scoped": True,
            "status": "not_configured",
            "note": "Dealix founder revenue truth is never exposed to customer tenants.",
        }
        revenue_next_step = {
            "ar": "اربط خط أساس الإيراد الخاص بهذا المستأجر",
            "en": "Connect this tenant's revenue baseline.",
        }

    return {
        "schema_version": 1,
        "tenant_id": tenant_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "title_ar": "مركز الأوامر اليومي — Dealix Full-Ops",
        "title_en": "Daily Command Center — Dealix Full-Ops",
        "today_top_3_decisions": top_3,
        "growth_queue": growth,
        "sales_queue": sales,
        "support_queue": support,
        "cs_queue": cs,
        "delivery_queue": delivery,
        "compliance_alerts": compliance,
        "executive_summary": executive,
        "blocked_actions": blocked,
        "proof_summary": {
            "note_ar": "أدلة العميل توثَّق في docs/proof-events/ عند توفّرها",
            "note_en": (
                "Customer proof events are recorded under docs/proof-events/ when available."
            ),
        },
        "revenue_truth": revenue_truth,
        "revenue_execution_next_step": revenue_next_step,
        "next_best_actions": {
            "ar": "ابدأ بأعلى p0/p1 في كل قائمة، وتجاهل المحظور",
            "en": "Start with the highest p0/p1 in each queue; skip blocked items.",
        },
        "hard_gates": _HARD_GATES,
        "degraded": bool(degraded),
        "degraded_sections": degraded,
    }
