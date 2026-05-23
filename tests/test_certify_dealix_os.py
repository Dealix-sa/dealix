"""Smoke tests for the Dealix OS certification orchestrator."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
ORCH = REPO / "scripts" / "certify_dealix_os.py"


def _populate_private_ops(root: Path) -> None:
    """Build a minimum-viable private-ops tree."""
    for sub in (
        "founder",
        "intelligence",
        "outreach",
        "sales",
        "finance",
        "runtime",
        "logs",
        "security",
        "delivery",
    ):
        (root / sub).mkdir(parents=True, exist_ok=True)


def _run_orchestrator(
    private_ops: Path, env_extra: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, str(ORCH), "--private-ops", str(private_ops)],
        capture_output=True,
        text=True,
        cwd=REPO,
        env=env,
    )


def test_orchestrator_writes_report_even_on_failures(tmp_path: Path) -> None:
    private_ops = tmp_path / "ops"
    _populate_private_ops(private_ops)

    result = _run_orchestrator(private_ops)
    # First run on an empty fixture must fail (no business evidence, etc.)
    # but the report itself must be written.
    assert result.returncode != 0
    report = private_ops / "founder" / "dealix_os_certification.md"
    assert report.is_file()
    text = report.read_text(encoding="utf-8")
    assert "Dealix OS Certification Report" in text
    assert "## Checks" in text


def test_orchestrator_emits_certification_line(tmp_path: Path) -> None:
    private_ops = tmp_path / "ops"
    _populate_private_ops(private_ops)

    result = _run_orchestrator(private_ops)
    assert "CERTIFICATION=" in result.stdout


@pytest.mark.parametrize(
    "level",
    ["CERTIFIED", "PARTIAL", "NOT CERTIFIED"],
)
def test_certification_level_value_is_known(level: str) -> None:
    # Sanity: the orchestrator only ever emits these three.
    assert level in {"CERTIFIED", "PARTIAL", "NOT CERTIFIED"}


def test_orchestrator_requires_private_ops_flag() -> None:
    result = subprocess.run(
        [sys.executable, str(ORCH)],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert result.returncode != 0
    assert "--private-ops" in result.stderr
