"""Track B2 — Pricing → evidence-first checkout request flow assertions.

Verifies:
- /checkout.html exists with all 5 priced tiers (sprint, growth, scale, partner, enterprise)
- /checkout-success.html exists and reads request_id from URL
- /pricing.html CTAs route to /checkout.html?tier=X
- NO_LIVE_CHARGE banner is visible on checkout.html
- VAT wording is deferred to the approved invoice/payment path
- Footer trust badges remain present
"""

from __future__ import annotations

import re
from pathlib import Path

LANDING = Path(__file__).resolve().parents[1] / "landing"


def _read(name: str) -> str:
    return (LANDING / name).read_text(encoding="utf-8")


def test_checkout_html_exists():
    assert (LANDING / "checkout.html").exists()


def test_checkout_success_html_exists():
    assert (LANDING / "checkout-success.html").exists()


def test_checkout_html_lists_all_pricing_tiers():
    html = _read("checkout.html")
    for key in ("sprint", "growth", "scale", "partner", "enterprise"):
        assert f"{key}:" in html or f'"{key}"' in html, f"checkout.html missing tier {key!r}"


def test_checkout_html_includes_amount_for_each_priced_tier():
    html = _read("checkout.html")
    for amount in ("499", "2999", "7999", "12000"):
        assert amount in html, f"checkout.html missing amount {amount!r}"


def test_checkout_html_has_no_live_charge_banner():
    html = _read("checkout.html")
    assert "NO_LIVE_CHARGE" in html
    assert "TEST" in html
    assert "REQUEST ≠ INVOICE ≠ REVENUE" in html


def test_checkout_html_defers_vat_to_approved_invoice_path():
    html = _read("checkout.html")
    assert "السعر والضريبة" in html
    assert "المسار المعتمد" in html
    assert "VAT 15% مُحتسب" not in html
    assert "الفاتورة جاهزة" not in html


def test_checkout_html_has_footer_trust_badges():
    html = _read("checkout.html")
    for badge in ("Saudi-PDPL", "Approval-first", "Proof-backed"):
        assert badge in html, f"checkout.html missing footer badge {badge!r}"


def test_checkout_html_uses_test_intent_endpoint_only_for_test_path():
    html = _read("checkout.html")
    assert "/api/v1/payment-ops/invoice-intent" in html
    manual_start = html.index("if(method==='bank_transfer_manual')")
    test_path_start = html.index("btn.disabled=true", manual_start)
    assert "/api/v1/payment-ops/invoice-intent" not in html[manual_start:test_path_start]


def test_checkout_html_handles_enterprise_tier_separately():
    html = _read("checkout.html")
    assert "mailto:sales@dealix.sa" in html
    assert "Enterprise assessment request" in html


def test_checkout_success_reads_request_id_from_url():
    html = _read("checkout-success.html")
    assert "request_id" in html
    assert "invoice_id" not in html


def test_checkout_success_is_request_not_invoice_or_payment():
    html = _read("checkout-success.html")
    assert "test_request_recorded" in html
    assert "REQUEST ≠ INVOICE ≠ REVENUE" in html
    assert "لم يتم خصم أي مبلغ" in html
    assert "لم تصدر فاتورة حية" in html
    assert "لم يبدأ تنفيذ الخدمة" in html
    assert "VAT 15%" not in html


def test_checkout_success_has_no_live_charge_disclaimer():
    html = _read("checkout-success.html")
    assert "NO_LIVE_CHARGE" in html


def test_checkout_success_has_footer_trust_badges():
    html = _read("checkout-success.html")
    for badge in ("Saudi-PDPL", "Approval-first", "Proof-backed"):
        assert badge in html, f"checkout-success.html missing footer badge {badge!r}"


def test_pricing_ctas_route_to_checkout():
    html = _read("pricing.html")
    for tier_key in ("sprint", "growth", "scale", "partner"):
        pattern = f"/checkout.html?tier={tier_key}"
        assert pattern in html, f"pricing.html missing CTA for tier={tier_key}"


def test_pricing_no_longer_routes_priced_tiers_to_launchpad():
    html = _read("pricing.html")
    ctas = re.findall(r'class="cta"\s+href="([^"]+)"', html)
    for href in ctas:
        if href.startswith("mailto:"):
            continue
        assert href.startswith("/checkout.html") or href == "/diagnostic.html", (
            f"pricing.html CTA points to unexpected target: {href}"
        )


def test_robots_txt_disallows_checkout_pages():
    robots = (LANDING / "robots.txt").read_text(encoding="utf-8")
    assert "Disallow: /checkout.html" in robots
    assert "Disallow: /checkout-success.html" in robots


def test_robots_txt_allows_ai_crawlers():
    robots = (LANDING / "robots.txt").read_text(encoding="utf-8")
    for bot in ("PerplexityBot", "ChatGPT-User", "GPTBot", "ClaudeBot"):
        assert f"User-agent: {bot}" in robots, f"robots.txt missing AI crawler {bot}"


def test_llms_txt_exists_and_lists_hard_gates():
    llms = (LANDING / "llms.txt").read_text(encoding="utf-8")
    for gate in (
        "NO_LIVE_SEND",
        "NO_LIVE_CHARGE",
        "NO_COLD_WHATSAPP",
        "NO_LINKEDIN_AUTOMATION",
        "NO_SCRAPING",
        "NO_FAKE_PROOF",
        "NO_FAKE_REVENUE",
        "NO_UNAPPROVED_TESTIMONIAL",
    ):
        assert gate in llms, f"llms.txt missing hard gate {gate!r}"


def test_llms_txt_lists_pricing_tiers():
    llms = (LANDING / "llms.txt").read_text(encoding="utf-8")
    assert "499 SAR" in llms
    assert "2,999 SAR" in llms or "2999 SAR" in llms
    assert "12,000 SAR" in llms or "12000 SAR" in llms


def test_llms_txt_includes_vision_2030_alignment():
    llms = (LANDING / "llms.txt").read_text(encoding="utf-8")
    assert "Vision 2030" in llms
    assert "PDPL" in llms
