"""Unit tests for api/routers/vision2030_alignment.py.

Pure unit tests — no HTTP client, no DB, no async.
Imports business-logic functions directly from the router module.
"""

from __future__ import annotations

import pytest

from api.routers.vision2030_alignment import (
    _DISCLAIMER_AR,
    _DISCLAIMER_EN,
    _KNOWN_SECTORS,
    _PILLARS,
    generate_narrative,
    get_sector_alignment,
    list_pillars,
)


# ---------------------------------------------------------------------------
# Pillar listing
# ---------------------------------------------------------------------------


def test_pillars_returns_three_pillars() -> None:
    result = list_pillars()
    assert "pillars" in result
    assert len(result["pillars"]) == 3


def test_pillars_all_have_ar_en_names() -> None:
    result = list_pillars()
    for pillar in result["pillars"]:
        assert pillar.get("name_ar"), f"Missing name_ar on pillar {pillar.get('pillar_id')}"
        assert pillar.get("name_en"), f"Missing name_en on pillar {pillar.get('pillar_id')}"


def test_pillars_have_ai_relevance_score() -> None:
    result = list_pillars()
    for pillar in result["pillars"]:
        score = pillar.get("ai_relevance_score")
        assert isinstance(score, (int, float)), (
            f"ai_relevance_score must be numeric for pillar {pillar.get('pillar_id')}"
        )
        assert 0 <= score <= 100, (
            f"ai_relevance_score out of range for pillar {pillar.get('pillar_id')}"
        )


def test_pillars_have_dealix_solutions() -> None:
    result = list_pillars()
    for pillar in result["pillars"]:
        solutions = pillar.get("dealix_solutions")
        assert isinstance(solutions, list), (
            f"dealix_solutions must be a list for pillar {pillar.get('pillar_id')}"
        )
        assert len(solutions) >= 1, (
            f"dealix_solutions is empty for pillar {pillar.get('pillar_id')}"
        )


def test_pillars_have_pillar_id() -> None:
    result = list_pillars()
    ids = {p["pillar_id"] for p in result["pillars"]}
    assert "thriving_economy" in ids
    assert "vibrant_society" in ids
    assert "ambitious_nation" in ids


def test_pillars_governance_decision_present() -> None:
    result = list_pillars()
    assert result.get("governance_decision") == "ALLOW_WITH_REVIEW"


# ---------------------------------------------------------------------------
# Sector alignment
# ---------------------------------------------------------------------------


def test_sector_alignment_fintech() -> None:
    result = get_sector_alignment("fintech")

    assert result["sector"] == "fintech"
    assert isinstance(result["overall_alignment_score"], int)
    assert 60 <= result["overall_alignment_score"] <= 95
    assert isinstance(result["aligned_pillars"], list)
    assert len(result["aligned_pillars"]) >= 1
    assert isinstance(result["vision2030_programs"], list)
    assert len(result["vision2030_programs"]) >= 1
    assert result.get("narrative_ar")
    assert result.get("narrative_en")
    assert result.get("governance_decision") == "ALLOW_WITH_REVIEW"


@pytest.mark.parametrize(
    "sector",
    [
        "b2b_saas",
        "agency",
        "healthcare_clinic",
        "real_estate",
        "logistics",
        "fintech",
        "engineering",
    ],
)
def test_sector_alignment_all_sectors(sector: str) -> None:
    result = get_sector_alignment(sector)

    assert result["sector"] == sector
    assert 60 <= result["overall_alignment_score"] <= 95
    assert isinstance(result["aligned_pillars"], list)
    assert len(result["aligned_pillars"]) >= 1
    assert isinstance(result["vision2030_programs"], list)
    assert len(result["vision2030_programs"]) >= 1
    assert result.get("narrative_ar")
    assert result.get("narrative_en")
    assert result.get("governance_decision") == "ALLOW_WITH_REVIEW"


def test_sector_alignment_unknown_raises_key_error() -> None:
    with pytest.raises(KeyError):
        get_sector_alignment("unknown_sector_xyz")


def test_sector_alignment_has_vision2030_programs() -> None:
    result = get_sector_alignment("real_estate")
    programs = result["vision2030_programs"]
    assert isinstance(programs, list)
    assert len(programs) >= 1
    # Real estate should include at least one major national program
    combined = " ".join(programs)
    assert any(prog in combined for prog in ("NEOM", "Qiddiya", "NTP"))


def test_sector_alignment_no_guaranteed_language_in_narratives() -> None:
    for sector in _KNOWN_SECTORS:
        result = get_sector_alignment(sector)
        for field in ("narrative_ar", "narrative_en"):
            text = result.get(field, "")
            assert "نضمن" not in text, (
                f"Guaranteed-outcome language found in {field} for {sector}"
            )
            assert "guarantee" not in text.lower(), (
                f"Guaranteed-outcome language found in {field} for {sector}"
            )
            assert "سيحقق" not in text, (
                f"Future-certain language 'سيحقق' found in {field} for {sector}"
            )


# ---------------------------------------------------------------------------
# Generate narrative
# ---------------------------------------------------------------------------


def test_generate_narrative_returns_both_languages() -> None:
    result = generate_narrative(
        sector="fintech",
        company_name="Noor Financial",
        use_case="AI-powered credit scoring",
    )
    assert result.get("narrative_ar")
    assert result.get("narrative_en")


def test_generate_narrative_includes_disclaimer() -> None:
    result = generate_narrative(
        sector="b2b_saas",
        company_name="CloudOps SA",
        use_case="automated revenue operations",
    )
    assert result.get("disclaimer_ar") == _DISCLAIMER_AR
    assert result.get("disclaimer_en") == _DISCLAIMER_EN


def test_generate_narrative_disclaimer_text_content() -> None:
    result = generate_narrative(
        sector="agency",
        company_name="Riyadh Agency",
        use_case="AI customer targeting",
    )
    # The disclaimer must mention "review" / "راجع" in each language
    assert "راجعها" in result["disclaimer_ar"]
    assert "review" in result["disclaimer_en"].lower()


def test_generate_narrative_has_governance_decision() -> None:
    result = generate_narrative(
        sector="logistics",
        company_name="Fast Cargo Co",
        use_case="route optimisation AI",
    )
    assert result.get("governance_decision") == "ALLOW_WITH_REVIEW"


def test_generate_narrative_has_alignment_score() -> None:
    result = generate_narrative(
        sector="real_estate",
        company_name="Al Masar Real Estate",
        use_case="AI lead scoring",
    )
    score = result.get("alignment_score")
    assert isinstance(score, (int, float))
    assert 0 < score <= 100


def test_generate_narrative_has_key_pillars() -> None:
    result = generate_narrative(
        sector="engineering",
        company_name="Construct KSA",
        use_case="project management AI",
    )
    pillars = result.get("key_pillars")
    assert isinstance(pillars, list)
    assert len(pillars) >= 1


def test_generate_narrative_healthcare_high_alignment() -> None:
    result = generate_narrative(
        sector="healthcare_clinic",
        company_name="Medcare Clinic",
        use_case="patient triage AI",
    )
    assert result["alignment_score"] >= 80


def test_generate_narrative_company_name_in_output() -> None:
    result = generate_narrative(
        sector="fintech",
        company_name="Sama Finance",
        use_case="fraud detection AI",
    )
    # Company name should appear somewhere in at least one narrative
    assert (
        "Sama Finance" in result["narrative_en"]
        or "Sama Finance" in result["narrative_ar"]
    )


def test_generate_narrative_unknown_sector_falls_back_gracefully() -> None:
    # Must not raise — unknown sector triggers fallback narrative
    result = generate_narrative(
        sector="unknown_sector_xyz",
        company_name="Generic Corp",
        use_case="AI workflow automation",
    )
    assert result.get("narrative_ar")
    assert result.get("narrative_en")
    assert result.get("governance_decision") == "ALLOW_WITH_REVIEW"
    assert isinstance(result.get("alignment_score"), (int, float))


def test_generate_narrative_no_guaranteed_language() -> None:
    for sector in _KNOWN_SECTORS:
        result = generate_narrative(
            sector=sector,
            company_name="Test Company",
            use_case="AI process automation",
        )
        for field in ("narrative_ar", "narrative_en"):
            text = result.get(field, "")
            assert "نضمن" not in text, (
                f"Guaranteed-outcome language found in {field} for {sector}"
            )
            assert "guarantee" not in text.lower(), (
                f"Guaranteed-outcome language found in {field} for {sector}"
            )


def test_generate_narrative_returns_sector_and_use_case() -> None:
    result = generate_narrative(
        sector="b2b_saas",
        company_name="DataFlow Inc",
        use_case="AI sales assistant",
    )
    assert result["sector"] == "b2b_saas"
    assert result["use_case"] == "AI sales assistant"
    assert result["company_name"] == "DataFlow Inc"


# ---------------------------------------------------------------------------
# Module-level data integrity checks
# ---------------------------------------------------------------------------


def test_known_sectors_is_complete() -> None:
    expected = {
        "b2b_saas",
        "agency",
        "healthcare_clinic",
        "real_estate",
        "logistics",
        "fintech",
        "engineering",
    }
    assert _KNOWN_SECTORS == expected


def test_pillars_module_constant_not_mutated_by_list_pillars() -> None:
    # Calling list_pillars must not mutate the module-level constant
    result = list_pillars()
    assert result["pillars"] is _PILLARS
