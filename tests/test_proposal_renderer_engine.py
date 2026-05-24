"""Tests for the Track B.3 Proposal Renderer engine.

A separate test file (``..._engine.py``) is used to avoid colliding with
the pre-existing ``tests/test_proposal_renderer.py`` which exercises the
legacy markdown renderer at
``auto_client_acquisition.sales_os.proposal_renderer``.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from auto_client_acquisition.revenue_pipeline.lead import Lead
from dealix.commercial_ops.proposal_renderer import (
    SUPPORTED_LANGUAGES,
    SUPPORTED_TIERS,
    TIER_REGISTRY,
    ProposalRenderer,
    VAT_RATE_KSA,
    compute_price_breakdown,
    format_sar,
    load_pricing,
    render_proposal_pdf,
    resolve_tier_price,
)

_PRICING = load_pricing()


def _lead() -> Lead:
    return Lead.make(slot_id="slot-A", sector="b2b_services", region="Riyadh")


# ─────────────────────────────────────────────────────────────────────
# 1. Every tier renders without error in all 3 languages
# ─────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("tier", SUPPORTED_TIERS)
@pytest.mark.parametrize("language", SUPPORTED_LANGUAGES)
def test_render_html_for_every_tier_and_language(tier: str, language: str) -> None:
    r = ProposalRenderer()
    html = r.render_html(lead=_lead(), tier=tier, language=language)
    assert html.startswith("<!DOCTYPE html>")
    assert "Dealix" in html
    assert TIER_REGISTRY[tier].title_en in html or TIER_REGISTRY[tier].title_ar in html


# ─────────────────────────────────────────────────────────────────────
# 2. AR / EN / bilingual variants behave differently
# ─────────────────────────────────────────────────────────────────────


def test_language_variants_differ() -> None:
    r = ProposalRenderer()
    lead = _lead()
    ar = r.render_html(lead=lead, tier="mini_sprint", language="ar")
    en = r.render_html(lead=lead, tier="mini_sprint", language="en")
    bi = r.render_html(lead=lead, tier="mini_sprint", language="bilingual")
    assert 'dir="rtl"' in ar
    assert 'dir="ltr"' in en
    assert 'dir="rtl"' in bi  # bilingual page wraps RTL but contains both
    assert "Executive Summary" in en
    assert "الملخّص التنفيذي" in ar
    # Bilingual must contain both:
    assert "Executive Summary" in bi and "الملخّص التنفيذي" in bi


# ─────────────────────────────────────────────────────────────────────
# 3. VAT-15% (KSA) is computed correctly
# ─────────────────────────────────────────────────────────────────────


def test_vat_calculation_is_15_percent() -> None:
    bd = compute_price_breakdown(10_000)
    assert bd.vat_rate == VAT_RATE_KSA == 0.15
    assert bd.vat_sar == 1_500
    assert bd.total_sar == 11_500


def test_vat_appears_in_rendered_html() -> None:
    r = ProposalRenderer()
    html = r.render_html(lead=_lead(), tier="mini_sprint", language="en")
    # Subtotal + VAT row must both be present.
    assert "Subtotal" in html
    assert "VAT" in html
    assert "15%" in html


# ─────────────────────────────────────────────────────────────────────
# 4. PDPL + ZATCA badges are always present
# ─────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("tier", SUPPORTED_TIERS)
@pytest.mark.parametrize("language", SUPPORTED_LANGUAGES)
def test_pdpl_and_zatca_badges_present(tier: str, language: str) -> None:
    r = ProposalRenderer()
    html = r.render_html(lead=_lead(), tier=tier, language=language)
    assert "PDPL Compliant" in html
    assert "ZATCA Phase 2 Ready" in html


# ─────────────────────────────────────────────────────────────────────
# 5. Pricing comes from pricing.yaml — never hardcoded
# ─────────────────────────────────────────────────────────────────────


def test_resolve_tier_price_matches_yaml() -> None:
    for tier_id, spec in TIER_REGISTRY.items():
        cursor = _PRICING
        for key in spec.pricing_yaml_path:
            cursor = cursor[key]
        assert resolve_tier_price(tier_id, _PRICING) == cursor


def test_no_hardcoded_pricing_in_source() -> None:
    """The renderer source file must reference YAML, not number literals."""
    src = (
        Path(__file__).resolve().parents[1]
        / "dealix"
        / "commercial_ops"
        / "proposal_renderer.py"
    ).read_text(encoding="utf-8")
    # No 4-digit-or-greater pricing literals (e.g., 4999, 9999, 15000, 25000, 35000).
    forbidden = ("4999", "9999", "15000", "25000", "35000")
    for token in forbidden:
        assert token not in src, f"hardcoded pricing literal {token!r} found in renderer source"


def test_custom_pricing_override_takes_precedence() -> None:
    r = ProposalRenderer()
    html = r.render_html(
        lead=_lead(),
        tier="mini_sprint",
        language="en",
        custom_pricing={"mini_sprint": 12_345},
    )
    assert "12,345" in html
    # VAT @ 15% on 12,345 = 1,852 (rounded)
    assert "1,852" in html


# ─────────────────────────────────────────────────────────────────────
# 6. PDF rendering works and page budget is honoured
# ─────────────────────────────────────────────────────────────────────


def test_render_pdf_writes_valid_pdf_bytes(tmp_path: Path) -> None:
    pdf = render_proposal_pdf(
        lead=_lead(), tier="mini_sprint", language="bilingual"
    )
    assert pdf.startswith(b"%PDF-")
    out = tmp_path / "proposal_mini_sprint_bilingual.pdf"
    out.write_bytes(pdf)
    assert out.stat().st_size > 1_000


def test_pdf_page_budget_mini_sprint_under_5_pages() -> None:
    try:
        from weasyprint import HTML  # type: ignore[import-not-found]
    except Exception:
        pytest.skip("WeasyPrint unavailable; cannot count pages precisely")
    r = ProposalRenderer()
    html = r.render_html(lead=_lead(), tier="mini_sprint", language="bilingual")
    doc = HTML(string=html, base_url=str(r.template_dir)).render()
    assert len(doc.pages) <= TIER_REGISTRY["mini_sprint"].page_budget


def test_pdf_page_budget_custom_ai_under_15_pages() -> None:
    try:
        from weasyprint import HTML  # type: ignore[import-not-found]
    except Exception:
        pytest.skip("WeasyPrint unavailable; cannot count pages precisely")
    r = ProposalRenderer()
    html = r.render_html(lead=_lead(), tier="custom_ai", language="bilingual")
    doc = HTML(string=html, base_url=str(r.template_dir)).render()
    assert len(doc.pages) <= TIER_REGISTRY["custom_ai"].page_budget


# ─────────────────────────────────────────────────────────────────────
# 7. Bilingual layout uses two columns
# ─────────────────────────────────────────────────────────────────────


def test_bilingual_template_uses_two_column_grid() -> None:
    r = ProposalRenderer()
    html = r.render_html(lead=_lead(), tier="mini_sprint", language="bilingual")
    assert "bilingual-grid" in html
    assert "col-ar" in html
    assert "col-en" in html


# ─────────────────────────────────────────────────────────────────────
# 8. AR digits formatter uses Arabic-Indic numerals
# ─────────────────────────────────────────────────────────────────────


def test_format_sar_ar_uses_arabic_digits() -> None:
    s = format_sar(12_345, language="ar")
    assert "SAR" in s
    # Must NOT contain Western digits
    assert not re.search(r"\d", s)
    # And SHOULD contain at least one Arabic-Indic digit
    assert any(c in "٠١٢٣٤٥٦٧٨٩" for c in s)


def test_format_sar_en_uses_western_digits() -> None:
    s = format_sar(12_345, language="en")
    assert "12,345" in s and "SAR" in s


# ─────────────────────────────────────────────────────────────────────
# 9. No PII leakage from the Lead into logs / context
# ─────────────────────────────────────────────────────────────────────


def test_lead_view_uses_placeholders_when_no_label_provided() -> None:
    from dealix.commercial_ops.proposal_renderer import LeadView

    view = LeadView.from_lead(_lead())
    assert "placeholder" in view.customer_label
    assert "placeholder" in view.customer_handle


def test_render_html_does_not_leak_customer_phone_or_email() -> None:
    r = ProposalRenderer()
    html = r.render_html(
        lead=_lead(),
        tier="managed_ops",
        language="bilingual",
        customer_label="Sample Customer Co.",
        customer_handle="sample-customer",
    )
    # Even when a label is supplied, no PII patterns should appear
    assert "@" not in html  # no emails
    assert "+966" not in html  # no Saudi phone
    assert "Sample Customer Co." in html  # but the supplied label is shown


# ─────────────────────────────────────────────────────────────────────
# 10. Invalid inputs raise clear errors
# ─────────────────────────────────────────────────────────────────────


def test_render_unknown_tier_raises_value_error() -> None:
    r = ProposalRenderer()
    with pytest.raises(ValueError, match="Unknown tier"):
        r.render_html(lead=_lead(), tier="not_a_tier", language="en")


def test_render_unknown_language_raises_value_error() -> None:
    r = ProposalRenderer()
    with pytest.raises(ValueError, match="Unknown language"):
        r.render_html(lead=_lead(), tier="mini_sprint", language="fr")


def test_custom_pricing_must_be_positive_int() -> None:
    r = ProposalRenderer()
    with pytest.raises(ValueError):
        r.render_html(
            lead=_lead(),
            tier="mini_sprint",
            language="en",
            custom_pricing={"mini_sprint": 0},
        )


# ─────────────────────────────────────────────────────────────────────
# 11. Router smoke test (preview + render + tiers)
# ─────────────────────────────────────────────────────────────────────


def test_router_preview_returns_html_and_governance_decision() -> None:
    from fastapi.testclient import TestClient

    from api.main import app

    client = TestClient(app)
    resp = client.post(
        "/api/v1/proposals/preview",
        json={
            "customer_id": "cust_test",
            "lead_id": "lead_test",
            "tier": "mini_sprint",
            "language": "bilingual",
            "sector": "b2b_services",
            "region": "Riyadh",
        },
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["governance_decision"] == "ALLOW_WITH_REVIEW"
    assert body["html"].startswith("<!DOCTYPE html>")
    assert "PDPL Compliant" in body["html"]


def test_router_render_returns_pdf() -> None:
    from fastapi.testclient import TestClient

    from api.main import app

    client = TestClient(app)
    resp = client.post(
        "/api/v1/proposals/render",
        json={
            "customer_id": "cust_test",
            "lead_id": "lead_test",
            "tier": "mini_sprint",
            "language": "ar",
            "sector": "b2b_services",
            "region": "Riyadh",
        },
    )
    assert resp.status_code == 200, resp.text
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.content.startswith(b"%PDF-")
    assert resp.headers.get("x-governance-decision") == "ALLOW_WITH_REVIEW"


def test_router_tiers_catalog() -> None:
    from fastapi.testclient import TestClient

    from api.main import app

    client = TestClient(app)
    resp = client.get("/api/v1/proposals/tiers")
    assert resp.status_code == 200
    body = resp.json()
    assert set(body["tiers"]) == set(SUPPORTED_TIERS)
    assert set(body["languages"]) == set(SUPPORTED_LANGUAGES)
    assert body["pricing_source"] == "dealix/config/pricing.yaml"


def test_router_invalid_tier_returns_422() -> None:
    from fastapi.testclient import TestClient

    from api.main import app

    client = TestClient(app)
    resp = client.post(
        "/api/v1/proposals/preview",
        json={
            "customer_id": "cust_test",
            "lead_id": "lead_test",
            "tier": "nope",
            "language": "ar",
        },
    )
    assert resp.status_code == 422
