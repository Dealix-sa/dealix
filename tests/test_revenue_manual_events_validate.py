"""Tests for the manual revenue events ledger validator (V7)."""

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


def test_example_ledger_valid() -> None:
    mod = _load("revenue_manual_events_validate")
    ok, errors = mod.validate(ROOT / "data" / "revenue_manual_events.example.jsonl")
    assert ok, errors


def test_invalid_event_type_rejected(tmp_path) -> None:
    mod = _load("revenue_manual_events_validate")
    bad = tmp_path / "bad.jsonl"
    bad.write_text(
        '{"event_id":"E1","created_at":"x","event_type":"AUTO_SEND",'
        '"company":"c","vertical":"v","source_draft_id":"d","channel":"email",'
        '"amount_sar":0,"stage_before":"raw_lead","stage_after":"researched",'
        '"notes":"n","founder_initials":"BA"}\n',
        encoding="utf-8",
    )
    ok, errors = mod.validate(bad)
    assert not ok
    assert any("invalid event_type" in e for e in errors)
