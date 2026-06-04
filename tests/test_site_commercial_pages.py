"""The commercial website pages exist and carry SEO metadata + JSON-LD."""

from __future__ import annotations

from _launch_util import ROOT

APP = ROOT / "apps" / "web" / "app"

PAGES = [
    "commercial/page.tsx",
    "services/page.tsx",
    "pricing/page.tsx",
    "trust/page.tsx",
    "launch/page.tsx",
    "contact/page.tsx",
    "case-method/page.tsx",
    "media/page.tsx",
    "faq/page.tsx",
    "verticals/page.tsx",
    "en/page.tsx",
]


def test_pages_exist():
    for rel in PAGES:
        assert (APP / rel).exists(), rel


def test_pages_export_metadata():
    for rel in PAGES:
        text = (APP / rel).read_text(encoding="utf-8")
        assert "metadata" in text, rel


def test_faq_has_faq_jsonld():
    text = (APP / "faq" / "page.tsx").read_text(encoding="utf-8")
    assert "faqJsonLd" in text


def test_hero_copy_is_bilingual():
    data = (APP / "_launch" / "data.ts").read_text(encoding="utf-8")
    assert "AI Revenue & Operations OS" in data
    assert "نظام تشغيل الإيرادات والعمليات" in data


def test_sitemap_includes_commercial_routes():
    sitemap = (APP / "sitemap.ts").read_text(encoding="utf-8")
    for route in ["/commercial", "/pricing", "/verticals", "/trust", "/faq"]:
        assert route in sitemap
