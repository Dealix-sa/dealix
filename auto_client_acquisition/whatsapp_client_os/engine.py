"""Orchestrator engine for the WhatsApp Client OS — the governed "brain".

Pipeline (deterministic; the LLM only ever drafts copy, never decides):

    inbound → classify intent → policy guard → handoff check
            → state transition → build card(s) → persist → response

Hard rules enforced here:
- a blocked (secrets / unsafe) message NEVER advances state and NEVER stores
  the offending value;
- ambiguity / sensitive data / pricing / contracts / complaints / repeated
  unknown → human handoff with a context packet;
- every recommendation card carries a catalog id + evidence level.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from auto_client_acquisition.whatsapp_client_os import (
    action_card_builder as cards,
)
from auto_client_acquisition.whatsapp_client_os import (
    assessment as asmt,
)
from auto_client_acquisition.whatsapp_client_os import (
    client_profile_store as store,
)
from auto_client_acquisition.whatsapp_client_os import (
    conversation_state as fsm,
)
from auto_client_acquisition.whatsapp_client_os import (
    handoff_router,
    templates,
)
from auto_client_acquisition.whatsapp_client_os.intent_router import classify
from auto_client_acquisition.whatsapp_client_os.schemas import (
    ClientAssessment,
    ClientCard,
    ClientIntent,
    HandoffRequest,
    IntentResult,
    WhatsAppSession,
)


@dataclass(slots=True)
class ClientOSResponse:
    intent: ClientIntent
    session: WhatsAppSession
    cards: list[ClientCard] = field(default_factory=list)
    message_ar: str = ""
    handoff: HandoffRequest | None = None
    assessment: ClientAssessment | None = None
    blocked: bool = False


def new_session(
    *, client_handle: str, company_name: str = "", locale: str = "ar"
) -> WhatsAppSession:
    return WhatsAppSession(
        session_id=f"wa_{uuid.uuid4().hex[:12]}",
        client_handle=client_handle,
        company_name=company_name,
        locale=locale,  # type: ignore[arg-type]
        stage="new",
    )


def _answers_from_meta(session: WhatsAppSession) -> list[dict[str, str]]:
    raw = session.meta.get("assessment_answers")
    return list(raw) if isinstance(raw, list) else []


def _start_assessment(session: WhatsAppSession) -> ClientOSResponse:
    session.meta["assessment_answers"] = []
    first = asmt.AXIS_ORDER[0]
    spec = asmt.axis_spec(first)
    _, total = asmt.progress([])
    card = cards.assessment_question_card(spec, step=1, total=total)  # type: ignore[arg-type]
    updated = fsm.advance(session, "assessment_start")
    return ClientOSResponse(
        intent="assessment_start",
        session=updated,
        cards=[card],
        message_ar=templates.render("assessment_start", step=1, total=total),
    )


def _handle_assessment_answer(session: WhatsAppSession, ir: IntentResult) -> ClientOSResponse:
    # button id form: asmt:<axis>:<option_id>
    parts = ir.raw_text.split(":")
    answered = _answers_from_meta(session)
    if len(parts) == 3 and parts[0] == "asmt":
        axis, option_id = parts[1], parts[2]
        if not any(a.get("axis") == axis for a in answered):
            answered.append({"axis": axis, "option_id": option_id})
            session.meta["assessment_answers"] = answered

    answered_axes = [a["axis"] for a in answered]
    nxt = asmt.next_axis(answered_axes)
    if nxt is not None:
        spec = asmt.axis_spec(nxt)
        done, total = asmt.progress(answered_axes)
        card = cards.assessment_question_card(spec, step=done + 1, total=total)  # type: ignore[arg-type]
        updated = fsm.advance(session, "assessment_answer", assessment_complete=False)
        return ClientOSResponse(
            intent="assessment_answer",
            session=updated,
            cards=[card],
            message_ar=templates.render("assessment_start", step=done + 1, total=total),
        )

    # Complete → build + persist assessment, then recommend.
    answer_objs = [asmt.make_answer(a["axis"], a["option_id"]) for a in answered]  # type: ignore[arg-type]
    assessment = asmt.build_assessment(
        client_handle=session.client_handle,
        answers=answer_objs,
        company_name=session.company_name,
    )
    store.save_assessment(assessment)
    session.assessment_id = assessment.assessment_id
    updated = fsm.advance(session, "assessment_answer", assessment_complete=True)
    # assessment_complete → recommendation
    updated = fsm.advance(updated, "unknown")  # assessment_complete → recommendation default
    rec_card = cards.recommendation_card(assessment)
    store.queue_action_card(rec_card)
    return ClientOSResponse(
        intent="assessment_answer",
        session=updated,
        cards=[rec_card],
        assessment=assessment,
        message_ar=templates.render(
            "assessment_result",
            overall=assessment.score.overall if assessment.score else 0,
            offer_name_ar=assessment.recommended_offer_ar,
            next_action_ar=assessment.next_action_ar,
        ),
    )


def _maybe_handoff(
    session: WhatsAppSession,
    ir: IntentResult,
    *,
    last_messages: list[str] | None,
    is_complaint: bool,
) -> ClientOSResponse | None:
    reason = handoff_router.detect_reason(
        intent=ir.intent,
        stage=session.stage,
        is_complaint=is_complaint,
        unknown_streak=int(session.meta.get("unknown_streak", 0)),
    )
    if reason is None:
        return None
    handoff = handoff_router.build_handoff(session, reason=reason, last_messages=last_messages)
    store.record_handoff(handoff)
    updated = fsm.advance(session, "human_handoff")
    return ClientOSResponse(
        intent="human_handoff",
        session=updated,
        message_ar="حوّلتك لشخص من فريق Dealix مع ملخّص محادثتك. بنرجع لك سريعًا.",
        handoff=handoff,
    )


def handle_inbound(
    session: WhatsAppSession,
    *,
    text: str = "",
    button_id: str = "",
    last_messages: list[str] | None = None,
    is_complaint: bool = False,
) -> ClientOSResponse:
    """Process one inbound message and return the governed response."""
    ir = classify(text=text, button_id=button_id)

    # 1) Blocked — never advance, never store the value.
    if ir.intent == "blocked_unsafe":
        if "secrets_in_chat" in ir.matched:
            card = cards.secrets_refusal_card()
            handoff = handoff_router.build_handoff(
                session, reason="secrets_attempt", last_messages=last_messages
            )
            store.record_handoff(handoff)
            store.queue_action_card(card)
            store.save_session(session)  # stage unchanged
            return ClientOSResponse(
                intent="blocked_unsafe",
                session=session,
                cards=[card],
                handoff=handoff,
                blocked=True,
                message_ar=card.body_ar,
            )
        card = cards.unsafe_refusal_card(", ".join(ir.matched))
        store.queue_action_card(card)
        store.save_session(session)
        return ClientOSResponse(
            intent="blocked_unsafe",
            session=session,
            cards=[card],
            blocked=True,
            message_ar=card.body_ar,
        )

    # 2) Human handoff triggers.
    handoff_resp = _maybe_handoff(
        session, ir, last_messages=last_messages, is_complaint=is_complaint
    )
    if handoff_resp is not None:
        store.save_session(handoff_resp.session)
        return handoff_resp

    # 3) Intent-specific flows.
    if ir.intent in {"welcome"} or (session.stage == "new" and ir.intent == "unknown"):
        updated = fsm.advance(session, "welcome")
        resp = ClientOSResponse(
            intent="welcome",
            session=updated,
            cards=[cards.welcome_menu()],
            message_ar=templates.render("welcome"),
        )
    elif ir.intent == "not_sure":
        # «ما أعرف» → start the scan (lowers friction)
        resp = _start_assessment(session)
    elif ir.intent in {"diagnose", "assessment_start"}:
        resp = _start_assessment(session)
    elif ir.intent == "assessment_answer":
        resp = _handle_assessment_answer(session, ir)
    elif ir.intent == "connect_tools":
        from auto_client_acquisition.whatsapp_client_os.permission_guard import (
            build_permission_request,
        )

        req = build_permission_request(
            level="L2",
            system="CRM",
            scope="read contacts",
            purpose_ar="قراءة leads فقط",
            needs_secret=True,
        )
        updated = fsm.advance(session, "connect_tools")
        resp = ClientOSResponse(
            intent="connect_tools",
            session=updated,
            cards=[cards.permission_card(req)],
            message_ar=templates.render(
                "permission_request",
                system=req.system,
                purpose_ar=req.purpose_ar,
                risk=req.risk,
                duration_days=req.duration_days,
            ),
        )
    elif ir.intent in {"request_proposal", "review_report", "campaign_followup", "book_call"}:
        updated = fsm.advance(session, ir.intent)
        offer_ar = ""
        if session.assessment_id:
            a = store.get_assessment(session.assessment_id)
            offer_ar = a.recommended_offer_ar if a else ""
        card = cards.approval_card(
            draft_text_ar="جهّزنا لك المسوّدة — تحتاج موافقتك قبل أي إرسال.",
            catalog_ref=offer_ar,
        )
        resp = ClientOSResponse(
            intent=ir.intent,
            session=updated,
            cards=[card],
            message_ar=templates.render("proposal_ready", offer_name_ar=offer_ar or "—"),
        )
    elif ir.intent == "support":
        updated = fsm.advance(session, "support")
        resp = ClientOSResponse(
            intent="support",
            session=updated,
            cards=[cards.support_menu()],
            message_ar=templates.render("support_escalation"),
        )
    else:
        # Unknown → re-show menu, increment streak (handoff after repeats).
        session.meta["unknown_streak"] = int(session.meta.get("unknown_streak", 0)) + 1
        updated = fsm.advance(session, "unknown")
        resp = ClientOSResponse(
            intent="unknown",
            session=updated,
            cards=[cards.welcome_menu()],
            message_ar="ما فهمت تمامًا — اختر من القائمة أو «ما أعرف — اقترح علي».",
        )

    # reset unknown streak on a recognized intent
    if resp.intent != "unknown":
        resp.session.meta["unknown_streak"] = 0
    store.save_session(resp.session)
    return resp


__all__ = ["ClientOSResponse", "handle_inbound", "new_session"]
