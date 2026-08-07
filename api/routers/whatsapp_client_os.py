"""WhatsApp Client OS router — the client-facing, governed WhatsApp surface.

A *business workflow assistant*, never a general-purpose chatbot. Every
endpoint is governed by the Client OS engine, which enforces the doctrine:
no secrets in chat, no cold/blast/scraping/LinkedIn-automation, human approval
for external sends, and human handoff for ambiguity / sensitive data / pricing
/ contracts / complaints.

Endpoints (prefix ``/api/v1/whatsapp-client-os``):
- POST /message                      — main intake (text or button) → governed reply
- POST /assessment/start             — start the readiness scan
- POST /assessment/answer            — answer one axis
- GET  /assessment/{id}/report       — readiness report (markdown + json)
- GET  /sessions                     — list sessions (founder ops)
- GET  /sessions/{id}                — one session
- GET  /action-cards                 — queued action/approval/permission cards
- POST /handoff/human                — force a human handoff with context
- GET  /metrics                      — funnel/conversion metrics
- GET  /permissions/levels           — the L0–L5 permission ladder
- GET  /templates                    — available message template keys
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.whatsapp_client_os import (
    action_card_builder as cards,
)
from auto_client_acquisition.whatsapp_client_os import (
    client_profile_store as store,
)
from auto_client_acquisition.whatsapp_client_os import (
    handoff_router,
    permission_levels,
    templates,
)
from auto_client_acquisition.whatsapp_client_os.engine import (
    ClientOSResponse,
    handle_inbound,
    new_session,
)
from auto_client_acquisition.whatsapp_client_os.metrics import compute_metrics
from auto_client_acquisition.whatsapp_client_os.schemas import InboundMessage

router = APIRouter(prefix="/api/v1/whatsapp-client-os", tags=["whatsapp-client-os"])


# ── Request bodies ───────────────────────────────────────────────────────
class _StartAssessmentBody(BaseModel):
    client_handle: str = Field(..., min_length=1)
    company_name: str = ""
    session_id: str = ""


class _AnswerBody(BaseModel):
    session_id: str = Field(..., min_length=1)
    client_handle: str = Field(..., min_length=1)
    axis: str = Field(..., min_length=1)
    option_id: str = Field(..., min_length=1)


class _HandoffBody(BaseModel):
    session_id: str = Field(..., min_length=1)
    client_handle: str = Field(..., min_length=1)
    reason: str = "explicit_request"
    last_messages: list[str] = Field(default_factory=list)


# ── Helpers ────────────────────────────────────────────────────────────--
def _resolve_session(
    *, session_id: str, client_handle: str, company_name: str = "", locale: str = "ar"
):
    if session_id:
        existing = store.get_session(session_id)
        if existing is not None:
            return existing
    return new_session(client_handle=client_handle, company_name=company_name, locale=locale)


def _serialize(resp: ClientOSResponse) -> dict[str, Any]:
    return {
        "intent": resp.intent,
        "blocked": resp.blocked,
        "message_ar": resp.message_ar,
        "session": resp.session.model_dump(mode="json"),
        "cards": [c.model_dump(mode="json") for c in resp.cards],
        "whatsapp_payloads": [cards.to_whatsapp_payload(c) for c in resp.cards],
        "handoff": resp.handoff.model_dump(mode="json") if resp.handoff else None,
        "assessment": resp.assessment.model_dump(mode="json") if resp.assessment else None,
        "safety_summary": "no_live_send_no_secrets_in_chat",
    }


# ── Endpoints ────────────────────────────────────────────────────────────
@router.post("/message")
def post_message(body: InboundMessage) -> dict[str, Any]:
    """Main intake: classify, guard, transition, and return a governed reply."""
    session = _resolve_session(
        session_id=body.session_id,
        client_handle=body.client_handle,
        company_name=body.company_name,
        locale=body.locale,
    )
    resp = handle_inbound(
        session,
        text=body.text,
        button_id=body.button_id,
        is_complaint=body.is_complaint,
    )
    return _serialize(resp)


@router.post("/assessment/start")
def start_assessment(body: _StartAssessmentBody) -> dict[str, Any]:
    session = _resolve_session(
        session_id=body.session_id, client_handle=body.client_handle, company_name=body.company_name
    )
    resp = handle_inbound(session, button_id="asmt:start")
    return _serialize(resp)


@router.post("/assessment/answer")
def answer_assessment(body: _AnswerBody) -> dict[str, Any]:
    session = store.get_session(body.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session_not_found")
    resp = handle_inbound(session, button_id=f"asmt:{body.axis}:{body.option_id}")
    return _serialize(resp)


@router.get("/assessments")
def list_assessments(limit: int = 100) -> dict[str, Any]:
    items = store.list_assessments(limit=limit)
    return {"count": len(items), "assessments": [a.model_dump(mode="json") for a in items]}


@router.get("/assessment/{assessment_id}/report")
def assessment_report(assessment_id: str) -> dict[str, Any]:
    a = store.get_assessment(assessment_id)
    if a is None:
        raise HTTPException(status_code=404, detail="assessment_not_found")
    score = a.score
    md_lines = [
        f"# تقرير جاهزية — {a.company_name or a.client_handle}",
        "",
        f"- النتيجة الكلية: **{score.overall if score else 0}/100**",
        f"- جاهزية الإيراد: {score.revenue_readiness if score else 0}",
        f"- نضج المتابعة: {score.follow_up_maturity if score else 0}",
        f"- جاهزية الأتمتة: {score.automation_readiness if score else 0}",
        f"- المخاطرة: {score.risk if score else 'medium'}",
        "",
        f"## التوصية: {a.recommended_offer_ar}",
        *[f"- {r}" for r in a.rationale_ar],
        "",
        f"**أول workflow:** {a.first_workflow_ar}",
        f"**الخطوة القادمة:** {a.next_action_ar}",
        "",
        "## الصلاحيات المطلوبة",
        *[f"- {p}" for p in a.required_permissions],
    ]
    return {"assessment": a.model_dump(mode="json"), "report_markdown": "\n".join(md_lines)}


@router.get("/sessions")
def list_sessions(limit: int = 100) -> dict[str, Any]:
    items = store.list_sessions(limit=limit)
    return {"count": len(items), "sessions": [s.model_dump(mode="json") for s in items]}


@router.get("/sessions/{session_id}")
def get_session(session_id: str) -> dict[str, Any]:
    s = store.get_session(session_id)
    if s is None:
        raise HTTPException(status_code=404, detail="session_not_found")
    return s.model_dump(mode="json")


@router.get("/action-cards")
def list_action_cards(limit: int = 100) -> dict[str, Any]:
    items = store.list_action_cards(limit=limit)
    return {"count": len(items), "action_cards": [c.model_dump(mode="json") for c in items]}


@router.post("/handoff/human")
def handoff_human(body: _HandoffBody) -> dict[str, Any]:
    session = store.get_session(body.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session_not_found")
    reason = body.reason if body.reason in handoff_router._REASON_TEXT_AR else "explicit_request"
    handoff = handoff_router.build_handoff(
        session, reason=reason, last_messages=body.last_messages  # type: ignore[arg-type]
    )
    store.record_handoff(handoff)
    return handoff.model_dump(mode="json")


@router.get("/metrics")
def metrics() -> dict[str, Any]:
    return compute_metrics()


@router.get("/permissions/levels")
def permission_ladder() -> dict[str, Any]:
    return {
        "levels": [
            {
                "level": s.level,
                "meaning_ar": s.meaning_ar,
                "example_ar": s.example_ar,
                "risk": s.risk,
                "requires_explanation": s.requires_explanation,
                "requires_explicit_approval": s.requires_explicit_approval,
                "whatsapp_only_allowed": s.whatsapp_only_allowed,
            }
            for s in permission_levels.all_specs()
        ],
        "rules_ar": [
            "الافتراضي L0/L1.",
            "أي L2+ يحتاج شرح وموافقة.",
            "أي L4+ يحتاج approval صريح.",
            "L5 لا يتم عبر واتساب وحده — مسار آمن ومراجعة بشرية.",
        ],
    }


@router.get("/templates")
def list_templates() -> dict[str, Any]:
    return {"keys": templates.available_keys(), "canonical": list(templates.TEMPLATE_KEYS)}
