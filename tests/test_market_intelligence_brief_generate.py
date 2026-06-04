"""Tests for the Market Intelligence Brief generator (V7)."""

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


def test_market_brief_written() -> None:
    mod = _load("market_intelligence_brief_generate")
    payload = mod.build(date="2026-06-04")
    assert payload["source"] == "manual_research_only"
    assert payload["verticals_tracked"] >= 1
    base = ROOT / "outputs" / "market_intelligence" / "2026-06-04"
    assert (base / "market_brief.md").exists()
    assert (base / "market_brief.json").exists()
