"""Tests for the Company Utilization verifier (V7)."""

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


def test_company_utilization_passes() -> None:
    mod = _load("company_utilization_verify")
    result = mod.verify()
    assert result["status"] == "PASS", result
    assert result["missing_generators"] == []
    assert result["missing_validators"] == []
