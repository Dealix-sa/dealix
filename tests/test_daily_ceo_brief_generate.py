"""Tests for the Daily CEO Brief generator (V7)."""

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


def test_ceo_brief_written() -> None:
    mod = _load("daily_ceo_brief_generate")
    result = mod.generate(date="2026-06-04")
    content = Path(result["out_path"]).read_text(encoding="utf-8")
    for heading in (
        "## Top 5 priorities",
        "## Revenue status",
        "## Safety status",
        "## What NOT to do today",
        "## Tomorrow focus",
    ):
        assert heading in content, heading


def test_ceo_brief_no_autosend() -> None:
    mod = _load("daily_ceo_brief_generate")
    result = mod.generate(date="2026-06-04")
    content = Path(result["out_path"]).read_text(encoding="utf-8")
    assert "Do not auto-send" in content
