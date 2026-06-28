"""Email desk — ingest an inbox thread and draft threaded replies.

"Grab the email and do everything" — safely. The desk ingests already-provided
email messages (it does not connect to a live mailbox here), classifies the
latest inbound, and drafts the next reply with a mandatory unsubscribe footer.
Sending stays gated by :func:`app.commercial.safety.can_send_email`.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Mapping

from app.commercial import channels
from app.commercial.engagement_schemas import EmailThread, OutboundPayload
from app.commercial.reasoning import CommercialBrain, HeuristicBrain
from app.commercial.reply_classifier import classify_reply


def _now() -> str:
    return datetime.now(UTC).isoformat()


def ingest_thread(
    account_id: str,
    subject: str,
    messages: list[Mapping[str, Any]],
) -> EmailThread:
    """Build an EmailThread from raw messages (each: {direction, from, body})."""
    thread = EmailThread(
        thread_id=f"thread_{account_id}",
        account_id=account_id,
        subject=subject,
        messages=[dict(m) for m in messages],
        stage="qualifying" if any(m.get("direction") == "inbound" for m in messages) else "opener",
    )
    return thread


def latest_inbound(thread: EmailThread) -> str:
    for msg in reversed(thread.messages):
        if msg.get("direction") == "inbound":
            return str(msg.get("body", ""))
    return ""


def draft_reply(
    thread: EmailThread,
    account: Any,
    *,
    motion: str = "sales_prospecting",
    brain: CommercialBrain | None = None,
    client_rules: Mapping[str, Any] | None = None,
) -> OutboundPayload:
    """Draft the next email reply for a thread (with unsubscribe footer)."""
    brain = brain or HeuristicBrain()
    inbound = latest_inbound(thread)
    intent = classify_reply(inbound, thread.thread_id).reply_type if inbound else ""

    context = {
        "conversation_id": thread.thread_id,
        "account_id": thread.account_id,
        "motion": motion,
        "channel": "email",
        "stage": thread.stage,
        "last_intent": intent,
        "icp_score": _g(account, "icp_score", 0.0),
        "opted_out": str(_g(account, "contactability_status", "")).lower()
        in ("opted_out", "blocked"),
        "company_name": _g(account, "company_name", ""),
        "pain_hypothesis": _g(account, "pain_hypothesis", ""),
        "objection_type": intent,
    }
    rec = brain.recommend_action(context)
    context["recommended_action"] = rec.recommended_action
    context["persuasion_angle"] = rec.persuasion_angle
    draft = brain.draft_reply(context)

    subject = thread.subject or "Dealix — your commercial follow-up"
    if not subject.lower().startswith("re:") and any(
        m.get("direction") == "inbound" for m in thread.messages
    ):
        subject = f"Re: {subject}"

    payload = channels.prepare_email(
        conversation_id=thread.thread_id,
        account_id=thread.account_id,
        draft={"body_ar": draft["ar"], "body_en": draft["en"], "owner_decision": "pending"},
        account=account,
        subject=subject,
        client_rules=client_rules,
    )
    payload.safety.setdefault("recommendation", rec.to_dict())

    # Record the drafted reply on the thread (draft, not sent).
    thread.messages.append(
        {
            "direction": "outbound",
            "from": "dealix",
            "body": payload.body_en,
            "is_draft": True,
            "created_at": _now(),
        }
    )
    return payload


def _g(obj: Any, key: str, default: Any = "") -> Any:
    if isinstance(obj, Mapping):
        return obj.get(key, default)
    return getattr(obj, key, default)
