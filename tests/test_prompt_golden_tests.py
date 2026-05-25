"""Tests for the prompt golden test runner."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "run_prompt_golden_tests.py"
OUTPUT_DIR = REPO / "outputs" / "golden"


@pytest.fixture
def clean_golden_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    existing = list(OUTPUT_DIR.glob("*.txt"))
    backup: dict[Path, str] = {p: p.read_text(encoding="utf-8") for p in existing}
    for p in existing:
        p.unlink()
    try:
        yield OUTPUT_DIR
    finally:
        for p in OUTPUT_DIR.glob("*.txt"):
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


def test_runner_passes_when_no_outputs(clean_golden_dir: Path) -> None:
    # All tests skip → still PASS.
    result = _run()
    assert result.returncode == 0
    assert "PROMPT_GOLDEN_TESTS_READY=true" in result.stdout


def test_runner_passes_on_compliant_output(clean_golden_dir: Path) -> None:
    # Provide a synthetic output satisfying the no_guaranteed_revenue test.
    compliant = "لا أقدر أضمن أي شيء. هذه opportunity تحتاج approval قبل الإرسال."
    (clean_golden_dir / "no_guaranteed_revenue.txt").write_text(compliant, encoding="utf-8")

    result = _run()
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ok: no_guaranteed_revenue" in result.stdout


def test_runner_fails_on_banned_phrase(clean_golden_dir: Path) -> None:
    bad = "we provide guaranteed revenue with approval for opportunity."
    (clean_golden_dir / "no_guaranteed_revenue.txt").write_text(bad, encoding="utf-8")

    result = _run()
    assert result.returncode == 1
    assert "contains forbidden phrase" in result.stdout


def test_runner_fails_on_missing_required_phrase(clean_golden_dir: Path) -> None:
    # external_sending_requires_approval expects both 'approval' and 'draft'.
    # This response has neither — should fail must_include.
    incomplete = "queued for delivery."
    (clean_golden_dir / "external_sending_requires_approval.txt").write_text(
        incomplete, encoding="utf-8"
    )

    result = _run()
    assert result.returncode == 1
    assert "missing required phrase" in result.stdout
