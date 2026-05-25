"""Tests for the Dealix CEO Operating System v2 — verifier + scripts."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"
PRIVATE = REPO_ROOT / "dealix-ops-private"


def _run(script: Path, *args: str, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        cwd=str(REPO_ROOT),
    )


def test_verifier_runs_without_crash() -> None:
    script = SCRIPTS / "verify_founder_ceo_architecture.py"
    assert script.exists(), "verify_founder_ceo_architecture.py must exist"
    proc = _run(script, "--json")
    # Exit code can be 0 (PASS) or 1 (FAIL) — both are valid.
    assert proc.returncode in (0, 1), f"unexpected exit {proc.returncode}: {proc.stderr}"
    data = json.loads(proc.stdout)
    assert set(data.keys()) >= {"verdict", "total", "passed", "failed", "failures"}
    assert data["verdict"] in {"PASS", "FAIL"}
    assert isinstance(data["total"], int) and data["total"] > 0
    assert isinstance(data["failures"], list)


def test_verifier_summary_mode() -> None:
    script = SCRIPTS / "verify_founder_ceo_architecture.py"
    proc = _run(script, "--summary")
    assert proc.returncode in (0, 1)
    # Strip ANSI before matching.
    out = re.sub(r"\x1b\[[0-9;]*m", "", proc.stdout).strip()
    assert "founder_ceo_architecture" in out
    assert "PASS" in out or "FAIL" in out


def test_business_score_runs() -> None:
    proc = _run(SCRIPTS / "ceo_business_score.py", "--json")
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert "overall" in data
    assert "dimensions" in data
    assert isinstance(data["dimensions"], list)
    assert len(data["dimensions"]) == 6
    expected_keys = {"dimension_en", "dimension_ar", "score", "note"}
    for d in data["dimensions"]:
        assert expected_keys <= set(d.keys())


def test_finance_snapshot_runs() -> None:
    proc = _run(SCRIPTS / "ceo_finance_snapshot.py", "--json")
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    expected = {
        "cash_collected_30d",
        "cash_collected_total",
        "pipeline_weighted",
        "mrr",
        "monthly_burn",
        "runway_months",
    }
    assert expected <= set(data.keys())


def test_stage_runs() -> None:
    proc = _run(SCRIPTS / "ceo_stage.py")
    assert proc.returncode == 0, proc.stderr
    text = proc.stdout
    # Should mention one of the four stage names.
    stage_names = ["Proof of Interest", "Proof of Conversion", "Proof of Delivery", "Proof of Retention"]
    assert any(name in text for name in stage_names), text


def test_stage_json_mode() -> None:
    proc = _run(SCRIPTS / "ceo_stage.py", "--json")
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert "stage_number" in data
    assert "name_en" in data and "name_ar" in data
    assert 1 <= data["stage_number"] <= 4


def test_master_dashboard_runs() -> None:
    proc = _run(SCRIPTS / "ceo_master_dashboard.py", timeout=60)
    assert proc.returncode == 0, proc.stderr
    assert "Dealix CEO Master Dashboard" in proc.stdout


def test_private_scaffold_present() -> None:
    assert PRIVATE.exists() and PRIVATE.is_dir()
    expected = [
        "founder",
        "pipeline",
        "sales",
        "sales/call_notes",
        "sales/proposal_notes",
        "revenue",
        "revenue/invoices",
        "revenue/receipts",
        "revenue/payments",
        "finance",
        "offers/revenue_sprint",
        "clients",
        "delivery",
        "delivery/samples",
        "delivery/research",
        "delivery/reports",
        "delivery/qa",
        "delivery/handoffs",
        "learning",
    ]
    for sub in expected:
        path = PRIVATE / sub
        assert path.exists() and path.is_dir(), f"missing dir: {sub}"

    # Required CSV templates with headers (no real data).
    csv_templates = [
        "revenue/cash_collected.csv",
        "revenue/pipeline_value.csv",
        "revenue/mrr_tracker.csv",
        "revenue/revenue_action_log.csv",
        "finance/expenses.csv",
        "pipeline/pipeline_tracker.csv",
        "learning/message_performance.csv",
        "learning/sector_performance.csv",
    ]
    for rel in csv_templates:
        p = PRIVATE / rel
        assert p.exists(), f"missing csv template: {rel}"
        first = p.read_text(encoding="utf-8").splitlines()[0]
        assert "," in first, f"csv lacks a header row: {rel}"


def test_makefile_has_ceo_targets() -> None:
    mk = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    for target in [
        "ceo-verify",
        "ceo-daily",
        "ceo-business-score",
        "ceo-stage",
        "ceo-finance",
        "ceo-dashboard",
        "ceo-weekly-close",
        "ceo-kill-defer",
        "ceo-audit",
        "ceo-help",
    ]:
        assert target in mk, f"Makefile missing CEO target: {target}"


def test_verifier_with_empty_csvs() -> None:
    # CEO scripts must not crash when CSVs are header-only.
    for script in (
        SCRIPTS / "ceo_business_score.py",
        SCRIPTS / "ceo_finance_snapshot.py",
        SCRIPTS / "ceo_stage.py",
    ):
        proc = _run(script)
        assert proc.returncode == 0, f"{script.name} crashed: {proc.stderr}"
