"""WhatsApp interactive button loop.

Builds WhatsApp interactive reply-button payloads (max 3 buttons), parses
inbound webhook events (button presses or free text) into intents, and drives
the conversation engine one step at a time.

**No HTTP send happens here.** :class:`GatedWhatsAppSender` exists to define the
future live-send seam, but it refuses unless every safety gate passes — and
even then this build does not wire a real transport.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.commercial import safety
from app.commercial.channels import MAX_WA_BUTTONS, normalise_buttons
from app.commercial.conversation import handle_inbound, start_conversation
from app.commercial.engagement_schemas import Conversation, OutboundPayload
from app.commercial.reasoning import CommercialBrain


def build_interactive_payload(text: str, buttons: list[Any]) -> dict[str, Any]:
    """Return a WhatsApp Cloud API 'interactive' button message body.

    Shape matches WhatsApp's interactive/button schema. Enforces <=3 buttons
    and <=20-char titles via :func:`normalise_buttons`.
    """
    norm = normalise_buttons(buttons)
    if len(norm) > MAX_WA_BUTTONS:  # defensive; normalise already caps
        norm = norm[:MAX_WA_BUTTONS]
    return {
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": text},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": b.id, "title": b.title}}
                    for b in norm
                ]
            },
        },
    }


def parse_webhook(event: Mapping[str, Any]) -> dict[str, Any]:
    """Extract a normalised inbound from a WhatsApp webhook-like event.

    Returns ``{"from": ..., "text": ..., "button_id": ..., "button_intent": ...}``.
    Accepts both a simplified shape and the nested Cloud API shape.
    """
    # Simplified shape.
    if "button_id" in event or "text" in event:
        return {
            "from": event.get("from", ""),
            "text": str(event.get("text", "")),
            "button_id": event.get("button_id"),
            "button_intent": event.get("button_intent"),
        }

    # Nested Cloud API shape: entry[].changes[].value.messages[]
    try:
        msg = event["entry"][0]["changes"][0]["value"]["messages"][0]
    except (KeyError, IndexError, TypeError):
        return {"from": "", "text": "", "button_id": None, "button_intent": None}

    frm = msg.get("from", "")
    if msg.get("type") == "interactive":
        reply = msg.get("interactive", {}).get("button_reply", {})
        return {
            "from": frm,
            "text": reply.get("title", ""),
            "button_id": reply.get("id"),
            "button_intent": None,  # caller maps id→intent via button metadata
        }
    return {"from": frm, "text": msg.get("text", {}).get("body", ""), "button_id": None,
            "button_intent": None}


def start(
    account: Any,
    *,
    motion: str = "sales_prospecting",
    brain: CommercialBrain | None = None,
    client_rules: Mapping[str, Any] | None = None,
) -> tuple[Conversation, OutboundPayload]:
    """Open a WhatsApp conversation (opener draft with buttons)."""
    return start_conversation(
        account, motion=motion, channel="whatsapp", brain=brain, client_rules=client_rules
    )


def step(
    conversation: Conversation,
    event: Mapping[str, Any],
    *,
    account: Any,
    brain: CommercialBrain | None = None,
    client_rules: Mapping[str, Any] | None = None,
) -> OutboundPayload:
    """Process one inbound webhook event and prepare the next draft payload."""
    parsed = parse_webhook(event)
    # Resolve button intent: prefer explicit intent, else look up by id in the
    # last outbound turn's buttons.
    button_intent = parsed.get("button_intent")
    if not button_intent and parsed.get("button_id"):
        button_intent = _intent_for_button(conversation, parsed["button_id"])
    return handle_inbound(
        conversation,
        inbound_text=parsed.get("text", ""),
        account=account,
        brain=brain,
        button_intent=button_intent,
        client_rules=client_rules,
    )


def _intent_for_button(conversation: Conversation, button_id: str) -> str | None:
    for turn in reversed(conversation.turns):
        if turn.get("direction") == "outbound":
            for b in turn.get("buttons", []):
                if b.get("id") == button_id:
                    return b.get("intent") or None
    return None


class GatedWhatsAppSender:
    """Future live-send seam. Refuses unless all safety gates pass.

    This build intentionally does NOT attach a real HTTP transport. The method
    returns the decision and the would-be payload; it never transmits.
    """

    def send(
        self,
        payload: OutboundPayload,
        account: Any,
        client_rules: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        action = {
            "message_status": "approved" if payload.send_status == "approved" else "draft",
            "owner_decision": "send",
            "text": f"{payload.body_ar}\n{payload.body_en}",
            "has_unsubscribe": True,
        }
        decision = safety.can_send_whatsapp(action, account, client_rules)
        return {
            "transmitted": False,  # never true in this build
            "allowed": decision.allowed,
            "reason": decision.reason,
            "blocked_by": decision.blocked_by,
            "payload_id": payload.payload_id,
            "note": "Live transport is intentionally not wired. Draft-only.",
        }
