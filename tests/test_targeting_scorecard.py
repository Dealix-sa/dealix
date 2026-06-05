"""Scorecard: bounded scores, auditable reasons, correct bands, reject handling."""

from __future__ import annotations

from scripts.targeting_scorecard import rank, score_company


def _strong_company() -> dict:
    return {
        "company_name": "Strong Co",
        "website": "https://strong.example.sa",
        "city": "riyadh",
        "sector": "consulting",
        "b2b": True,
        "contact_channel": "warm_introduction",
        "no_case_studies": True,
        "many_services_no_focus": True,
        "fragmented_tools": True,
        "hiring_signal": True,
        "growth_signal": True,
        "serves_many_clients": True,
        "source_urls": [
            "https://strong.example.sa",
            "https://news.example/strong",
            "https://strong.example.sa/about",
        ],
        "evidence_count": 3,
    }


def test_score_is_bounded_0_100() -> None:
    s = score_company(_strong_company())
    assert 0 <= s["score"] <= 100


def test_every_axis_has_a_reason() -> None:
    s = score_company(_strong_company())
    for axis, payload in s["axes"].items():
        assert "points" in payload
        assert s["axis_reasons"].get(axis), f"axis {axis} missing reason"


def test_strong_company_grades_high() -> None:
    s = score_company(_strong_company())
    assert s["grade"] in {"A+", "A", "B"}
    assert s["decision"] in {"review_today", "strong_target", "needs_research"}


def test_thin_company_scores_low_and_is_penalized() -> None:
    thin = {
        "company_name": "Thin Co",
        "website": "",
        "city": "other",
        "sector": "manufacturing_industrial",
        "b2b": True,
        "contact_channel": "",
        "source_urls": ["https://dir.example/thin"],
        "evidence_count": 1,
    }
    s = score_company(thin)
    penalties = {p["penalty"] for p in s["penalties"]}
    assert "single_source_only" in penalties
    assert "no_official_website" in penalties
    assert "no_pain_signal" in penalties
    assert s["score"] < score_company(_strong_company())["score"]


def test_compliance_risk_field_forces_reject() -> None:
    risky = _strong_company()
    risky["personal_phone"] = True
    s = score_company(risky)
    assert s["reject"] is True
    assert s["grade"] == "REJECT"
    assert s["score"] == 0


def test_rank_sorts_high_to_low_and_rejects_last() -> None:
    companies = [
        _strong_company(),
        {
            "company_name": "R",
            "sector": "consulting",
            "personal_phone": True,
            "source_urls": ["a", "b"],
            "evidence_count": 2,
            "contact_channel": "warm_introduction",
            "website": "x",
        },
    ]
    ranked = rank(companies)
    assert ranked[0]["reject"] is False
    assert ranked[-1]["reject"] is True


def test_axis_points_never_exceed_axis_max() -> None:
    # Pile on every pain signal; pain_signal axis must still cap at its max (20).
    c = _strong_company()
    for sig in (
        "weak_cta",
        "unclear_followup",
        "no_case_studies",
        "many_services_no_focus",
        "fragmented_tools",
        "recurring_support",
        "delivery_no_visibility",
        "many_clients_no_memory",
    ):
        c[sig] = True
    s = score_company(c)
    assert s["axes"]["pain_signal"]["points"] <= 20
