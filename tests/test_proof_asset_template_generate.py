"""Tests for the Proof Asset template generator (V7)."""

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


def test_templates_written() -> None:
    mod = _load("proof_asset_template_generate")
    result = mod.generate()
    out_dir = Path(result["out_dir"])
    for name in (
        "anonymized_case_template.md",
        "before_after_workflow_template.md",
        "proof_permission_checklist.md",
    ):
        assert (out_dir / name).exists(), name


def test_no_fake_claims_guardrail() -> None:
    mod = _load("proof_asset_template_generate")
    result = mod.generate()
    perm = (Path(result["out_dir"]) / "proof_permission_checklist.md").read_text(encoding="utf-8")
    assert "consent" in perm.lower()
