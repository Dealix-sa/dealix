"""
Unit tests for api/routers/content_calendar.py

Tests cover:
- Annual events: 6 events, bilingual, campaign windows
- Ramadan strategy: 4 weeks, week 4 avoid sales, post-Eid window
- Monthly themes: 12 months, bilingual, all have focus/content_type
- Router metadata: prefix, tags
"""
from __future__ import annotations

import pytest

from api.routers.content_calendar import (
    _ANNUAL_EVENTS,
    _RAMADAN_CONTENT_STRATEGY,
    _MONTHLY_THEMES,
    router,
)


class TestAnnualEvents:
    def test_six_events(self):
        assert len(_ANNUAL_EVENTS) == 6

    def test_all_have_bilingual_names(self):
        for e in _ANNUAL_EVENTS:
            assert e.get("event"), f"Missing event name: {e}"
            assert e.get("event_ar"), f"Missing event_ar: {e['event']}"

    def test_all_have_gregorian_dates(self):
        for e in _ANNUAL_EVENTS:
            assert 1 <= e["gregorian_month"] <= 12
            assert 1 <= e["gregorian_day"] <= 31

    def test_all_have_campaign_windows(self):
        for e in _ANNUAL_EVENTS:
            assert e["campaign_window_days_before"] >= 0
            assert e["campaign_window_days_after"] >= 0

    def test_founding_day_feb_22(self):
        founding = next(e for e in _ANNUAL_EVENTS if "Founding" in e["event"])
        assert founding["gregorian_month"] == 2
        assert founding["gregorian_day"] == 22

    def test_national_day_sep_23(self):
        nd = next(e for e in _ANNUAL_EVENTS if "National Day" in e["event"])
        assert nd["gregorian_month"] == 9
        assert nd["gregorian_day"] == 23

    def test_leap_conference_february(self):
        leap = next(e for e in _ANNUAL_EVENTS if "LEAP" in e["event"])
        assert leap["gregorian_month"] == 2

    def test_q1_budget_january(self):
        q1 = next(e for e in _ANNUAL_EVENTS if "Q1" in e["event"])
        assert q1["gregorian_month"] == 1

    def test_zatca_present(self):
        zatca = next((e for e in _ANNUAL_EVENTS if "ZATCA" in e["event"]), None)
        assert zatca is not None

    def test_fintech_forum_present(self):
        fintech = next((e for e in _ANNUAL_EVENTS if "Fintech" in e["event"] or "FinTech" in e["event"]), None)
        assert fintech is not None

    def test_all_have_b2b_opportunity(self):
        for e in _ANNUAL_EVENTS:
            assert e.get("b2b_opportunity_en"), f"{e['event']} missing b2b_opportunity_en"
            assert e.get("b2b_opportunity_ar"), f"{e['event']} missing b2b_opportunity_ar"

    def test_all_have_content_ideas(self):
        for e in _ANNUAL_EVENTS:
            assert len(e.get("content_ideas", [])) >= 2, f"{e['event']} needs ≥2 content ideas"

    def test_national_day_requires_arabic_first(self):
        nd = next(e for e in _ANNUAL_EVENTS if "National Day" in e["event"])
        avoid_text = (nd.get("avoid_en") or "").lower()
        assert "arabic" in avoid_text

    def test_leap_has_verify_dates_note(self):
        leap = next(e for e in _ANNUAL_EVENTS if "LEAP" in e["event"])
        avoid_text = (leap.get("avoid_en") or leap.get("avoid_ar") or "").lower()
        assert "verify" in avoid_text or "تحقق" in avoid_text

    def test_zatca_no_legal_claims_guidance(self):
        zatca = next(e for e in _ANNUAL_EVENTS if "ZATCA" in e["event"])
        avoid_en = (zatca.get("avoid_en") or "").lower()
        assert "legal" in avoid_en or "tax advisor" in avoid_en or "consult" in avoid_en

    def test_event_types_are_known(self):
        valid_types = {"national_holiday", "industry_event", "business_cycle", "compliance_deadline"}
        for e in _ANNUAL_EVENTS:
            assert e["type"] in valid_types, f"{e['event']} has unknown type: {e['type']}"

    def test_month_filter_works(self):
        feb_events = [e for e in _ANNUAL_EVENTS if e["gregorian_month"] == 2]
        assert len(feb_events) >= 2  # Founding Day + LEAP


class TestRamadanStrategy:
    def test_four_weeks(self):
        assert len(_RAMADAN_CONTENT_STRATEGY["weeks"]) == 4

    def test_weeks_numbered_1_to_4(self):
        weeks = [w["week"] for w in _RAMADAN_CONTENT_STRATEGY["weeks"]]
        assert weeks == [1, 2, 3, 4]

    def test_all_weeks_have_bilingual_themes(self):
        for w in _RAMADAN_CONTENT_STRATEGY["weeks"]:
            assert w.get("theme_en"), f"Week {w['week']} missing theme_en"
            assert w.get("theme_ar"), f"Week {w['week']} missing theme_ar"

    def test_all_weeks_have_content_approach(self):
        for w in _RAMADAN_CONTENT_STRATEGY["weeks"]:
            assert w.get("content_approach_en"), f"Week {w['week']} missing content_approach_en"
            assert w.get("content_approach_ar"), f"Week {w['week']} missing content_approach_ar"

    def test_week1_no_sales_pitches(self):
        week1 = _RAMADAN_CONTENT_STRATEGY["weeks"][0]
        avoid = (week1.get("avoid") or "").lower()
        assert "sales" in avoid

    def test_week4_no_cold_sales_eid(self):
        week4 = _RAMADAN_CONTENT_STRATEGY["weeks"][3]
        avoid = (week4.get("avoid") or "").lower()
        assert "sales" in avoid or "cold" in avoid

    def test_has_post_eid_window(self):
        assert "post_eid_window" in _RAMADAN_CONTENT_STRATEGY

    def test_post_eid_window_bilingual(self):
        pew = _RAMADAN_CONTENT_STRATEGY["post_eid_window"]
        assert pew.get("timing_en")
        assert pew.get("timing_ar")
        assert pew.get("strategy_en")
        assert pew.get("strategy_ar")

    def test_post_eid_strategy_mentions_b2b(self):
        strategy = _RAMADAN_CONTENT_STRATEGY["post_eid_window"]["strategy_en"].lower()
        assert "b2b" in strategy or "executive" in strategy or "budget" in strategy

    def test_all_weeks_have_cadence(self):
        for w in _RAMADAN_CONTENT_STRATEGY["weeks"]:
            assert w.get("post_cadence"), f"Week {w['week']} missing post_cadence"


class TestMonthlyThemes:
    def test_twelve_months(self):
        assert len(_MONTHLY_THEMES) == 12

    def test_months_1_to_12(self):
        months = [t["month"] for t in _MONTHLY_THEMES]
        assert months == list(range(1, 13))

    def test_all_have_bilingual_themes(self):
        for t in _MONTHLY_THEMES:
            assert t.get("theme_en"), f"Month {t['month']} missing theme_en"
            assert t.get("theme_ar"), f"Month {t['month']} missing theme_ar"

    def test_all_have_focus(self):
        for t in _MONTHLY_THEMES:
            assert t.get("focus"), f"Month {t['month']} missing focus"

    def test_all_have_content_type(self):
        for t in _MONTHLY_THEMES:
            assert t.get("content_type"), f"Month {t['month']} missing content_type"

    def test_february_mentions_leap(self):
        feb = next(t for t in _MONTHLY_THEMES if t["month"] == 2)
        assert "LEAP" in feb["theme_en"] or "LEAP" in feb["focus"]

    def test_september_mentions_national_day(self):
        sep = next(t for t in _MONTHLY_THEMES if t["month"] == 9)
        assert "National" in sep["theme_en"] or "national" in sep["focus"].lower()

    def test_ramadan_month_community_focus(self):
        # Ramadan is typically March-April; month 3 or 4 should reference it
        mar = next(t for t in _MONTHLY_THEMES if t["month"] == 3)
        assert "ramadan" in mar["theme_en"].lower() or "community" in mar["focus"].lower()

    def test_q4_push_october(self):
        oct_theme = next(t for t in _MONTHLY_THEMES if t["month"] == 10)
        assert "Q4" in oct_theme["theme_en"] or "sales" in oct_theme["content_type"].lower()

    def test_january_new_year_planning(self):
        jan = next(t for t in _MONTHLY_THEMES if t["month"] == 1)
        assert "plan" in jan["theme_en"].lower() or "budget" in jan["focus"].lower()


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/content-calendar"

    def test_router_tags(self):
        assert "Sales" in router.tags
