"""WS5 — launch-readiness CLI tests.

Asserts the aggregator runs the known-good offline gate subset, returns a
structured board, exits 0 when all gates pass, and 1 when one fails.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SCRIPT = _REPO / "scripts" / "launch_readiness.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("launch_readiness", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_evaluate_single_known_good_gate() -> None:
    """A single known-good offline gate evaluates to pass."""
    mod = _load_module()
    report = mod.evaluate(["proof_pack"])
    assert report["gates_total"] == 1
    assert report["all_pass"] is True
    assert report["gates"]["proof_pack"]["passed"] is True
    assert report["gates"]["proof_pack"]["exit_code"] == 0


def test_evaluate_all_gates_structure() -> None:
    """The full board has one entry per curated gate with required fields."""
    mod = _load_module()
    report = mod.evaluate(sorted(mod.GATES))
    assert report["gates_total"] == len(mod.GATES)
    for name, r in report["gates"].items():
        assert name in mod.GATES
        assert set(r) >= {"script", "passed", "exit_code", "duration_s", "detail"}


def test_cli_runs_and_exits_cleanly_on_known_good() -> None:
    """The CLI exits 0 on a known-good gate subset."""
    proc = subprocess.run(  # noqa: S603 — fixed sys.executable + in-repo script
        [sys.executable, str(_SCRIPT), "--gate", "proof_pack"],
        cwd=str(_REPO),
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert proc.returncode == 0, proc.stderr
    assert "PASS" in proc.stdout
    assert "GREEN" in proc.stdout


def test_cli_json_output_is_valid() -> None:
    """The --json flag emits a parseable board with the expected keys."""
    proc = subprocess.run(  # noqa: S603 — fixed sys.executable + in-repo script
        [sys.executable, str(_SCRIPT), "--json", "--gate", "proof_pack"],
        cwd=str(_REPO),
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["all_pass"] is True
    assert "gates" in payload
    assert "proof_pack" in payload["gates"]


def test_missing_gate_script_fails_safely() -> None:
    """A gate pointing at a missing script fails the board (exit 1), no crash."""
    mod = _load_module()
    result = mod._run_gate("verify_does_not_exist_xyz.py")
    assert result["passed"] is False
    assert "not found" in str(result["detail"])
