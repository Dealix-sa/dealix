"""WhatsApp Client OS router.

Thin I/O layer over ``auto_client_acquisition.whatsapp_client_os``. The brain
runs a controlled pipeline; this router never performs a live external send or
charge, never echoes the raw WhatsApp id, and returns a ``governance_decision``
on every response.

Endpoints (self-prefix ``/api/v1/whatsapp-client``):
- POST ``/message``        — process one inbound message through the brain.
- POST ``/scan``           — score a full 10-axis readiness scan.
- POST ``/triage``         — quick 4-question "recommend for me" read.
- GET  ``/scan/questions`` — scan + triage question definitions.
- GET  ``/flows``          — the controlled flow map.
- GET  ``/metrics``        — founder-facing aggregation (read-only).
- GET/POST ``/webhook``    — Meta verification + inbound processing (no send).
"""

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.governance_os import GovernanceDecision
from auto_client_acquisition.whatsapp_client_os import brain, metrics
from auto_client_acquisition.whatsapp_client_os import session_store as store
from auto_client_acquisition.whatsapp_client_os.action_cards import recommendation_card
from auto_client_acquisition.whatsapp_client_os.flows import flows_as_data
from auto_client_acquisition.whatsapp_client_os.readiness_scan import (
    QUICK_TRIAGE_QUESTIONS,
    READINESS_AXES,
    quick_triage,
    score_assessment,
)

router = APIRouter(prefix="/api/v1/whatsapp-client", tags=["whatsapp-client"])


class MessageBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    wa_id: str = Field(..., min_length=3, max_length=64)
    text: str = Field("", max_length=4000)
    company: str = Field("", max_length=120)


class ScanBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answers: dict[str, str] = Field(default_factory=dict)
    company: str = Field("", max_length=120)
    session_id: str = Field("", max_length=64)


class TriageBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answers: dict[str, str] = Field(default_factory=dict)


@router.post("/message")
async def post_message(body: MessageBody) -> dict[str, Any]:
    resp = brain.handle_message(wa_id=body.wa_id, text=body.text, company=body.company)
    return resp.to_dict()


@router.post("/scan")
async def post_scan(body: ScanBody) -> dict[str, Any]:
    assessment = score_assessment(
        answers=body.answers, company=body.company, session_id=body.session_id
    )
    store.save_assessment(assessment)
    card = recommendation_card(body.session_id, assessment)
    store.save_card(card)
    return {
        "assessment": assessment.to_dict(),
        "recommendation_card": card.to_dict(),
        "governance_decision": GovernanceDecision.ALLOW.value,
    }


@router.post("/triage")
async def post_triage(body: TriageBody) -> dict[str, Any]:
    assessment = quick_triage(body.answers)
    return {
        "assessment": assessment.to_dict(),
        "governance_decision": GovernanceDecision.ALLOW.value,
    }


@router.get("/scan/questions")
async def get_scan_questions() -> dict[str, Any]:
    axes = [
        {
            "id": a.id,
            "title_ar": a.title_ar,
            "title_en": a.title_en,
            "question_ar": a.question_ar,
            "options": [
                {"value": o.value, "label_ar": o.label_ar, "score": o.score} for o in a.options
            ],
        }
        for a in READINESS_AXES
    ]
    return {
        "axes": axes,
        "quick_triage": list(QUICK_TRIAGE_QUESTIONS),
        "governance_decision": GovernanceDecision.ALLOW.value,
    }


@router.get("/flows")
async def get_flows() -> dict[str, Any]:
    return {
        "flows": flows_as_data(),
        "governance_decision": GovernanceDecision.ALLOW.value,
    }


@router.get("/metrics")
async def get_metrics() -> dict[str, Any]:
    return metrics.compute_metrics()


@router.get("/webhook")
async def verify_webhook(
    mode: str = Query("", alias="hub.mode"),
    token: str = Query("", alias="hub.verify_token"),
    challenge: str = Query("", alias="hub.challenge"),
) -> Response:
    """Meta webhook verification handshake (echo challenge when token matches)."""
    expected = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
    if mode == "subscribe" and expected and token == expected:
        return Response(content=challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="verification_failed")


@router.post("/webhook")
async def receive_webhook(request: Request) -> dict[str, Any]:
    """Process an inbound WhatsApp message.

    Returns the computed draft reply / card. It does NOT send anything — the
    operator surface or portal performs the (manual) send after review.
    """
    payload = await request.json()
    wa_id, text = _extract_message(payload)
    if not wa_id:
        return {"processed": False, "governance_decision": GovernanceDecision.ALLOW.value}
    resp = brain.handle_message(wa_id=wa_id, text=text)
    return {"processed": True, "sent": False, **resp.to_dict()}


def _extract_message(payload: dict[str, Any]) -> tuple[str, str]:
    """Best-effort extraction of (wa_id, text) from a Cloud API payload."""
    try:
        change = payload["entry"][0]["changes"][0]["value"]
        msg = change["messages"][0]
        wa_id = str(msg.get("from", ""))
        text = str(msg.get("text", {}).get("body", "")) if msg.get("type") == "text" else ""
        return wa_id, text
    except (KeyError, IndexError, TypeError):
        return "", ""


__all__ = ["router"]
