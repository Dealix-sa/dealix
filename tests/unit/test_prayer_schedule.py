"""
Unit tests for api/routers/prayer_schedule.py

Tests cover:
- City list structure and bilingual fields
- Prayer window computation logic
- Business window generation (morning/post-Dhuhr/afternoon slots)
- Known cities: Riyadh, Jeddah, Dammam, Mecca, Medina
- Time helpers: _time_to_minutes, _minutes_to_time
- Router metadata (prefix, tags)
"""
from __future__ import annotations

import pytest

from api.routers.prayer_schedule import (
    _CITIES,
    _PRAYER_NAMES,
    _compute_business_windows,
    _time_to_minutes,
    _minutes_to_time,
    router,
)


class TestTimeHelpers:
    def test_time_to_minutes_noon(self):
        assert _time_to_minutes("12:00") == 720

    def test_time_to_minutes_morning(self):
        assert _time_to_minutes("08:00") == 480

    def test_time_to_minutes_evening(self):
        assert _time_to_minutes("20:30") == 1230

    def test_minutes_to_time_noon(self):
        assert _minutes_to_time(720) == "12:00"

    def test_minutes_to_time_early(self):
        assert _minutes_to_time(60) == "01:00"

    def test_round_trip(self):
        for t in ("05:00", "12:10", "18:20", "19:50"):
            assert _minutes_to_time(_time_to_minutes(t)) == t


class TestCityData:
    def test_has_riyadh(self):
        assert "riyadh" in _CITIES

    def test_has_jeddah(self):
        assert "jeddah" in _CITIES

    def test_has_dammam(self):
        assert "dammam" in _CITIES

    def test_has_mecca(self):
        assert "mecca" in _CITIES

    def test_has_medina(self):
        assert "medina" in _CITIES

    def test_all_cities_have_bilingual_names(self):
        for city_id, city in _CITIES.items():
            assert city["name_ar"], f"{city_id} missing name_ar"
            assert city["name_en"], f"{city_id} missing name_en"

    def test_all_cities_have_six_prayer_times(self):
        required_keys = {"fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"}
        for city_id, city in _CITIES.items():
            assert required_keys == set(city["typical_windows"].keys()), city_id

    def test_all_cities_in_ast(self):
        for city_id, city in _CITIES.items():
            assert city["utc_offset"] == "+03:00"

    def test_prayer_times_are_ordered(self):
        # fajr < sunrise < dhuhr < asr < maghrib < isha
        order = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]
        for city_id, city in _CITIES.items():
            times = [_time_to_minutes(city["typical_windows"][p]) for p in order]
            assert times == sorted(times), f"{city_id} prayer times not ordered"


class TestPrayerNames:
    def test_six_prayers(self):
        assert len(_PRAYER_NAMES) == 6

    def test_all_have_ar_and_en(self):
        for p, names in _PRAYER_NAMES.items():
            assert "ar" in names and names["ar"]
            assert "en" in names and names["en"]

    def test_ramadan_is_ramadan(self):
        assert "رمضان" not in _PRAYER_NAMES  # Ramadan is a month, not a prayer


class TestBusinessWindowComputation:
    def _riyadh_windows(self):
        return _CITIES["riyadh"]["typical_windows"]

    def test_produces_at_least_two_windows(self):
        slots = _compute_business_windows(self._riyadh_windows())
        assert len(slots) >= 2

    def test_morning_window_present(self):
        slots = _compute_business_windows(self._riyadh_windows())
        labels = [s["label_en"] for s in slots]
        assert "Morning block" in labels

    def test_post_dhuhr_window_present(self):
        slots = _compute_business_windows(self._riyadh_windows())
        labels = [s["label_en"] for s in slots]
        assert "Post-Dhuhr block" in labels

    def test_all_windows_have_bilingual_labels(self):
        slots = _compute_business_windows(self._riyadh_windows())
        for slot in slots:
            assert "label_en" in slot and slot["label_en"]
            assert "label_ar" in slot and slot["label_ar"]

    def test_all_windows_have_start_end(self):
        slots = _compute_business_windows(self._riyadh_windows())
        for slot in slots:
            assert "start" in slot
            assert "end" in slot

    def test_morning_starts_at_0800(self):
        slots = _compute_business_windows(self._riyadh_windows())
        morning = next(s for s in slots if s["label_en"] == "Morning block")
        assert morning["start"] == "08:00"

    def test_morning_ends_before_dhuhr(self):
        windows = self._riyadh_windows()
        dhuhr = _time_to_minutes(windows["dhuhr"])
        slots = _compute_business_windows(windows)
        morning = next(s for s in slots if s["label_en"] == "Morning block")
        end_min = _time_to_minutes(morning["end"])
        assert end_min < dhuhr

    def test_quality_fields_present(self):
        slots = _compute_business_windows(self._riyadh_windows())
        for slot in slots:
            assert "quality" in slot
            assert slot["quality"] in ("excellent", "good", "fair")


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/prayer-schedule"

    def test_router_tags(self):
        assert "Saudi Market" in router.tags
