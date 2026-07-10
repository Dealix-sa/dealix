"""Tests for the single canonical Dealix Company OS runtime."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "commercial" / "run_canonical_company_os.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("canonical_company_os_test_module", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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
        "crm_kpi_pending": True,
    }
    action = module.revenue_next_action(status)
    assert "proof pack" in action


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
