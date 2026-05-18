"""Tests for the daily LLM cost alert (Launch Gate O4).

Validates:
- evaluate_spend verdict: under / at / over threshold
- breach is inclusive at the threshold (>= per gate O4 DoD)
- is_estimate=True (Article 8 — costs are estimates)
- build_report aggregates the costs payload without any network
- render_markdown is bilingual-safe and surfaces the verdict
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import daily_cost_alert as dca


def test_under_threshold_is_ok() -> None:
    v = dca.evaluate_spend(total_usd=3.50, threshold_usd=10.0)
    assert v["breached"] is False
    assert v["severity"] == "ok"
    assert v["headroom_usd"] == 6.5


def test_at_threshold_breaches_inclusive() -> None:
    """Gate O4 DoD: alert if daily spend > $10 — boundary is inclusive."""
    v = dca.evaluate_spend(total_usd=10.0, threshold_usd=10.0)
    assert v["breached"] is True
    assert v["severity"] == "alert"


def test_over_threshold_breaches() -> None:
    v = dca.evaluate_spend(total_usd=42.0, threshold_usd=10.0)
    assert v["breached"] is True
    assert v["headroom_usd"] == -32.0


def test_spend_is_marked_estimate() -> None:
    """Article 8 — every cost number is an estimate."""
    v = dca.evaluate_spend(total_usd=0.0, threshold_usd=10.0)
    assert v["is_estimate"] is True


def test_build_report_aggregates_without_network(monkeypatch) -> None:
    """build_report must not touch the network when _fetch_costs is stubbed."""
    fake = {
        "totals": {"usd": 12.3456, "calls": 7},
        "by_group": {"claude-sonnet-4-5": {"usd": 12.3456, "calls": 7}},
    }
    monkeypatch.setattr(dca, "_fetch_costs", lambda **_: fake)
    report = dca.build_report(
        window_hours=24,
        threshold_usd=10.0,
        api_base="http://unused",
        api_key=None,
        admin_key=None,
    )
    assert report["gate"] == "O4"
    assert report["breached"] is True
    assert report["calls"] == 7
    assert report["total_usd"] == 12.3456


def test_render_markdown_surfaces_verdict() -> None:
    report = {
        "gate": "O4",
        "generated_at": "2026-05-18T06:00:00+00:00",
        "window_hours": 24,
        "total_usd": 12.34,
        "threshold_usd": 10.0,
        "breached": True,
        "headroom_usd": -2.34,
        "severity": "alert",
        "is_estimate": True,
        "by_model": {"claude-sonnet-4-5": {"usd": 12.34, "calls": 7}},
        "calls": 7,
    }
    md = dca.render_markdown(report)
    assert "Daily Cost Alert" in md
    assert "ALERT" in md
    assert "claude-sonnet-4-5" in md
    assert "no auto-send" in md


def test_unreachable_api_raises_runtime_error(monkeypatch) -> None:
    """A network failure surfaces as RuntimeError (mapped to exit code 2)."""

    def _boom(**_):
        raise RuntimeError("costs API unreachable at http://x: connection refused")

    monkeypatch.setattr(dca, "_fetch_costs", _boom)
    try:
        dca.build_report(
            window_hours=24,
            threshold_usd=10.0,
            api_base="http://x",
            api_key=None,
            admin_key=None,
        )
    except RuntimeError as exc:
        assert "unreachable" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected RuntimeError")
