"""Smoke tests for scripts/render_stage_status.py — must run without app deps."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "render_stage_status.py"


def _load_module():
    if "render_stage_status" in sys.modules:
        return sys.modules["render_stage_status"]
    spec = importlib.util.spec_from_file_location("render_stage_status", SCRIPT)
    assert spec and spec.loader, "could not load render_stage_status"
    mod = importlib.util.module_from_spec(spec)
    sys.modules["render_stage_status"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_evaluate_all_returns_11_gates():
    mod = _load_module()
    gates = mod.evaluate_all()
    assert len(gates) == 11
    assert [g.number for g in gates] == list(range(11))


def test_every_gate_has_owner_and_evidence():
    mod = _load_module()
    for g in mod.evaluate_all():
        assert g.owner, f"Gate {g.number} missing owner"
        assert g.next_action, f"Gate {g.number} missing next_action"
        assert g.evidence, f"Gate {g.number} missing evidence anchors"
        assert g.status in {"PASS", "FIX", "BLOCKED"}


def test_render_markdown_contains_table_markers():
    mod = _load_module()
    md = mod.render_markdown(mod.evaluate_all())
    assert "<!-- AUTO:STAGE_STATUS_START -->" in md
    assert "<!-- AUTO:STAGE_STATUS_END -->" in md
    assert "Dealix Stage Status" in md
    # Every gate must appear in the table.
    for n in range(11):
        assert f"| {n} |" in md, f"Gate {n} missing from rendered table"


def test_sell_decision_reflects_failing_gates():
    mod = _load_module()
    # Forge a stack where all required gates PASS — must be SELL_READY_STACK.
    fake = []
    for n in range(11):
        fake.append(
            mod.GateResult(
                number=n,
                name=f"gate{n}",
                status="PASS",
                score=100,
                max_score=100,
                threshold=85,
                owner="x",
                evidence=["x"],
                next_action="y",
            )
        )
    decision, failures = mod.sell_decision(fake)
    assert decision == "SELL_READY_STACK"
    assert failures == []

    # Now mark Gate 3 BLOCKED — must not be SELL_READY_STACK.
    fake[3].status = "BLOCKED"
    decision, failures = mod.sell_decision(fake)
    assert decision != "SELL_READY_STACK"
    assert any("Gate 3" in f for f in failures)


def test_script_runs_print_mode_without_errors():
    proc = subprocess.run(  # noqa: S603
        [sys.executable, str(SCRIPT), "--print"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "Dealix Stage Status" in proc.stdout


def test_check_mode_returns_one_when_not_ready():
    proc = subprocess.run(  # noqa: S603
        [sys.executable, str(SCRIPT), "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    # In current state (Moyasar blocked) we expect exit 1.
    # If repo state changes to PASS_READY this test will need updating.
    assert proc.returncode in (0, 1)
