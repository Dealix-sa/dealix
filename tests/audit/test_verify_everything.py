"""Smoke + behavioral tests for the master verifier and its sub-verifiers.

We do NOT assert PASS — these tests prove the verifier MACHINERY works
even when called against a synthetic broken state. The actual repo
state is tested by `make everything` in CI.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "scripts"


def run(script: Path, *args: str, cwd: Path = REPO) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=60,
    )


# ---------------------------------------------------------------------------
# 1. The verifier scripts exist, are syntactically valid, and respond to --help
# ---------------------------------------------------------------------------
VERIFIER_SCRIPTS = (
    "verify_everything.py",
    "verify_repo_completeness.py",
    "verify_non_empty_files.py",
    "verify_wiring.py",
    "verify_business_os.py",
    "verify_ai_governance_system.py",
    "verify_policy_as_code.py",
    "verify_agent_registry.py",
    "verify_machine_registry.py",
    "verify_eval_gate.py",
    "verify_prompt_output_quality.py",
    "verify_live_send_safety.py",
    "verify_railway_readiness.py",
    "verify_production_safety.py",
)


@pytest.mark.parametrize("name", VERIFIER_SCRIPTS)
def test_verifier_exists_and_compiles(name: str) -> None:
    p = SCRIPTS / name
    assert p.exists(), f"missing verifier: {name}"
    compile(p.read_text(encoding="utf-8"), str(p), "exec")


def test_master_verifier_emits_report_text() -> None:
    """verify_everything.py must produce a structured report we can parse."""
    proc = run(SCRIPTS / "verify_everything.py")
    # Whatever the verdict, the report header must appear.
    combined = (proc.stdout or "") + (proc.stderr or "")
    assert "DEALIX EVERYTHING VERIFICATION" in combined
    assert proc.returncode in (0, 1), f"unexpected exit: {proc.returncode}"


def test_master_verifier_emits_json() -> None:
    proc = run(SCRIPTS / "verify_everything.py", "--json")
    import json as _json
    payload = _json.loads(proc.stdout)
    assert "results" in payload
    assert "total_layers" in payload
    assert payload["total_layers"] == len(payload["results"])


def test_master_verifier_rejects_unknown_layer() -> None:
    proc = run(SCRIPTS / "verify_everything.py", "--layer", "no_such_layer")
    assert proc.returncode == 2, "unknown layer must exit 2"


# ---------------------------------------------------------------------------
# 2. Synthetic-failure tests: confirm verifiers DO fail on bad inputs
# ---------------------------------------------------------------------------
def test_non_empty_files_detects_stub(tmp_path: Path) -> None:
    """If a manifest-listed file is shorter than threshold, verifier must fail."""
    # Build a minimal fake repo
    fake_manifest = tmp_path / "dealix_manifest.yaml"
    fake_doc = tmp_path / "tiny.md"
    fake_doc.write_text("TODO: write this later", encoding="utf-8")
    fake_manifest.write_text(
        """
version: 2
name: test
owner: test
global_rules:
  min_doc_size_bytes: 600
  min_script_size_bytes: 500
  min_yaml_size_bytes: 200
layers:
  smoke:
    required_files:
      - tiny.md
""".strip(),
        encoding="utf-8",
    )

    # Copy the verifier into the fake repo at scripts/
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    src = SCRIPTS / "verify_non_empty_files.py"
    (scripts_dir / "verify_non_empty_files.py").write_text(
        src.read_text(encoding="utf-8"), encoding="utf-8"
    )

    proc = subprocess.run(
        [sys.executable, str(scripts_dir / "verify_non_empty_files.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 1, "stub file must trigger failure"
    assert "too_small" in (proc.stdout + proc.stderr) or "stub_marker" in (
        proc.stdout + proc.stderr
    )


def test_agent_registry_rejects_missing_kill_switch(tmp_path: Path) -> None:
    fake_repo = tmp_path
    (fake_repo / "registries").mkdir()
    bad = fake_repo / "registries" / "agent_registry.yaml"
    bad.write_text(
        """
version: 1
agents:
  bad_agent:
    owner: founder
    risk_class: A1
    eval_required: false
    audit_required: false
    allowed_write_targets: []
""".strip(),
        encoding="utf-8",
    )
    (fake_repo / "scripts").mkdir()
    src = SCRIPTS / "verify_agent_registry.py"
    (fake_repo / "scripts" / "verify_agent_registry.py").write_text(
        src.read_text(encoding="utf-8"), encoding="utf-8"
    )
    proc = subprocess.run(
        [sys.executable, str(fake_repo / "scripts" / "verify_agent_registry.py")],
        cwd=fake_repo,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 1, "missing kill_switch must trigger failure"
    assert "kill_switch" in (proc.stdout + proc.stderr)


def test_live_send_safety_flags_direct_send(tmp_path: Path) -> None:
    fake = tmp_path
    (fake / "api").mkdir()
    (fake / "scripts").mkdir()
    (fake / "docs" / "trust").mkdir(parents=True)

    # Gate doc exists and is complete.
    (fake / "docs" / "trust" / "LIVE_SEND_SAFETY_GATE.md").write_text(
        "approval policy audit suppression daily_limit mock_mode kill_switch\n" * 30,
        encoding="utf-8",
    )

    # But an api/ file contains a banned direct-send pattern.
    (fake / "api" / "bad.py").write_text(
        "def go():\n    send_whatsapp_direct('hi')\n",
        encoding="utf-8",
    )

    src = SCRIPTS / "verify_live_send_safety.py"
    (fake / "scripts" / "verify_live_send_safety.py").write_text(
        src.read_text(encoding="utf-8"), encoding="utf-8"
    )

    proc = subprocess.run(
        [sys.executable, str(fake / "scripts" / "verify_live_send_safety.py")],
        cwd=fake,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 1
    assert "direct_send_call" in (proc.stdout + proc.stderr)


# ---------------------------------------------------------------------------
# 3. The actual repo manifest must be discoverable by verify_everything.py
# ---------------------------------------------------------------------------
def test_master_verifier_finds_real_manifest() -> None:
    proc = run(SCRIPTS / "verify_everything.py", "--json")
    import json as _json
    payload = _json.loads(proc.stdout)
    # Manifest declares ~21 layers — guard against silent removal.
    assert payload["total_layers"] >= 15
