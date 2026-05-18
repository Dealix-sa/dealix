"""Payment->delivery audit-link ledger tests — Workstream B (B3).

Asserts the append-only ledger writers record the payment->delivery handoff
and Proof Pack finalization, and that ledger I/O failure never blocks the
payment state machine or the deliverable lifecycle.
"""

from __future__ import annotations

import importlib

import pytest

from auto_client_acquisition.deliverables.delivery_ledger import (
    record_delivery_kickoff,
    record_proof_pack_finalized,
)


@pytest.fixture()
def ledgers_dir(tmp_path, monkeypatch):
    """Point the ledger writers at an isolated temp ledgers dir."""
    monkeypatch.setenv("DEALIX_LEDGERS_DIR", str(tmp_path))
    return tmp_path


def test_record_delivery_kickoff_appends_dated_row(ledgers_dir) -> None:
    ok = record_delivery_kickoff(
        payment_id="pay_abc",
        delivery_kickoff_id="dk_123",
        customer_handle="acme",
        amount_sar=499.0,
    )
    assert ok is True
    text = (ledgers_dir / "DELIVERY_LEDGER.md").read_text(encoding="utf-8")
    assert "Delivery kickoff log (append-only)" in text
    assert "dk_123" in text
    assert "pay_abc" in text
    assert "acme" in text
    assert "499 SAR" in text


def test_record_delivery_kickoff_is_append_only(ledgers_dir) -> None:
    record_delivery_kickoff(
        payment_id="pay_1", delivery_kickoff_id="dk_1", customer_handle="c1"
    )
    record_delivery_kickoff(
        payment_id="pay_2", delivery_kickoff_id="dk_2", customer_handle="c2"
    )
    text = (ledgers_dir / "DELIVERY_LEDGER.md").read_text(encoding="utf-8")
    assert "dk_1" in text and "dk_2" in text
    # Header written once only.
    assert text.count("Delivery kickoff log (append-only)") == 1


def test_record_proof_pack_finalized_appends_row(ledgers_dir) -> None:
    ok = record_proof_pack_finalized(
        deliverable_id="deliv_x",
        customer_handle="acme",
        proof_event_id="proof_evt_1",
        score=88,
        tier="case_candidate",
    )
    assert ok is True
    text = (ledgers_dir / "PROOF_LEDGER.md").read_text(encoding="utf-8")
    assert "Proof Pack finalized log (append-only)" in text
    assert "deliv_x" in text
    assert "proof_evt_1" in text
    assert "88/100" in text


def test_ledger_failure_returns_false_not_raise(tmp_path, monkeypatch) -> None:
    """A non-writable ledgers dir degrades to False — never raises."""
    bad = tmp_path / "nope" / "missing"
    monkeypatch.setenv("DEALIX_LEDGERS_DIR", str(bad / "deeper" / "x"))
    # Point at a path whose parent is a file, forcing an OSError on append.
    blocker = tmp_path / "blocker"
    blocker.write_text("x", encoding="utf-8")
    monkeypatch.setenv("DEALIX_LEDGERS_DIR", str(blocker))
    ok = record_delivery_kickoff(
        payment_id="p", delivery_kickoff_id="dk", customer_handle="c"
    )
    assert ok is False


def test_kickoff_delivery_writes_to_ledger(tmp_path, monkeypatch) -> None:
    """The audit link: kickoff_delivery records to DELIVERY_LEDGER.md."""
    monkeypatch.setenv("DEALIX_LEDGERS_DIR", str(tmp_path))
    orch = importlib.import_module(
        "auto_client_acquisition.payment_ops.orchestrator"
    )
    rec = orch.create_invoice_intent(
        customer_handle="ledger-test",
        amount_sar=499.0,
        method="bank_transfer",
    )
    orch.upload_manual_evidence(
        payment_id=rec.payment_id, evidence_reference="BANK-99999"
    )
    orch.confirm_payment(payment_id=rec.payment_id, confirmed_by="founder")
    kicked, reason = orch.kickoff_delivery(payment_id=rec.payment_id)
    assert kicked is not None
    assert reason == "delivery_kicked_off"
    text = (tmp_path / "DELIVERY_LEDGER.md").read_text(encoding="utf-8")
    assert kicked.delivery_kickoff_id in text
    assert rec.payment_id in text
