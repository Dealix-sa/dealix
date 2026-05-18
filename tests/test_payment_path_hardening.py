"""Coverage for the launch-readiness payment-path hardening changes.

Covers:
  * MoyasarClient.key_mode (B3)
  * payment_ops.find_payments_by_session (C4b helper)
  * DiagnosticIntentBody.payment_method validation (C4a)
  * sprint_runner /run payment guard (C4b)
"""
from __future__ import annotations

import importlib
from unittest.mock import patch

import pytest

from dealix.payments.moyasar import MoyasarClient


# ── B3: MoyasarClient.key_mode ──────────────────────────────────────


def test_key_mode_test_key() -> None:
    assert MoyasarClient(secret_key="sk_test_abc123").key_mode == "test"


def test_key_mode_live_key() -> None:
    assert MoyasarClient(secret_key="sk_live_abc123").key_mode == "live"


def test_key_mode_unknown_when_missing_or_bad_prefix() -> None:
    assert MoyasarClient(secret_key="").key_mode == "unknown"
    assert MoyasarClient(secret_key="garbage").key_mode == "unknown"


# ── C4b: find_payments_by_session ───────────────────────────────────


def test_find_payments_by_session_empty_for_unknown() -> None:
    from auto_client_acquisition.payment_ops import find_payments_by_session

    assert find_payments_by_session("no-such-session-xyz") == []
    assert find_payments_by_session("") == []


def test_find_payments_by_session_returns_linked_record(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    from auto_client_acquisition.payment_ops import orchestrator

    monkeypatch.setattr(orchestrator, "_JSONL_PATH", str(tmp_path / "p.jsonl"))
    orchestrator._INDEX.clear()
    rec = orchestrator.create_invoice_intent(
        customer_handle="acme",
        amount_sar=1500.0,
        method="moyasar_test",
        service_session_id="eng_link_001",
    )
    found = orchestrator.find_payments_by_session("eng_link_001")
    assert len(found) == 1
    assert found[0].payment_id == rec.payment_id
    orchestrator._INDEX.clear()


# ── C4a: DiagnosticIntentBody.payment_method ────────────────────────


def test_diagnostic_body_defaults_to_moyasar_test() -> None:
    diag = importlib.import_module("api.routers.diagnostic")
    body = diag.DiagnosticIntentBody(axes_0_5={})
    assert body.payment_method == "moyasar_test"


def test_diagnostic_body_rejects_invalid_payment_method() -> None:
    diag = importlib.import_module("api.routers.diagnostic")
    with pytest.raises(ValueError):
        diag.DiagnosticIntentBody(axes_0_5={}, payment_method="paypal")


def test_diagnostic_body_accepts_valid_payment_method() -> None:
    diag = importlib.import_module("api.routers.diagnostic")
    body = diag.DiagnosticIntentBody(axes_0_5={}, payment_method="bank_transfer")
    assert body.payment_method == "bank_transfer"


# ── C4b: sprint_runner /run payment guard ───────────────────────────


@pytest.mark.asyncio
async def test_sprint_run_blocked_when_payment_unconfirmed(async_client) -> None:
    """An engagement with a linked, unconfirmed payment cannot run the Sprint."""
    from auto_client_acquisition.full_ops_contracts.schemas import PaymentStateRecord

    pending = PaymentStateRecord(
        payment_id="pay_guard_1",
        customer_handle="acme",
        service_session_id="eng_guard_001",
        amount_sar=1500.0,
        method="moyasar_test",
        status="invoice_intent",
    )
    with patch(
        "auto_client_acquisition.payment_ops.find_payments_by_session",
        return_value=[pending],
    ):
        res = await async_client.post(
            "/api/v1/sprint/run",
            json={"engagement_id": "eng_guard_001", "customer_id": "acme"},
        )
    assert res.status_code == 409
    assert res.json()["detail"]["error"] == "payment_not_confirmed"


@pytest.mark.asyncio
async def test_sprint_run_allowed_when_payment_confirmed(async_client) -> None:
    from auto_client_acquisition.full_ops_contracts.schemas import PaymentStateRecord

    confirmed = PaymentStateRecord(
        payment_id="pay_guard_2",
        customer_handle="acme",
        service_session_id="eng_guard_002",
        amount_sar=1500.0,
        method="moyasar_test",
        status="payment_confirmed",
    )
    with patch(
        "auto_client_acquisition.payment_ops.find_payments_by_session",
        return_value=[confirmed],
    ):
        res = await async_client.post(
            "/api/v1/sprint/run",
            json={"engagement_id": "eng_guard_002", "customer_id": "acme"},
        )
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_sprint_run_unguarded_when_no_payment_linked(async_client) -> None:
    """An engagement with no linked payment runs free (pre-payment diagnostic)."""
    with patch(
        "auto_client_acquisition.payment_ops.find_payments_by_session",
        return_value=[],
    ):
        res = await async_client.post(
            "/api/v1/sprint/run",
            json={"engagement_id": "eng_free_001", "customer_id": "acme"},
        )
    assert res.status_code == 200
