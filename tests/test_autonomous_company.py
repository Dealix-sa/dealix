"""Invariants for the Autonomous Company OS: stage derivation, revenue
recognition, opt-in safety, idempotent ingest, and draft-only rendering."""

from __future__ import annotations

from datetime import date

from dealix.autonomous_company import decision_engine, pipeline, revenue, state
from dealix.autonomous_company.schemas import Deal, DealEvent, DealStage


def _deal(name, events, opted_in=True, value=499):
    return Deal(
        id=name,
        account_name=name,
        opted_in=opted_in,
        value_sar=value,
        events=[DealEvent(event=e, at="2026-07-01") for e in events],
    )


def test_stage_derives_from_evidence():
    d = _deal("a", ["lead_identified", "message_sent_manually", "call_booked"])
    assert pipeline.derive_stage(d) == DealStage.ENGAGED
    d.events.append(DealEvent(event="payment_received", at="2026-07-02"))
    assert pipeline.derive_stage(d) == DealStage.WON


def test_lost_is_terminal():
    d = _deal("a", ["lead_identified", "payment_received", "lost"])
    assert pipeline.derive_stage(d) == DealStage.LOST


def test_revenue_only_on_payment_received():
    unpaid = _deal("u", ["lead_identified", "message_sent_manually"])
    paid = _deal("p", ["lead_identified", "payment_received"], value=1500)
    assert revenue.recognized_revenue([unpaid]) == 0
    assert revenue.recognized_revenue([unpaid, paid]) == 1500


def test_not_opted_in_lead_gets_no_outreach_draft():
    today = date(2026, 7, 8)
    cold = _deal("cold", ["lead_identified"], opted_in=False)
    warm = _deal("warm", ["lead_identified"], opted_in=True)
    decision = decision_engine.decide([cold, warm], today, top_n=10)
    by_id = {r.deal_id: r for r in decision.recommendations}
    assert not by_id["cold"].requires_approval
    assert not by_id["cold"].draft
    assert by_id["warm"].requires_approval
    assert by_id["warm"].draft


def test_won_deal_action_is_internal_not_send():
    today = date(2026, 7, 8)
    paid = _deal("p", ["lead_identified", "payment_received"], value=5000)
    decision = decision_engine.decide([paid], today, top_n=10)
    assert decision.recommendations[0].requires_approval is False


def test_ingest_is_idempotent(tmp_path):
    inbox = tmp_path / "inbox.json"
    inbox.write_text(
        '{"leads": [{"account_name": "Acme Co", "opted_in": true}]}',
        encoding="utf-8",
    )
    today = date(2026, 7, 8)
    deals, added1 = state.ingest_inbox([], today, path=inbox)
    assert added1 == 1
    deals, added2 = state.ingest_inbox(deals, today, path=inbox)
    assert added2 == 0
    assert len(deals) == 1
