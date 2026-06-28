"""Test that the brain engine never makes deterministic future claims.

Scans all generated outputs (radar, memo, action plan, brain day summary) for
deterministic phrases and verifies scenario/confidence language is used
instead.
"""
from __future__ import annotations

import os
import sys

import pytest

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from scripts.brain.generate_30_day_action_plan import generate_30_day_action_plan
from scripts.brain.generate_future_radar import (
    DETERMINISTIC_PHRASES,
    generate_future_radar,
)
from scripts.brain.generate_weekly_board_memo import generate_weekly_board_memo
from scripts.brain.run_brain_day import run_brain_day


@pytest.fixture
def reports_dir(tmp_path):
    return str(tmp_path)


def _assert_no_deterministic(text: str) -> None:
    lowered = text.lower()
    for phrase in DETERMINISTIC_PHRASES:
        assert phrase not in lowered, (
            f"Deterministic phrase '{phrase}' found in brain output: ...{lowered[max(0, lowered.find(phrase)-20):lowered.find(phrase)+len(phrase)+20]}..."
        )


def test_future_radar_no_deterministic_claims():
    radar = generate_future_radar()
    _assert_no_deterministic(radar["note"])
    for horizon_data in radar["horizons"].values():
        for area_data in horizon_data.values():
            for scenario_data in area_data.values():
                _assert_no_deterministic(scenario_data["scenario"])
                assert scenario_data["confidence"] in ("low", "medium", "high")


def test_future_radar_rejects_deterministic_input():
    from scripts.brain.generate_future_radar import _scenario

    with pytest.raises(ValueError, match="deterministic phrase"):
        _scenario("This will happen.", "medium")


def test_action_plan_no_deterministic_claims(reports_dir):
    plan = generate_30_day_action_plan(reports_dir=reports_dir)
    _assert_no_deterministic(plan)


def test_weekly_memo_no_deterministic_claims(reports_dir):
    memo = generate_weekly_board_memo(reports_dir=reports_dir)
    _assert_no_deterministic(memo)


def test_brain_day_summary_no_deterministic_claims(reports_dir):
    result = run_brain_day(reports_dir=reports_dir)
    with open(result["reports"]["summary"], encoding="utf-8") as fh:
        summary = fh.read()
    _assert_no_deterministic(summary)


def test_radar_has_confidence_levels():
    radar = generate_future_radar()
    for horizon_data in radar["horizons"].values():
        for area_data in horizon_data.values():
            for scenario_data in area_data.values():
                assert "confidence" in scenario_data
                assert scenario_data["confidence"] in ("low", "medium", "high")
