"""Tier-1 frontend contracts for the current Dealix product truth.

These tests preserve the useful conversion, safety, proof, and portal contracts
without reviving retired fixed-price, Checkout, or deep-page funnels.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

import pytest
from defusedxml import ElementTree

LANDING = Path(__file__).resolve().parents[1] / "landing"
SITEMAP_NAMESPACE = {"sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def _read(name: str) -> str:
    return (LANDING / name).read_text(encoding="utf-8")


# Homepage positioning and acquisition path

def test_index_has_revenue_command_center_h1() -> None:
    html = _read("index.html")
    match = re.search(r'<h1[^>]*class="hero__title"[^>]*>([^<]+)</h1>', html)
    assert match, "hero H1 with class 'hero__title' not found"
    text = match.group(1).strip()
    assert "غرفة قيادة" in text or "Revenue Command Center" in text
    assert len(text.split()) <= 8, "Tier-1 H1 should remain concise"


def test_index_primary_cta_points_to_diagnostic() -> None:
    html = _read("index.html")
    block = re.search(r'<div class="hero__ctas">(.*?)</div>', html, re.DOTALL)
    assert block, "hero CTA block not found"
    for anchor in re.finditer(r'<a\s+([^>]+)>', block.group(1)):
        attrs = anchor.group(1)
        if "btn--primary" in attrs:
            href = re.search(r'href="([^"]+)"', attrs)
            assert href and "/diagnostic.html" in href.group(1)
            return
    pytest.fail("hero primary diagnostic CTA not found")


def test_index_nav_is_bounded_and_keeps_mega_menu() -> None:
    html = _read("index.html")
    nav = re.search(r'<nav class="nav__links"[^>]*>(.*?)</nav>', html, re.DOTALL)
    assert nav, "primary navigation missing"
    body = re.sub(
        r'<div class="ds-mega-menu__panel".*?</div>\s*</div>',
        "",
        nav.group(1),
        flags=re.DOTALL,
    )
    assert len(re.findall(r'<a\s+[^>]*href=', body)) <= 7
    assert "ds-mega-menu" in html
    assert "ds-mega-menu__panel" in html


# WhatsApp Decision Layer remains a clearly synthetic approval demo

def test_index_wadl_is_demo_and_uses_design_system_components() -> None:
    html = _read("index.html")
    css = _read("assets/css/design-system.css")
    block = re.search(r'id="wadl"(.*?)</section>', html, re.DOTALL)
    assert block, "#wadl section missing"
    assert "DEMO" in block.group(1)
    for cls in ("ds-wadl", "ds-wadl__phone", "ds-wadl__msg", "ds-wadl__chip"):
        assert cls in html, f"homepage missing {cls}"
        assert cls in css, f"design system missing {cls}"


def test_index_preserves_conversion_and_truth_sections() -> None:
    html = _read("index.html")
    for anchor in (
        "pillars",
        "for-who",
        "sectors",
        "how",
        "problem",
        "wadl",
        "portal-preview",
        "trust",
        "proof",
        "proof-strip",
        "pricing",
        "pilot",
        "faq",
    ):
        assert f'id="{anchor}"' in html, f"homepage section #{anchor} missing"


# Customer portal and proof UX

def test_customer_portal_today_decision_precedes_ops() -> None:
    html = _read("customer-portal.html")
    today_idx = html.find('id="today-decision"')
    ops_idx = html.find('id="ops-grid"')
    assert today_idx > 0 and ops_idx > 0 and today_idx < ops_idx
    assert 'class="ds-portal-deep"' in html
    assert "src-pill" in html and "DEMO" in html


def test_proof_page_keeps_l1_to_l5_ladder() -> None:
    html = _read("proof.html")
    for level in ("L1", "L2", "L3", "L4", "L5"):
        assert level in html
    for cls in ("ds-evidence-ladder", "ds-evidence-level--l1", "ds-evidence-level--l5"):
        assert cls in html


# Current two-entry commercial doctrine

def test_pricing_exposes_only_current_two_entry_path() -> None:
    html = _read("pricing.html")
    cards = re.findall(r'<article class="card(?:\s[^"]*)?"', html)
    assert len(cards) == 2, f"expected two current commercial entries; found {len(cards)}"
    assert "Free Mini Diagnostic" in html
    assert "Revenue Command Pilot — 30 days" in html
    assert "free_entry" in html
    assert "quote_only" in html
    assert "عرض سعر بعد الاكتشاف" in html


def test_pricing_rejects_retired_public_checkout_and_fixed_prices() -> None:
    html = _read("pricing.html")
    assert "/checkout.html" not in html
    assert "ضمان المبيعات" not in html

    retired_price_patterns = (
        r"\b499\s*(?:SAR|ريال)",
        r"\b999\s*(?:SAR|ريال)",
        r"\b12[,.]?000\s*(?:SAR|ريال)",
        r"\b25[,.]?000\s*(?:SAR|ريال)",
    )
    for pattern in retired_price_patterns:
        assert not re.search(pattern, html, re.IGNORECASE), (
            f"retired pricing doctrine returned: {pattern}"
        )

    assert html.count('/diagnostic.html') >= 2
    assert "لا Checkout عام" in html


# Trust and diagnostic surfaces

def test_trust_center_lists_hard_safety_gates() -> None:
    html = _read("trust-center.html")
    for code in (
        "NO_LIVE_SEND",
        "NO_LIVE_CHARGE",
        "NO_COLD_WHATSAPP",
        "NO_LINKEDIN_AUTOMATION",
        "NO_SCRAPING",
        "NO_FAKE_PROOF",
        "NO_FAKE_REVENUE",
        "NO_UNAPPROVED_TESTIMONIAL",
    ):
        assert code in html


def test_diagnostic_describes_bounded_outputs() -> None:
    html = _read("diagnostic.html")
    for token in ("فرص", "رسالة عربيّة", "أفضل قناة", "مخاطرة", "قرار التالي"):
        assert token in html


# Canonical sitemap and public-surface retirement

def test_sitemaps_use_canonical_domain_and_current_surfaces_only() -> None:
    expected_paths = {
        "/",
        "/pricing.html",
        "/diagnostic.html",
        "/proof.html",
        "/trust-center.html",
        "/privacy.html",
        "/terms.html",
    }
    retired_paths = {
        "/checkout.html",
        "/launchpad.html",
        "/compare.html",
        "/roi.html",
        "/case-study.html",
    }

    for name in ("sitemap.xml", "sitemap_dealix.xml"):
        root = ElementTree.fromstring(_read(name))
        locations = [
            element.text.strip()
            for element in root.findall("sitemap:url/sitemap:loc", SITEMAP_NAMESPACE)
            if element.text
        ]
        assert locations, f"{name} contains no sitemap locations"

        urls = [urlsplit(location) for location in locations]
        assert all(url.scheme == "https" for url in urls), name
        assert all(url.hostname == "dealix.me" for url in urls), name
        assert all(url.port is None and not url.query and not url.fragment for url in urls), name

        paths = {url.path for url in urls}
        assert paths == expected_paths, f"{name} has unexpected canonical paths: {paths}"
        assert paths.isdisjoint(retired_paths), name


@pytest.mark.parametrize("page", ["agency-partner.html", "trust-center.html"])
def test_retained_tier1_pages_keep_approval_and_proof_badges(page: str) -> None:
    html = _read(page)
    assert "Approval-first" in html
    assert "Proof-backed" in html
