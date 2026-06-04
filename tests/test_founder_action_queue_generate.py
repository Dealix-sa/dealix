"""Tests for the Founder Action Queue generator (V7)."""

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


def test_generates_action_queue(tmp_path) -> None:
    mod = _load("founder_action_queue_generate")
    result = mod.generate(date="2026-06-04", limit=10)
    assert result["actions"] == 10
    out_dir = Path(result["out_dir"])
    for name in (
        "founder_actions.csv",
        "founder_actions.md",
        "manual_send_queue.example.csv",
        "call_priority_list.md",
        "today_revenue_plan.md",
    ):
        assert (out_dir / name).exists(), name


def test_no_send_in_outputs() -> None:
    mod = _load("founder_action_queue_generate")
    result = mod.generate(date="2026-06-04", limit=5)
    plan = (Path(result["out_dir"]) / "today_revenue_plan.md").read_text(encoding="utf-8")
    assert "manually" in plan.lower()
