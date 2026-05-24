"""Hermes API — kernel pipeline + Trust plane endpoints (Wave 2).

Exposes:

    POST /api/v1/hermes/signals                  → run full pipeline
    GET  /api/v1/hermes/runs/{run_id}            → fetch run
    GET  /api/v1/hermes/approvals/pending        → list pending tickets
    POST /api/v1/hermes/approvals/{id}/approve   → approve a ticket
    POST /api/v1/hermes/approvals/{id}/deny      → deny a ticket
    GET  /api/v1/hermes/events/recent?limit=50   → recent events
    GET  /api/v1/hermes/evidence/{pack_id}       → fetch an evidence pack
    GET  /api/v1/hermes/agents                   → registered agents
    GET  /api/v1/hermes/tools                    → registered tools
    POST /api/v1/hermes/incidents/declare        → declare an incident

Auth: every endpoint requires `X-Admin-API-Key` matching
`DEALIX_ADMIN_API_KEY` (defaults to `dev-key` in local dev).
"""

from __future__ import annotations

import hmac
import logging
import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes import (
    EventBus,
    HermesOrchestrator,
    OrchestratorRun,
    Signal,
)
from dealix.hermes.core.signals import SignalSource
from dealix.hermes.core.schemas import WorkspaceScope
from dealix.trust.agent_registry import AgentRegistry, seed_default_registry
from dealix.trust.approvals import ApprovalQueue
from dealix.trust.evidence import EvidenceStore
from dealix.trust.incident_response import (
    IncidentResponse,
    IncidentSeverity,
)
from dealix.trust.tool_registry import ToolRegistry, seed_default_tool_registry


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/hermes", tags=["hermes"])


# ─────────────────────────────────────────────────────────────
# Auth — admin API key gate
# ─────────────────────────────────────────────────────────────


_DEV_KEY_DEFAULT = "dev-key"
_DEV_KEY_WARNED = False


def _admin_key() -> str:
    global _DEV_KEY_WARNED
    key = os.getenv("DEALIX_ADMIN_API_KEY")
    if key:
        return key
    if not _DEV_KEY_WARNED:
        logger.warning(
            "DEALIX_ADMIN_API_KEY not set; falling back to dev default. "
            "Set the env var in production."
        )
        _DEV_KEY_WARNED = True
    return _DEV_KEY_DEFAULT


def require_admin_api_key(
    x_admin_api_key: str | None = Header(default=None, alias="X-Admin-API-Key"),
) -> None:
    expected = _admin_key()
    if not x_admin_api_key or not hmac.compare_digest(x_admin_api_key, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-Admin-API-Key",
        )


# ─────────────────────────────────────────────────────────────
# State singleton
# ─────────────────────────────────────────────────────────────


def _approval_persist_path() -> Path:
    raw = os.getenv(
        "DEALIX_HERMES_APPROVAL_PATH",
        "var/hermes/approvals.jsonl",
    )
    return Path(raw)


def _evidence_persist_path() -> Path:
    raw = os.getenv(
        "DEALIX_HERMES_EVIDENCE_PATH",
        "var/hermes/evidence.jsonl",
    )
    return Path(raw)


class _HermesState:
    """Module-level singleton holding the Hermes runtime state."""

    def __init__(
        self,
        approval_path: Path | None = None,
        evidence_path: Path | None = None,
    ) -> None:
        approval_path = approval_path or _approval_persist_path()
        evidence_path = evidence_path or _evidence_persist_path()

        self.event_bus = EventBus()
        self.agents: AgentRegistry = seed_default_registry()
        self.tools: ToolRegistry = seed_default_tool_registry()
        self.approvals = ApprovalQueue(persist_path=approval_path)
        self.evidence = EvidenceStore(persist_path=evidence_path)
        self.incidents = IncidentResponse(
            agent_registry=self.agents,
            tool_registry=self.tools,
        )
        self.orchestrator = HermesOrchestrator(
            event_bus=self.event_bus,
            agent_registry=self.agents,
            tool_registry=self.tools,
            approval_center=self.approvals,
        )
        self.runs: dict[str, OrchestratorRun] = {}


_state: _HermesState | None = None


def get_state() -> _HermesState:
    global _state
    if _state is None:
        _state = _HermesState()
    return _state


def reset_state_for_tests(
    approval_path: Path | None = None,
    evidence_path: Path | None = None,
) -> _HermesState:
    """Reset the singleton — used by the test suite to isolate state."""
    global _state, _DEV_KEY_WARNED
    _DEV_KEY_WARNED = False
    _state = _HermesState(
        approval_path=approval_path,
        evidence_path=evidence_path,
    )
    return _state


# ─────────────────────────────────────────────────────────────
# Request / response models
# ─────────────────────────────────────────────────────────────


class SignalIn(BaseModel):
    """Inbound signal payload (orchestrator generates signal_id)."""

    model_config = ConfigDict(extra="forbid")

    source: SignalSource
    raw_text: str = Field(..., min_length=1, max_length=20_000)
    channel: str = Field(..., min_length=1, max_length=64)
    workspace: WorkspaceScope = WorkspaceScope.INTERNAL
    metadata: dict[str, str] = Field(default_factory=dict)


class RunOut(BaseModel):
    """Public projection of an OrchestratorRun (API-safe)."""

    model_config = ConfigDict(extra="forbid")

    run_id: str
    status: str
    signal_id: str
    opp_id: str | None
    decision_id: str | None
    plan_id: str | None
    approval_ticket_id: str | None
    outcome_id: str | None
    asset_id: str | None
    events_published: list[str]
    blocked_reason: str | None
    sovereignty_level: str | None
    score: float | None


class ApprovalActionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    by: str = Field(..., min_length=1, max_length=128)
    note: str | None = Field(default=None, max_length=600)


class DenyActionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    by: str = Field(..., min_length=1, max_length=128)
    reason: str = Field(..., min_length=1, max_length=600)


class IncidentDeclareIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    severity: IncidentSeverity
    summary: str = Field(..., min_length=1, max_length=600)
    owner: str = Field(default="sami", min_length=1, max_length=128)
    implicated_agents: list[str] = Field(default_factory=list, max_length=64)
    implicated_tools: list[str] = Field(default_factory=list, max_length=64)


class EventOut(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str
    event_type: str
    actor: str
    entity_type: str
    entity_id: str
    risk_level: str
    sovereignty_level: str


class AgentOut(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_id: str
    name: str
    family: str
    permission_level: str
    status: str
    allowed_tools: list[str]


class ToolOut(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tool_id: str
    name: str
    vendor: str
    risk_level: str
    requires_approval: bool
    allowlisted: bool
    block_reason: str | None


# ─────────────────────────────────────────────────────────────
# Mapping helpers
# ─────────────────────────────────────────────────────────────


def _run_to_out(run_id: str, run: OrchestratorRun) -> RunOut:
    ids = run.step_ids()
    return RunOut(
        run_id=run_id,
        status=run.status.value,
        signal_id=ids["signal_id"],
        opp_id=ids["opp_id"],
        decision_id=ids["decision_id"],
        plan_id=ids["plan_id"],
        approval_ticket_id=ids["approval_ticket_id"],
        outcome_id=ids["outcome_id"],
        asset_id=ids["asset_id"],
        events_published=list(run.events_published),
        blocked_reason=run.blocked_reason,
        sovereignty_level=(
            run.sovereignty_verdict.level.value
            if run.sovereignty_verdict
            else None
        ),
        score=run.scored.score if run.scored else None,
    )


# ─────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────


@router.post(
    "/signals",
    response_model=RunOut,
    dependencies=[Depends(require_admin_api_key)],
)
def ingest_signal(body: SignalIn) -> RunOut:
    """Walk the full Hermes pipeline for a new signal.

    تستقبل إشارة جديدة وتشغل خط أنابيب Hermes الكامل.
    """
    state = get_state()
    signal = Signal(
        source=body.source,
        raw_text=body.raw_text,
        channel=body.channel,
        workspace=body.workspace,
        metadata=body.metadata,
    )
    run = state.orchestrator.run(signal)
    run_id = f"run_{signal.signal_id}"
    state.runs[run_id] = run
    return _run_to_out(run_id, run)


@router.get(
    "/runs/{run_id}",
    response_model=RunOut,
    dependencies=[Depends(require_admin_api_key)],
)
def get_run(run_id: str) -> RunOut:
    """Retrieve a previously executed pipeline run."""
    state = get_state()
    run = state.runs.get(run_id)
    if run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"unknown run_id: {run_id}",
        )
    return _run_to_out(run_id, run)


@router.get(
    "/approvals/pending",
    dependencies=[Depends(require_admin_api_key)],
)
def list_pending_approvals() -> dict[str, Any]:
    """List pending approval tickets across the kernel."""
    state = get_state()
    tickets = state.approvals.pending()
    return {
        "count": len(tickets),
        "tickets": [t.model_dump(mode="json") for t in tickets],
    }


@router.post(
    "/approvals/{ticket_id}/approve",
    dependencies=[Depends(require_admin_api_key)],
)
def approve_ticket(ticket_id: str, body: ApprovalActionIn) -> dict[str, Any]:
    """Approve a pending approval ticket."""
    state = get_state()
    try:
        ticket = state.approvals.approve(ticket_id, by=body.by, note=body.note)
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return ticket.model_dump(mode="json")


@router.post(
    "/approvals/{ticket_id}/deny",
    dependencies=[Depends(require_admin_api_key)],
)
def deny_ticket(ticket_id: str, body: DenyActionIn) -> dict[str, Any]:
    """Deny a pending approval ticket."""
    state = get_state()
    try:
        ticket = state.approvals.deny(ticket_id, by=body.by, reason=body.reason)
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return ticket.model_dump(mode="json")


@router.get(
    "/events/recent",
    dependencies=[Depends(require_admin_api_key)],
)
def recent_events(limit: int = Query(default=50, ge=1, le=500)) -> dict[str, Any]:
    """Return the most recent events from the EventBus."""
    state = get_state()
    events = state.event_bus.recent(limit=limit)
    out = [
        EventOut(
            event_id=e.event_id,
            event_type=e.event_type.value,
            actor=e.actor,
            entity_type=e.entity_type,
            entity_id=e.entity_id,
            risk_level=e.risk_level.value,
            sovereignty_level=e.sovereignty_level,
        )
        for e in events
    ]
    return {"count": len(out), "events": [o.model_dump() for o in out]}


@router.get(
    "/evidence/{pack_id}",
    dependencies=[Depends(require_admin_api_key)],
)
def get_evidence(pack_id: str) -> dict[str, Any]:
    """Return the evidence pack for the given pack_id."""
    state = get_state()
    try:
        pack = state.evidence.get(pack_id)
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return pack.model_dump(mode="json")


@router.get(
    "/agents",
    dependencies=[Depends(require_admin_api_key)],
)
def list_agents() -> dict[str, Any]:
    """Return all registered agents."""
    state = get_state()
    out: list[AgentOut] = []
    for entry in state.agents.all():
        out.append(
            AgentOut(
                agent_id=entry.agent_id,
                name=entry.name,
                family=entry.family.value,
                permission_level=entry.permission_level.value,
                status=entry.status.value,
                allowed_tools=sorted(entry.allowed_tools),
            )
        )
    return {"count": len(out), "agents": [a.model_dump() for a in out]}


@router.get(
    "/tools",
    dependencies=[Depends(require_admin_api_key)],
)
def list_tools() -> dict[str, Any]:
    """Return all registered tools."""
    state = get_state()
    out: list[ToolOut] = []
    for entry in state.tools.all():
        out.append(
            ToolOut(
                tool_id=entry.tool_id,
                name=entry.name,
                vendor=entry.vendor,
                risk_level=entry.risk_level.value,
                requires_approval=entry.requires_approval,
                allowlisted=entry.allowlisted,
                block_reason=entry.block_reason,
            )
        )
    return {"count": len(out), "tools": [t.model_dump() for t in out]}


@router.post(
    "/incidents/declare",
    dependencies=[Depends(require_admin_api_key)],
)
def declare_incident(body: IncidentDeclareIn) -> dict[str, Any]:
    """Declare an incident. SEV1/SEV2 auto-pause implicated agents."""
    state = get_state()
    incident = state.incidents.declare(
        severity=body.severity,
        summary=body.summary,
        owner=body.owner,
        implicated_agents=body.implicated_agents,
        implicated_tools=body.implicated_tools,
    )
    return incident.model_dump(mode="json")


__all__ = ["router", "get_state", "reset_state_for_tests"]
