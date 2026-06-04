"""Tests for the Weekly Board Report generator (V7)."""

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


def test_board_report_sections() -> None:
    mod = _load("weekly_board_report_generate")
    result = mod.generate(date="2026-06-04")
    content = Path(result["out_path"]).read_text(encoding="utf-8")
    for heading in (
        "## Executive summary",
        "## Revenue pipeline",
        "## Risks",
        "## Decisions needed",
        "## Cash/revenue assumptions",
        "## Next week plan",
    ):
        assert heading in content, heading


def test_board_report_no_assumed_numbers() -> None:
    mod = _load("weekly_board_report_generate")
    result = mod.generate(date="2026-06-04")
    content = Path(result["out_path"]).read_text(encoding="utf-8")
    assert "No assumed numbers" in content
