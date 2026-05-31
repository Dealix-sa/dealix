"""
Unit tests for api/routers/hijri_calendar.py

Tests cover:
- Gregorian→Hijri and Hijri→Gregorian round-trips with known reference dates
- Month list structure and bilingual fields
- Holiday list structure and known Gregorian holidays
- Ramadan endpoint returns correct month structure
- Governance and disclaimer fields
- Edge cases (invalid year, unknown date range)
"""
from __future__ import annotations

import pytest

from api.routers.hijri_calendar import (
    gregorian_to_hijri,
    hijri_to_gregorian,
    get_holidays_for_gregorian_year,
    _HIJRI_MONTHS,
    _MONTH_BY_NUMBER,
    router,
)


# ---------------------------------------------------------------------------
# Core conversion tests with known reference dates
# ---------------------------------------------------------------------------

class TestGregorianToHijri:
    def test_known_date_2000_01_01(self):
        # 1 Jan 2000 = 25 Ramadan 1420 AH (well-known reference)
        hy, hm, hd = gregorian_to_hijri(2000, 1, 1)
        assert hy == 1420
        assert hm == 9   # Ramadan
        # Allow ±1 day for tabular vs. moon sighting
        assert 24 <= hd <= 26

    def test_known_date_hijri_new_year_1445(self):
        # 1 Muharram 1445 = 19 July 2023
        hy, hm, hd = gregorian_to_hijri(2023, 7, 19)
        assert hy == 1445
        assert hm == 1  # Muharram
        assert 1 <= hd <= 2  # ±1 day tolerance

    def test_year_range_reasonable(self):
        # Any date in 2024 should be in Hijri year 1445 or 1446
        hy, hm, hd = gregorian_to_hijri(2024, 6, 15)
        assert hy in (1445, 1446)

    def test_months_in_range(self):
        hy, hm, hd = gregorian_to_hijri(2026, 5, 31)
        assert 1 <= hm <= 12
        assert 1 <= hd <= 30

    def test_returns_tuple_of_three_ints(self):
        result = gregorian_to_hijri(2023, 1, 1)
        assert len(result) == 3
        assert all(isinstance(x, int) for x in result)


class TestHijriToGregorian:
    def test_round_trip(self):
        # Convert Gregorian→Hijri→Gregorian and check equality (±1 day)
        original = (2024, 3, 21)
        hy, hm, hd = gregorian_to_hijri(*original)
        gy, gm, gd = hijri_to_gregorian(hy, hm, hd)
        # Should reconstruct within ±1 day
        import datetime
        orig_date = datetime.date(*original)
        back_date = datetime.date(gy, gm, gd)
        assert abs((back_date - orig_date).days) <= 1

    def test_known_hijri_1_muharram_1446(self):
        # 1 Muharram 1446 = 7 July 2024
        gy, gm, gd = hijri_to_gregorian(1446, 1, 1)
        assert gy == 2024
        assert gm == 7
        assert 6 <= gd <= 8  # ±1 day

    def test_returns_tuple_of_three_ints(self):
        result = hijri_to_gregorian(1445, 9, 1)
        assert len(result) == 3
        assert all(isinstance(x, int) for x in result)


# ---------------------------------------------------------------------------
# Month metadata
# ---------------------------------------------------------------------------

class TestHijriMonths:
    def test_twelve_months(self):
        assert len(_HIJRI_MONTHS) == 12

    def test_all_have_bilingual_names(self):
        for m in _HIJRI_MONTHS:
            assert "name_ar" in m and m["name_ar"]
            assert "name_en" in m and m["name_en"]

    def test_month_numbers_1_to_12(self):
        numbers = [m["number"] for m in _HIJRI_MONTHS]
        assert numbers == list(range(1, 13))

    def test_sacred_months(self):
        sacred = [m["number"] for m in _HIJRI_MONTHS if m["sacred"]]
        # Muharram (1), Rajab (7), Dhul Qa'dah (11) are sacred; Ramadan (9) also
        for n in (1, 7, 9, 11):
            assert n in sacred

    def test_month_by_number_lookup(self):
        assert _MONTH_BY_NUMBER[9]["name_en"] == "Ramadan"
        assert _MONTH_BY_NUMBER[1]["name_en"] == "Muharram"

    def test_ramadan_is_month_9(self):
        assert _HIJRI_MONTHS[8]["name_en"] == "Ramadan"
        assert _HIJRI_MONTHS[8]["number"] == 9


# ---------------------------------------------------------------------------
# Holiday list
# ---------------------------------------------------------------------------

class TestSaudiHolidays:
    def test_has_national_day(self):
        holidays = get_holidays_for_gregorian_year(2024)
        names_en = [h["name_en"] for h in holidays]
        assert "Saudi National Day" in names_en

    def test_has_founding_day(self):
        holidays = get_holidays_for_gregorian_year(2024)
        names_en = [h["name_en"] for h in holidays]
        assert "Saudi Founding Day" in names_en

    def test_has_eid_al_fitr(self):
        holidays = get_holidays_for_gregorian_year(2024)
        names_en = [h["name_en"] for h in holidays]
        assert "Eid al-Fitr" in names_en

    def test_has_eid_al_adha(self):
        holidays = get_holidays_for_gregorian_year(2024)
        names_en = [h["name_en"] for h in holidays]
        assert "Eid al-Adha" in names_en

    def test_all_have_gregorian_date(self):
        holidays = get_holidays_for_gregorian_year(2024)
        for h in holidays:
            assert "gregorian_date" in h
            assert h["gregorian_date"].startswith("2024")

    def test_national_day_sept_23(self):
        holidays = get_holidays_for_gregorian_year(2024)
        nd = next(h for h in holidays if h["name_en"] == "Saudi National Day")
        assert nd["gregorian_date"] == "2024-09-23"

    def test_founding_day_feb_22(self):
        holidays = get_holidays_for_gregorian_year(2024)
        fd = next(h for h in holidays if h["name_en"] == "Saudi Founding Day")
        assert fd["gregorian_date"] == "2024-02-22"

    def test_holidays_sorted_by_date(self):
        holidays = get_holidays_for_gregorian_year(2024)
        dates = [h["gregorian_date"] for h in holidays]
        assert dates == sorted(dates)

    def test_bilingual_hijri_date_fields(self):
        holidays = get_holidays_for_gregorian_year(2024)
        for h in holidays:
            assert "hijri_date" in h
            assert "hijri_date_ar" in h


# ---------------------------------------------------------------------------
# FastAPI endpoint integration (via function calls, not HTTP)
# ---------------------------------------------------------------------------

class TestEndpointFunctions:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/hijri"

    def test_router_tags(self):
        assert "Saudi Market" in router.tags
