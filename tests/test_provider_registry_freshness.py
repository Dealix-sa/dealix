"""Tests for the provider registry freshness guard.

The `improve` skill's cheap executor selects models from
`data/ai/free_llm_provider_registry.json`; these tests pin the freshness
evaluation so a stale registry is caught before dispatch.
"""

from __future__ import annotations

import datetime as _dt
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "ops" / "check_provider_registry_freshness.py"

_spec = importlib.util.spec_from_file_location("provider_registry_freshness", MODULE_PATH)
assert _spec and _spec.loader
freshness = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(freshness)


def _registry(**over: object) -> dict:
    base = {
        "last_reviewed": "2026-07-05",
        "providers": [{"name": "OpenRouter"}, {"name": "Groq"}],
        "upstream_readme_sha_observed": "abc123",
    }
    base.update(over)
    return base


def test_fresh_registry_is_ok() -> None:
    status = freshness.evaluate(
        _registry(), today=_dt.date(2026, 7, 20), max_age=45
    )
    assert status["ok"] is True
    assert status["stale"] is False
    assert status["age_days"] == 15
    assert status["problems"] == []


def test_stale_registry_flagged() -> None:
    status = freshness.evaluate(
        _registry(), today=_dt.date(2026, 9, 1), max_age=45
    )
    assert status["ok"] is False
    assert status["stale"] is True
    assert status["age_days"] > 45


def test_missing_last_reviewed_is_problem() -> None:
    reg = _registry()
    reg.pop("last_reviewed")
    status = freshness.evaluate(reg, today=_dt.date(2026, 7, 20))
    assert status["ok"] is False
    assert any("last_reviewed" in p for p in status["problems"])


def test_missing_drift_anchor_is_problem() -> None:
    reg = _registry()
    reg.pop("upstream_readme_sha_observed")
    status = freshness.evaluate(reg, today=_dt.date(2026, 7, 20))
    assert status["ok"] is False
    assert any("drift anchor" in p for p in status["problems"])


def test_no_providers_is_problem() -> None:
    status = freshness.evaluate(
        _registry(providers=[]), today=_dt.date(2026, 7, 20)
    )
    assert status["ok"] is False
    assert any("no providers" in p for p in status["problems"])


def test_future_review_date_is_problem() -> None:
    status = freshness.evaluate(
        _registry(last_reviewed="2027-01-01"), today=_dt.date(2026, 7, 20)
    )
    assert status["ok"] is False
    assert any("future" in p for p in status["problems"])


def test_real_registry_parses_and_evaluates() -> None:
    """The committed registry must at least be well-formed for the guard."""
    status = freshness.evaluate(freshness.load_registry(), max_age=100000)
    # With an effectively infinite max age, only structural problems can fail it.
    assert status["problems"] == []
    assert status["providers"] > 0
