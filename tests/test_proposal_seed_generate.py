"""Tests for the Proposal Seed generator (V7)."""

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


def test_proposal_sections_present() -> None:
    mod = _load("proposal_seed_generate")
    content = mod.build(
        {"company": "Test Co", "vertical": "retail", "pain_angle": "x", "date": "2026-06-04"}
    )
    for heading in (
        "## Situation",
        "## Diagnosed pain",
        "## Scope",
        "## Price range SAR",
        "## Acceptance criteria",
        "## Next step",
    ):
        assert heading in content, heading


def test_proposal_is_review_only() -> None:
    mod = _load("proposal_seed_generate")
    result = mod.generate(
        {"company": "Test Co", "vertical": "retail", "date": "2026-06-04"}
    )
    content = Path(result["out_path"]).read_text(encoding="utf-8")
    assert "REVIEW ONLY" in content
    assert "manually" in content.lower()
