"""Unit tests for the Dealix Implementation Audit system.

These tests pin the contract that audit_dealix_implementation.py, the
verifier scripts, the execution_engine package, and the dealix_cli package
all enforce. If any test here fails, the audit-as-source-of-truth promise
in DEALIX_IMPLEMENTATION_AUDIT.md is broken.
"""

from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


# ──────────────────────────────────────────────────────────────────────────
# Structure: required files for the audit to even be runnable
# ──────────────────────────────────────────────────────────────────────────


REQUIRED_PUBLIC_FILES = (
    "DEALIX_IMPLEMENTATION_AUDIT.md",
    "DEALIX_STAGE_GATED_ROADMAP.md",
    "DEALIX_30_DAY_EXECUTION_PLAN.md",
    "docs/revenue/REVENUE_COMMAND_CENTER.md",
    "docs/trust/TRUST_COMMAND_CENTER.md",
    "docs/delivery/revenue_sprint/REVENUE_SPRINT_FACTORY.md",
    "docs/offers/revenue_sprint/REVENUE_SPRINT_KIT.md",
    "docs/ops/OPERATING_READINESS_LEVELS.md",
    "docs/founder/GO_NO_GO_DECISION_SYSTEM.md",
    "docs/product/NO_OVERBUILD_POLICY.md",
    "docs/learning/LEARNING_LOOP.md",
    "execution_engine/__init__.py",
    "execution_engine/evidence_scanner.py",
    "execution_engine/stage_checklist_updater.py",
    "dealix_cli/__init__.py",
    "dealix_cli/__main__.py",
    "dealix_cli/commands.py",
    "scripts/audit_dealix_implementation.py",
    "templates/private_ops_audit_template.py",
    ".github/workflows/dealix-implementation-audit.yml",
)


@pytest.mark.parametrize("relative", REQUIRED_PUBLIC_FILES)
def test_required_file_exists(relative: str) -> None:
    path = REPO_ROOT / relative
    assert path.exists(), f"required file missing: {relative}"


REQUIRED_VERIFIERS = (
    "verify_tier0_safety.py",
    "verify_tier1_revenue.py",
    "verify_tier2_delivery.py",
    "verify_revenue_sprint_kit.py",
    "verify_execution_engine.py",
    "verify_stage_evidence_automation.py",
    "verify_stage_gated_roadmap.py",
    "verify_cli.py",
    "verify_dashboard_v2.py",
    "verify_weekly_automation.py",
    "verify_no_autonomous_external_actions.py",
    "verify_trust_boundary_terms.py",
)


@pytest.mark.parametrize("name", REQUIRED_VERIFIERS)
def test_verifier_exists_and_passes(name: str) -> None:
    path = REPO_ROOT / "scripts" / name
    assert path.exists(), f"missing verifier: {name}"
    result = subprocess.run([sys.executable, str(path)], cwd=REPO_ROOT, capture_output=True, text=True)
    assert result.returncode == 0, f"{name} failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"


# ──────────────────────────────────────────────────────────────────────────
# Audit script behaviour
# ──────────────────────────────────────────────────────────────────────────


def test_master_audit_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/audit_dealix_implementation.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"master audit failed:\n{result.stdout}\n{result.stderr}"
    assert "PASS: Dealix public implementation audit passed." in result.stdout


def test_master_audit_json_summary() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/audit_dealix_implementation.py", "--json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert '"passed": true' in result.stdout
    assert '"failures": []' in result.stdout


# ──────────────────────────────────────────────────────────────────────────
# CLI surface
# ──────────────────────────────────────────────────────────────────────────


def test_cli_help_lists_all_subcommands() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "dealix_cli", "--help"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    for sub in ("daily", "stage", "advance", "kit", "weekly-close", "audit", "init"):
        assert sub in result.stdout, f"subcommand `{sub}` missing from help"


def test_cli_init_creates_layout() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [sys.executable, "-m", "dealix_cli", "init", "--private-ops", tmp],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        for required in (
            "founder/decision_queue.md",
            "pipeline/pipeline_tracker.csv",
            "revenue/revenue_action_log.csv",
            "stage/current_stage.md",
            "stage/stage_exit_checklist.csv",
            "audit_private_ops.py",
        ):
            assert (Path(tmp) / required).exists(), f"init did not create {required}"


def test_cli_stage_on_empty_private_ops() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        # bootstrap
        subprocess.run(
            [sys.executable, "-m", "dealix_cli", "init", "--private-ops", tmp],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        result = subprocess.run(
            [sys.executable, "-m", "dealix_cli", "stage", "--private-ops", tmp],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Evidence Report" in result.stdout
        assert "stage `setup`" in result.stdout


# ──────────────────────────────────────────────────────────────────────────
# Execution engine
# ──────────────────────────────────────────────────────────────────────────


def test_evidence_scanner_fails_on_empty_pipeline(tmp_path: Path) -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from execution_engine import scan_evidence

    (tmp_path / "stage").mkdir()
    (tmp_path / "stage" / "current_stage.md").write_text("stage: pipeline\n", encoding="utf-8")
    report = scan_evidence(tmp_path)
    assert report.stage == "pipeline"
    assert not report.passed


def test_evidence_scanner_passes_with_25_leads(tmp_path: Path) -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from execution_engine import scan_evidence

    (tmp_path / "stage").mkdir()
    (tmp_path / "stage" / "current_stage.md").write_text("stage: pipeline\n", encoding="utf-8")
    (tmp_path / "pipeline").mkdir()
    with (tmp_path / "pipeline" / "pipeline_tracker.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "lead_name", "stage", "next_action"])
        writer.writeheader()
        for i in range(1, 26):
            writer.writerow({"id": str(i), "lead_name": f"lead_{i}", "stage": "new", "next_action": "research"})
    report = scan_evidence(tmp_path)
    assert report.passed, [r.detail for r in report.results]


def test_evidence_scanner_rejects_missing_next_action(tmp_path: Path) -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from execution_engine import scan_evidence

    (tmp_path / "stage").mkdir()
    (tmp_path / "stage" / "current_stage.md").write_text("stage: pipeline\n", encoding="utf-8")
    (tmp_path / "pipeline").mkdir()
    with (tmp_path / "pipeline" / "pipeline_tracker.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "lead_name", "stage", "next_action"])
        writer.writeheader()
        for i in range(1, 26):
            writer.writerow({"id": str(i), "lead_name": f"lead_{i}", "stage": "new", "next_action": ""})
    report = scan_evidence(tmp_path)
    assert not report.passed


def test_checklist_updater_marks_done(tmp_path: Path) -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from execution_engine import scan_evidence, update_checklist

    (tmp_path / "stage").mkdir()
    (tmp_path / "stage" / "current_stage.md").write_text("stage: pipeline\n", encoding="utf-8")
    (tmp_path / "pipeline").mkdir()
    with (tmp_path / "pipeline" / "pipeline_tracker.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "lead_name", "stage", "next_action"])
        writer.writeheader()
        for i in range(1, 26):
            writer.writerow({"id": str(i), "lead_name": f"lead_{i}", "stage": "new", "next_action": "research"})

    report = scan_evidence(tmp_path)
    checklist_path = tmp_path / "stage" / "stage_exit_checklist.csv"
    rows = update_checklist(checklist_path, report)
    assert checklist_path.exists()
    assert any(r.status == "done" for r in rows)


# ──────────────────────────────────────────────────────────────────────────
# Trust boundary doctrine
# ──────────────────────────────────────────────────────────────────────────


REQUIRED_TRUST_PHRASES = (
    "No external send is automated.",
    "approval_evidence must be a path",
    "force-push, hard-reset, branch deletion on shared branches",
)


@pytest.mark.parametrize("phrase", REQUIRED_TRUST_PHRASES)
def test_trust_doc_phrase_intact(phrase: str) -> None:
    trust_doc = (REPO_ROOT / "docs" / "trust" / "TRUST_COMMAND_CENTER.md").read_text(encoding="utf-8")
    assert phrase in trust_doc, f"trust phrase removed or weakened: {phrase!r}"


def test_no_autonomous_external_actions_in_audit_modules() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/verify_no_autonomous_external_actions.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout
