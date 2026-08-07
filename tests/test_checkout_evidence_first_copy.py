"""Commercial trust checks for the public checkout/test-request flow."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKOUT = ROOT / "landing" / "checkout.html"
SUCCESS = ROOT / "landing" / "checkout-success.html"

FORBIDDEN_PUBLIC_CLAIMS = (
    "حتّى 2,500 lead/شهر",
    "Lead غير محدود",
    "SLA 99.9%",
    "دعم خلال 4 ساعات",
    "Next Best Offer تلقائي",
    "WhatsApp approval flow",
    "Moyasar invoicing مدمج",
    "الفاتورة جاهزة",
    "سيتواصل معك المؤسس خلال 24 ساعة",
    "Proof Pack جاهز يوم 7",
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkout_is_explicitly_a_test_request_not_live_revenue() -> None:
    text = _text(CHECKOUT)

    assert "وضع TEST" in text
    assert "NO_LIVE_CHARGE" in text
    assert "REQUEST ≠ INVOICE ≠ REVENUE" in text
    assert "إنشاء طلب بدء تجريبي" in text
    assert "إنشاء الفاتورة" not in text
    assert "لا يُسجل الإيراد قبل دليل payment_received حقيقي" in text
    assert "تم استلام الدفع" not in text


def test_success_page_does_not_claim_invoice_payment_or_service_start() -> None:
    text = _text(SUCCESS)

    assert "تم تسجيل طلب البدء" in text
    assert "لم يتم خصم أي مبلغ" in text
    assert "لم تصدر فاتورة حية" in text
    assert "لم يبدأ تنفيذ الخدمة" in text
    assert "request_id" in text
    assert "invoice_id" not in text
    assert "test_request_recorded" in text


def test_unverified_capacity_sla_and_automation_claims_are_absent() -> None:
    combined = _text(CHECKOUT) + "\n" + _text(SUCCESS)

    for claim in FORBIDDEN_PUBLIC_CLAIMS:
        assert claim.casefold() not in combined.casefold()


def test_bank_transfer_is_manual_validated_and_does_not_call_invoice_intent() -> None:
    text = _text(CHECKOUT)
    manual_start = text.index("if(method==='bank_transfer_manual')")
    test_request_start = text.index("btn.disabled=true", manual_start)
    manual_block = text[manual_start:test_request_start]

    assert "form.reportValidity()" in text
    assert "طلب تعليمات التحويل" in manual_block
    assert "No payment has been made" in manual_block
    assert "Email: " in manual_block
    assert "Phone: " in manual_block
    assert "mailto:sales@dealix.sa" in manual_block
    assert "/api/v1/payment-ops/invoice-intent" not in manual_block


def test_test_intent_redirect_uses_request_semantics() -> None:
    text = _text(CHECKOUT)

    assert "/api/v1/payment-ops/invoice-intent" in text
    assert "request_id=" in text
    assert "invoice_id=" not in text
    assert "تم تسجيل طلب تجريبي في TEST mode" in text
