"""WhatsApp Client OS — the brain (orchestration pipeline).

The brain is NOT a free LLM. It is a controlled pipeline:

    normalize -> identify session -> classify intent -> load state
    -> secret guard (route integrations to the secure portal)
    -> human-handoff check -> choose allowed next action / build card
    -> outbound policy guard -> audit log (redacted)

It never performs a live external send or charge, never asks for secrets in
text, and always carries a ``governance_decision``.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from auto_client_acquisition.friction_log.sanitizer import sanitize_notes
from auto_client_acquisition.governance_os import GovernanceDecision
from auto_client_acquisition.whatsapp_client_os import action_cards as cards
from auto_client_acquisition.whatsapp_client_os import session_store as store
from auto_client_acquisition.whatsapp_client_os import templates as tpl
from auto_client_acquisition.whatsapp_client_os.flows import flow_for_intent
from auto_client_acquisition.whatsapp_client_os.human_handoff import (
    build_handoff_brief,
    should_handoff,
)
from auto_client_acquisition.whatsapp_client_os.intent_router import classify_intent
from auto_client_acquisition.whatsapp_client_os.permission_os import secret_guard
from auto_client_acquisition.whatsapp_client_os.policy_guard import guard_outbound
from auto_client_acquisition.whatsapp_client_os.readiness_scan import READINESS_AXES
from auto_client_acquisition.whatsapp_client_os.schemas import (
    ActionCard,
    ClientSession,
    Intent,
    MessageEvent,
    hash_wa_id,
)
from auto_client_acquisition.whatsapp_client_os.support_triage import triage


@dataclass(frozen=True, slots=True)
class BrainResponse:
    session_id: str
    intent: str
    flow: str
    confidence: float
    reply_ar: str
    reply_en: str
    governance_decision: str
    card: dict[str, Any] | None = None
    handoff_brief: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "intent": self.intent,
            "flow": self.flow,
            "confidence": self.confidence,
            "reply_ar": self.reply_ar,
            "reply_en": self.reply_en,
            "governance_decision": self.governance_decision,
            "card": self.card,
            "handoff_brief": self.handoff_brief,
        }


def _scan_first_question() -> tuple[str, str]:
    axis = READINESS_AXES[0]
    opts = " / ".join(o.label_ar for o in axis.options)
    ar = f"{tpl.t('scan_intro', 'ar')}\n{axis.question_ar}\n[{opts}]"
    en = f"{tpl.t('scan_intro', 'en')}\n{axis.title_en}"
    return ar, en


def _route(intent: Intent, session: ClientSession, text: str) -> tuple[str, str, ActionCard | None]:
    """Map an intent to (reply_ar, reply_en, optional card)."""
    sid = session.session_id
    if intent == Intent.WELCOME:
        return tpl.t("welcome", "ar"), tpl.t("welcome", "en"), None
    if intent == Intent.START_SCAN:
        ar, en = _scan_first_question()
        return ar, en, None
    if intent == Intent.RECOMMEND_ME:
        return tpl.t("recommend_intro", "ar"), tpl.t("recommend_intro", "en"), None
    if intent == Intent.VIEW_SERVICES:
        return tpl.t("view_services_intro", "ar"), tpl.t("view_services_intro", "en"), None
    if intent == Intent.BUILD_FOLLOWUP:
        return tpl.t("followup_sources", "ar"), tpl.t("followup_sources", "en"), None
    if intent == Intent.REVIEW_DRAFT:
        return tpl.t("draft_review_prompt", "ar"), tpl.t("draft_review_prompt", "en"), None
    if intent == Intent.REVIEW_PROPOSAL:
        return tpl.t("view_services_intro", "ar"), tpl.t("view_services_intro", "en"), None
    if intent == Intent.GIVE_PERMISSION:
        card = cards.permission_card(sid)
        return card.body_ar, card.body_en, card
    if intent == Intent.START_PAYMENT:
        card = cards.payment_handoff_card(sid, offer_id="")
        return card.body_ar, card.body_en, card
    if intent == Intent.PROOF_PACK:
        card = cards.proof_pack_card(sid, summary_ar="حزمة الإثبات جاهزة للعرض في البوابة.")
        return card.body_ar, card.body_en, card
    if intent == Intent.RENEWAL:
        card = cards.renewal_card(
            sid, offer_id="", value_summary_ar="ملخص القيمة الملاحظة حتى الآن."
        )
        return card.body_ar, card.body_en, card
    if intent == Intent.REQUEST_SUPPORT:
        result = triage(text)
        card = cards.support_escalation_card(
            sid, category=result.category, needs_human=result.needs_human
        )
        return card.body_ar, card.body_en, card
    return tpl.t("unknown_fallback", "ar"), tpl.t("unknown_fallback", "en"), None


def handle_message(
    *,
    wa_id: str,
    text: str,
    company: str = "",
    persist: bool = True,
) -> BrainResponse:
    """Process one inbound WhatsApp message through the controlled pipeline."""
    wa_hash = hash_wa_id(wa_id)
    session = store.latest_session_for(wa_hash) if persist else None
    is_first = session is None or session.turn_count == 0
    if session is None:
        session = ClientSession(wa_id_hash=wa_hash, company=company)

    redacted_in = sanitize_notes(text)
    sg = secret_guard(text)
    intent, confidence = classify_intent(text, is_first_turn=is_first)
    low_conf = intent == Intent.UNKNOWN and confidence < 0.4
    handoff = should_handoff(text, turn_count=session.turn_count, low_confidence=low_conf)

    card: ActionCard | None = None
    handoff_brief: dict[str, Any] | None = None

    if intent == Intent.BLOCKED_UNSAFE:
        reply_ar = tpl.t("blocked_unsafe", "ar")
        reply_en = tpl.t("blocked_unsafe", "en")
        decision = GovernanceDecision.BLOCK.value
        flow = session.current_flow
    elif sg.contains_secret:
        card = cards.permission_card(session.session_id)
        reply_ar = f"{sg.reason_ar}\n{card.body_ar}"
        reply_en = f"{sg.reason_en}\n{card.body_en}"
        decision = GovernanceDecision.REQUIRE_APPROVAL.value
        flow = flow_for_intent(Intent.GIVE_PERMISSION)
    elif handoff.needed or intent == Intent.REQUEST_HUMAN:
        reasons = handoff.reasons or ("explicit_request",)
        reply_ar = tpl.t("human_handoff", "ar")
        reply_en = tpl.t("human_handoff", "en")
        handoff_brief = build_handoff_brief(
            session_id=session.session_id,
            company=session.company,
            reasons=reasons,
            last_text_redacted=redacted_in,
        )
        decision = GovernanceDecision.ESCALATE.value
        flow = flow_for_intent(Intent.REQUEST_SUPPORT)
    else:
        reply_ar, reply_en, card = _route(intent, session, text)
        flow = flow_for_intent(intent)
        decision = (
            card.governance_decision if card else guard_outbound(reply_ar).governance_decision
        )

    # Outbound guard backstop — never emit blocked text.
    if card is None and decision == GovernanceDecision.ALLOW.value:
        guard = guard_outbound(reply_ar)
        if not guard.allowed:
            reply_ar = tpl.t("unknown_fallback", "ar")
            reply_en = tpl.t("unknown_fallback", "en")
            decision = guard.governance_decision

    if persist:
        updated = replace(
            session,
            company=company or session.company,
            current_flow=flow,
            last_intent=intent.value,
            turn_count=session.turn_count + 1,
            handoff_open=session.handoff_open or handoff_brief is not None,
        )
        store.save_session(updated)
        store.append_message(
            MessageEvent(
                session_id=session.session_id,
                direction="inbound",
                intent=intent.value,
                text_redacted=redacted_in,
            )
        )
        if card is not None:
            store.save_card(card)
        store.append_message(
            MessageEvent(
                session_id=session.session_id,
                direction="outbound",
                intent=intent.value,
                text_redacted=sanitize_notes(reply_ar),
                card_id=card.card_id if card else "",
            )
        )

    return BrainResponse(
        session_id=session.session_id,
        intent=intent.value,
        flow=flow,
        confidence=confidence,
        reply_ar=reply_ar,
        reply_en=reply_en,
        governance_decision=decision,
        card=card.to_dict() if card else None,
        handoff_brief=handoff_brief,
    )


__all__ = ["BrainResponse", "handle_message"]
