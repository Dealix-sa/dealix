"""
Hermes Control Plane — internal HTTP surface.

Single router that exposes the Hermes runtime, approvals queue, audit trace,
product readiness, controls evaluation, and kill switch to internal callers.
Every response that originates from `HermesRuntime.run` is shaped by
`HermesResponse.to_dict()` (the canonical Section 58 shape).

No authentication is enforced at this layer — trust comes from the network
policy that fronts the service. Approval (HOLD) and denial (DENY) are
modelled as product states, not HTTP errors.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.contracts import (
    Actor,
    ActorKind,
    ContextPacket,
    DataSensitivity,
    OutputKind,
)
from dealix.hermes.control_plane import HermesRuntime
from dealix.hermes.control_plane.kill_switch import KillTargetKind
from dealix.hermes.control_plane.runtime import DraftBundle
from dealix.hermes.products import (
    OfferRegistry,
    ProductReadinessGate,
    default_registry as default_offer_registry,
)
from dealix.hermes.trust import default_library as default_trust_library


router = APIRouter(prefix="/api/v1/hermes", tags=["hermes"])


# ────────────────────────────────────────────────────────────────
# Module-level singleton state. Kept in a small dataclass-like
# holder so tests can replace it without rewiring imports.
# ────────────────────────────────────────────────────────────────


class _State:
    def __init__(self) -> None:
        self.runtime: HermesRuntime = HermesRuntime()
        self.offers: OfferRegistry = default_offer_registry()
        self.readiness: ProductReadinessGate = ProductReadinessGate()


_state = _State()


# ────────────────────────────────────────────────────────────────
# Serialization helper
# ────────────────────────────────────────────────────────────────


def _jsonable(value: Any) -> Any:
    """Recursively convert datetimes, enums, dataclasses into JSON-safe."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return {k: _jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_jsonable(v) for v in value]
    return str(value)


# ────────────────────────────────────────────────────────────────
# Pydantic v2 models
# ────────────────────────────────────────────────────────────────


class ActorIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    actor_id: str
    kind: str
    display_name: str | None = None
    org_id: str | None = None
    customer_id: str | None = None
    partner_id: str | None = None


class DraftIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    text: str
    prices_sar: list[int] = Field(default_factory=list)
    urls: list[str] = Field(default_factory=list)
    structured: dict[str, Any] = Field(default_factory=dict)


class RunIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    actor: ActorIn
    intent: str
    payload: dict[str, Any] = Field(default_factory=dict)
    data_sensitivity: str | None = None
    declared_output_kind: str | None = None
    customer_id: str | None = None
    draft: DraftIn | None = None
    signals: dict[str, Any] = Field(default_factory=dict)
    target_agent_id: str | None = None
    target_workflow_id: str | None = None


class DecideIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    decided_by: str
    approve: bool
    note: str | None = None


class KillSwitchIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    tripped_by: str
    reason: str


class RestoreIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    restored_by: str
    reason: str


# ────────────────────────────────────────────────────────────────
# Helpers to build a ContextPacket from the incoming request body
# ────────────────────────────────────────────────────────────────


def _parse_actor_kind(value: str) -> ActorKind:
    try:
        return ActorKind(value)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=f"unknown actor kind `{value}`",
        ) from exc


def _parse_sensitivity(value: str | None) -> DataSensitivity:
    if value is None:
        return DataSensitivity.INTERNAL
    try:
        return DataSensitivity(value)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=f"unknown data sensitivity `{value}`",
        ) from exc


def _parse_output_kind(value: str | None) -> OutputKind:
    if value is None:
        return OutputKind.DRAFT
    try:
        return OutputKind(value)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=f"unknown output kind `{value}`",
        ) from exc


def _parse_kill_kind(value: str) -> KillTargetKind:
    try:
        return KillTargetKind(value)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=(
                f"unknown kill target kind `{value}`. "
                f"allowed: {[k.value for k in KillTargetKind]}"
            ),
        ) from exc


# ────────────────────────────────────────────────────────────────
# Endpoints
# ────────────────────────────────────────────────────────────────


@router.post("/run")
async def run(payload: RunIn = Body(...)) -> dict[str, Any]:
    actor = Actor(
        actor_id=payload.actor.actor_id,
        kind=_parse_actor_kind(payload.actor.kind),
        display_name=payload.actor.display_name,
        org_id=payload.actor.org_id,
        customer_id=payload.actor.customer_id,
        partner_id=payload.actor.partner_id,
    )
    context = ContextPacket(
        actor=actor,
        intent=payload.intent,
        payload=payload.payload,
        data_sensitivity=_parse_sensitivity(payload.data_sensitivity),
        declared_output_kind=_parse_output_kind(payload.declared_output_kind),
        customer_id=payload.customer_id,
    )
    draft: DraftBundle | None = None
    if payload.draft is not None:
        draft = DraftBundle(
            text=payload.draft.text,
            prices_sar=list(payload.draft.prices_sar),
            urls=list(payload.draft.urls),
            structured=dict(payload.draft.structured),
        )

    outcome = _state.runtime.run(
        context=context,
        intent=payload.intent,
        draft=draft,
        signals=dict(payload.signals),
        target_agent_id=payload.target_agent_id,
        target_workflow_id=payload.target_workflow_id,
    )
    body = outcome.response.to_dict()
    body["request_id"] = outcome.request_id
    if outcome.approval_ticket is not None:
        body["approval_ticket_id"] = outcome.approval_ticket.ticket_id
    return body


@router.get("/approvals")
async def list_approvals() -> dict[str, Any]:
    tickets = _state.runtime.approval.list_pending()
    return {
        "count": len(tickets),
        "tickets": [_jsonable(t) for t in tickets],
    }


@router.post("/approvals/{ticket_id}/decide")
async def decide_approval(
    ticket_id: str,
    payload: DecideIn = Body(...),
) -> dict[str, Any]:
    try:
        ticket = _state.runtime.approval.decide(
            ticket_id,
            decided_by=payload.decided_by,
            approve=payload.approve,
            note=payload.note,
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=404, detail=f"approval ticket `{ticket_id}` not found"
        ) from exc
    return {"ticket": _jsonable(ticket)}


@router.get("/trace/{request_id}")
async def trace(request_id: str) -> dict[str, Any]:
    events = _state.runtime.audit.trace(request_id)
    return {
        "request_id": request_id,
        "count": len(events),
        "events": [_jsonable(e) for e in events],
    }


@router.get("/offers")
async def list_offers() -> dict[str, Any]:
    offers = _state.offers.all()
    return {
        "count": len(offers),
        "offers": [_jsonable(o) for o in offers],
    }


@router.get("/offers/{offer_id}/readiness")
async def offer_readiness(offer_id: str) -> dict[str, Any]:
    offer = _state.offers.get(offer_id)
    if offer is None:
        raise HTTPException(
            status_code=404, detail=f"offer `{offer_id}` not registered"
        )
    result = _state.readiness.assess(offer)
    return result.to_dict()


@router.get("/controls/evaluate")
async def controls_evaluate(
    is_external_action: bool = Query(default=False),
    approval_ticket_id: str | None = Query(default=None),
    contains_sensitive_data: bool = Query(default=False),
    leaving_workspace: bool = Query(default=False),
    mcp_server_id: str | None = Query(default=None),
    mcp_review_signed_off: bool = Query(default=False),
    execution_id: str | None = Query(default=None),
    outcome_recorded: bool = Query(default=False),
    incident_id: str | None = Query(default=None),
    remediation_recorded: bool = Query(default=False),
    contains_external_claim: bool = Query(default=False),
    evidence_pack_id: str | None = Query(default=None),
    citation_url: str | None = Query(default=None),
    enterprise_pricing: bool = Query(default=False),
    founder_approved: bool = Query(default=False),
    agent_owner: str | None = Query(default=None),
    tool_owner: str | None = Query(default=None),
) -> dict[str, Any]:
    ctx: dict[str, Any] = {
        "is_external_action": is_external_action,
        "approval_ticket_id": approval_ticket_id,
        "contains_sensitive_data": contains_sensitive_data,
        "leaving_workspace": leaving_workspace,
        "mcp_server_id": mcp_server_id,
        "mcp_review_signed_off": mcp_review_signed_off,
        "execution_id": execution_id,
        "outcome_recorded": outcome_recorded,
        "incident_id": incident_id,
        "remediation_recorded": remediation_recorded,
        "contains_external_claim": contains_external_claim,
        "evidence_pack_id": evidence_pack_id,
        "citation_url": citation_url,
        "enterprise_pricing": enterprise_pricing,
        "founder_approved": founder_approved,
        "agent_owner": agent_owner,
        "tool_owner": tool_owner,
    }
    verdicts = default_trust_library().evaluate_all(ctx)
    return {
        "ctx": ctx,
        "count": len(verdicts),
        "verdicts": [_jsonable(v) for v in verdicts],
    }


@router.post("/kill-switch/{kind}/{target_id}/trip")
async def kill_switch_trip(
    kind: str,
    target_id: str,
    payload: KillSwitchIn = Body(...),
) -> dict[str, Any]:
    target_kind = _parse_kill_kind(kind)
    record = _state.runtime.kill_switch.trip(
        target_kind,
        target_id,
        tripped_by=payload.tripped_by,
        reason=payload.reason,
    )
    return {"record": _jsonable(record)}


@router.post("/kill-switch/{kind}/{target_id}/restore")
async def kill_switch_restore(
    kind: str,
    target_id: str,
    payload: RestoreIn = Body(...),
) -> dict[str, Any]:
    target_kind = _parse_kill_kind(kind)
    record = _state.runtime.kill_switch.restore(
        target_kind,
        target_id,
        restored_by=payload.restored_by,
        reason=payload.reason,
    )
    return {"record": _jsonable(record)}


@router.get("/kill-switch/active")
async def kill_switch_active() -> dict[str, Any]:
    records = _state.runtime.kill_switch.all_tripped()
    return {
        "count": len(records),
        "records": [_jsonable(r) for r in records],
    }
