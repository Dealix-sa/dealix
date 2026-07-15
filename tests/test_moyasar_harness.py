"""Tests for the pure-logic Moyasar harness (payment_ops.moyasar_harness)."""

from __future__ import annotations

import hashlib
import hmac
import json

import pytest

from auto_client_acquisition.payment_ops.moyasar_harness import (
    MAX_AMOUNT_HALALAS,
    MOYASAR_CURRENCY,
    MoyasarHarnessError,
    MoyasarPaymentRequest,
    build_payment_request,
    enforce_test_mode,
    parse_webhook_event,
    verify_webhook_hmac,
)


def test_build_payment_request_converts_sar_to_halalas() -> None:
    req = build_payment_request(
        amount_sar=499.0,
        description="Revenue Intelligence Sprint",
        callback_url="https://api.dealix.me/callback",
    )
    assert isinstance(req, MoyasarPaymentRequest)
    assert req.amount_halalas == 49900
    assert req.currency == MOYASAR_CURRENCY
    payload = req.to_dict()
    assert payload["amount"] == 49900
    assert payload["currency"] == "SAR"


def test_build_payment_request_rejects_zero_amount() -> None:
    with pytest.raises(MoyasarHarnessError):
        build_payment_request(amount_sar=0, description="x", callback_url="u")


def test_build_payment_request_rejects_below_minimum() -> None:
    with pytest.raises(MoyasarHarnessError, match="below Moyasar minimum"):
        build_payment_request(amount_sar=0.5, description="x", callback_url="u")


def test_build_payment_request_rejects_above_safety_cap() -> None:
    too_big = (MAX_AMOUNT_HALALAS + 100) / 100
    with pytest.raises(MoyasarHarnessError, match="above safety cap"):
        build_payment_request(amount_sar=too_big, description="x", callback_url="u")


def test_build_payment_request_rejects_blank_description() -> None:
    with pytest.raises(MoyasarHarnessError, match="description"):
        build_payment_request(amount_sar=499, description="", callback_url="u")


def test_enforce_test_mode_allows_test_key() -> None:
    enforce_test_mode("sk_test_abc123")


def test_enforce_test_mode_rejects_live_key_without_opt_in(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEALIX_MOYASAR_MODE", raising=False)
    with pytest.raises(MoyasarHarnessError, match="DEALIX_MOYASAR_MODE=live"):
        enforce_test_mode("sk_live_xyz")


def test_enforce_test_mode_allows_live_key_with_opt_in(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEALIX_MOYASAR_MODE", "live")
    enforce_test_mode("sk_live_xyz")


def test_enforce_test_mode_rejects_empty_key() -> None:
    with pytest.raises(MoyasarHarnessError, match="empty"):
        enforce_test_mode("")


def test_verify_webhook_hmac_accepts_correct_signature() -> None:
    secret = "shhh"
    body = b'{"type":"payment_paid","data":{"id":"p_1","status":"paid","amount":49900}}'
    sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify_webhook_hmac(secret=secret, body=body, signature_hex=sig) is True


def test_verify_webhook_hmac_rejects_tampered_body() -> None:
    secret = "shhh"
    body = b'{"type":"payment_paid","data":{"id":"p_1","status":"paid","amount":49900}}'
    sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    tampered = body.replace(b"49900", b"100")
    assert verify_webhook_hmac(secret=secret, body=tampered, signature_hex=sig) is False


def test_verify_webhook_hmac_rejects_missing_inputs() -> None:
    assert verify_webhook_hmac(secret="", body=b"x", signature_hex="a") is False
    assert verify_webhook_hmac(secret="x", body=b"x", signature_hex="") is False


def test_parse_webhook_event_paid_event() -> None:
    body = json.dumps(
        {
            "type": "payment_paid",
            "data": {
                "id": "p_abc",
                "status": "paid",
                "amount": 49900,
                "currency": "SAR",
                "metadata": {"engagement_id": "ENG-001"},
            },
        }
    ).encode("utf-8")
    event = parse_webhook_event(body)
    assert event.is_paid is True
    assert event.payment_id == "p_abc"
    assert event.amount_halalas == 49900
    assert event.metadata == {"engagement_id": "ENG-001"}


def test_parse_webhook_event_failed_event_is_not_paid() -> None:
    body = json.dumps(
        {"type": "payment_failed", "data": {"id": "p_x", "status": "failed", "amount": 49900}}
    ).encode("utf-8")
    event = parse_webhook_event(body)
    assert event.is_paid is False


def test_parse_webhook_event_rejects_invalid_json() -> None:
    with pytest.raises(MoyasarHarnessError, match="valid JSON"):
        parse_webhook_event(b"not-json{")


def test_parse_webhook_event_rejects_missing_fields() -> None:
    with pytest.raises(MoyasarHarnessError, match="missing"):
        parse_webhook_event(b'{"type":"payment_paid","data":{}}')


def test_parse_webhook_event_rejects_non_object_body() -> None:
    with pytest.raises(MoyasarHarnessError, match="JSON object"):
        parse_webhook_event(b"[]")
