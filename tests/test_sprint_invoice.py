"""Manual ZATCA invoice for the 7-Day Revenue Proof Sprint."""

from __future__ import annotations

import base64
from datetime import datetime, timezone
from decimal import Decimal

from auto_client_acquisition.payment_ops.sprint_invoice import (
    PAYMENT_MEANS_BANK_TRANSFER,
    SPRINT_LINE_DESCRIPTION,
    SPRINT_PRICE_SAR,
    build_payment_schedule,
    build_sprint_invoice,
    build_sprint_invoice_payload,
    render_invoice_summary,
)
from integrations.zatca import BuyerInfo, SellerInfo, build_sample_invoice


def _seller() -> SellerInfo:
    return SellerInfo(
        name="Dealix",
        vat_number="300000000000003",
        crn_number="1010000000",
        street="King Fahd Road",
        city="Riyadh",
        postal_code="12345",
    )


def _buyer() -> BuyerInfo:
    return BuyerInfo(name="Acme KSA", vat_number="310000000000003")


def test_build_payment_schedule_splits_50_50_exactly() -> None:
    deposit, final = build_payment_schedule(Decimal("573.85"))
    assert deposit.percent == 50
    assert final.percent == 50
    assert deposit.amount_with_vat_sar + final.amount_with_vat_sar == Decimal("573.85")
    assert "عربون" in deposit.label_ar
    assert "Proof Pack" in final.trigger_en


def test_build_sprint_invoice_payload_has_499_line_and_vat() -> None:
    payload = build_sprint_invoice_payload(
        invoice_number="INV-SPRINT-001",
        seller=_seller(),
        buyer=_buyer(),
    )
    assert payload.invoice_type == "standard"
    assert payload.payment_means_code == PAYMENT_MEANS_BANK_TRANSFER
    assert len(payload.line_items) == 1
    assert payload.line_items[0].description == SPRINT_LINE_DESCRIPTION
    assert payload.subtotal == SPRINT_PRICE_SAR
    # 15% VAT on 499.00 = 74.85
    assert payload.vat_total == Decimal("74.85")
    assert payload.grand_total == Decimal("573.85")


def test_build_sprint_invoice_renders_xml_and_qr() -> None:
    issued = datetime(2026, 5, 18, 9, 0, 0, tzinfo=timezone.utc)
    invoice = build_sprint_invoice(
        invoice_number="INV-SPRINT-002",
        seller=_seller(),
        buyer=_buyer(),
        issue_datetime=issued,
    )
    assert invoice.grand_total_sar == Decimal("573.85")
    assert invoice.vat_sar == Decimal("74.85")
    assert "<?xml" in invoice.xml
    assert "Invoice" in invoice.xml
    # QR base64 decodes and carries the 5 ZATCA TLV tags.
    raw = base64.b64decode(invoice.qr_code_b64)
    tags_seen: set[int] = set()
    i = 0
    while i < len(raw) - 1:
        tag = raw[i]
        length = raw[i + 1]
        if i + 2 + length > len(raw):
            break
        tags_seen.add(tag)
        i += 2 + length
    assert {1, 2, 3, 4, 5}.issubset(tags_seen)
    # Schedule sums back to grand total.
    total = sum(m.amount_with_vat_sar for m in invoice.schedule)
    assert total == invoice.grand_total_sar


def test_render_invoice_summary_is_bilingual() -> None:
    invoice = build_sprint_invoice(
        invoice_number="INV-SPRINT-003",
        seller=_seller(),
        buyer=_buyer(),
    )
    summary = render_invoice_summary(invoice)
    # Arabic primary content present.
    assert "رقم الفاتورة" in summary
    assert "تحويل بنكي" in summary
    # English secondary content present.
    assert "Invoice number" in summary
    assert "7-Day Revenue Proof Sprint" in summary
    assert "Payment schedule" in summary


def test_build_sample_invoice_is_zatca_decodable() -> None:
    sample = build_sample_invoice()
    assert sample["qr_base64"]
    assert "<?xml" in sample["xml"]
    raw = base64.b64decode(sample["qr_base64"])
    assert raw[0] == 1  # first TLV tag is seller name
