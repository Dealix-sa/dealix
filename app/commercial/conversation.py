"""Conversation engine — the multi-turn state machine.

Drives a single conversation forward: given the current state and an optional
inbound message, it asks the brain for the next best action, advances the
stage, drafts the next reply, and prepares the exact channel payload (draft).

This is channel-agnostic; WhatsApp button loops and email threads are thin
wrappers over this engine. Nothing is sent.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Mapping

from app.commercial import channels
from app.commercial.engagement_schemas import (
    Conversation,
    ConversationTurn,
    InteractiveButton,
    OutboundPayload,
)
from app.commercial.reasoning import CommercialBrain, HeuristicBrain
from app.commercial.reply_classifier import classify_reply

# Stage → the (max 3) interactive buttons we offer next.
_STAGE_BUTTONS: dict[str, list[tuple[str, str, str]]] = {
    "opener": [
        ("btn_yes", "نعم، تواصل", "interested"),
        ("btn_info", "أرسل التفاصيل", "send_details"),
        ("btn_later", "ليس الآن", "not_now"),
    ],
    "qualifying": [
        ("btn_call", "احجز مكالمة", "meeting_request"),
        ("btn_info", "أرسل التفاصيل", "send_details"),
        ("btn_later", "ليس الآن", "not_now"),
    ],
    "value": [
        ("btn_call", "احجز مكالمة", "meeting_request"),
        ("btn_proposal", "أريد مقترحاً", "send_details"),
        ("btn_later", "لاحقاً", "not_now"),
    ],
    "negotiation": [
        ("btn_pilot", "تجربة أصغر", "interested"),
        ("btn_call", "نناقش هاتفياً", "meeting_request"),
        ("btn_later", "ليس الآن", "not_now"),
    ],
    "booking": [
        ("btn_slot1", "الموعد ١", "meeting_request"),
        ("btn_slot2", "الموعد ٢", "meeting_request"),
        ("btn_slot3", "الموعد ٣", "meeting_request"),
    ],
    "proposal": [
        ("btn_accept_review", "راجعت المقترح", "interested"),
        ("btn_questions", "عندي أسئلة", "support_question"),
        ("btn_later", "لاحقاً", "not_now"),
    ],
}

# Stages whose entry is an approval-gated commercial commitment.
APPROVAL_GATED_TRANSITIONS = ("won", "lost", "proposal")


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _buttons_for_stage(stage: str) -> list[InteractiveButton]:
    rows = _STAGE_BUTTONS.get(stage, [])
    return [InteractiveButton(id=i, title=t, intent=intent) for (i, t, intent) in rows]


def start_conversation(
    account: Any,
    *,
    motion: str,
    channel: str,
    brain: CommercialBrain | None = None,
    client_rules: Mapping[str, Any] | None = None,
) -> tuple[Conversation, OutboundPayload]:
    """Open a conversation: prepare the first (opener) draft + payload."""
    brain = brain or HeuristicBrain()
    account_id = _g(account, "account_id")
    conv = Conversation(
        conversation_id=f"conv_{account_id}_{channel}",
        account_id=account_id,
        motion=motion,
        channel=channel,
        stage="opener",
        opt_in=bool(_g(account, "whatsapp_opt_in", False)),
        opted_out=str(_g(account, "contactability_status", "")).lower() in ("opted_out", "blocked"),
    )
    payload = _advance(conv, inbound_text=None, brain=brain, account=account, client_rules=client_rules)
    return conv, payload


def handle_inbound(
    conversation: Conversation,
    inbound_text: str,
    *,
    account: Any,
    brain: CommercialBrain | None = None,
    button_intent: str | None = None,
    client_rules: Mapping[str, Any] | None = None,
) -> OutboundPayload:
    """Process an inbound message/button and prepare the next draft payload."""
    brain = brain or HeuristicBrain()
    # A button press carries an explicit intent; otherwise classify the text.
    if button_intent:
        intent = button_intent
    else:
        intent = classify_reply(inbound_text, conversation.conversation_id).reply_type
    conversation.last_intent = intent

    # Record the inbound turn.
    conversation.turns.append(
        ConversationTurn(
            turn_id=f"t{len(conversation.turns)}",
            direction="inbound",
            channel=conversation.channel,
            text=inbound_text,
            intent=intent,
            stage_before=conversation.stage,
            stage_after=conversation.stage,
            is_draft=False,
            created_at=_now(),
        ).to_dict()
    )
    return _advance(
        conversation, inbound_text=inbound_text, brain=brain, account=account,
        client_rules=client_rules,
    )


def _advance(
    conversation: Conversation,
    *,
    inbound_text: str | None,
    brain: CommercialBrain,
    account: Any,
    client_rules: Mapping[str, Any] | None,
) -> OutboundPayload:
    context = {
        "conversation_id": conversation.conversation_id,
        "account_id": conversation.account_id,
        "motion": conversation.motion,
        "channel": conversation.channel,
        "stage": conversation.stage,
        "last_intent": conversation.last_intent,
        "icp_score": _g(account, "icp_score", 0.0),
        "opted_out": conversation.opted_out,
        "company_name": _g(account, "company_name", ""),
        "pain_hypothesis": _g(account, "pain_hypothesis", ""),
        "objection_type": conversation.last_intent,
    }
    rec = brain.recommend_action(context)
    context["recommended_action"] = rec.recommended_action
    context["persuasion_angle"] = rec.persuasion_angle

    # Terminal opt-out.
    if rec.next_stage == "opted_out":
        conversation.opted_out = True
        conversation.status = "opted_out"

    stage_before = conversation.stage
    next_stage = rec.next_stage or conversation.stage

    draft = brain.draft_reply(context)
    buttons = _buttons_for_stage(next_stage) if conversation.channel == "whatsapp" else []

    payload = channels.prepare_for_channel(
        conversation.channel,
        conversation_id=conversation.conversation_id,
        account_id=conversation.account_id,
        draft={"body_ar": draft["ar"], "body_en": draft["en"], "owner_decision": "pending"},
        account=account,
        buttons=buttons,
        client_rules=client_rules,
    )

    # Approval-gated stage entry stays as a recommendation; we do not flip the
    # conversation into won/lost/proposal without an explicit owner decision.
    if next_stage in APPROVAL_GATED_TRANSITIONS:
        conversation.next_action = (
            f"Approval required to enter stage '{next_stage}' "
            f"(action: {rec.recommended_action})"
        )
    else:
        conversation.stage = next_stage
        conversation.next_action = rec.recommended_action

    conversation.risk_level = rec.risk_level

    # Record the outbound (draft) turn.
    conversation.turns.append(
        ConversationTurn(
            turn_id=f"t{len(conversation.turns)}",
            direction="outbound",
            channel=conversation.channel,
            text=f"{draft['ar']} | {draft['en']}",
            buttons=[b.to_dict() for b in buttons],
            intent=rec.recommended_action,
            stage_before=stage_before,
            stage_after=conversation.stage,
            is_draft=True,
            reasoning=" ".join(rec.rationale),
            created_at=_now(),
        ).to_dict()
    )
    # Stash the recommendation for the caller (command room).
    payload.safety.setdefault("recommendation", rec.to_dict())
    return payload


def _g(obj: Any, key: str, default: Any = "") -> Any:
    if isinstance(obj, Mapping):
        return obj.get(key, default)
    return getattr(obj, key, default)
