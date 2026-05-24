"""AI Stack HTTP surface — unified runner + status for the L1..L11 stack.

The router publishes four endpoints under ``/api/v1/ai-stack``:

* ``POST /run``                — execute the full eleven-layer stack
* ``GET  /status``             — health snapshot of every layer
* ``GET  /layers``             — descriptive map of layer roles + modules
* ``GET  /proposals/{tenant}`` — list shadow-mode improvement proposals
* ``GET  /run/{run_id}``       — fetch a stored result (in-memory store)

All endpoints are governed by the same eleven non-negotiables as the rest
of the stack: no live sends, no live charges, no inventing KPIs, no proof
without governance clearance, no revenue before invoice_paid. Every run is
hash-bound to a proof pack so a customer can audit what they saw.
"""

from __future__ import annotations

import threading
from collections.abc import Mapping
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.ai_stack_os import (
    AIStackInput,
    AIStackOrchestrator,
    AIStackResult,
    Offer,
    SourcePassportInput,
    layer_versions,
    snapshot_health,
)
from auto_client_acquisition.ai_stack_os.layer_health import _LAYER_MODULES
from auto_client_acquisition.self_evolving_os import (
    derive_suggestions,
    get_default_repository,
    get_default_store,
    proposal_from_suggestion,
)

router = APIRouter(prefix="/api/v1/ai-stack", tags=["AI Stack"])


# Hard gates surfaced for parity with other governed routers.
_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_invented_kpis": True,
    "no_revenue_before_invoice_paid": True,
    "source_passport_required": True,
    "bilingual_required": True,
    "self_evolving_shadow_only": True,
}


# In-memory result store with optional retention cap. Production deployments
# swap this for a Postgres-backed store, but the in-memory variant is
# perfectly serviceable for the demo path the AI Stack UI consumes.
_RESULT_STORE: dict[str, AIStackResult] = {}
_RESULT_LOCK = threading.RLock()
_RESULT_MAX = 256


def _store_result(result: AIStackResult) -> None:
    with _RESULT_LOCK:
        _RESULT_STORE[result.run_id] = result
        if len(_RESULT_STORE) > _RESULT_MAX:
            # Evict oldest by insertion order — simple FIFO is fine for demo loads.
            oldest = next(iter(_RESULT_STORE))
            _RESULT_STORE.pop(oldest, None)


def _fetch_result(run_id: str) -> AIStackResult | None:
    with _RESULT_LOCK:
        return _RESULT_STORE.get(run_id)


# Module-level orchestrator — shared across requests so the vector store and
# learning store accumulate context across a session.
_ORCHESTRATOR_LOCK = threading.Lock()
_ORCHESTRATOR: AIStackOrchestrator | None = None


def _orchestrator() -> AIStackOrchestrator:
    global _ORCHESTRATOR
    with _ORCHESTRATOR_LOCK:
        if _ORCHESTRATOR is None:
            _ORCHESTRATOR = AIStackOrchestrator()
        return _ORCHESTRATOR


def reset_orchestrator_for_tests() -> None:
    global _ORCHESTRATOR
    with _ORCHESTRATOR_LOCK:
        _ORCHESTRATOR = None
    with _RESULT_LOCK:
        _RESULT_STORE.clear()


# ── Schemas ──────────────────────────────────────────────────────────────


class RunRequest(BaseModel):
    """Request body for ``POST /run``."""

    tenant_id: str = Field(min_length=1)
    customer_handle: str = Field(min_length=1)
    company_name: str = Field(min_length=1, max_length=200)
    sector: str = Field(default="general", max_length=80)
    challenge_ar: str = Field(min_length=3, max_length=2000)
    challenge_en: str = Field(default="", max_length=2000)
    offer_tier: Offer = Field(default=Offer.FREE_DIAGNOSTIC)
    source_passport: SourcePassportInput
    rag_documents: list[dict[str, Any]] = Field(default_factory=list)
    actor: str = Field(default="api_user", max_length=120)
    locale_primary: str = Field(default="ar", pattern=r"^(ar|en)$")


class LayerDescription(BaseModel):
    layer: str
    label: str
    module: str


class LayersResponse(BaseModel):
    hard_gates: dict[str, bool]
    layer_versions: dict[str, str]
    layers: list[LayerDescription]


class ProposalsResponse(BaseModel):
    tenant_id: str
    proposal_count: int
    proposals: list[dict[str, Any]]


# ── Endpoints ────────────────────────────────────────────────────────────


@router.post("/run", response_model=AIStackResult)
async def run_stack(request: RunRequest) -> AIStackResult:
    """Execute the eleven-layer AI Stack and return the structured result.

    The endpoint is **synchronous** — the AI Stack's default handlers are
    deterministic and run in milliseconds. Production LLM-backed handlers
    should remain bounded; if a deployment swaps in long-running handlers
    they SHOULD push the orchestrator behind a job queue.
    """
    payload = AIStackInput(
        tenant_id=request.tenant_id,
        customer_handle=request.customer_handle,
        company_name=request.company_name,
        sector=request.sector,
        challenge_ar=request.challenge_ar,
        challenge_en=request.challenge_en,
        offer_tier=request.offer_tier,
        source_passport=request.source_passport,
        rag_documents=request.rag_documents,
        actor=request.actor,
        locale_primary=request.locale_primary,
    )
    try:
        result = _orchestrator().run(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    _store_result(result)
    return result


@router.get("/status")
async def status() -> dict[str, Any]:
    """Health snapshot for every layer (read-only, safe to poll)."""
    snapshot = snapshot_health()
    return {
        "overall_healthy": snapshot.overall_healthy,
        "snapshot_at": snapshot.snapshot_at,
        "hard_gates": dict(_HARD_GATES),
        "layers": [layer.to_dict() for layer in snapshot.layers],
    }


@router.get("/layers", response_model=LayersResponse)
async def list_layers() -> LayersResponse:
    """Descriptive map of the eleven layers + hard gates + best-effort versions."""
    return LayersResponse(
        hard_gates=dict(_HARD_GATES),
        layer_versions=layer_versions(),
        layers=[
            LayerDescription(layer=name, label=label, module=module)
            for name, module, label in _LAYER_MODULES
        ],
    )


@router.get("/run/{run_id}", response_model=AIStackResult)
async def get_run(run_id: str) -> AIStackResult:
    """Fetch a stored AI Stack run by id (in-memory; non-persistent across reboots)."""
    result = _fetch_result(run_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"run_id not found: {run_id!r}")
    return result


@router.get("/proposals/{tenant_id}", response_model=ProposalsResponse)
async def list_proposals(
    tenant_id: str,
    since_days: int = 30,
    minimum_severity: str = "info",
) -> ProposalsResponse:
    """Surface shadow-mode improvement proposals for human review.

    The endpoint derives suggestions from the learning store, wraps each
    in an ``ImprovementProposal`` (state=``pending_approval``), submits
    them to the default repository, and returns the pending list. No
    suggestion is ever auto-applied — that is the founder's call.
    """
    if since_days < 0:
        raise HTTPException(status_code=400, detail="since_days must be >= 0")
    if minimum_severity not in ("info", "watch", "act"):
        raise HTTPException(
            status_code=400,
            detail="minimum_severity must be one of: info, watch, act",
        )
    suggestions = derive_suggestions(
        tenant_id=tenant_id,
        store=get_default_store(),
        since_days=since_days,
        minimum_severity=minimum_severity,
    )
    repo = get_default_repository()
    proposals = [
        repo.submit(proposal_from_suggestion(s)) for s in suggestions
    ]
    return ProposalsResponse(
        tenant_id=tenant_id,
        proposal_count=len(proposals),
        proposals=[p.to_dict() for p in proposals],
    )


__all__ = ["reset_orchestrator_for_tests", "router"]
