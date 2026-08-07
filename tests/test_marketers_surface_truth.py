from __future__ import annotations

from pathlib import Path

from auto_client_acquisition.self_growth_os import internal_linking_planner

LANDING = Path(__file__).resolve().parents[1] / "landing"


def test_marketers_page_is_noindex_and_routes_to_current_diagnostic() -> None:
    html = (LANDING / "marketers.html").read_text(encoding="utf-8")

    assert 'content="noindex,follow"' in html
    assert 'href="/diagnostic.html"' in html
    assert "quote-only" not in html.lower() or "عرض سعر" in html
    assert "/checkout.html" not in html
    assert "mailto:" not in html
    assert "sami.assiri11@gmail.com" not in html


def test_marketers_page_is_not_a_canonical_core_authority_surface() -> None:
    assert "marketers.html" not in internal_linking_planner.CORE_PAGES
    assert "marketers.html" not in {
        "index.html",
        "pricing.html",
        "trust-center.html",
        "status.html",
        "founder.html",
    }
