"""Dealix Targeting OS — compliance gate enforces the non-negotiables."""

from __future__ import annotations

from scripts.targeting_compliance_gate import (
    gate_company,
    load_blocked,
    source_type_is_allowed,
    url_is_allowed,
)

POLICY = load_blocked()


def test_policy_loads_with_expected_keys():
    for key in (
        "blocked_domains",
        "blocked_url_patterns",
        "blocked_source_types",
        "sensitive_sectors",
    ):
        assert key in POLICY


def test_linkedin_url_is_blocked():
    ok, reason = url_is_allowed("https://www.linkedin.com/company/acme", POLICY)
    assert ok is False
    assert "blocked_domain" in reason


def test_official_site_url_is_allowed():
    ok, _ = url_is_allowed("https://example.com/services", POLICY)
    assert ok is True


def test_login_gated_url_is_blocked():
    ok, reason = url_is_allowed("https://example.com/login?next=/data", POLICY)
    assert ok is False
    assert "blocked_pattern" in reason


def test_empty_url_is_blocked():
    ok, _ = url_is_allowed("", POLICY)
    assert ok is False


def test_forbidden_source_type_rejected():
    ok, reason = source_type_is_allowed("leaked_database", POLICY)
    assert ok is False
    assert "blocked_source_type" in reason


def test_company_with_two_official_sources_approved():
    company = {
        "company_name": "Clean Co",
        "sector": "b2b_consulting",
        "contact_channel": "contact_page",
        "source_urls": ["https://clean.example/services", "https://clean.example/clients"],
    }
    result = gate_company(company, POLICY)
    assert result["status"] == "approved"
    assert len(result["allowed_sources"]) == 2


def test_company_with_only_blocked_source_rejected():
    company = {
        "company_name": "Bad Co",
        "sector": "b2b_consulting",
        "source_urls": ["https://www.linkedin.com/company/bad"],
    }
    result = gate_company(company, POLICY)
    assert result["status"] == "reject"
    assert "blocked_source" in result["risk_flags"]


def test_forbidden_source_type_forces_reject():
    company = {
        "company_name": "Leak Co",
        "sector": "b2b_consulting",
        "source_urls": ["https://leak.example/services"],
        "source_types": ["leaked_database"],
    }
    result = gate_company(company, POLICY)
    assert result["status"] == "reject"
    assert "forbidden_source_type" in result["risk_flags"]


def test_single_source_company_needs_review():
    company = {
        "company_name": "Thin Co",
        "sector": "b2b_consulting",
        "contact_channel": "contact_page",
        "source_urls": ["https://thin.example/services"],
    }
    result = gate_company(company, POLICY)
    assert result["status"] == "needs_review"


def test_personal_mobile_channel_flagged():
    company = {
        "company_name": "Mobile Co",
        "sector": "b2b_consulting",
        "contact_channel": "personal_mobile",
        "source_urls": ["https://m.example/services", "https://m.example/about"],
    }
    result = gate_company(company, POLICY)
    assert "no_official_channel" in result["risk_flags"]


def test_sensitive_sector_needs_review():
    company = {
        "company_name": "Bank Co",
        "sector": "banking",
        "contact_channel": "contact_page",
        "source_urls": ["https://bank.example/a", "https://bank.example/b"],
    }
    result = gate_company(company, POLICY)
    assert result["status"] == "needs_review"
    assert "sensitive_sector" in result["risk_flags"]
