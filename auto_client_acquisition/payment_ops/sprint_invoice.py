"""Manual ZATCA-compliant invoice for the 7-Day Revenue Proof Sprint.

Builds a bilingual (Arabic primary, English secondary) ZATCA Phase 2
standard tax invoice for the fixed-price Sprint engagement and the
50/50 payment schedule:

  - 50% deposit on engagement acceptance
  - 50% on Proof Pack delivery

This module is the manual invoicing path. It does NOT charge any card
and does NOT call Moyasar. The founder collects payment by bank
transfer and confirms it via payment_ops.manual_payment.

It reuses integrations/zatca.py (TLVEncoder, ZATCAXMLBuilder,
InvoiceGenerator, the dataclasses) without modifying it.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal

from integrations.zatca import (
    BuyerInfo,
    InvoiceGenerator,
    LineItem,
    SellerInfo,
    ZATCAInvoicePayload,
)

SPRINT_PRICE_SAR: Decimal = Decimal("499.00")
SPRINT_LINE_DESCRIPTION_AR: str = "سبرنت إثبات الإيراد خلال 7 أيام"
SPRINT_LINE_DESCRIPTION_EN: str = "7-Day Revenue Proof Sprint"
# Bilingual description: Arabic primary, English secondary.
SPRINT_LINE_DESCRIPTION: str = (
    f"{SPRINT_LINE_DESCRIPTION_AR} / {SPRINT_LINE_DESCRIPTION_EN}"
)

# 30 = bank transfer per ZATCA UN/ECE 4461 payment means codes.
PAYMENT_MEANS_BANK_TRANSFER: int = 30


@dataclass(frozen=True)
class PaymentMilestone:
    """One leg of the 50/50 payment schedule."""

    label_ar: str
    label_en: str
    trigger_ar: str
    trigger_en: str
    percent: int
    amount_with_vat_sar: Decimal


@dataclass(frozen=True)
class SprintInvoice:
    """Result of building a Sprint invoice.

    Holds both the rendered ZATCA artefacts (XML, base64, QR) and the
    bilingual 50/50 payment schedule the founder sends to the customer.
    """

    invoice_number: str
    issue_datetime: datetime
    subtotal_sar: Decimal
    vat_sar: Decimal
    grand_total_sar: Decimal
    xml: str
    xml_b64: str
    qr_code_b64: str
    schedule: tuple[PaymentMilestone, PaymentMilestone]


def _q2(value: Decimal) -> Decimal:
    """Quantize a Decimal to 2 places (halalas precision)."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def build_payment_schedule(grand_total_with_vat_sar: Decimal) -> tuple[PaymentMilestone, PaymentMilestone]:
    """Build the 50/50 payment schedule for a Sprint engagement.

    The first milestone is the deposit due on acceptance, the second is
    due on Proof Pack delivery. The two amounts always sum exactly to
    the grand total (any rounding remainder lands on the final leg).
    """
    deposit = _q2(grand_total_with_vat_sar * Decimal("0.5"))
    final = _q2(grand_total_with_vat_sar - deposit)
    return (
        PaymentMilestone(
            label_ar="الدفعة الأولى — عربون",
            label_en="First payment — deposit",
            trigger_ar="عند قبول الاتفاقية",
            trigger_en="On engagement acceptance",
            percent=50,
            amount_with_vat_sar=deposit,
        ),
        PaymentMilestone(
            label_ar="الدفعة الثانية — رصيد",
            label_en="Second payment — balance",
            trigger_ar="عند تسليم حزمة الإثبات",
            trigger_en="On Proof Pack delivery",
            percent=50,
            amount_with_vat_sar=final,
        ),
    )


def build_sprint_invoice_payload(
    *,
    invoice_number: str,
    seller: SellerInfo,
    buyer: BuyerInfo,
    issue_datetime: datetime | None = None,
    previous_invoice_hash: str | None = None,
) -> ZATCAInvoicePayload:
    """Build the ZATCAInvoicePayload for one Sprint invoice.

    The single line item is the fixed-price Sprint at 499 SAR with the
    standard 15% VAT category. A bilingual note records the 50/50
    payment schedule for the customer.
    """
    line = LineItem(
        description=SPRINT_LINE_DESCRIPTION,
        quantity=Decimal("1"),
        unit_price_sar=SPRINT_PRICE_SAR,
        vat_category_code="S",
    )
    note = (
        "جدول السداد: 50٪ عربون عند قبول الاتفاقية و50٪ عند تسليم حزمة الإثبات. "
        "Payment schedule: 50% deposit on acceptance, 50% on Proof Pack delivery. "
        "السداد عبر تحويل بنكي. Payment by bank transfer."
    )
    return ZATCAInvoicePayload(
        invoice_type="standard",
        seller=seller,
        buyer=buyer,
        line_items=[line],
        invoice_number=invoice_number,
        invoice_series="DEALIX01",
        issue_datetime=issue_datetime,
        previous_invoice_hash=previous_invoice_hash,
        notes=note,
        payment_means_code=PAYMENT_MEANS_BANK_TRANSFER,
    )


def build_sprint_invoice(
    *,
    invoice_number: str,
    seller: SellerInfo,
    buyer: BuyerInfo,
    issue_datetime: datetime | None = None,
    previous_invoice_hash: str | None = None,
) -> SprintInvoice:
    """Generate a complete manual ZATCA invoice for the Sprint.

    Returns the rendered UBL 2.1 XML, its base64 form, the TLV QR code
    and the bilingual 50/50 payment schedule. No card is charged and no
    external API is contacted.
    """
    payload = build_sprint_invoice_payload(
        invoice_number=invoice_number,
        seller=seller,
        buyer=buyer,
        issue_datetime=issue_datetime,
        previous_invoice_hash=previous_invoice_hash,
    )
    xml, xml_b64, qr_code_b64 = InvoiceGenerator().generate(payload)
    schedule = build_payment_schedule(payload.grand_total)
    return SprintInvoice(
        invoice_number=invoice_number,
        issue_datetime=payload.issue_datetime or datetime.now(timezone.utc),
        subtotal_sar=_q2(payload.subtotal),
        vat_sar=_q2(payload.vat_total),
        grand_total_sar=_q2(payload.grand_total),
        xml=xml,
        xml_b64=xml_b64,
        qr_code_b64=qr_code_b64,
        schedule=schedule,
    )


def render_invoice_summary(invoice: SprintInvoice) -> str:
    """Render a bilingual plain-text summary of a Sprint invoice.

    Arabic appears first on each line, English second. Suitable for the
    founder to copy into an email alongside the XML attachment.
    """
    lines: list[str] = []
    lines.append(f"رقم الفاتورة / Invoice number: {invoice.invoice_number}")
    lines.append(
        "تاريخ الإصدار / Issue date: "
        + invoice.issue_datetime.strftime("%Y-%m-%d")
    )
    lines.append(f"البند / Line item: {SPRINT_LINE_DESCRIPTION}")
    lines.append(
        f"الإجمالي قبل الضريبة / Subtotal: {invoice.subtotal_sar} SAR"
    )
    lines.append(
        f"ضريبة القيمة المضافة 15٪ / VAT 15%: {invoice.vat_sar} SAR"
    )
    lines.append(
        f"الإجمالي شامل الضريبة / Grand total: {invoice.grand_total_sar} SAR"
    )
    lines.append("جدول السداد / Payment schedule:")
    for milestone in invoice.schedule:
        lines.append(
            f"  - {milestone.label_ar} ({milestone.percent}٪) "
            f"{milestone.trigger_ar}: {milestone.amount_with_vat_sar} SAR"
        )
        lines.append(
            f"    {milestone.label_en} ({milestone.percent}%) "
            f"{milestone.trigger_en}: {milestone.amount_with_vat_sar} SAR"
        )
    lines.append("طريقة السداد / Payment method: تحويل بنكي / bank transfer")
    return "\n".join(lines)


__all__ = [
    "PAYMENT_MEANS_BANK_TRANSFER",
    "PaymentMilestone",
    "SPRINT_LINE_DESCRIPTION",
    "SPRINT_LINE_DESCRIPTION_AR",
    "SPRINT_LINE_DESCRIPTION_EN",
    "SPRINT_PRICE_SAR",
    "SprintInvoice",
    "build_payment_schedule",
    "build_sprint_invoice",
    "build_sprint_invoice_payload",
    "render_invoice_summary",
]
