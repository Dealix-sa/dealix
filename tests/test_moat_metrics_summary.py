"""V10 — moat_metrics_summary summarizes example moat metrics (assumptions only)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
_SCRIPT = REPO / "scripts" / "moat_metrics_summary.py"


def _load():
    spec = importlib.util.spec_from_file_location("moat_metrics_summary", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_example_inputs_exist() -> None:
    assert (REPO / "data" / "moat_metrics_inputs.example.jsonl").is_file()


def test_summarize_six_metrics() -> None:
    mod = _load()
    rows = mod.load_inputs(REPO / "data" / "moat_metrics_inputs.example.jsonl")
    summary = mod.summarize(rows)
    assert summary["metric_count"] == 6
    keys = {m["metric"] for m in summary["metrics"]}
    assert "delivery_reuse_rate" in keys
    assert "category_authority_score" in keys
    assert "ASSUMPTION" in summary["disclaimer"].upper()


def test_main_writes_markdown(tmp_path: Path) -> None:
    mod = _load()
    out = tmp_path / "MOAT.md"
    rc = mod.main(["--out", str(out)])
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    assert "Moat Metrics Summary" in text
    assert "ASSUMPTION" in text.upper()
