"""Dealix Targeting OS — scorecard rubric + penalties + grading."""

from __future__ import annotations

from scripts.targeting_scorecard import (
    compute_penalties,
    grade_for,
    load_weights,
    score_and_merge,
    score_company,
)

WEIGHTS = load_weights()

# A strong, fully-evidenced, in-phase company should land A/A+.
STRONG = {
    "company_name": "Strong Co",
    "website": "https://strong.example",
    "city": "Riyadh",
    "country": "Saudi Arabia",
    "sector": "b2b_consulting",
    "company_size_signal": "SMB/Mid-market",
    "contact_channel": "contact_page",
    "source_urls": [
        "https://strong.example/services",
        "https://strong.example/case-studies",
        "https://strong.example/careers",
    ],
    "evidence_count": 3,
    "pain_signals": ["no_case_studies", "generic_services_page"],
    "intent_signals": ["active_hiring", "recent_news"],
    "partnership_signal": True,
    "recommended_offer": "Command Sprint",
    "icp_in_phase": True,
}

# A weak, single-source, out-of-phase company should land low.
WEAK = {
    "company_name": "Weak Co",
    "website": "https://weak.example",
    "city": "",
    "sector": "",
    "contact_channel": "none",
    "source_urls": ["https://weak.example"],
    "evidence_count": 1,
    "pain_signals": [],
    "intent_signals": [],
    "recommended_offer": "",
    "icp_in_phase": False,
}


def test_weights_axes_sum_to_100():
    assert sum(WEIGHTS["axes"].values()) == 100


def test_strong_company_scores_a_grade():
    result = score_company(STRONG, weights=WEIGHTS)
    assert result["targeting_score"] >= 80
    assert result["grade"] in {"A", "A+"}
    assert result["force_reject"] is False


def test_weak_company_scores_low_grade():
    result = score_company(WEAK, weights=WEIGHTS)
    assert result["targeting_score"] < 60
    assert result["grade"] in {"C", "D"}


def test_score_is_bounded_0_100():
    for company in (STRONG, WEAK):
        s = score_company(company, weights=WEIGHTS)["targeting_score"]
        assert 0.0 <= s <= 100.0


def test_score_is_deterministic():
    a = score_company(STRONG, weights=WEIGHTS)
    b = score_company(STRONG, weights=WEIGHTS)
    assert a == b


def test_single_source_penalty_applied():
    company = dict(STRONG)
    company["source_urls"] = ["https://strong.example/services"]
    company["evidence_count"] = 1
    total, applied, force = compute_penalties(company, WEIGHTS)
    assert total <= -10
    assert any("single_source_only" in a for a in applied)
    assert force is False


def test_disallowed_source_forces_reject():
    company = dict(STRONG)
    company["risk_flags"] = ["blocked_source"]
    _total, _applied, force = compute_penalties(company, WEIGHTS)
    assert force is True
    result = score_company(company, weights=WEIGHTS)
    assert result["grade"] == "D"
    assert result["targeting_score"] < 60


def test_grade_bands_monotonic():
    assert grade_for(95, WEIGHTS)["grade"] == "A+"
    assert grade_for(85, WEIGHTS)["grade"] == "A"
    assert grade_for(75, WEIGHTS)["grade"] == "B"
    assert grade_for(65, WEIGHTS)["grade"] == "C"
    assert grade_for(40, WEIGHTS)["grade"] == "D"


def test_score_and_merge_sets_next_action():
    merged = score_and_merge(STRONG, weights=WEIGHTS)
    assert merged["targeting_score"] == merged["_score_detail"]["targeting_score"]
    assert merged["next_action"] == "Manual founder review"


def test_sensitive_sector_penalty():
    company = dict(STRONG)
    company["is_sensitive_sector"] = True
    company["risk_flags"] = ["sensitive_sector"]
    total, applied, _ = compute_penalties(company, WEIGHTS)
    assert any("sensitive_sector" in a for a in applied)
    assert total <= -15
