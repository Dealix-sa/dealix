"""SystemScorecard math."""
from __future__ import annotations

from control_plane.system_scorecard import score_system


def test_empty_signals_gives_zero():
    sc = score_system("trust", signals={})
    assert sc.score == 0
    assert sc.band == "ALERT"


def test_equal_weight_average():
    sc = score_system("trust", signals={"a": 1.0, "b": 0.0})
    assert sc.score == 50


def test_weighted_average_respects_weights():
    sc = score_system(
        "trust",
        signals={"a": 1.0, "b": 0.0},
        weights={"a": 9.0, "b": 1.0},
    )
    assert 85 <= sc.score <= 95


def test_band_thresholds():
    assert score_system("x", signals={"a": 0.95}).band == "HEALTHY"
    assert score_system("x", signals={"a": 0.70}).band == "WATCH"
    assert score_system("x", signals={"a": 0.10}).band == "ALERT"
