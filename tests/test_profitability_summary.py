"""V10 — profitability_summary computes margins from example inputs (assumptions only)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
_SCRIPT = REPO / "scripts" / "profitability_summary.py"


def _load():
    spec = importlib.util.spec_from_file_location("profitability_summary", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_example_inputs_exist() -> None:
    assert (REPO / "data" / "profitability_inputs.example.jsonl").is_file()
    assert (REPO / "config" / "profitability_model_schema.json").is_file()


def test_summarize_margins_and_assumption_flag() -> None:
    mod = _load()
    rows = mod.load_inputs(REPO / "data" / "profitability_inputs.example.jsonl")
    summary = mod.summarize(rows)
    assert "ASSUMPTION" in summary["disclaimer"].upper()
    assert len(summary["items"]) == 5
    sprint = next(i for i in summary["items"] if i["offer"] == "sprint_499")
    assert sprint["gross_margin"] == 499 - 180
    assert sprint["is_assumption"] is True


def test_main_writes_markdown(tmp_path: Path) -> None:
    mod = _load()
    out = tmp_path / "PROFITABILITY_SUMMARY.md"
    rc = mod.main(["--out", str(out)])
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    assert "Profitability Summary" in text
    assert "ASSUMPTION" in text.upper()
    # ROI is only ever referenced in the negative (policy: no guaranteed ROI).
    assert "no guaranteed roi" in text.lower()


def test_below_floor_is_flagged(tmp_path: Path) -> None:
    mod = _load()
    rows = [
        {
            "offer": "sprint_499",
            "currency": "SAR",
            "price": 100,
            "delivery_cost": 50,
            "units": 1,
            "is_assumption": True,
        }
    ]
    summary = mod.summarize(rows)
    assert "below_pricing_floor" in summary["items"][0]["flags"]
