"""Communication OS API.

Approval-first company-to-client communication hub. No endpoint sends externally.
The hub is resolved lazily so importing the FastAPI application never writes to
its deployment filesystem.
"""

from __future__ import annotations

import threading
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from intelligence.bilingual import LanguageCode, get_lang
from intelligence.comms_storage import CommunicationStorageUnavailable
from intelligence.serverless_communication_hub import ServerlessCommunicationHub

router = APIRouter(prefix="/api/v1/ops/comms", tags=["Communication OS"])

_hub: ServerlessCommunicationHub | None = None
_hub_lock = threading.Lock()


def _get_hub() -> ServerlessCommunicationHub:
    """Create the configured hub only when a route actually needs it."""

    global _hub
    if _hub is not None:
        return _hub
    with _hub_lock:
        if _hub is None:
            _hub = ServerlessCommunicationHub()
    return _hub


def _storage_unavailable(exc: Exception) -> HTTPException:
    return HTTPException(
        status_code=503,
        detail={
            "code": "communication_storage_unavailable",
            "message": "Communication storage is unavailable; write actions remain blocked.",
            "error_type": type(exc).__name__,
        },
    )


class DraftRequest(BaseModel):
    contact_id: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    contact_name: str = Field(..., min_length=1)
    channel: str = Field(..., min_length=1)
    subject_en: str = Field(..., min_length=1)
    subject_ar: str = Field(..., min_length=1)
    body_en: str = Field(..., min_length=1)
    body_ar: str = Field(..., min_length=1)
    tags: list[str] = Field(default_factory=list)
    lang: LanguageCode = "both"


class InboundLogRequest(BaseModel):
    contact_id: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    contact_name: str = Field(..., min_length=1)
    channel: str = Field(..., min_length=1)
    body_en: str = Field(..., min_length=1)
    body_ar: str = Field(..., min_length=1)
    tags: list[str] = Field(default_factory=list)


class SequenceRequest(BaseModel):
    name: str = Field(..., min_length=1)
    contact_id: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    steps: list[dict[str, Any]] = Field(..., min_length=1)


class ApprovalActionRequest(BaseModel):
    actor: str = Field(..., min_length=1)
    reason: str | None = None


@router.get("/readiness")
async def communication_readiness() -> dict[str, Any]:
    """Expose storage readiness without leaking connection details."""

    try:
        result = _get_hub().readiness()
    except (CommunicationStorageUnavailable, RuntimeError, ValueError) as exc:
        raise _storage_unavailable(exc) from exc
    if not result.get("ready"):
        raise HTTPException(status_code=503, detail=result)
    return result


@router.post("/draft")
async def create_draft(payload: DraftRequest) -> dict[str, Any]:
    try:
        entry = _get_hub().create_draft(
            contact_id=payload.contact_id,
            company_name=payload.company_name,
            contact_name=payload.contact_name,
            channel=payload.channel,  # type: ignore[arg-type]
            subject_en=payload.subject_en,
            subject_ar=payload.subject_ar,
            body_en=payload.body_en,
            body_ar=payload.body_ar,
            tags=payload.tags,
        )
    except CommunicationStorageUnavailable as exc:
        raise _storage_unavailable(exc) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"draft": entry.to_dict(payload.lang), "lang": payload.lang}


@router.post("/{entry_id}/submit")
async def submit_for_approval(entry_id: str, payload: ApprovalActionRequest) -> dict[str, Any]:
    try:
        result = _get_hub().submit_for_approval(entry_id, payload.actor)
    except CommunicationStorageUnavailable as exc:
        raise _storage_unavailable(exc) from exc
    if not result:
        raise HTTPException(status_code=404, detail="Draft not found")
    return {"entry": result.to_dict("both")}


@router.post("/{entry_id}/approve")
async def approve_draft(entry_id: str, payload: ApprovalActionRequest) -> dict[str, Any]:
    try:
        result = _get_hub().approve_draft(entry_id, payload.actor)
    except CommunicationStorageUnavailable as exc:
        raise _storage_unavailable(exc) from exc
    if not result:
        raise HTTPException(status_code=404, detail="Draft not found")
    return {"entry": result.to_dict("both")}


@router.post("/{entry_id}/reject")
async def reject_draft(entry_id: str, payload: ApprovalActionRequest) -> dict[str, Any]:
    try:
        result = _get_hub().reject_draft(entry_id, payload.reason or "")
    except CommunicationStorageUnavailable as exc:
        raise _storage_unavailable(exc) from exc
    if not result:
        raise HTTPException(status_code=404, detail="Draft not found")
    return {"entry": result.to_dict("both")}


@router.post("/{entry_id}/mark-sent")
async def mark_sent_externally(entry_id: str, payload: ApprovalActionRequest) -> dict[str, Any]:
    try:
        result = _get_hub().mark_sent_externally(entry_id, payload.actor)
    except CommunicationStorageUnavailable as exc:
        raise _storage_unavailable(exc) from exc
    if not result:
        raise HTTPException(status_code=400, detail="Entry not found or not approved")
    return {"entry": result.to_dict("both")}


@router.post("/log-inbound")
async def log_inbound(payload: InboundLogRequest) -> dict[str, Any]:
    try:
        entry = _get_hub().log_inbound(
            contact_id=payload.contact_id,
            company_name=payload.company_name,
            contact_name=payload.contact_name,
            channel=payload.channel,  # type: ignore[arg-type]
            body_en=payload.body_en,
            body_ar=payload.body_ar,
            tags=payload.tags,
        )
    except CommunicationStorageUnavailable as exc:
        raise _storage_unavailable(exc) from exc
    return {"entry": entry.to_dict("both")}


@router.get("/contact/{contact_id}/history")
async def contact_history(
    contact_id: str,
    lang: LanguageCode = Depends(get_lang),
) -> dict[str, Any]:
    try:
        return _get_hub().get_contact_history(contact_id, lang)
    except CommunicationStorageUnavailable as exc:
        raise _storage_unavailable(exc) from exc


@router.get("/pending-approvals")
async def pending_approvals(lang: LanguageCode = Depends(get_lang)) -> dict[str, Any]:
    try:
        return _get_hub().get_pending_approvals(lang)
    except CommunicationStorageUnavailable as exc:
        raise _storage_unavailable(exc) from exc


@router.post("/sequence")
async def create_sequence(payload: SequenceRequest) -> dict[str, Any]:
    try:
        sequence = _get_hub().create_sequence(
            name=payload.name,
            contact_id=payload.contact_id,
            company_name=payload.company_name,
            steps=payload.steps,
        )
    except CommunicationStorageUnavailable as exc:
        raise _storage_unavailable(exc) from exc
    return {"sequence": sequence.to_dict("both")}


@router.post("/sequence/{sequence_id}/advance")
async def advance_sequence(
    sequence_id: str,
    payload: ApprovalActionRequest,
) -> dict[str, Any]:
    try:
        return _get_hub().advance_sequence(sequence_id, payload.actor)
    except CommunicationStorageUnavailable as exc:
        raise _storage_unavailable(exc) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/sequence/{sequence_id}")
async def get_sequence(
    sequence_id: str,
    lang: LanguageCode = Depends(get_lang),
) -> dict[str, Any]:
    try:
        sequence = _get_hub()._load_sequence(sequence_id)
    except CommunicationStorageUnavailable as exc:
        raise _storage_unavailable(exc) from exc
    if sequence is None:
        raise HTTPException(status_code=404, detail="Sequence not found")
    return {"sequence": sequence.to_dict(lang), "lang": lang}


@router.get("/search")
async def search_communications(q: str, limit: int = 20) -> dict[str, Any]:
    try:
        return _get_hub().search_communications(q, limit)
    except CommunicationStorageUnavailable as exc:
        raise _storage_unavailable(exc) from exc


@router.get("/stats")
async def comms_stats() -> dict[str, Any]:
    try:
        return _get_hub().stats()
    except CommunicationStorageUnavailable as exc:
        raise _storage_unavailable(exc) from exc
