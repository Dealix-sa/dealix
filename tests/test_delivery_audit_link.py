"""WS3 — payment to delivery audit link tests.

Asserts the invoice.paid -> delivery -> proof.pack_delivered chain is
recorded to the JSONL ledger and readable back, joined by correlation_id.
Also asserts kickoff_delivery wires the first two links automatically.
"""
from __future__ import annotations

import importlib

import pytest

from auto_client_acquisition.payment_ops import delivery_audit_link as dal


@pytest.fixture()
def audit_path(tmp_path, monkeypatch):
    """Point the audit ledger at an isolated tmp file."""
    p = tmp_path / "audit.jsonl"
    monkeypatch.setenv("DEALIX_DELIVERY_AUDIT_PATH", str(p))
    return p


def test_record_invoice_paid_writes_event(audit_path) -> None:
    ev = dal.record_invoice_paid(
        customer_id="acme-pilot",
        payment_id="pay_abc123",
        amount_sar=499.0,
        correlation_id="pay_abc123",
        evidence_reference="moyasar:txn_1:wh_1",
    )
    assert ev.event_type == "invoice.paid"
    assert ev.customer_id == "acme-pilot"
    assert audit_path.exists()
    chain = dal.read_chain("pay_abc123")
    assert len(chain) == 1
    assert chain[0]["payload"]["amount_sar"] == 499.0


def test_record_delivery_started_links_causation(audit_path) -> None:
    paid = dal.record_invoice_paid(
        customer_id="acme-pilot",
        payment_id="pay_x",
        amount_sar=499.0,
        correlation_id="pay_x",
    )
    started = dal.record_delivery_started(
        customer_id="acme-pilot",
        payment_id="pay_x",
        delivery_kickoff_id="dk_001",
        correlation_id="pay_x",
        causation_event_id=paid.event_id,
    )
    assert started.event_type == "proof.pack_requested"
    assert started.causation_id == paid.event_id


def test_full_chain_is_complete_and_ordered(audit_path) -> None:
    cid = "pay_full"
    paid = dal.record_invoice_paid(
        customer_id="acme",
        payment_id="pay_full",
        amount_sar=499.0,
        correlation_id=cid,
    )
    started = dal.record_delivery_started(
        customer_id="acme",
        payment_id="pay_full",
        delivery_kickoff_id="dk_full",
        correlation_id=cid,
        causation_event_id=paid.event_id,
    )
    dal.record_proof_pack_delivered(
        customer_id="acme",
        payment_id="pay_full",
        delivery_kickoff_id="dk_full",
        correlation_id=cid,
        proof_score=72,
        proof_tier="L3",
        causation_event_id=started.event_id,
    )
    assert dal.chain_is_complete(cid) is True
    chain = dal.read_chain(cid)
    assert [r["event_type"] for r in chain] == [
        "invoice.paid",
        "proof.pack_requested",
        "proof.pack_delivered",
    ]
    assert chain[-1]["payload"]["proof_tier"] == "L3"


def test_incomplete_chain_reports_false(audit_path) -> None:
    dal.record_invoice_paid(
        customer_id="acme",
        payment_id="pay_partial",
        amount_sar=499.0,
        correlation_id="pay_partial",
    )
    assert dal.chain_is_complete("pay_partial") is False


def test_read_chain_unknown_correlation_returns_empty(audit_path) -> None:
    assert dal.read_chain("does-not-exist") == []
    assert dal.chain_is_complete("does-not-exist") is False


def test_correlation_id_required(audit_path) -> None:
    with pytest.raises(ValueError):
        dal.record_invoice_paid(
            customer_id="acme",
            payment_id="pay_1",
            amount_sar=499.0,
            correlation_id="",
        )


def test_kickoff_delivery_records_audit_link(audit_path, monkeypatch) -> None:
    """kickoff_delivery must wire the first two links of the chain."""
    monkeypatch.setattr(
        "auto_client_acquisition.payment_ops.orchestrator._persist",
        lambda rec: None,
    )
    from auto_client_acquisition.payment_ops import orchestrator

    rec = orchestrator.create_invoice_intent(
        customer_handle="kickoff-pilot",
        amount_sar=499.0,
        method="bank_transfer",
    )
    orchestrator._INDEX[rec.payment_id] = rec
    orchestrator.upload_manual_evidence(
        payment_id=rec.payment_id, evidence_reference="bank_ref_2026"
    )
    orchestrator.confirm_payment(payment_id=rec.payment_id, confirmed_by="founder")
    _, status = orchestrator.kickoff_delivery(payment_id=rec.payment_id)
    assert status == "delivery_kicked_off"
    chain = dal.read_chain(rec.payment_id)
    types = {r["event_type"] for r in chain}
    assert "invoice.paid" in types
    assert "proof.pack_requested" in types
