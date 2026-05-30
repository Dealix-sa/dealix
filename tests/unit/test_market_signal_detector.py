"""Unit tests for market_signal_detector."""

import pytest

from auto_client_acquisition.intelligence_os.market_signal_detector import (
    MarketSignal,
    SaudiFiscalQuarter,
    SignalType,
    TimingScore,
    detect_signals,
    score_timing,
)


class TestDetectSignals:
    def test_returns_list(self):
        signals = detect_signals({}, current_month=10)
        assert isinstance(signals, list)

    def test_always_includes_budget_cycle(self):
        signals = detect_signals({}, current_month=6)
        types = {s.signal_type for s in signals}
        assert SignalType.BUDGET_CYCLE in types

    def test_sorted_by_strength_descending(self):
        info = {"pain_expressed_recently": True, "recent_hire": True}
        signals = detect_signals(info, current_month=11)
        strengths = [s.strength for s in signals]
        assert strengths == sorted(strengths, reverse=True)

    def test_recent_hire_adds_trigger_signal(self):
        signals = detect_signals({"recent_hire": True}, current_month=6)
        types = {s.signal_type for s in signals}
        assert SignalType.TRIGGER_EVENT in types

    def test_funding_round_adds_growth_signal(self):
        signals = detect_signals({"funding_round": True}, current_month=6)
        types = {s.signal_type for s in signals}
        assert SignalType.GROWTH_SIGNAL in types

    def test_pain_expressed_adds_pain_acute(self):
        signals = detect_signals({"pain_expressed_recently": True}, current_month=6)
        types = {s.signal_type for s in signals}
        assert SignalType.PAIN_ACUTE in types

    def test_competitor_adds_competitive_signal(self):
        signals = detect_signals({"competitor_used": True}, current_month=6)
        types = {s.signal_type for s in signals}
        assert SignalType.COMPETITIVE in types

    def test_regulatory_adds_regulatory_signal(self):
        signals = detect_signals({"regulatory_pressure": True}, current_month=6)
        types = {s.signal_type for s in signals}
        assert SignalType.REGULATORY in types

    def test_high_growth_rate_adds_growth_signal(self):
        signals = detect_signals({"growth_rate_pct": 30}, current_month=6)
        types = {s.signal_type for s in signals}
        assert SignalType.GROWTH_SIGNAL in types

    def test_low_growth_rate_no_growth_signal(self):
        signals = detect_signals({"growth_rate_pct": 5}, current_month=6)
        growth_signals = [s for s in signals if s.signal_type == SignalType.GROWTH_SIGNAL]
        assert len(growth_signals) == 0

    def test_all_signals_have_bilingual_content(self):
        info = {
            "recent_hire": True, "funding_round": True,
            "pain_expressed_recently": True, "competitor_used": True,
        }
        signals = detect_signals(info, current_month=11)
        for s in signals:
            assert len(s.trigger_ar) > 0
            assert len(s.trigger_en) > 0
            assert len(s.recommended_action_ar) > 0


class TestSaudiBudgetCalendar:
    @pytest.mark.parametrize("month,expected_min", [
        (11, 90),   # November — peak
        (10, 85),   # October — high
        (2, 80),    # February — strong
        (8, 35),    # August — weakest
        (7, 40),    # July — low
    ])
    def test_budget_score_by_month(self, month: int, expected_min: int):
        signals = detect_signals({}, current_month=month)
        budget_signal = next(s for s in signals if s.signal_type == SignalType.BUDGET_CYCLE)
        assert budget_signal.strength >= expected_min


class TestScoreTiming:
    def test_returns_timing_score(self):
        signals = detect_signals({}, current_month=10)
        result = score_timing(signals, current_month=10)
        assert isinstance(result, TimingScore)

    def test_overall_bounded(self):
        signals = detect_signals({"pain_expressed_recently": True, "funding_round": True}, current_month=11)
        result = score_timing(signals, current_month=11)
        assert 0 <= result.overall <= 100

    def test_empty_signals_returns_default(self):
        result = score_timing([], current_month=6)
        assert result.overall == 30
        assert result.trigger_event_score == 0

    def test_q4_month_gives_correct_quarter(self):
        signals = detect_signals({}, current_month=11)
        result = score_timing(signals, current_month=11)
        assert result.fiscal_quarter == SaudiFiscalQuarter.Q4

    def test_q1_month_gives_correct_quarter(self):
        signals = detect_signals({}, current_month=2)
        result = score_timing(signals, current_month=2)
        assert result.fiscal_quarter == SaudiFiscalQuarter.Q1

    def test_optimal_window_constant(self):
        signals = detect_signals({}, current_month=6)
        result = score_timing(signals, current_month=6)
        assert "Q4" in result.optimal_window_ar or "Q4" in result.optimal_window_en

    def test_high_signals_yield_high_overall(self):
        info = {
            "pain_expressed_recently": True,
            "funding_round": True,
            "recent_hire": True,
        }
        signals = detect_signals(info, current_month=11)
        result = score_timing(signals, current_month=11)
        assert result.overall >= 70

    def test_verdict_strings_nonempty(self):
        signals = detect_signals({}, current_month=10)
        result = score_timing(signals, current_month=10)
        assert len(result.timing_verdict_ar) > 0
        assert len(result.timing_verdict_en) > 0
