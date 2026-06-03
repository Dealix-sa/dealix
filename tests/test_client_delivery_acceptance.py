"""
Tests for scripts/checks/check_client_delivery_acceptance.py

Covers every public function in the check script using temporary JSONL files
so no real data files are modified.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Ensure repo root is importable
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.checks.check_client_delivery_acceptance import (
    check_acceptance_record_exists,
    check_acceptance_required_fields,
    check_health_score,
    check_required_inputs_complete,
    check_sign_off_exists,
    check_uat_record_exists,
    check_weekly_report_exists,
    client_slug,
    find_record_for_client,
    load_jsonl,
    main,
    run_checks,
)

# ── Fixtures ──────────────────────────────────────────────────────────────────

SAMPLE_ACCEPTANCE = {
    "client_id": "test-001",
    "client_name": "Test Corp",
    "system": "followup_recovery_os",
    "sprint": "sprint-1",
    "delivery_owner": "Owner",
    "client_reviewer": "Reviewer",
    "scope": ["item a", "item b"],
    "out_of_scope": [],
    "required_inputs": [
        {"name": "Lead list", "received": True, "date_received": "2026-05-20"},
        {"name": "Brand guide", "received": True, "date_received": "2026-05-21"},
    ],
    "deliverables": [
        {"name": "Playbook", "version": "v1.0", "status": "accepted"}
    ],
    "acceptance_criteria": [
        {"criterion": "All inputs received", "met": True}
    ],
    "approval_method": "email",
    "created_at": "2026-06-01T10:00:00Z",
}

SAMPLE_UAT = {
    "client_id": "test-001",
    "client_name": "Test Corp",
    "system": "followup_recovery_os",
    "uat_date": "2026-05-30",
    "reviewer_name": "Reviewer",
    "scenarios": [
        {
            "scenario_id": "UAT-001",
            "given": "lead created",
            "when_action": "24h pass",
            "then_expected": "follow-up triggers",
            "passed": True,
            "notes": "",
        }
    ],
    "overall_result": "passed",
    "revision_items": [],
    "created_at": "2026-05-30T14:00:00Z",
}

SAMPLE_SIGN_OFF = {
    "client_id": "test-001",
    "client_name": "Test Corp",
    "system": "followup_recovery_os",
    "sprint": "sprint-1",
    "version": "v1.0",
    "delivery_date": "2026-06-01",
    "delivered_outputs": ["Playbook v1.0"],
    "acceptance_criteria_met": [{"criterion": "All inputs received", "met": True}],
    "decision": "accepted",
    "approval_method": "email",
    "approval_source": "reviewer@test.com",
    "approval_summary": "Approved.",
    "approval_date": "2026-06-01",
    "signed_by": "Reviewer",
    "sign_off_date": "2026-06-01",
    "created_at": "2026-06-01T16:00:00Z",
}

SAMPLE_HEALTH = {
    "client_id": "test-001",
    "client_name": "Test Corp",
    "system": "followup_recovery_os",
    "scores": {
        "required_inputs": 15,
        "deliverables": 25,
        "acceptance_criteria": 25,
        "client_uat": 15,
        "sign_off": 10,
        "weekly_value_report": 10,
    },
    "total_score": 100,
    "status": "delivered_clean",
    "computed_at": "2026-06-01T17:00:00Z",
}


def _write_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


# ── load_jsonl ─────────────────────────────────────────────────────────────────

def test_load_jsonl_returns_empty_for_missing_file(tmp_path: Path) -> None:
    result = load_jsonl(tmp_path / "nonexistent.jsonl")
    assert result == []


def test_load_jsonl_parses_valid_records(tmp_path: Path) -> None:
    p = tmp_path / "sample.jsonl"
    p.write_text('{"key": "value"}\n{"key": "other"}\n', encoding="utf-8")
    result = load_jsonl(p)
    assert len(result) == 2
    assert result[0]["key"] == "value"


def test_load_jsonl_skips_blank_lines(tmp_path: Path) -> None:
    p = tmp_path / "sample.jsonl"
    p.write_text('\n{"key": "val"}\n\n', encoding="utf-8")
    result = load_jsonl(p)
    assert len(result) == 1


def test_load_jsonl_skips_malformed_lines(tmp_path: Path) -> None:
    p = tmp_path / "sample.jsonl"
    p.write_text('{"key": "val"}\nnot-json\n', encoding="utf-8")
    result = load_jsonl(p)
    assert len(result) == 1


# ── find_record_for_client ─────────────────────────────────────────────────────

def test_find_record_for_client_exact_match() -> None:
    records = [{"client_name": "Alpha Corp"}, {"client_name": "Beta Ltd"}]
    assert find_record_for_client(records, "Alpha Corp") == records[0]


def test_find_record_for_client_case_insensitive() -> None:
    records = [{"client_name": "Alpha Corp"}]
    assert find_record_for_client(records, "alpha corp") is not None


def test_find_record_for_client_returns_none_when_missing() -> None:
    records = [{"client_name": "Alpha Corp"}]
    assert find_record_for_client(records, "Gamma Inc") is None


def test_find_record_for_client_strips_whitespace() -> None:
    records = [{"client_name": "  Alpha Corp  "}]
    assert find_record_for_client(records, "Alpha Corp") is not None


# ── client_slug ────────────────────────────────────────────────────────────────

def test_client_slug_spaces_to_underscores() -> None:
    assert client_slug("Example Training Co") == "example_training_co"


def test_client_slug_hyphens_to_underscores() -> None:
    assert client_slug("Al-Rashidi Ltd") == "al_rashidi_ltd"


def test_client_slug_lowercases() -> None:
    assert client_slug("UPPER CASE") == "upper_case"


# ── check_acceptance_record_exists ─────────────────────────────────────────────

def test_check_acceptance_record_exists_pass(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = tmp_path / "client_acceptance.jsonl"
    _write_jsonl(p, SAMPLE_ACCEPTANCE)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "ACCEPTANCE_FILE", p)
    ok, msg = check_acceptance_record_exists("Test Corp")
    assert ok is True


def test_check_acceptance_record_exists_fail(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = tmp_path / "client_acceptance.jsonl"
    _write_jsonl(p, SAMPLE_ACCEPTANCE)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "ACCEPTANCE_FILE", p)
    ok, msg = check_acceptance_record_exists("Unknown Client")
    assert ok is False
    assert "Unknown Client" in msg


# ── check_acceptance_required_fields ──────────────────────────────────────────

def test_check_acceptance_required_fields_pass(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = tmp_path / "client_acceptance.jsonl"
    _write_jsonl(p, SAMPLE_ACCEPTANCE)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "ACCEPTANCE_FILE", p)
    ok, _ = check_acceptance_required_fields("Test Corp")
    assert ok is True


def test_check_acceptance_required_fields_fail_missing_scope(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import copy
    rec = copy.deepcopy(SAMPLE_ACCEPTANCE)
    rec["scope"] = []
    p = tmp_path / "client_acceptance.jsonl"
    _write_jsonl(p, rec)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "ACCEPTANCE_FILE", p)
    ok, msg = check_acceptance_required_fields("Test Corp")
    assert ok is False
    assert "scope" in msg


# ── check_required_inputs_complete ────────────────────────────────────────────

def test_check_required_inputs_complete_pass(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = tmp_path / "client_acceptance.jsonl"
    _write_jsonl(p, SAMPLE_ACCEPTANCE)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "ACCEPTANCE_FILE", p)
    ok, _ = check_required_inputs_complete("Test Corp")
    assert ok is True


def test_check_required_inputs_complete_fail_pending(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import copy
    rec = copy.deepcopy(SAMPLE_ACCEPTANCE)
    rec["required_inputs"][0]["received"] = False
    p = tmp_path / "client_acceptance.jsonl"
    _write_jsonl(p, rec)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "ACCEPTANCE_FILE", p)
    ok, msg = check_required_inputs_complete("Test Corp")
    assert ok is False
    assert "Lead list" in msg


def test_check_required_inputs_complete_fail_empty(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import copy
    rec = copy.deepcopy(SAMPLE_ACCEPTANCE)
    rec["required_inputs"] = []
    p = tmp_path / "client_acceptance.jsonl"
    _write_jsonl(p, rec)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "ACCEPTANCE_FILE", p)
    ok, msg = check_required_inputs_complete("Test Corp")
    assert ok is False


# ── check_uat_record_exists ────────────────────────────────────────────────────

def test_check_uat_record_exists_pass(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = tmp_path / "client_uat_results.jsonl"
    _write_jsonl(p, SAMPLE_UAT)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "UAT_FILE", p)
    ok, _ = check_uat_record_exists("Test Corp")
    assert ok is True


def test_check_uat_record_exists_fail(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = tmp_path / "client_uat_results.jsonl"
    _write_jsonl(p, SAMPLE_UAT)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "UAT_FILE", p)
    ok, _ = check_uat_record_exists("Nobody")
    assert ok is False


# ── check_sign_off_exists ──────────────────────────────────────────────────────

def test_check_sign_off_exists_pass(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = tmp_path / "client_sign_offs.jsonl"
    _write_jsonl(p, SAMPLE_SIGN_OFF)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "SIGN_OFF_FILE", p)
    ok, msg = check_sign_off_exists("Test Corp")
    assert ok is True
    assert "accepted" in msg


def test_check_sign_off_exists_fail_no_record(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = tmp_path / "client_sign_offs.jsonl"
    _write_jsonl(p, SAMPLE_SIGN_OFF)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "SIGN_OFF_FILE", p)
    ok, _ = check_sign_off_exists("Ghost Client")
    assert ok is False


def test_check_sign_off_exists_fail_no_decision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import copy
    rec = copy.deepcopy(SAMPLE_SIGN_OFF)
    del rec["decision"]
    p = tmp_path / "client_sign_offs.jsonl"
    _write_jsonl(p, rec)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "SIGN_OFF_FILE", p)
    ok, msg = check_sign_off_exists("Test Corp")
    assert ok is False
    assert "decision" in msg


# ── check_health_score ────────────────────────────────────────────────────────

def test_check_health_score_pass(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = tmp_path / "delivery_health_scores.jsonl"
    _write_jsonl(p, SAMPLE_HEALTH)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "HEALTH_SCORE_FILE", p)
    ok, _ = check_health_score("Test Corp")
    assert ok is True


def test_check_health_score_fail_below_threshold(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import copy
    rec = copy.deepcopy(SAMPLE_HEALTH)
    rec["total_score"] = 85
    p = tmp_path / "delivery_health_scores.jsonl"
    _write_jsonl(p, rec)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "HEALTH_SCORE_FILE", p)
    ok, msg = check_health_score("Test Corp")
    assert ok is False
    assert "85" in msg


def test_check_health_score_fail_no_record(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = tmp_path / "delivery_health_scores.jsonl"
    _write_jsonl(p, SAMPLE_HEALTH)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "HEALTH_SCORE_FILE", p)
    ok, _ = check_health_score("Missing Client")
    assert ok is False


def test_check_health_score_boundary_at_90(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import copy
    rec = copy.deepcopy(SAMPLE_HEALTH)
    rec["total_score"] = 90
    p = tmp_path / "delivery_health_scores.jsonl"
    _write_jsonl(p, rec)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "HEALTH_SCORE_FILE", p)
    ok, _ = check_health_score("Test Corp")
    assert ok is True


# ── check_weekly_report_exists ────────────────────────────────────────────────

def test_check_weekly_report_exists_pass(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    report_dir = tmp_path / "reports" / "delivery"
    report_dir.mkdir(parents=True)
    (report_dir / "client_test_corp_WEEKLY_2026-W22.md").write_text("report", encoding="utf-8")
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "REPORTS_DELIVERY_DIR", report_dir)
    ok, msg = check_weekly_report_exists("Test Corp")
    assert ok is True
    assert "WEEKLY" in msg


def test_check_weekly_report_exists_fail_no_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    report_dir = tmp_path / "reports" / "delivery"
    report_dir.mkdir(parents=True)
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "REPORTS_DELIVERY_DIR", report_dir)
    ok, msg = check_weekly_report_exists("Test Corp")
    assert ok is False


def test_check_weekly_report_exists_fail_no_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import scripts.checks.check_client_delivery_acceptance as mod
    monkeypatch.setattr(mod, "REPORTS_DELIVERY_DIR", tmp_path / "nonexistent")
    ok, _ = check_weekly_report_exists("Test Corp")
    assert ok is False


# ── run_checks (integration) ───────────────────────────────────────────────────

def _patch_all(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Patch all file paths to use temp directory with full valid data."""
    import scripts.checks.check_client_delivery_acceptance as mod

    acc_file = tmp_path / "client_acceptance.jsonl"
    uat_file = tmp_path / "client_uat_results.jsonl"
    so_file = tmp_path / "client_sign_offs.jsonl"
    hs_file = tmp_path / "delivery_health_scores.jsonl"
    report_dir = tmp_path / "reports" / "delivery"
    report_dir.mkdir(parents=True)

    _write_jsonl(acc_file, SAMPLE_ACCEPTANCE)
    _write_jsonl(uat_file, SAMPLE_UAT)
    _write_jsonl(so_file, SAMPLE_SIGN_OFF)
    _write_jsonl(hs_file, SAMPLE_HEALTH)
    (report_dir / "client_test_corp_WEEKLY_2026-W22.md").write_text("r", encoding="utf-8")

    monkeypatch.setattr(mod, "ACCEPTANCE_FILE", acc_file)
    monkeypatch.setattr(mod, "UAT_FILE", uat_file)
    monkeypatch.setattr(mod, "SIGN_OFF_FILE", so_file)
    monkeypatch.setattr(mod, "HEALTH_SCORE_FILE", hs_file)
    monkeypatch.setattr(mod, "REPORTS_DELIVERY_DIR", report_dir)


def test_run_checks_all_pass(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_all(monkeypatch, tmp_path)
    result = run_checks("Test Corp")
    assert result == 0


def test_run_checks_fail_unknown_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_all(monkeypatch, tmp_path)
    result = run_checks("Unknown Entity")
    assert result == 1


def test_main_returns_zero_for_valid_client(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_all(monkeypatch, tmp_path)
    result = main(["--client", "Test Corp"])
    assert result == 0


def test_main_returns_one_for_invalid_client(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_all(monkeypatch, tmp_path)
    result = main(["--client", "Ghost"])
    assert result == 1
