from __future__ import annotations

from dealix.hermes.growth import (
    TrustSignal,
    advance_revenue_status,
    check_entity_consistency,
    score_trust_signals,
)
from dealix.hermes.growth.geo import (
    AnswerEnginePage,
    build_comparison_table,
    build_faq,
    check_geo_entity_alignment,
    is_citation_ready,
    score_ai_visibility,
    score_answer_engine_page,
)
from dealix.hermes.growth.geo.citation_assets import CitationAsset
from dealix.hermes.growth.geo.faq_builder import FAQEntry
from dealix.hermes.growth.trust_signals import TrustSignalCategory
from dealix.hermes.money.verified_revenue import RevenueStatus
import pytest


def test_trust_signal_min_categories_flag():
    report = score_trust_signals(
        "page_home",
        [
            TrustSignal(TrustSignalCategory.CASE_STUDY, "Case 1"),
            TrustSignal(TrustSignalCategory.CUSTOMER_REVIEW, "5 stars"),
        ],
    )
    assert report.distinct_categories == 2
    assert any("only 2 distinct" in n for n in report.notes)


def test_entity_consistency_detects_discrepancy():
    canonical = {
        "company_name": "Dealix",
        "company_description": "Sovereign control plane",
        "offer_starting_price_sar": "1500",
        "primary_url": "https://dealix.sa",
        "primary_industry": "AI Governance",
        "primary_locale": "ar-SA",
    }
    surface = {
        "surface_id": "linkedin",
        "company_name": "DealiX AI",  # case-fold mismatch
        "company_description": "Sovereign control plane",
    }
    report = check_entity_consistency(canonical, [surface])
    assert report.consistent is False
    assert any("company_name" in d for d in report.discrepancies)


def test_answer_engine_page_score_penalizes_missing_pieces():
    page = AnswerEnginePage(
        slug="ai-governance-saudi-companies",
        title="AI Governance",
        intent="",
        h1_present=False,
        has_summary_above_fold=False,
        qa_blocks=2,
        comparison_tables=0,
        citation_sources=0,
        last_updated_iso="",
    )
    score = score_answer_engine_page(page)
    assert score.score < 30
    assert "missing_h1" in score.issues
    assert "missing_intent" in score.issues


def test_citation_ready_requires_structured_data():
    asset = CitationAsset(
        asset_id="ai_governance_checklist",
        title="AI Governance Checklist",
        canonical_url="https://dealix.sa/checklist",
        structured_data_present=False,
        machine_readable_summary="short",
        last_verified_iso="",
    )
    ready, issues = is_citation_ready(asset)
    assert ready is False
    assert "missing_structured_data" in issues


def test_build_faq_emits_schema_org():
    payload = build_faq(
        [FAQEntry("What is Dealix?", "A sovereign control plane.")]
    )
    assert payload["@type"] == "FAQPage"
    assert payload["mainEntity"][0]["name"] == "What is Dealix?"


def test_build_comparison_requires_columns_and_rows():
    table = build_comparison_table(
        "Plans",
        ["plan", "price_sar"],
        [{"plan": "Pilot", "price_sar": "1500"}, {"plan": "Kit", "price_sar": "9500"}],
    )
    assert table["columns"] == ["plan", "price_sar"]
    assert len(table["rows"]) == 2


def test_geo_entity_alignment_flags_missing_surfaces():
    canonical = {
        "company_name": "Dealix",
        "company_description": "Sovereign control plane",
        "offer_starting_price_sar": "1500",
        "primary_url": "https://dealix.sa",
        "primary_industry": "AI Governance",
        "primary_locale": "ar-SA",
    }
    surfaces = [
        {"surface_id": "homepage", "company_name": "Dealix"},
    ]
    check = check_geo_entity_alignment(canonical, surfaces)
    assert check.report.consistent is False
    assert any("missing_geo_surfaces" in d for d in check.report.discrepancies)


def test_ai_visibility_score_composes_drivers():
    v = score_ai_visibility(
        answer_pages_score=60,
        faq_coverage_score=70,
        comparison_pages_score=50,
        entity_consistency_score=80,
        trust_signal_score=60,
        review_visibility_score=40,
    )
    assert 0 <= v.score <= 100


def test_revenue_status_transitions():
    assert (
        advance_revenue_status(
            RevenueStatus.PROPOSAL_SENT, RevenueStatus.COMMITTED
        )
        == RevenueStatus.COMMITTED
    )
    with pytest.raises(ValueError):
        advance_revenue_status(RevenueStatus.INFLUENCED, RevenueStatus.PAID)
