"""Tests for the Revenue Execution OS verifier (V7)."""

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


def test_revenue_execution_verify_passes() -> None:
    mod = _load("revenue_execution_verify")
    result = mod.verify()
    assert result["status"] == "PASS", result
    assert result["checks"]["no_forbidden_send_patterns"] is True


def test_no_forbidden_send_in_generators() -> None:
    mod = _load("revenue_execution_verify")
    result = mod.verify()
    assert result["forbidden_hits"] == []
