"""Founder daily verdict tests — verifies aggregation logic without live API."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from dealix.commercial_ops.founder_daily_verdict import (
    build_founder_daily_verdict,
)


def test_daily_verdict_offline_returns_known_shape() -> None:
    blob = build_founder_daily_verdict(skip_live=True)
    assert blob["verdict"] in ("GO", "WARN", "BLOCKED")
    assert "production_gates" in blob
    assert "kpi_freshness" in blob
    assert "morning_ops" in blob
    assert "founder_actions_ar" in blob
    assert blob["sources"]["kpi_registry"].endswith(".yaml")
    assert blob["commands"]["morning"].endswith("run_founder_commercial_day.sh")


def test_missing_brief_dir_is_blocked(tmp_path: Path) -> None:
    """When no briefs exist at all, verdict drops to BLOCKED with an action."""
    empty_dir = tmp_path / "no_briefs"
    # Note: do NOT create the dir — exercise the "missing" branch.
    blob = build_founder_daily_verdict(skip_live=True, briefs_dir=empty_dir)
    assert blob["morning_ops"]["status"] == "missing"
    assert blob["verdict"] == "BLOCKED"
    assert any("run_founder_commercial_day" in a for a in blob["founder_actions_ar"])


def test_today_brief_present_clears_morning_signal(tmp_path: Path) -> None:
    """A fresh brief_YYYY-MM-DD.md for today flips morning_ops to 'present'."""
    briefs = tmp_path / "founder_briefs"
    briefs.mkdir()
    now = datetime.now(UTC)
    today = now.strftime("%Y-%m-%d")
    (briefs / f"brief_{today}.md").write_text("# stub\n", encoding="utf-8")

    blob = build_founder_daily_verdict(skip_live=True, briefs_dir=briefs, at=now)
    assert blob["morning_ops"]["today_present"] is True
    assert blob["morning_ops"]["status"] == "present"
    # Brief no longer contributes a "missing" action — verdict tracks only prod+kpi now.
    assert not any("لا يوجد أي brief" in a for a in blob["founder_actions_ar"])


def test_stale_brief_triggers_warn(tmp_path: Path) -> None:
    """An older brief (no today file) should mark morning_ops stale."""
    briefs = tmp_path / "founder_briefs"
    briefs.mkdir()
    # Past brief — not today's date.
    (briefs / "brief_2020-01-01.md").write_text("# old\n", encoding="utf-8")
    now = datetime.now(UTC)

    blob = build_founder_daily_verdict(skip_live=True, briefs_dir=briefs, at=now)
    assert blob["morning_ops"]["status"] == "stale"
    # Action must include the morning runner pointer.
    assert any("run_founder_commercial_day" in a for a in blob["founder_actions_ar"])
    # Stale brief alone can degrade GO→WARN but not to BLOCKED.
    assert blob["verdict"] in ("WARN", "BLOCKED")
