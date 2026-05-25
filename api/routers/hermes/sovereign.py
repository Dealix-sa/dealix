"""Sovereign console + approvals + kill switch."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.routers.hermes._dependencies import get_hermes
from dealix.hermes.kernel.schemas import SovereigntyLevel
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.sovereignty.kill_switch import KillTarget


router = APIRouter(prefix="/api/v1/hermes/sovereign", tags=["hermes-sovereign"])


@router.get("/console")
def console(orch: HermesOrchestrator = Depends(get_hermes)):
    return {
        "pending_approvals": len(orch.approvals.pending()),
        "open_risks": len(orch.risk_register.open_risks()),
        "open_incidents": len(orch.incident_register.open_incidents()),
        "killed_targets": len(orch.kill_switch.list_active()),
        "registered_agents": len(orch.agent_registry.list()),
        "registered_tools": len(orch.tool_registry.list()),
    }


@router.get("/approvals")
def approvals(orch: HermesOrchestrator = Depends(get_hermes)):
    return orch.approvals.list()


class OpenApprovalRequest(BaseModel):
    subject_id: str
    subject_type: str
    title: str
    summary: str
    sovereignty_level: SovereigntyLevel


@router.post("/approvals/open")
def open_approval(body: OpenApprovalRequest, orch: HermesOrchestrator = Depends(get_hermes)):
    return orch.approvals.open(
        subject_id=body.subject_id,
        subject_type=body.subject_type,
        title=body.title,
        summary=body.summary,
        sovereignty_level=body.sovereignty_level,
    )


@router.post("/approve")
def approve(approval_id: str, approver: str = "Sami", orch: HermesOrchestrator = Depends(get_hermes)):
    try:
        return orch.approvals.approve(approval_id, approver=approver)
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.post("/deny")
def deny(approval_id: str, denier: str = "Sami", reason: str = "", orch: HermesOrchestrator = Depends(get_hermes)):
    try:
        return orch.approvals.deny(approval_id, denier=denier, reason=reason)
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc


class KillRequest(BaseModel):
    target_type: KillTarget
    target_id: str
    reason: str


@router.post("/kill-switch")
def kill(body: KillRequest, orch: HermesOrchestrator = Depends(get_hermes)):
    return orch.kill_switch.kill(body.target_type, body.target_id, reason=body.reason)


@router.post("/kill-switch/restore")
def restore(target_type: KillTarget, target_id: str, orch: HermesOrchestrator = Depends(get_hermes)):
    rec = orch.kill_switch.restore(target_type, target_id)
    if rec is None:
        raise HTTPException(404, "kill record not found")
    return rec
