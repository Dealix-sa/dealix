"""Approval policy — every external action becomes a pending approval-queue item.

Nothing is ever sent. Each item carries the draft, reason, risk, and the four
founder decision options.
"""

from __future__ import annotations

from typing import Any

from dealix.conversation_engine.channel_adapter import (
    EMAIL,
    WHATSAPP,
    channel_allows_cold,
    channel_requires_approval,
)

DECISION_OPTIONS = ["approve", "revise", "reject", "hold"]


def _risk_for(channel: str, target: dict[str, Any]) -> str:
    band = target.get("band", "cold")
    if channel == WHATSAPP and not channel_allows_cold(WHATSAPP):
        # Cold WhatsApp is forbidden — flag high until warmth is confirmed.
        return "high"
    if band == "hot":
        return "low"
    if band == "warm":
        return "medium"
    return "medium"


def build_approval_items(
    target: dict[str, Any],
    match: dict[str, Any],
    channels_drafts: dict[str, Any],
    start_index: int,
) -> list[dict[str, Any]]:
    """Create approval-queue items for email + whatsapp drafts."""
    items: list[dict[str, Any]] = []
    company = target.get("company", "")
    contact = target.get("contact_name", "")
    offer = match.get("primary_offer", {})
    reason = (
        f"فرصة محتملة (score={target.get('score', 0)}) — مطابقة عرض "
        f"«{offer.get('name_ar', '')}»."
    )

    idx = start_index
    for channel in (EMAIL, WHATSAPP):
        draft = channels_drafts.get(channel, {})
        if channel == EMAIL:
            draft_text = draft.get("short_version", "")
        else:
            draft_text = draft.get("opening_message", "")
        items.append(
            {
                "id": f"APP-{idx:04d}",
                "target_company": company,
                "contact_name": contact,
                "channel": channel,
                "draft": draft_text,
                "reason": reason,
                "risk": _risk_for(channel, target),
                "proof_attached": "proof_pack",
                "decision_options": list(DECISION_OPTIONS),
                "approval_required": channel_requires_approval(channel),
                "status": "pending_founder_approval",
            }
        )
        idx += 1
    return items
