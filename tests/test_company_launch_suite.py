"""Company launch test suite."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

PYTHON = str(REPO_ROOT / ".venv" / "bin" / "python3") if (REPO_ROOT / ".venv" / "bin" / "python3").exists() else sys.executable


def run_script(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )


def test_no_auto_external_send_script() -> None:
    result = run_script([PYTHON, "scripts/verify_no_auto_external_send.py"])
    assert result.returncode == 0, result.stdout + result.stderr


def test_repo_large_files_script() -> None:
    result = run_script([PYTHON, "scripts/verify_repo_large_files.py"])
    assert result.returncode == 0, result.stdout + result.stderr


def test_secret_patterns_script() -> None:
    result = run_script([PYTHON, "scripts/verify_secret_patterns.py"])
    assert result.returncode == 0, result.stdout + result.stderr


def test_outreach_compliance_script() -> None:
    result = run_script([PYTHON, "scripts/verify_outreach_compliance.py"])
    assert result.returncode == 0, result.stdout + result.stderr


def test_company_launch_ready_script() -> None:
    result = run_script([PYTHON, "scripts/verify_company_launch_ready.py"])
    assert result.returncode == 0, result.stdout + result.stderr


def test_gmail_drafts_dry_run() -> None:
    result = run_script([PYTHON, "scripts/email/create_gmail_drafts_safe.py", "--outbox-dir", "outbox/2026-06-15"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DRY-RUN" in result.stdout


def test_command_room_builds() -> None:
    result = run_script([PYTHON, "scripts/command_room/build_command_room.py"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert (REPO_ROOT / "reports" / "command_room" / "index.html").exists()


def test_score_targets_deterministic() -> None:
    from scripts.revenue._lib import score_target

    row = {
        "company": "Test Co",
        "sector": "logistics",
        "city": "Riyadh",
        "website": "https://test.co",
        "public_contact": "info@test.co",
        "email": "info@test.co",
        "source_url": "https://test.co",
        "pain_hypothesis": "Orders are scattered and response time is slow",
        "offer_angle": "Command Center OS",
        "confidence": "0.7",
        "verification_status": "verified_public",
    }
    a = score_target(row)
    b = score_target(row)
    assert a == b
    assert a["tier"] == "hot"


def test_target_csv_validation() -> None:
    result = run_script([PYTHON, "scripts/revenue/find_targets_manual_workflow.py", "--validate", "data/outreach/research_queue.example.csv"])
    assert result.returncode == 0, result.stdout + result.stderr


def test_100_target_day_prepare_and_validate(tmp_path) -> None:
    batch_file = tmp_path / "ready_batch_test.csv"
    result = run_script([
        PYTHON, "scripts/revenue/prepare_100_target_day.py",
        "--input", "data/outreach/research_queue.example.csv",
        "--batch-size", "3",
        "--output", str(batch_file),
    ])
    assert result.returncode == 0, result.stdout + result.stderr
    result = run_script([PYTHON, "scripts/revenue/validate_100_target_day.py", "--input", str(batch_file)])
    assert result.returncode == 0, result.stdout + result.stderr


def test_batch_queue_respects_max_followups_and_cooldown() -> None:
    result = run_script([
        PYTHON,
        "scripts/revenue/batch_outreach_queue.py",
        "--input",
        "data/outreach/ready_batch_2026-06-15.csv",
        "--batch-size",
        "3",
        "--cooldown-days",
        "1",
        "--max-followups",
        "3",
    ])
    assert result.returncode == 0, result.stdout + result.stderr


def test_outreach_drafts_contain_opt_out() -> None:
    outbox = REPO_ROOT / "outbox" / "2026-06-15"
    if not outbox.exists():
        pytest.skip("No drafts generated")
    for path in outbox.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert any(word in text for word in ["إيقاف", "unsubscribe", "STOP", "إلغاء"]), f"{path} missing opt-out"


def test_followup_max_count_enforced() -> None:
    from scripts.revenue._lib import REPO_ROOT
    from scripts.revenue.generate_followups import count_followups

    out_dir = REPO_ROOT / "outbox" / "2026-06-15"
    out_dir.mkdir(parents=True, exist_ok=True)
    # Create dummy follow-up files for a slug
    slug = "testcompany"
    paths = []
    try:
        for i in range(1, 4):
            path = out_dir / f"{slug}_followup_d{i}.md"
            path.write_text(
                "Subject: follow-up\n\ntest\n\nإذا لم ترغب في التواصل أرسل إيقاف.",
                encoding="utf-8",
            )
            paths.append(path)
        assert count_followups(out_dir, slug) == 3
    finally:
        for path in paths:
            path.unlink(missing_ok=True)


def test_no_duplicate_daily_contact() -> None:
    result = run_script([PYTHON, "scripts/revenue/batch_outreach_queue.py", "--input", "data/outreach/ready_batch_2026-06-15.csv", "--batch-size", "3"])
    assert result.returncode == 0
    path = REPO_ROOT / "data" / "outreach" / "batch_queue_2026-06-15.csv"
    if path.exists():
        rows = list(csv.DictReader(path.open("r", encoding="utf-8-sig")))
        emails = [r["email"] for r in rows if r.get("email")]
        assert len(emails) == len(set(emails)), "Duplicate emails in batch queue"


def test_server_preflight_runs() -> None:
    result = run_script([PYTHON, "scripts/server/server_preflight.py"])
    # It may fail on missing env vars, but it must run without crashing.
    assert "Dealix Server Preflight" in result.stdout


def test_server_env_contract_runs() -> None:
    result = run_script([PYTHON, "scripts/server/verify_env_contract.py"])
    assert "Dealix Env Contract Verification" in result.stdout


def test_public_surfaces_documented() -> None:
    result = run_script([PYTHON, "scripts/server/verify_public_surfaces.py"])
    assert result.returncode == 0, result.stdout + result.stderr
    path = REPO_ROOT / "reports" / "server" / "public_surfaces.json"
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert "backend" in data
    assert "frontend" in data
