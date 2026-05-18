"""Manual (non-Moyasar) bank-transfer payment recording."""

from __future__ import annotations

from decimal import Decimal

import pytest

from auto_client_acquisition.payment_ops.manual_payment import (
    MANUAL_PAYMENT_TIER,
    MANUAL_PROVIDER,
    ManualPaymentError,
    build_manual_payment_record,
    record_manual_payment,
    sar_to_halalas,
)
from auto_client_acquisition.value_os.value_ledger import clear_for_test, list_events


@pytest.fixture(autouse=True)
def _isolated_ledger(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    monkeypatch.setenv("VALUE_LEDGER_BACKEND", "jsonl")
    clear_for_test()
    yield
    clear_for_test()


def test_sar_to_halalas_rounds_correctly() -> None:
    assert sar_to_halalas("499.00") == 49900
    assert sar_to_halalas(286.93) == 28693
    assert sar_to_halalas(Decimal("0.005")) == 1


def test_build_manual_payment_record_uses_bank_transfer_provider() -> None:
    rec = build_manual_payment_record(
        customer_id="cust_001",
        bank_reference="DEALIX-PILOT-01-TRF",
        amount_sar="573.85",
    )
    assert rec.provider == MANUAL_PROVIDER
    assert rec.provider != "moyasar"
    assert rec.amount_halalas == 57385
    assert rec.status == "paid"
    assert rec.raw_event["no_live_charge"] is True


def test_build_manual_payment_record_rejects_short_reference() -> None:
    with pytest.raises(ManualPaymentError):
        build_manual_payment_record(
            customer_id="cust_001",
            bank_reference="ab",
            amount_sar="499",
        )


def test_build_manual_payment_record_rejects_non_positive_amount() -> None:
    with pytest.raises(ManualPaymentError):
        build_manual_payment_record(
            customer_id="cust_001",
            bank_reference="DEALIX-PILOT-01-TRF",
            amount_sar="0",
        )


def test_record_manual_payment_writes_verified_value_event() -> None:
    persisted: list[object] = []
    result = record_manual_payment(
        customer_id="cust_002",
        bank_reference="DEALIX-PILOT-02-TRF",
        amount_sar="286.93",
        confirmed_by="founder",
        persist=persisted.append,
    )
    assert result.provider == MANUAL_PROVIDER
    assert result.amount_halalas == 28693
    assert len(persisted) == 1
    assert result.value_event.tier == MANUAL_PAYMENT_TIER == "verified"
    assert result.value_event.source_ref == "DEALIX-PILOT-02-TRF"

    events = list_events(customer_id="cust_002")
    assert len(events) == 1
    assert events[0].tier == "verified"
    assert events[0].kind == "manual_payment_received"


def test_record_manual_payment_requires_confirmed_by() -> None:
    with pytest.raises(ManualPaymentError):
        record_manual_payment(
            customer_id="cust_003",
            bank_reference="DEALIX-PILOT-03-TRF",
            amount_sar="499",
            confirmed_by="",
        )
