"""WhatsApp Client OS — doctrine (non-negotiables) enforcement.

These tests are the load-bearing guardrails: secrets never enter the chat,
unsafe channel requests are blocked, and the only possible outbound mode is
``approved_manual`` (never live send).
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.whatsapp_client_os import whatsapp_policy_guard as guard


@pytest.mark.parametrize(
    "text",
    [
        "my key is sk-abcdefghijklmnopqrstuvwxyz0123",
        "ANTHROPIC sk-ant-abcdefghijklmnop1234567890",
        "AKIA1234567890ABCD is the aws key",
        "hubspot pat-na1-1234abcd-5678efgh-90ab",
        "api_key = supersecretvalue12345",
        "كلمة السر: hunter2hunter2",
    ],
)
def test_secrets_are_detected_and_refused(text: str) -> None:
    scan = guard.scan_for_secrets(text)
    assert scan.found is True
    assert scan.kinds  # at least one kind
    assert "الرابط الآمن" in scan.secure_portal_alternative_ar
    # The matched value must never be echoed back.
    assert "sk-" not in scan.refusal_ar
    assert "pat-" not in scan.refusal_ar


def test_clean_text_is_not_flagged_as_secret() -> None:
    assert guard.scan_for_secrets("نبغى نحسّن المتابعة مع العملاء").found is False
    assert guard.scan_for_secrets("").found is False


@pytest.mark.parametrize(
    ("text", "reason"),
    [
        ("ابغى أرسل واتساب بارد لكل الأرقام", "cold_whatsapp"),
        ("send a broadcast blast to everyone", "broadcast_blast"),
        ("استخدم قائمة مشتراة", "purchased_list"),
        ("اعمل scraping للأرقام", "scraping"),
        ("ابغى linkedin automation", "linkedin_automation"),
    ],
)
def test_unsafe_requests_are_blocked(text: str, reason: str) -> None:
    scan = guard.scan_for_unsafe_request(text)
    assert scan.blocked is True
    assert reason in scan.reasons
    assert scan.safe_alternative_ar


def test_guard_inbound_maps_doctrine_violations() -> None:
    res = guard.guard_inbound("اعمل scraping وأرسل واتساب بارد للجميع")
    assert res.allowed is False
    assert res.unsafe_scan.blocked is True
    assert "no_scraping" in res.doctrine_violations
    assert "no_cold_whatsapp" in res.doctrine_violations


def test_outbound_can_never_be_live_send() -> None:
    # Even with all consent conditions, the best outcome is approved_manual.
    decision = guard.evaluate_outbound(
        consent_record_exists=True,
        approved_template_or_24h_window=True,
        human_approved=True,
    )
    assert decision.action_mode in {"approved_manual", "blocked"}
    assert decision.action_mode != "live_send"


def test_outbound_missing_conditions_is_blocked() -> None:
    decision = guard.evaluate_outbound()
    assert decision.allowed is False
    assert decision.action_mode == "blocked"
