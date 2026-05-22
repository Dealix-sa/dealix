"""HTTP surface for the Customer Success autonomy layer.

Exposes the latest cycle report, an admin-gated trigger to run a new
cycle, and a per-customer snapshot endpoint. No external send is ever
issued from these routes — every retention action is approval-gated and
flows through the founder's approval queue.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key
from auto_client_acquisition.customer_success_autonomy.cs_cycle import (
    CustomerSuccessCycleReport,
    latest_cs_report,
    run_customer_success_cycle,
)
from auto_client_acquisition.customer_success_autonomy.signal_aggregator import (
    aggregate_customer_signals,
)

router = APIRouter(
    prefix="/api/v1/customer-success/autonomous",
    tags=["customer-success-autonomous"],
)


def _empty_state() -> dict[str, Any]:
    return {
        "cycle_id": "",
        "generated_at": "",
        "on_date": "",
        "title_ar": "",
        "title_en": "",
        "summary": {
            "active_customers": 0,
            "opportunities_total": 0,
            "at_risk": 0,
            "expansion_ready": 0,
            "renewals_due": 0,
            "nps_detractors": 0,
        },
        "opportunities": [],
        "approvals_created": 0,
        "work_items_created": 0,
        "hard_gates": [
            "no_live_send",
            "no_live_charge",
            "approval_required_for_external_actions",
            "no_unconsented_outreach",
            "no_fake_proof",
        ],
        "warnings": [],
        "report_paths": {},
    }


@router.get("/latest")
async def latest() -> dict[str, Any]:
    """Return the most recent persisted CS cycle report, or empty-state."""
    return latest_cs_report() or _empty_state()


@router.post("/run", dependencies=[Depends(require_admin_key)])
async def run(body: dict[str, Any] | None = None) -> dict[str, Any]:
    """Trigger a CS autonomy cycle. Admin-gated."""
    body = body or {}
    customer_ids = body.get("customer_ids")
    inputs_by_customer = body.get("inputs_by_customer") or {}
    on_date = body.get("on_date")
    report: CustomerSuccessCycleReport = run_customer_success_cycle(
        customer_ids=customer_ids if isinstance(customer_ids, list) else None,
        on_date=on_date,
        inputs_by_customer=(
            inputs_by_customer if isinstance(inputs_by_customer, dict) else None
        ),
    )
    return report.to_dict()


@router.get("/customers/{customer_id}/snapshot")
async def customer_snapshot(customer_id: str) -> dict[str, Any]:
    """Return the aggregated retention snapshot for one customer."""
    snap = aggregate_customer_signals(customer_id)
    return snap.to_dict()


__all__ = ["router"]
