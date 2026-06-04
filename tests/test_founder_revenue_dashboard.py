"""Tests for the Founder Revenue Dashboard (V7)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def test_dashboard_has_all_metrics() -> None:
    mod = _load("founder_revenue_dashboard")
    metrics = mod.build(date="2026-06-04")
    for key in (
        "drafts_generated_today",
        "founder_actions_today",
        "approved_manual_actions",
        "manual_sends_recorded",
        "positive_replies_recorded",
        "discovery_calls_booked",
        "diagnostics_sold",
        "pilots_proposed",
        "pilots_sold",
        "retainers_started",
        "pipeline_value_sar",
        "realized_revenue_sar",
        "top_vertical",
        "top_channel",
        "top_objection",
        "stuck_stage",
        "next_best_action",
    ):
        assert key in metrics, key


def test_outputs_written() -> None:
    mod = _load("founder_revenue_dashboard")
    mod.build(date="2026-06-04")
    base = ROOT / "outputs" / "revenue_dashboard"
    assert (base / "latest_dashboard.md").exists()
    assert (base / "latest_dashboard.json").exists()
