"""Tests for the Diagnostic Pack generator (V7)."""

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


def test_diagnostic_pack_files() -> None:
    mod = _load("diagnostic_pack_generate")
    result = mod.generate(
        {
            "company": "Test Co",
            "vertical": "logistics",
            "pain_angle": "manual updates",
            "notes": "n/a",
            "selected_offer": "Paid Diagnostic",
            "date": "2026-06-04",
        }
    )
    out_dir = Path(result["out_dir"])
    for name in (
        "diagnostic_brief.md",
        "workflow_map.md",
        "risk_map.md",
        "pilot_recommendation.md",
        "proposal_seed.md",
        "handover_checklist.md",
    ):
        assert (out_dir / name).exists(), name


def test_no_guaranteed_roi() -> None:
    mod = _load("diagnostic_pack_generate")
    result = mod.generate(
        {
            "company": "Test Co2",
            "vertical": "retail",
            "pain_angle": "x",
            "notes": "",
            "selected_offer": "Paid Diagnostic",
            "date": "2026-06-04",
        }
    )
    brief = (Path(result["out_dir"]) / "diagnostic_brief.md").read_text(encoding="utf-8")
    assert "No guaranteed ROI" in brief
