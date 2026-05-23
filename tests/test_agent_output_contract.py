"""Tests for verify_agent_outputs.py against the agent output contract."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "verify_agent_outputs.py"
SCHEMA = REPO / "dealix/contracts/schemas/agent_output_contract.schema.json"
OUTPUT_DIR = REPO / "outputs" / "agents"


VALID_OUTPUT = {
    "summary": "Approved outreach drafted for top 3 ERP accounts.",
    "evidence": ["intelligence/lead_intelligence_base.csv:row=14"],
    "risk_level": "Medium",
    "approval_class": "A2",
    "next_action": "Founder reviews drafts in approval_center.md.",
    "owner": "sales_agent_v1",
    "safe_to_use": "Needs Review",
}


@pytest.fixture
def clean_outputs_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    existing = list(OUTPUT_DIR.glob("*.json"))
    backup: dict[Path, str] = {p: p.read_text(encoding="utf-8") for p in existing}
    for p in existing:
        p.unlink()
    try:
        yield OUTPUT_DIR
    finally:
        for p in OUTPUT_DIR.glob("*.json"):
            p.unlink()
        for p, text in backup.items():
            p.write_text(text, encoding="utf-8")


def _run() -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=REPO,
        env=env,
    )


def test_schema_file_is_valid_json() -> None:
    data = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert "required" in data
    assert "summary" in data["required"]
    assert "approval_class" in data["required"]


def test_empty_dir_passes(clean_outputs_dir: Path) -> None:
    result = _run()
    assert result.returncode == 0
    assert "AGENT_OUTPUTS_READY=true" in result.stdout


def test_valid_output_passes(clean_outputs_dir: Path) -> None:
    (clean_outputs_dir / "valid.json").write_text(json.dumps(VALID_OUTPUT), encoding="utf-8")
    result = _run()
    assert result.returncode == 0, result.stdout + result.stderr
    assert "AGENT_OUTPUTS_READY=true" in result.stdout


def test_missing_required_field_fails(clean_outputs_dir: Path) -> None:
    bad = {k: v for k, v in VALID_OUTPUT.items() if k != "evidence"}
    (clean_outputs_dir / "bad.json").write_text(json.dumps(bad), encoding="utf-8")
    result = _run()
    assert result.returncode == 1
    assert "missing field evidence" in result.stdout


def test_invalid_enum_fails(clean_outputs_dir: Path) -> None:
    bad = dict(VALID_OUTPUT)
    bad["risk_level"] = "Catastrophic"
    (clean_outputs_dir / "bad_enum.json").write_text(json.dumps(bad), encoding="utf-8")
    result = _run()
    assert result.returncode == 1
    assert "invalid risk_level" in result.stdout


def test_a3_cannot_be_safe_to_use_yes(clean_outputs_dir: Path) -> None:
    bad = dict(VALID_OUTPUT)
    bad["approval_class"] = "A3"
    bad["safe_to_use"] = "Yes"
    (clean_outputs_dir / "a3_yes.json").write_text(json.dumps(bad), encoding="utf-8")
    result = _run()
    assert result.returncode == 1
    assert "A3 outputs must not be marked safe_to_use=Yes" in result.stdout


def test_malformed_json_fails(clean_outputs_dir: Path) -> None:
    (clean_outputs_dir / "broken.json").write_text("{ not json", encoding="utf-8")
    result = _run()
    assert result.returncode == 1
    assert "invalid JSON" in result.stdout
