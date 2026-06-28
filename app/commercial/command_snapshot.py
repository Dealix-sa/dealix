"""Command Room snapshot builder.

Aggregates every artefact of a run into a single :class:`CommandRoomSnapshot`
plus a human-readable Markdown rendering. Highlights the decision queue,
risks and the next 10 actions for the operator.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Mapping

from app.commercial.safety import safe_defaults
from app.commercial.schemas import CommandRoomSnapshot


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _as_dicts(items: list[Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for it in items:
        if hasattr(it, "to_dict"):
            out.append(it.to_dict())
        elif isinstance(it, Mapping):
            out.append(dict(it))
        else:
            out.append({"value": str(it)})
    return out


def _build_decision_queue(
    cards: list[Any], replies: list[Any], proposals: list[Any]
) -> list[dict[str, Any]]:
    queue: list[dict[str, Any]] = []
    for card in cards:
        if _get(card, "owner_decision") == "pending":
            queue.append(
                {
                    "type": "card_review",
                    "ref": _get(card, "card_id"),
                    "ask": "Approve / hold / discard this Growth Card draft",
                    "risk": _get(card, "risk_level", "medium"),
                }
            )
    for reply in replies:
        if _get(reply, "risk_level") == "high":
            queue.append(
                {
                    "type": "reply_escalation",
                    "ref": _get(reply, "reply_id"),
                    "ask": _get(reply, "recommended_action"),
                    "risk": "high",
                }
            )
    for prop in proposals:
        if _get(prop, "approval_required", True):
            queue.append(
                {
                    "type": "proposal_approval",
                    "ref": _get(prop, "proposal_id"),
                    "ask": f"Approve proposal brief ({_get(prop, 'package_name')}) — pricing range only",
                    "risk": "medium",
                }
            )
    return queue


def _build_risks(accounts: list[Any], cards: list[Any]) -> list[dict[str, Any]]:
    risks: list[dict[str, Any]] = []
    for acc in accounts:
        if not _get(acc, "source_url"):
            risks.append(
                {
                    "ref": _get(acc, "account_id"),
                    "risk": "missing_source_url",
                    "impact": "send blocked — unverified lead",
                }
            )
        if str(_get(acc, "contactability_status", "")).lower() in ("opted_out", "blocked"):
            risks.append(
                {
                    "ref": _get(acc, "account_id"),
                    "risk": "not_contactable",
                    "impact": "no outreach permitted",
                }
            )
    for card in cards:
        if _get(card, "risk_level") == "high":
            risks.append(
                {
                    "ref": _get(card, "card_id"),
                    "risk": "high_risk_card",
                    "impact": "manual review required before any action",
                }
            )
    return risks


def _next_actions(
    decision_queue: list[dict[str, Any]], followups: list[Any]
) -> list[str]:
    actions: list[str] = []
    for item in decision_queue[:7]:
        actions.append(f"[{item['type']}] {item['ask']} → {item['ref']}")
    for task in followups[:3]:
        actions.append(
            f"[followup] D{_get(task, 'due_in_days')} {_get(task, 'channel')} → {_get(task, 'card_id')}"
        )
    return actions[:10]


def build_snapshot(
    *,
    accounts: list[Any],
    cards: list[Any],
    replies: list[Any],
    negotiation_drafts: list[Any],
    booking_options: list[Any],
    proposals: list[Any],
    followups: list[Any],
    delivery_handoffs: list[Any],
    generated_at: str | None = None,
) -> CommandRoomSnapshot:
    decision_queue = _build_decision_queue(cards, replies, proposals)
    risks = _build_risks(accounts, cards)
    next_actions = _next_actions(decision_queue, followups)

    summary = {
        "accounts": len(accounts),
        "cards": len(cards),
        "replies": len(replies),
        "negotiation_drafts": len(negotiation_drafts),
        "booking_options": len(booking_options),
        "proposal_briefs": len(proposals),
        "followup_tasks": len(followups),
        "delivery_handoffs": len(delivery_handoffs),
        "decisions_required": len(decision_queue),
        "risks": len(risks),
        "safety_posture": safe_defaults(),
    }

    return CommandRoomSnapshot(
        generated_at=generated_at or datetime.now(UTC).isoformat(),
        summary=summary,
        accounts=_as_dicts(accounts),
        cards=_as_dicts(cards),
        replies=_as_dicts(replies),
        negotiation_drafts=_as_dicts(negotiation_drafts),
        booking_options=_as_dicts(booking_options),
        proposal_briefs=_as_dicts(proposals),
        followup_tasks=_as_dicts(followups),
        delivery_handoffs=_as_dicts(delivery_handoffs),
        risks=risks,
        decision_queue=decision_queue,
        next_actions=next_actions,
    )


def render_markdown(snapshot: CommandRoomSnapshot) -> str:
    s = snapshot.summary
    posture = s.get("safety_posture", {})
    lines: list[str] = []
    lines.append("# Dealix Commercial Growth OS — Command Room")
    lines.append("")
    lines.append(f"_Generated: {snapshot.generated_at}_")
    lines.append("")
    lines.append("## Safety posture (fail-closed)")
    lines.append("")
    lines.append(f"- Outbound mode: **{posture.get('outbound_mode')}**")
    lines.append(f"- External send enabled: **{posture.get('external_send_enabled')}**")
    lines.append(f"- WhatsApp live send: **{posture.get('whatsapp_allow_live_send')}**")
    lines.append(f"- Calendar write: **{posture.get('calendar_write_enabled')}**")
    lines.append(f"- Proposal finalisation: **{posture.get('proposal_finalization_enabled')}**")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Accounts: {s['accounts']}")
    lines.append(f"- Growth Cards: {s['cards']}")
    lines.append(f"- Replies classified: {s['replies']}")
    lines.append(f"- Negotiation drafts: {s['negotiation_drafts']}")
    lines.append(f"- Booking options: {s['booking_options']}")
    lines.append(f"- Proposal briefs: {s['proposal_briefs']}")
    lines.append(f"- Follow-up tasks: {s['followup_tasks']}")
    lines.append(f"- Delivery handoffs: {s['delivery_handoffs']}")
    lines.append(f"- Decisions required: **{s['decisions_required']}**")
    lines.append(f"- Risks: **{s['risks']}**")
    lines.append("")
    lines.append("## Decisions required")
    lines.append("")
    if snapshot.decision_queue:
        for item in snapshot.decision_queue:
            lines.append(f"- **{item['type']}** ({item['risk']}): {item['ask']} — `{item['ref']}`")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Risks")
    lines.append("")
    if snapshot.risks:
        for r in snapshot.risks:
            lines.append(f"- `{r['ref']}` — {r['risk']}: {r['impact']}")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Next 10 actions")
    lines.append("")
    if snapshot.next_actions:
        for i, a in enumerate(snapshot.next_actions, 1):
            lines.append(f"{i}. {a}")
    else:
        lines.append("- None")
    lines.append("")
    lines.append(
        "> Safe-by-default: no external message has been sent, no calendar event "
        "written, and no proposal price finalised. All actions above are drafts "
        "awaiting human approval."
    )
    lines.append("")
    return "\n".join(lines)
