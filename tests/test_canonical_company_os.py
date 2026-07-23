"""Tests for the single canonical Dealix Company OS runtime."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from dealix.commercial_ops import first_paid_tracker

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "commercial" / "run_canonical_company_os.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("canonical_company_os_test_module", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _configure_tracker_paths(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    evidence = tmp_path / "evidence.csv"
    kpi = tmp_path / "kpi.yaml"
    dod = tmp_path / "dod.md"
    soft = tmp_path / "soft.yaml"
    kpi.write_text("status: synced\n", encoding="utf-8")
    dod.write_text("# DoD\n", encoding="utf-8")
    soft.write_text("status: ready\n", encoding="utf-8")
    monkeypatch.setattr(first_paid_tracker, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(first_paid_tracker, "EVIDENCE", evidence)
    monkeypatch.setattr(first_paid_tracker, "KPI_YAML", kpi)
    monkeypatch.setattr(first_paid_tracker, "DOD_DOC", dod)
    monkeypatch.setattr(first_paid_tracker, "SOFT_LAUNCH_TRACKER", soft)
    return evidence


def test_revenue_next_action_requires_payment_before_revenue() -> None:
    module = _load_module()
    status = {
        "payment_received_real": 0,
        "proof_pack_delivered_real": 0,
        "crm_kpi_pending": True,
    }
    action = module.revenue_next_action(status)
    assert "payment evidence" in action


def test_revenue_next_action_requires_proof_after_payment() -> None:
    module = _load_module()
    status = {
        "payment_received_real": 1,
        "proof_pack_delivered_real": 0,
        "payment_without_proof_companies": ["Alpha Co"],
        "matching_close_companies": [],
        "crm_kpi_pending": True,
    }
    action = module.revenue_next_action(status)
    assert "proof pack" in action
    assert "Alpha Co" in action


def test_first_close_requires_payment_and_proof_for_same_company(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    evidence = _configure_tracker_paths(monkeypatch, tmp_path)
    evidence.write_text(
        "event_id,event_date,event_type,company,notes\n"
        "pay-1,2026-07-11,payment_received,Alpha Co,real payment\n"
        "proof-1,2026-07-11,proof_pack_delivered,Beta Co,real delivery\n",
        encoding="utf-8",
    )

    status = first_paid_tracker.analyze_first_paid_diagnostic()

    assert status["payment_received_real"] == 1
    assert status["proof_pack_delivered_real"] == 1
    assert status["matching_close_real"] == 0
    assert status["matching_close_companies"] == []
    assert status["first_close_ready"] is False
    assert status["verdict"] == "IN_PROGRESS"


def test_first_close_accepts_normalized_same_company_evidence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    evidence = _configure_tracker_paths(monkeypatch, tmp_path)
    evidence.write_text(
        "event_id,event_date,event_type,company,notes\n"
        "pay-1,2026-07-11,payment_received,Alpha Co,real payment\n"
        "proof-1,2026-07-11,proof_pack_delivered,  alpha   co  ,real delivery\n",
        encoding="utf-8",
    )

    status = first_paid_tracker.analyze_first_paid_diagnostic()

    assert status["matching_close_real"] == 1
    assert status["matching_close_companies"] == ["Alpha Co"]
    assert status["first_close_ready"] is True
    assert status["verdict"] == "CLOSED"


def test_runtime_target_mode_rejects_missing_malformed_or_empty_data(tmp_path: Path) -> None:
    module = _load_module()
    targets = tmp_path / "targets.json"

    assert module._runtime_target_mode(targets) == "safe_seed_only"
    targets.write_text("{broken", encoding="utf-8")
    assert module._runtime_target_mode(targets) == "safe_seed_only"
    targets.write_text("{}", encoding="utf-8")
    assert module._runtime_target_mode(targets) == "safe_seed_only"
    targets.write_text("[]", encoding="utf-8")
    assert module._runtime_target_mode(targets) == "safe_seed_only"
    targets.write_text('[{"company_name": "Real warm target"}]', encoding="utf-8")
    assert module._runtime_target_mode(targets) == "runtime_data"


def test_unsafe_live_flag_halts_cycle(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    module = _load_module()
    monkeypatch.setenv("LIVE_OUTBOUND_ENABLED", "true")
    with pytest.raises(RuntimeError, match="LIVE_OUTBOUND_ENABLED"):
        module.run(limit=1, output_root=tmp_path)


def test_canonical_cycle_generates_evidence_backed_packet(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    module = _load_module()
    for name in module.FORBIDDEN_ENV_FLAGS:
        monkeypatch.delenv(name, raising=False)

    monkeypatch.setattr(
        module,
        "load_revenue_status",
        lambda: {
            "evidence_path": "evidence.csv",
            "total_events": 0,
            "real_company_events": 0,
            "invoice_sent_real": 0,
            "payment_received_real": 0,
            "proof_pack_delivered_real": 0,
            "matching_close_real": 0,
            "matching_close_companies": [],
            "payment_without_proof_companies": [],
            "proof_without_payment_companies": [],
            "crm_kpi_pending": True,
            "first_close_ready": False,
            "dod_doc": "dod.md",
            "verdict": "PIPELINE_OPEN",
            "revenue_ladder_ar": "test",
            "soft_launch_tracker": "tracker.yaml",
        },
    )

    payload = module.run(limit=2, output_root=tmp_path)

    assert payload["mode"] == "draft-only"
    assert payload["safety"]["external_send"] is False
    assert payload["safety"]["payment_capture"] is False
    assert payload["revenue_status"]["payment_received_real"] == 0
    assert payload["revenue_status"]["verdict"] == "PIPELINE_OPEN"
    assert payload["approval_queue"]
    assert all(item["status"] == "pending_founder_approval" for item in payload["approval_queue"])
    assert (tmp_path / "latest.json").is_file()
    assert (tmp_path / "latest.md").is_file()


def test_only_one_scheduled_company_os_workflow_after_consolidation() -> None:
    canonical = (ROOT / ".github" / "workflows" / "dealix-autonomous-company-os.yml").read_text(
        encoding="utf-8"
    )
    assert "run_canonical_company_os.py" in canonical
    assert 'cron: "0 5 * * *"' in canonical
    assert not (ROOT / ".github" / "workflows" / "self-operating-company-os.yml").exists()


def test_canonical_workflow_is_read_only_and_verified_before_merge() -> None:
    canonical = (ROOT / ".github" / "workflows" / "dealix-autonomous-company-os.yml").read_text(
        encoding="utf-8"
    )

    assert "pull_request:" in canonical
    assert "push:" in canonical
    assert "contents: read" in canonical
    assert "issues: write" not in canonical
    assert "pull-requests: write" not in canonical
    assert 'PRODUCTION_MUTATION_ENABLED: "false"' in canonical
    assert 'LIVE_PAYMENT_CAPTURE_ENABLED: "false"' in canonical
    assert "if: always()" in canonical
