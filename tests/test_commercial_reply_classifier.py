"""Reply classifier maps inbound text to controlled reply types (AR + EN)."""

from __future__ import annotations

import pytest

from app.commercial import reply_classifier


@pytest.mark.parametrize(
    "text,expected",
    [
        ("This is interesting, tell me more", "interested"),
        ("Can we schedule a call/demo?", "meeting_request"),
        ("It's too expensive, any discount?", "price_objection"),
        ("Not now, maybe next quarter", "not_now"),
        ("Not interested, no thanks", "no_interest"),
        ("Please unsubscribe me, stop", "unsubscribe"),
        ("We want a contract and signed agreement", "contract_request"),
        ("Interested in a partnership", "partnership_interest"),
        ("غير مهتم لا شكرا", "no_interest"),
        ("السعر غالي على ميزانيتنا", "price_objection"),
        ("ايقاف لا ترسل لي", "unsubscribe"),
    ],
)
def test_classification(text, expected):
    res = reply_classifier.classify_reply(text, card_id="c1")
    assert res.reply_type == expected


def test_unsubscribe_is_high_risk():
    res = reply_classifier.classify_reply("unsubscribe please", "c1")
    assert res.risk_level == "high"
    assert "opt-out" in res.recommended_action.lower()


def test_contract_request_escalates():
    res = reply_classifier.classify_reply("send the contract to sign", "c1")
    assert res.reply_type == "contract_request"
    assert res.risk_level == "high"
    assert "escalate" in res.recommended_action.lower()


def test_unknown_falls_through():
    res = reply_classifier.classify_reply("zxqv random noise", "c1")
    assert res.reply_type == "unknown"
