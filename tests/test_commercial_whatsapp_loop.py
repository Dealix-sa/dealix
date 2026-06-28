"""WhatsApp interactive button loop: <=3 buttons, parse webhooks, never send."""

from __future__ import annotations

import pytest

from app.commercial import safety
from app.commercial import whatsapp_loop as wl
from app.commercial.engagement_schemas import InteractiveButton
from app.commercial.schemas import CommercialAccount


@pytest.fixture(autouse=True)
def _clear_flags(monkeypatch):
    for key in safety.SAFE_DEFAULT_FLAGS:
        monkeypatch.delenv(key, raising=False)
    yield


def _account(opt_in=True):
    return CommercialAccount(
        account_id="a1",
        company_name="Acme",
        source_url="https://x.sa/c",
        source_type="client_provided",
        verification_status="verified",
        contactability_status="contactable",
        whatsapp="+966500000000",
        whatsapp_opt_in=opt_in,
        icp_score=80.0,
        pain_hypothesis="lead follow-up",
    )


def test_interactive_payload_caps_three_buttons():
    buttons = [
        InteractiveButton(id=f"b{i}", title=f"Option number {i} is long enough", intent="x")
        for i in range(5)
    ]
    body = wl.build_interactive_payload("hello", buttons)
    btns = body["interactive"]["action"]["buttons"]
    assert len(btns) == 3
    for b in btns:
        assert len(b["reply"]["title"]) <= 20
        assert b["type"] == "reply"


def test_parse_simplified_button_event():
    parsed = wl.parse_webhook({"from": "+9665", "button_id": "btn_yes", "button_intent": "interested"})
    assert parsed["button_id"] == "btn_yes"
    assert parsed["button_intent"] == "interested"


def test_parse_nested_cloud_api_button_event():
    event = {
        "entry": [
            {"changes": [{"value": {"messages": [
                {"from": "+9665", "type": "interactive",
                 "interactive": {"button_reply": {"id": "btn_yes", "title": "Yes"}}}
            ]}}]}
        ]
    }
    parsed = wl.parse_webhook(event)
    assert parsed["button_id"] == "btn_yes"
    assert parsed["from"] == "+9665"


def test_full_loop_opener_then_button_press():
    acc = _account()
    conv, opener = wl.start(acc)
    assert opener.channel == "whatsapp"
    assert len(opener.buttons) <= 3
    nxt = wl.step(conv, {"button_id": "btn_yes", "button_intent": "interested"}, account=acc)
    assert conv.stage == "booking"
    assert nxt.requires_approval is True


def test_button_intent_resolved_from_prior_turn():
    acc = _account()
    conv, opener = wl.start(acc)
    # Use an id present in the opener's buttons, without passing an explicit intent.
    bid = opener.buttons[0]["id"]
    wl.step(conv, {"button_id": bid}, account=acc)
    assert conv.last_intent  # an intent was resolved from the button metadata


def test_gated_sender_never_transmits():
    acc = _account()
    conv, opener = wl.start(acc)
    out = wl.GatedWhatsAppSender().send(opener, acc)
    assert out["transmitted"] is False
    assert out["allowed"] is False  # draft-only env


def test_cold_whatsapp_blocked_no_optin():
    acc = _account(opt_in=False)
    conv, opener = wl.start(acc)
    out = wl.GatedWhatsAppSender().send(opener, acc)
    assert out["allowed"] is False
    assert any("opt-in" in b for b in out["blocked_by"])
