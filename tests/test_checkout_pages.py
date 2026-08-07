"""Commercial-surface guards for the retired public Checkout path.

Historical test-only Checkout files may remain in the repository, but current
public authority surfaces must route to discovery, never expose the retired
fixed-price ladder, and never imply a live charge, invoice, or revenue event.
"""

from __future__ import annotations

import re
from pathlib import Path

LANDING = Path(__file__).resolve().parents[1] / "landing"


def _read(name: str) -> str:
    return (LANDING / name).read_text(encoding="utf-8")


def test_historical_checkout_files_remain_non_authoritative_and_no_live_charge() -> None:
    for name in ("checkout.html", "checkout-success.html"):
        path = LANDING / name
        assert path.exists(), f"historical test-only surface missing: {name}"
        html = path.read_text(encoding="utf-8")
        assert "NO_LIVE_CHARGE" in html
        assert "REQUEST ≠ INVOICE ≠ REVENUE" in html


def test_checkout_request_does_not_claim_invoice_payment_or_delivery() -> None:
    html = _read("checkout-success.html")
    assert "request_id" in html
    assert "invoice_id" not in html
    assert "test_request_recorded" in html
    assert "لم يتم خصم أي مبلغ" in html
    assert "لم تصدر فاتورة حية" in html
    assert "لم يبدأ تنفيذ الخدمة" in html
    assert "VAT 15%" not in html


def test_checkout_page_keeps_test_intent_separate_from_manual_path() -> None:
    html = _read("checkout.html")
    assert "/api/v1/payment-ops/invoice-intent" in html
    manual_start = html.index("if(method==='bank_transfer_manual')")
    test_path_start = html.index("btn.disabled=true", manual_start)
    assert "/api/v1/payment-ops/invoice-intent" not in html[manual_start:test_path_start]


def test_current_pricing_has_no_checkout_or_fixed_tier_ctas() -> None:
    html = _read("pricing.html")
    assert "/checkout.html" not in html
    assert "Free Mini Diagnostic" in html
    assert "Revenue Command Pilot — 30 days" in html
    assert "quote_only" in html
    for retired in ("499", "2999", "7999", "12000", "12,000"):
        assert retired not in html

    ctas = re.findall(r'class="cta"\s+href="([^"]+)"', html)
    assert ctas, "current pricing CTAs missing"
    assert all(href == "/diagnostic.html" for href in ctas)


def test_robots_disallows_historical_checkout_pages() -> None:
    robots = _read("robots.txt")
    assert "Disallow: /checkout.html" in robots
    assert "Disallow: /checkout-success.html" in robots


def test_sitemaps_do_not_publish_checkout_pages() -> None:
    for name in ("sitemap.xml", "sitemap_dealix.xml"):
        sitemap = _read(name)
        assert "/checkout.html" not in sitemap
        assert "/checkout-success.html" not in sitemap


def test_llms_exposes_current_two_entry_path_without_fixed_prices() -> None:
    llms = _read("llms.txt")
    assert "Free Mini Diagnostic" in llms
    assert "Revenue Command Pilot — 30 days" in llms
    assert "free_entry" in llms
    assert "quote_only" in llms
    assert "Revenue requires payment evidence" in llms
    assert "Completed delivery requires proof evidence" in llms
    for retired in (
        "499 SAR",
        "2,999 SAR",
        "2999 SAR",
        "12,000 SAR",
        "12000 SAR",
        "/checkout.html",
    ):
        assert retired not in llms


def test_llms_keeps_approval_and_outbound_boundaries() -> None:
    llms = _read("llms.txt").lower()
    for statement in (
        "no cold whatsapp",
        "no linkedin scraping",
        "explicit human approval",
        "no fake customer",
    ):
        assert statement in llms


def test_checkout_is_absent_from_current_authority_links() -> None:
    for name in ("index.html", "pricing.html", "llms.txt"):
        assert "/checkout.html" not in _read(name), name
