"""Regression tests for canonical Company OS target validation and fallback."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "commercial" / "run_canonical_company_os.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("canonical_company_os_target_fallback", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _revenue_status() -> dict[str, object]:
    return {
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
    }


@pytest.mark.parametrize(
    "raw_targets",
    [
        "[]",
        '["bad"]',
        '[{"company_name": "Broken score", "urgency": "not-a-number"}]',
    ],
)
def test_invalid_runtime_targets_force_nonempty_seed_packet(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    raw_targets: str,
) -> None:
    module = _load_module()
    for name in module.FORBIDDEN_ENV_FLAGS:
        monkeypatch.delenv(name, raising=False)

    feature = module.load_feature_module()
    data_root = tmp_path / "data"
    data_root.mkdir()
    (data_root / "targets.json").write_text(raw_targets, encoding="utf-8")
    feature.DATA_ROOT = data_root

    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "load_feature_module", lambda: feature)
    monkeypatch.setattr(module, "load_revenue_status", _revenue_status)

    payload = module.run(limit=2, output_root=tmp_path / "reports")

    assert payload["target_mode"] == "safe_seed_only"
    assert payload["opportunity_graph"]
    assert payload["approval_queue"]
    assert all(item["status"] == "pending_founder_approval" for item in payload["approval_queue"])
    assert any(item["area"] == "real_targets" for item in payload["priorities"])
    assert any(event["event"] == "target_input_validated" for event in payload["proof_log"])


def test_valid_runtime_targets_remain_runtime_data(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    module = _load_module()
    for name in module.FORBIDDEN_ENV_FLAGS:
        monkeypatch.delenv(name, raising=False)

    feature = module.load_feature_module()
    data_root = tmp_path / "data"
    data_root.mkdir()
    (data_root / "targets.json").write_text(
        '[{"company_name": "Approved Warm Co", "target_type": "inbound", "urgency": 90}]',
        encoding="utf-8",
    )
    feature.DATA_ROOT = data_root

    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "load_feature_module", lambda: feature)
    monkeypatch.setattr(module, "load_revenue_status", _revenue_status)

    payload = module.run(limit=2, output_root=tmp_path / "reports")

    assert payload["target_mode"] == "runtime_data"
    assert payload["opportunity_graph"][0]["company_name"] == "Approved Warm Co"
    assert not any(item["area"] == "real_targets" for item in payload["priorities"])
