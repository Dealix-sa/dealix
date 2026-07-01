"""Tests for scripts/dealix_startup_release_gate.py.

Verifies the gate runs cleanly, produces valid JSON, and emits PASS
verdict when the repo is in a sound state. No network calls; no live
charge APIs.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GATE_SCRIPT = ROOT / "scripts" / "dealix_startup_release_gate.py"


def test_gate_script_exists():
    assert GATE_SCRIPT.is_file(), f"Missing gate script: {GATE_SCRIPT}"


def test_gate_runs_and_exits_zero():
    result = subprocess.run(
        [sys.executable, str(GATE_SCRIPT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"Gate exited {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


def test_gate_emits_pass_verdict():
    result = subprocess.run(
        [sys.executable, str(GATE_SCRIPT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert "STARTUP_RELEASE_GATE_VERDICT=PASS" in result.stdout, (
        f"Expected PASS verdict in output:\n{result.stdout}"
    )


def test_gate_writes_valid_json_reports(tmp_path, monkeypatch):
    """Gate writes valid JSON to all 4 report dirs."""
    import importlib.util
    import types

    spec = importlib.util.spec_from_file_location("dealix_startup_release_gate", GATE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Patch output dirs to tmp_path
    monkeypatch.setattr(module, "OUT_DIR", tmp_path / "startup_release_gate")
    monkeypatch.setattr(module, "STARTUP_OUT_DIR", tmp_path / "startup_command_center")
    monkeypatch.setattr(module, "BRIEF_OUT_DIR", tmp_path / "founder_daily_brief")
    monkeypatch.setattr(module, "PROOF_OUT_DIR", tmp_path / "startup_proof_pack")

    rc = module.main(strict=False)
    assert rc == 0

    for sub in ["startup_release_gate", "startup_command_center", "founder_daily_brief", "startup_proof_pack"]:
        report_path = tmp_path / sub / "latest.json"
        assert report_path.exists(), f"Missing report: {report_path}"
        data = json.loads(report_path.read_text())
        assert "generated_at" in data
        assert data.get("is_estimate") is True


def test_gate_service_catalog_check():
    """Service catalog check should pass — 17 offerings registered."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("dealix_startup_release_gate", GATE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module._check("SERVICE_CATALOG", module.check_service_catalog)
    assert result["status"] == "PASS"
    assert "17" in result["detail"]


def test_gate_hard_gates_check():
    """All 17 offerings must enforce no_live_send."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("dealix_startup_release_gate", GATE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module._check("HARD_GATES", module.check_hard_gates)
    assert result["status"] == "PASS"


def test_gate_client_template_check():
    """All 6 client template phases must be present."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("dealix_startup_release_gate", GATE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module._check("CLIENT_TEMPLATE", module.check_client_template)
    assert result["status"] == "PASS"
    assert "6" in result["detail"]
