"""Saudi Opportunity Command Room HTTP surface — draft-first, approval-guarded.

Admin-key protected. Mirrors the style of revenue_ops_autopilot: no endpoint
performs a live send. The only send-adjacent action (``mark-sent``) merely
records that a human manually sent an already-approved draft.
"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from api.security.api_key import require_admin_key
from dealix.opportunity_graph.collectors.csv_importer import _parse_csv_text
from dealix.opportunity_graph.pipeline import (
    decide_draft,
    mark_sent,
    run_daily_targeting,
    score_and_segment,
)
from dealix.opportunity_graph.reports import build_daily_report, build_weekly_proof_pack
from dealix.opportunity_graph.store import get_store

router = APIRouter(
    prefix="/api/v1/opportunity-command",
    dependencies=[Depends(require_admin_key)],
    tags=["opportunity-command-room"],
)


@router.get("/today")
def today() -> dict[str, Any]:
    """Draft-only daily command report as structured JSON."""
    report = build_daily_report(store=get_store())
    return report.model_dump(mode="json")


@router.get("/companies")
def list_companies(
    segment: Annotated[str | None, Query()] = None,
    min_score: Annotated[int, Query(ge=0)] = 0,
) -> dict[str, Any]:
    companies = get_store().load_companies()
    rows = [
        c.model_dump(mode="json")
        for c in companies
        if c.total_score >= min_score and (segment is None or c.segment == segment)
    ]
    rows.sort(key=lambda r: r["total_score"], reverse=True)
    return {"count": len(rows), "companies": rows}


@router.post("/import")
def import_companies(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Import companies from a CSV string (authorized, founder-provided only)."""
    csv_text = str(payload.get("csv") or "")
    if not csv_text.strip():
        raise HTTPException(status_code=400, detail="Provide a non-empty 'csv' field.")
    companies = _parse_csv_text(csv_text)
    scored = [score_and_segment(c) for c in companies]
    get_store().upsert_companies(scored)
    return {"imported": len(scored), "note": "Scored and stored. Draft-only; nothing sent."}


@router.post("/score")
def score_cycle(payload: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """Run a full draft-only targeting cycle over the seed + stored companies."""
    limit = int(payload.get("limit", 50))
    draft_top = int(payload.get("draft_top", 20))
    summary = run_daily_targeting(store=get_store(), limit=limit, draft_top=draft_top)
    return summary


@router.get("/drafts")
def list_drafts(status: Annotated[str | None, Query()] = None) -> dict[str, Any]:
    drafts = get_store().load_drafts()
    rows = [
        d.model_dump(mode="json")
        for d in drafts
        if status is None or d.approval_status == status
    ]
    return {"count": len(rows), "drafts": rows}


@router.post("/draft/{draft_id}/approve")
def approve_draft(draft_id: str, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    actor = str(payload.get("actor") or "").strip()
    if not actor:
        raise HTTPException(status_code=400, detail="'actor' (human approver) is required.")
    try:
        draft = decide_draft(draft_id, "approve", actor=actor, note=str(payload.get("note", "")))
    except KeyError:
        raise HTTPException(status_code=404, detail="Draft not found.")
    return draft.model_dump(mode="json")


@router.post("/draft/{draft_id}/reject")
def reject_draft(draft_id: str, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    actor = str(payload.get("actor") or "").strip()
    if not actor:
        raise HTTPException(status_code=400, detail="'actor' is required.")
    decision = str(payload.get("decision", "reject"))
    if decision not in ("reject", "revise"):
        raise HTTPException(status_code=400, detail="decision must be 'reject' or 'revise'.")
    try:
        draft = decide_draft(draft_id, decision, actor=actor, note=str(payload.get("note", "")))
    except KeyError:
        raise HTTPException(status_code=404, detail="Draft not found.")
    return draft.model_dump(mode="json")


@router.post("/draft/{draft_id}/mark-sent")
def mark_draft_sent(draft_id: str, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Record a MANUAL human send of an approved draft. Does not send anything."""
    human_sender = str(payload.get("human_sender") or "").strip()
    if not human_sender:
        raise HTTPException(status_code=400, detail="'human_sender' is required.")
    try:
        draft = mark_sent(draft_id, human_sender=human_sender)
    except KeyError:
        raise HTTPException(status_code=404, detail="Draft not found.")
    except PermissionError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return draft.model_dump(mode="json")


@router.get("/proof-pack")
def proof_pack(client_id: Annotated[str, Query()] = "dealix_internal") -> dict[str, Any]:
    pack = build_weekly_proof_pack(store=get_store(), client_id=client_id)
    return pack.model_dump(mode="json")
