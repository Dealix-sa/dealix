"""Observability router."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from api.routers.hermes._dependencies import get_hermes
from dealix.hermes.observability.system_health import SystemHealth
from dealix.hermes.orchestrator import HermesOrchestrator


router = APIRouter(prefix="/api/v1/hermes/observability", tags=["hermes-observability"])


@router.get("/system-health")
def health(orch: HermesOrchestrator = Depends(get_hermes)) -> SystemHealth:
    return SystemHealth(
        open_incidents=len(orch.incident_register.open_incidents()),
        open_risks=len(orch.risk_register.open_risks()),
        pending_approvals=len(orch.approvals.pending()),
        killed_assets=sum(1 for a in orch.kernel.assets.list() if a.killed),
        revenue_at_risk_sar=0.0,
    )


@router.get("/lifecycle-events")
def events(orch: HermesOrchestrator = Depends(get_hermes)):
    return orch.kernel.all_events()
