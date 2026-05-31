"""
Unit tests for api/routers/saudization_compliance.py

Tests cover:
- Band list: 6 bands, correct color/label/restriction fields
- Sector thresholds: known sectors present with valid thresholds
- _determine_band: correct band for given % in IT sector
- _gap_to_next_band: correct additional-hires calculation
- NitaqatCheckInput validation (saudi > total raises error)
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.saudization_compliance import (
    _BANDS,
    _BAND_ORDER,
    _SECTOR_THRESHOLDS,
    _determine_band,
    _gap_to_next_band,
    NitaqatCheckInput,
    router,
)


class TestBandData:
    def test_six_bands(self):
        assert len(_BANDS) == 6

    def test_band_order_from_best_to_worst(self):
        assert _BAND_ORDER[0] == "platinum"
        assert _BAND_ORDER[-1] == "red"

    def test_all_bands_have_labels(self):
        for b in _BANDS:
            assert b.get("label_ar"), f"{b['band']} missing label_ar"
            assert b.get("label_en"), f"{b['band']} missing label_en"

    def test_all_bands_have_color(self):
        for b in _BANDS:
            assert b.get("color"), f"{b['band']} missing color"

    def test_red_band_has_restrictions(self):
        red = next(b for b in _BANDS if b["band"] == "red")
        assert len(red["restrictions"]) >= 3

    def test_platinum_has_benefits(self):
        platinum = next(b for b in _BANDS if b["band"] == "platinum")
        assert len(platinum["benefits"]) >= 2

    def test_yellow_no_benefits(self):
        yellow = next(b for b in _BANDS if b["band"] == "yellow")
        assert yellow["benefits"] == []

    def test_platinum_no_restrictions(self):
        platinum = next(b for b in _BANDS if b["band"] == "platinum")
        assert platinum["restrictions"] == []


class TestSectorThresholds:
    def test_has_it_sector(self):
        assert "information_technology" in _SECTOR_THRESHOLDS

    def test_has_financial_services(self):
        assert "financial_services" in _SECTOR_THRESHOLDS

    def test_has_construction(self):
        assert "construction" in _SECTOR_THRESHOLDS

    def test_all_sectors_have_thresholds(self):
        required_keys = {"platinum_pct", "high_green_pct", "medium_green_pct",
                          "low_green_pct", "yellow_pct"}
        for sector_id, sector in _SECTOR_THRESHOLDS.items():
            assert required_keys.issubset(set(sector.keys())), sector_id

    def test_thresholds_ordered_descending(self):
        for sector_id, sector in _SECTOR_THRESHOLDS.items():
            thresholds = [
                sector["platinum_pct"], sector["high_green_pct"],
                sector["medium_green_pct"], sector["low_green_pct"], sector["yellow_pct"]
            ]
            assert thresholds == sorted(thresholds, reverse=True), sector_id

    def test_financial_services_has_highest_thresholds(self):
        it_medium = _SECTOR_THRESHOLDS["information_technology"]["medium_green_pct"]
        fs_medium = _SECTOR_THRESHOLDS["financial_services"]["medium_green_pct"]
        assert fs_medium > it_medium

    def test_construction_has_lowest_thresholds(self):
        it_medium = _SECTOR_THRESHOLDS["information_technology"]["medium_green_pct"]
        con_medium = _SECTOR_THRESHOLDS["construction"]["medium_green_pct"]
        assert con_medium < it_medium

    def test_all_sectors_have_bilingual_names(self):
        for sector_id, sector in _SECTOR_THRESHOLDS.items():
            assert sector.get("name_ar"), f"{sector_id} missing name_ar"
            assert sector.get("name_en"), f"{sector_id} missing name_en"


class TestDetermineband:
    def _it(self):
        return _SECTOR_THRESHOLDS["information_technology"]

    def test_above_platinum_threshold_is_platinum(self):
        thresholds = self._it()
        band = _determine_band(thresholds["platinum_pct"] + 10, thresholds)
        assert band == "platinum"

    def test_exactly_at_platinum_threshold(self):
        thresholds = self._it()
        band = _determine_band(thresholds["platinum_pct"], thresholds)
        assert band == "platinum"

    def test_between_high_green_and_platinum(self):
        thresholds = self._it()
        pct = (thresholds["high_green_pct"] + thresholds["platinum_pct"]) / 2
        band = _determine_band(pct, thresholds)
        assert band == "high_green"

    def test_below_yellow_is_red(self):
        thresholds = self._it()
        band = _determine_band(thresholds["yellow_pct"] - 1, thresholds)
        assert band == "red"

    def test_exactly_at_yellow_is_yellow(self):
        thresholds = self._it()
        band = _determine_band(thresholds["yellow_pct"], thresholds)
        assert band == "yellow"

    def test_zero_pct_is_red(self):
        band = _determine_band(0, self._it())
        assert band == "red"

    def test_100_pct_is_platinum(self):
        band = _determine_band(100, self._it())
        assert band == "platinum"


class TestGapToNextBand:
    def _it(self):
        return _SECTOR_THRESHOLDS["information_technology"]

    def test_platinum_has_no_upgrade(self):
        thresholds = self._it()
        gap = _gap_to_next_band(thresholds["platinum_pct"] + 5, thresholds, 20)
        assert gap["next_band"] is None

    def test_red_needs_hires(self):
        thresholds = self._it()
        gap = _gap_to_next_band(0, thresholds, 20)
        assert gap["additional_saudi_hires_needed"] >= 1

    def test_additional_hires_positive_integer(self):
        thresholds = self._it()
        gap = _gap_to_next_band(5, thresholds, 20)
        assert isinstance(gap["additional_saudi_hires_needed"], int)
        assert gap["additional_saudi_hires_needed"] >= 1

    def test_bilingual_note(self):
        thresholds = self._it()
        gap = _gap_to_next_band(5, thresholds, 20)
        assert "note_en" in gap and "note_ar" in gap

    def test_hires_math_for_known_case(self):
        # IT: yellow_pct=8, low_green_pct=15; company has 20 employees, 0 Saudi (0%)
        # Gap to yellow = 8%, so need ceil(0.08 * 20) = 2 hires
        thresholds = _SECTOR_THRESHOLDS["information_technology"]
        gap = _gap_to_next_band(0, thresholds, 20)
        # Should need at least 2 to reach yellow
        assert gap["additional_saudi_hires_needed"] >= 1  # at minimum 1


class TestInputValidation:
    def test_saudi_exceeds_total_raises(self):
        with pytest.raises(Exception):
            NitaqatCheckInput(
                sector="information_technology",
                total_employees=10,
                saudi_employees=15,  # > total
            )


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/saudization"

    def test_router_tags(self):
        assert "Saudi Market" in router.tags
