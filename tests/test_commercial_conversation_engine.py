"""The conversation engine advances state correctly and stays draft-only."""

from __future__ import annotations

import pytest

from app.commercial import safety
from app.commercial.conversation import handle_inbound, start_conversation
from app.commercial.schemas import CommercialAccount


@pytest.fixture(autouse=True)
def _clear_flags(monkeypatch):
    for key in safety.SAFE_DEFAULT_FLAGS:
        monkeypatch.delenv(key, raising=False)
    yield


def _account(**kw):
    base = dict(
        account_id="a1",
        company_name="Acme",
        source_url="https://x.sa/c",
        source_type="client_provided",
        verification_status="verified",
        contactability_status="contactable",
        public_email="a@x.sa",
        whatsapp="+966500000000",
        whatsapp_opt_in=True,
        icp_score=80.0,
        pain_hypothesis="lead follow-up",
        recommended_motion="sales_prospecting",
    )
    base.update(kw)
    return CommercialAccount(**base)


def test_start_creates_opener_draft():
    conv, payload = start_conversation(_account(), motion="sales_prospecting", channel="whatsapp")
    assert conv.stage == "qualifying"  # opener advances to qualifying
    assert payload.requires_approval is True
    assert payload.send_status in ("draft", "blocked")
    assert len(conv.turns) == 1  # one outbound draft turn


def test_interested_button_advances_to_booking():
    acc = _account()
    conv, _ = start_conversation(acc, motion="sales_prospecting", channel="whatsapp")
    handle_inbound(conv, "نعم", account=acc, button_intent="interested")
    assert conv.stage == "booking"
    assert conv.last_intent == "interested"


def test_price_objection_moves_to_negotiation():
    acc = _account()
    conv, _ = start_conversation(acc, motion="sales_prospecting", channel="whatsapp")
    handle_inbound(conv, "السعر غالي", account=acc)
    assert conv.stage == "negotiation"


def test_unsubscribe_is_terminal_optout():
    acc = _account()
    conv, _ = start_conversation(acc, motion="sales_prospecting", channel="whatsapp")
    handle_inbound(conv, "unsubscribe please stop", account=acc)
    assert conv.opted_out is True
    assert conv.status == "opted_out"


def test_whatsapp_buttons_capped_and_present():
    acc = _account()
    conv, payload = start_conversation(acc, motion="sales_prospecting", channel="whatsapp")
    assert 0 < len(payload.buttons) <= 3


def test_email_channel_has_no_buttons():
    acc = _account()
    conv, payload = start_conversation(acc, motion="sales_prospecting", channel="email")
    assert payload.kind == "email"
    assert payload.buttons == []


def test_turns_record_reasoning_and_draft_flag():
    acc = _account()
    conv, _ = start_conversation(acc, motion="sales_prospecting", channel="whatsapp")
    outbound = [t for t in conv.turns if t["direction"] == "outbound"][0]
    assert outbound["is_draft"] is True
    assert outbound["reasoning"]
