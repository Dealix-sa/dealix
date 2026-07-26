"""Regression contract for the public marketers landing page."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "landing" / "marketers.html"


def _page() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_marketers_page_is_explicitly_pilot_stage_and_approval_first() -> None:
    html = _page()

    required_contracts = (
        "مرحلة بايلوت",
        "Draft-first",
        "Approval-first",
        "لا إرسال حيّ",
        "لا يوجد ضمان لنتيجة تجارية",
        "لا يصبح التزامًا إلا داخل اتفاق مكتوب ومعتمد",
        "لا تصبح إعلانًا عن منصة مكتملة ذاتية الخدمة",
    )
    for contract in required_contracts:
        assert contract in html


def test_marketers_page_does_not_publish_unverified_prices_or_capability_claims() -> None:
    lowered = _page().lower()

    forbidden_claims = (
        "ابدأ بـ 1 ريال",
        "1 ر.س",
        "999 ر.س",
        "2,999 ر.س",
        "7,999 ر.س",
        "99.9% uptime",
        "34% تحسّن في roas",
        "18 ساعة/أسبوع",
        "60% وقت إعداد التقارير",
        "متوافق مرحلة 2",
        "4.8★",
        "دقة 88%+",
        "60% من عملائنا",
        "soc 2 compliance",
        "soc 2 (q3 2026)",
        "sla 1 ساعة",
        "sla 4 ساعات",
        "15 ساعة أسبوعياً",
        "تحسين تلقائي",
        "فواتير متوافقة مع zatca",
        "البيانات في aws me-south-1",
        "أسعارنا 40-60% أرخص",
        "توفّرلك 15 ساعة/أسبوع",
        "حملات غير محدودة",
        "عملاء غير محدودين",
    )
    for claim in forbidden_claims:
        assert claim.lower() not in lowered


def test_marketers_page_does_not_capture_or_send_data_directly() -> None:
    lowered = _page().lower()

    assert "<form" not in lowered
    assert "fetch(" not in lowered
    assert "xmlhttprequest" not in lowered
    assert "mailto:" in lowered
    assert "/trust-center.html" in lowered
    assert "/privacy.html" in lowered
