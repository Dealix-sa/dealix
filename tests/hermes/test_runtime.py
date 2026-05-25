"""Hermes runtime pipeline — gates, approvals, trust failures."""

from __future__ import annotations

from dealix.hermes.contracts import (
    Actor,
    ActorKind,
    ContextPacket,
    OutputKind,
)
from dealix.hermes.control_plane import HermesRuntime
from dealix.hermes.control_plane.approval_gate import ApprovalStatus
from dealix.hermes.control_plane.runtime import DraftBundle


def _public_actor() -> Actor:
    return Actor(actor_id="anon_1", kind=ActorKind.PUBLIC)


def _founder_actor() -> Actor:
    return Actor(actor_id="founder_1", kind=ActorKind.FOUNDER)


def _ctx(actor: Actor, intent: str) -> ContextPacket:
    return ContextPacket(
        actor=actor,
        intent=intent,
        declared_output_kind=OutputKind.ACTION,
    )


def test_public_actor_external_intent_is_denied_by_authorization() -> None:
    runtime = HermesRuntime()
    ctx = _ctx(_public_actor(), "external.send.email")
    outcome = runtime.run(context=ctx, intent="external.send.email")
    assert outcome.response.success is False
    assert outcome.response.error is not None
    assert outcome.response.error["code"] == "denied"


def test_founder_external_email_with_clean_draft_holds_for_approval() -> None:
    runtime = HermesRuntime()
    ctx = _ctx(_founder_actor(), "external.send.email")
    draft = DraftBundle(
        text="مرحبًا، نود حجز اجتماع لمناقشة الفرصة.",
        prices_sar=[2500],
    )
    outcome = runtime.run(
        context=ctx, intent="external.send.email", draft=draft
    )
    assert outcome.response.success is True
    assert outcome.response.risk["approval_required"] is True
    assert outcome.approval_ticket is not None
    assert outcome.approval_ticket.status == ApprovalStatus.PENDING


def test_founder_draft_with_arabic_100_percent_overclaim_fails_trust() -> None:
    runtime = HermesRuntime()
    ctx = _ctx(_founder_actor(), "external.send.email")
    draft = DraftBundle(
        text="نضمن لك نتائج 100% بدون مخاطر — العرض حصري لك.",
    )
    outcome = runtime.run(
        context=ctx, intent="external.send.email", draft=draft
    )
    assert outcome.response.success is False
    assert outcome.response.error is not None
    assert "trust" in (outcome.response.error.get("message") or "")


def test_decide_approve_marks_ticket_as_approved() -> None:
    runtime = HermesRuntime()
    ctx = _ctx(_founder_actor(), "external.send.email")
    draft = DraftBundle(text="اجتماع تعريفي قصير الأسبوع القادم.")
    outcome = runtime.run(
        context=ctx, intent="external.send.email", draft=draft
    )
    assert outcome.approval_ticket is not None
    decided = runtime.approval.decide(
        outcome.approval_ticket.ticket_id,
        decided_by="founder_1",
        approve=True,
        note="ok to send",
    )
    assert decided.status == ApprovalStatus.APPROVED
    assert decided.decided_by == "founder_1"
    assert decided.decision_note == "ok to send"
