"""Tests for the Operating Memory schema validator (V7)."""

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


def test_schemas_valid() -> None:
    mod = _load("operating_memory_validate")
    ok, errors = mod.validate(ROOT / "config" / "operating_memory_schemas.json")
    assert ok, errors


def test_missing_field_detected(tmp_path) -> None:
    mod = _load("operating_memory_validate")
    bad = tmp_path / "bad.json"
    bad.write_text(
        '{"schemas":{"decision_memory":{"required":["memory_id","decision"]},'
        '"client_memory":{"required":["memory_id"]},'
        '"market_memory":{"required":["memory_id"]},'
        '"revenue_memory":{"required":["memory_id"]}},'
        '"examples":{"decision_memory":[{"memory_id":"d1"}]}}',
        encoding="utf-8",
    )
    ok, errors = mod.validate(bad)
    assert not ok
    assert any("missing required field 'decision'" in e for e in errors)
