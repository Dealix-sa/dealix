"""Multi-channel outbound preparation — WhatsApp, email, LinkedIn, phone.

Each adapter turns a drafted reply into the *exact* payload its channel would
need, and attaches the :class:`SafetyDecision` that governs whether it could
ever actually be sent. **No adapter performs any network I/O.** Sending is the
job of a future gated transport; here we only prepare and gate.

Channel rules:
  * WhatsApp — interactive messages, max 3 reply buttons, title <= 20 chars,
    opt-in required, cold WhatsApp forbidden.
  * Email — must carry an unsubscribe/opt-out affordance.
  * LinkedIn — manual only: we produce a copy-paste pack + an operator task.
  * Phone — manual task only.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.commercial import safety
from app.commercial.engagement_schemas import InteractiveButton, OutboundPayload

MAX_WA_BUTTONS = 3
MAX_WA_BUTTON_TITLE = 20


class ChannelError(ValueError):
    pass


def _truncate_title(title: str) -> str:
    title = title.strip()
    return title if len(title) <= MAX_WA_BUTTON_TITLE else title[: MAX_WA_BUTTON_TITLE - 1] + "…"


def normalise_buttons(buttons: list[Any]) -> list[InteractiveButton]:
    """Coerce/validate buttons to <=3 WhatsApp-safe interactive buttons."""
    out: list[InteractiveButton] = []
    for i, b in enumerate(buttons[:MAX_WA_BUTTONS]):
        if isinstance(b, InteractiveButton):
            bid, title, intent = b.id, b.title, b.intent
        elif isinstance(b, Mapping):
            bid = str(b.get("id") or f"btn_{i}")
            title = str(b.get("title") or b.get("label") or f"Option {i+1}")
            intent = str(b.get("intent", ""))
        else:
            bid, title, intent = f"btn_{i}", str(b), ""
        out.append(InteractiveButton(id=bid, title=_truncate_title(title), intent=intent))
    return out


def _base_action(payload_kind_owner_decision: str, draft: Mapping[str, Any]) -> dict[str, Any]:
    """Build the action dict the safety gates expect."""
    return {
        "message_status": draft.get("message_status", "draft"),
        "owner_decision": draft.get("owner_decision", "pending"),
        "text": f"{draft.get('body_ar', '')}\n{draft.get('body_en', '')}",
        "has_unsubscribe": draft.get("has_unsubscribe", False),
    }


def prepare_whatsapp(
    *,
    conversation_id: str,
    account_id: str,
    draft: Mapping[str, Any],
    account: Any,
    buttons: list[Any] | None = None,
    client_rules: Mapping[str, Any] | None = None,
) -> OutboundPayload:
    btns = normalise_buttons(buttons or [])
    action = _base_action("whatsapp", draft)
    decision = safety.can_send_whatsapp(action, account, client_rules)
    return OutboundPayload(
        payload_id=f"wa_{conversation_id}",
        conversation_id=conversation_id,
        account_id=account_id,
        channel="whatsapp",
        kind="interactive_buttons" if btns else "text",
        body_ar=str(draft.get("body_ar", "")),
        body_en=str(draft.get("body_en", "")),
        buttons=[b.to_dict() for b in btns],
        requires_approval=True,
        send_status="draft" if not decision.allowed else "approved",
        safety=decision.to_dict(),
    )


def prepare_email(
    *,
    conversation_id: str,
    account_id: str,
    draft: Mapping[str, Any],
    account: Any,
    subject: str = "",
    client_rules: Mapping[str, Any] | None = None,
) -> OutboundPayload:
    # Email must always carry an unsubscribe affordance.
    unsubscribe = "للإلغاء، ردّ بكلمة (إيقاف) / To unsubscribe, reply STOP."
    body_ar = f"{draft.get('body_ar', '')}\n\n— {unsubscribe}"
    body_en = f"{draft.get('body_en', '')}\n\n— {unsubscribe}"
    action = {
        "message_status": draft.get("message_status", "draft"),
        "owner_decision": draft.get("owner_decision", "pending"),
        "text": f"{body_ar}\n{body_en}",
        "has_unsubscribe": True,
    }
    decision = safety.can_send_email(action, account, client_rules)
    return OutboundPayload(
        payload_id=f"em_{conversation_id}",
        conversation_id=conversation_id,
        account_id=account_id,
        channel="email",
        kind="email",
        subject=subject or "Dealix — a quick idea for your commercial follow-up",
        body_ar=body_ar,
        body_en=body_en,
        headers={"List-Unsubscribe": "<mailto:unsubscribe@dealix.me>"},
        requires_approval=True,
        send_status="draft" if not decision.allowed else "approved",
        safety=decision.to_dict(),
    )


def prepare_linkedin(
    *,
    conversation_id: str,
    account_id: str,
    draft: Mapping[str, Any],
    account: Any,
) -> OutboundPayload:
    """LinkedIn is **manual only** — we never automate sending on LinkedIn."""
    return OutboundPayload(
        payload_id=f"li_{conversation_id}",
        conversation_id=conversation_id,
        account_id=account_id,
        channel="linkedin_manual",
        kind="linkedin_manual",
        body_ar=str(draft.get("body_ar", "")),
        body_en=str(draft.get("body_en", "")),
        requires_approval=True,
        send_status="draft",
        safety={
            "allowed": False,
            "reason": "LinkedIn automation is A3-restricted — manual send only",
            "blocked_by": ["linkedin_automation_forbidden"],
            "audit_level": "standard",
        },
        manual_instructions=(
            "Copy the EN/AR text and send manually from your own LinkedIn account "
            "after a genuine connection. Do not automate."
        ),
    )


def prepare_phone(
    *,
    conversation_id: str,
    account_id: str,
    draft: Mapping[str, Any],
) -> OutboundPayload:
    return OutboundPayload(
        payload_id=f"ph_{conversation_id}",
        conversation_id=conversation_id,
        account_id=account_id,
        channel="phone",
        kind="phone_task",
        body_ar=str(draft.get("body_ar", "")),
        body_en=str(draft.get("body_en", "")),
        requires_approval=True,
        send_status="draft",
        safety={"allowed": False, "reason": "phone is a manual task", "blocked_by": []},
        manual_instructions="Call task for the owner — talking points above.",
    )


def prepare_for_channel(
    channel: str,
    *,
    conversation_id: str,
    account_id: str,
    draft: Mapping[str, Any],
    account: Any,
    buttons: list[Any] | None = None,
    subject: str = "",
    client_rules: Mapping[str, Any] | None = None,
) -> OutboundPayload:
    """Dispatch to the right adapter for ``channel``."""
    if channel == "whatsapp":
        return prepare_whatsapp(
            conversation_id=conversation_id, account_id=account_id, draft=draft,
            account=account, buttons=buttons, client_rules=client_rules,
        )
    if channel == "email":
        return prepare_email(
            conversation_id=conversation_id, account_id=account_id, draft=draft,
            account=account, subject=subject, client_rules=client_rules,
        )
    if channel == "linkedin_manual":
        return prepare_linkedin(
            conversation_id=conversation_id, account_id=account_id, draft=draft, account=account,
        )
    if channel == "phone":
        return prepare_phone(
            conversation_id=conversation_id, account_id=account_id, draft=draft,
        )
    # Unknown channel → safe, blocked text draft.
    return OutboundPayload(
        payload_id=f"x_{conversation_id}", conversation_id=conversation_id,
        account_id=account_id, channel=channel, kind="text",
        body_ar=str(draft.get("body_ar", "")), body_en=str(draft.get("body_en", "")),
        requires_approval=True, send_status="blocked",
        safety={"allowed": False, "reason": f"unknown channel: {channel}", "blocked_by": [channel]},
    )
