"""Tests for dealix.launch_os.vertical_scorer.

Covers all 15 Saudi verticals, ranking order, top_wedge, required fields,
score bounds, and sub-score integrity.
"""

from __future__ import annotations

import pytest

from dealix.launch_os.vertical_scorer import (
    SAUDI_VERTICALS,
    VerticalScore,
    rank_verticals,
    top_wedge,
)

# ---------------------------------------------------------------------------
# Known sector names — the 15 canonical sectors
# ---------------------------------------------------------------------------

EXPECTED_SECTORS = {
    "automotive",
    "real_estate",
    "contracting",
    "healthcare_clinics",
    "food_and_beverage",
    "education",
    "retail_chains",
    "logistics",
    "professional_services",
    "financial_services",
    "legal",
    "hospitality",
    "manufacturing",
    "government",
    "telecom",
}


# ---------------------------------------------------------------------------
# SAUDI_VERTICALS catalogue
# ---------------------------------------------------------------------------

class TestSaudiVerticalsCatalogue:
    def test_exactly_15_verticals_present(self) -> None:
        assert len(SAUDI_VERTICALS) == 15

    def test_all_expected_sectors_are_present(self) -> None:
        found = {v.sector for v in SAUDI_VERTICALS}
        assert found == EXPECTED_SECTORS

    def test_no_duplicate_sectors(self) -> None:
        sectors = [v.sector for v in SAUDI_VERTICALS]
        assert len(sectors) == len(set(sectors))

    def test_every_vertical_is_vertical_score_instance(self) -> None:
        for v in SAUDI_VERTICALS:
            assert isinstance(v, VerticalScore)

    def test_every_vertical_has_non_empty_sector_string(self) -> None:
        for v in SAUDI_VERTICALS:
            assert isinstance(v.sector, str) and v.sector.strip()

    def test_every_vertical_has_arabic_notes(self) -> None:
        """At least one non-ASCII character in notes_ar indicates Arabic content."""
        for v in SAUDI_VERTICALS:
            assert any(ord(c) > 127 for c in v.notes_ar), (
                f"{v.sector} has empty or ASCII-only notes_ar"
            )

    def test_every_vertical_has_english_notes(self) -> None:
        for v in SAUDI_VERTICALS:
            assert v.notes_en.strip(), f"{v.sector} has empty notes_en"


# ---------------------------------------------------------------------------
# VerticalScore fields and sub-scores
# ---------------------------------------------------------------------------

class TestVerticalScoreFields:
    @pytest.mark.parametrize("sector", sorted(EXPECTED_SECTORS))
    def test_sector_has_all_required_sub_score_fields(self, sector: str) -> None:
        vertical = next(v for v in SAUDI_VERTICALS if v.sector == sector)
        assert hasattr(vertical, "revenue_potential")
        assert hasattr(vertical, "pain_clarity")
        assert hasattr(vertical, "regulatory_ease")
        assert hasattr(vertical, "ai_readiness")
        assert hasattr(vertical, "competition_gap")
        assert hasattr(vertical, "total_score")

    @pytest.mark.parametrize("sector", sorted(EXPECTED_SECTORS))
    def test_sector_total_score_equals_sum_of_sub_scores(self, sector: str) -> None:
        v = next(vert for vert in SAUDI_VERTICALS if vert.sector == sector)
        expected = (
            v.revenue_potential
            + v.pain_clarity
            + v.regulatory_ease
            + v.ai_readiness
            + v.competition_gap
        )
        assert v.total_score == expected

    @pytest.mark.parametrize("sector", sorted(EXPECTED_SECTORS))
    def test_no_vertical_has_impossible_total_score(self, sector: str) -> None:
        v = next(vert for vert in SAUDI_VERTICALS if vert.sector == sector)
        assert 0 <= v.total_score <= 100, (
            f"{v.sector} has out-of-range total_score={v.total_score}"
        )

    def test_revenue_potential_within_0_to_25_for_all(self) -> None:
        for v in SAUDI_VERTICALS:
            assert 0 <= v.revenue_potential <= 25, (
                f"{v.sector} revenue_potential={v.revenue_potential} out of 0-25"
            )

    def test_pain_clarity_within_0_to_25_for_all(self) -> None:
        for v in SAUDI_VERTICALS:
            assert 0 <= v.pain_clarity <= 25, (
                f"{v.sector} pain_clarity={v.pain_clarity} out of 0-25"
            )

    def test_regulatory_ease_within_0_to_20_for_all(self) -> None:
        for v in SAUDI_VERTICALS:
            assert 0 <= v.regulatory_ease <= 20, (
                f"{v.sector} regulatory_ease={v.regulatory_ease} out of 0-20"
            )

    def test_ai_readiness_within_0_to_15_for_all(self) -> None:
        for v in SAUDI_VERTICALS:
            assert 0 <= v.ai_readiness <= 15, (
                f"{v.sector} ai_readiness={v.ai_readiness} out of 0-15"
            )

    def test_competition_gap_within_0_to_15_for_all(self) -> None:
        for v in SAUDI_VERTICALS:
            assert 0 <= v.competition_gap <= 15, (
                f"{v.sector} competition_gap={v.competition_gap} out of 0-15"
            )


# ---------------------------------------------------------------------------
# rank_verticals
# ---------------------------------------------------------------------------

class TestRankVerticals:
    def test_rank_verticals_returns_all_15(self) -> None:
        ranked = rank_verticals()
        assert len(ranked) == 15

    def test_rank_verticals_sorted_descending(self) -> None:
        ranked = rank_verticals()
        scores = [v.total_score for v in ranked]
        assert scores == sorted(scores, reverse=True)

    def test_rank_verticals_first_has_highest_score(self) -> None:
        ranked = rank_verticals()
        assert ranked[0].total_score >= ranked[-1].total_score

    def test_rank_verticals_all_sectors_preserved(self) -> None:
        ranked = rank_verticals()
        sectors = {v.sector for v in ranked}
        assert sectors == EXPECTED_SECTORS

    def test_rank_verticals_returns_vertical_score_instances(self) -> None:
        for v in rank_verticals():
            assert isinstance(v, VerticalScore)

    def test_rank_verticals_is_stable_across_calls(self) -> None:
        first = [v.sector for v in rank_verticals()]
        second = [v.sector for v in rank_verticals()]
        assert first == second


# ---------------------------------------------------------------------------
# top_wedge
# ---------------------------------------------------------------------------

class TestTopWedge:
    def test_top_wedge_returns_vertical_score(self) -> None:
        w = top_wedge()
        assert isinstance(w, VerticalScore)

    def test_top_wedge_sector_is_non_empty_string(self) -> None:
        w = top_wedge()
        assert isinstance(w.sector, str) and w.sector.strip()

    def test_top_wedge_has_highest_score_of_all_verticals(self) -> None:
        w = top_wedge()
        for v in SAUDI_VERTICALS:
            assert w.total_score >= v.total_score

    def test_top_wedge_score_above_practical_minimum(self) -> None:
        """The recommended wedge should have a meaningful score (>= 80 per docstring)."""
        w = top_wedge()
        assert w.total_score >= 80

    def test_top_wedge_matches_first_of_rank_verticals(self) -> None:
        w = top_wedge()
        ranked = rank_verticals()
        assert w.sector == ranked[0].sector
        assert w.total_score == ranked[0].total_score
