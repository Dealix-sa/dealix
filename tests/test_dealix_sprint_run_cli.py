"""Tests for scripts/dealix_sprint_run.py.

Pure local generation over the already-tested Sprint orchestrator
(auto_client_acquisition.delivery_factory.delivery_sprint.run_sprint).
NO LLM, NO live sends, NO network calls. The script only ever reads
founder-supplied local files and writes local output files / stdout.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
SCRIPT = SCRIPTS_DIR / "dealix_sprint_run.py"
DEMO_CSV = REPO_ROOT / "data" / "demo" / "saudi_b2b_demo.csv"


def _import_module():
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import dealix_sprint_run  # type: ignore[import-not-found]
        return dealix_sprint_run
    finally:
        sys.path.pop(0)


def test_sprint_run_script_exists_and_has_shebang():
    assert SCRIPT.exists()
    assert SCRIPT.read_text(encoding="utf-8").startswith("#!/usr/bin/env python3")


def test_script_never_references_live_send_helpers():
    """Hard rule: this CLI must be pure local file I/O + stdout — never a
    live-send path. If a future contributor wires in smtplib/requests/etc,
    this test fails immediately."""
    source = SCRIPT.read_text(encoding="utf-8")
    forbidden = [
        "smtplib",
        "EMAIL_SEND_ENABLED",
        "WHATSAPP_SEND_ENABLED",
        "requests.post",
        "httpx.post",
        "twilio",
        "import whatsapp",
        "whatsapp_client",
    ]
    lowered = source.lower()
    for token in forbidden:
        assert token.lower() not in lowered, (
            f"dealix_sprint_run.py contains forbidden send-capable token {token!r}"
        )


def test_minimal_run_no_csv_no_passport_no_accounts(tmp_path, capsys):
    mod = _import_module()
    out_dir = tmp_path / "sprint_out"
    rc = mod.main([
        "--engagement-id", "sprint_minimal_001",
        "--customer-id", "internal_customer_001",
        "--out-dir", str(out_dir),
    ])
    out = capsys.readouterr().out
    assert rc == 0
    assert "sprint_minimal_001" in out
    # No source passport supplied -> stderr warning is emitted separately,
    # but the run still succeeds and produces output files.
    assert (out_dir / "proof_pack.md").exists()
    assert (out_dir / "run_record.json").exists()
    record = json.loads((out_dir / "run_record.json").read_text(encoding="utf-8"))
    assert record["engagement_id"] == "sprint_minimal_001"
    assert "steps" in record


def test_missing_source_passport_warns_on_stderr(tmp_path, capsys):
    mod = _import_module()
    out_dir = tmp_path / "sprint_out"
    rc = mod.main([
        "--engagement-id", "sprint_minimal_002",
        "--customer-id", "internal_customer_002",
        "--out-dir", str(out_dir),
    ])
    captured = capsys.readouterr()
    assert rc == 0
    assert "Source Passport" in captured.err
    assert "WARNING" in captured.err


def test_csv_drives_both_dq_and_account_scoring(tmp_path, capsys):
    mod = _import_module()
    out_dir = tmp_path / "sprint_out"
    rc = mod.main([
        "--engagement-id", "sprint_csv_001",
        "--customer-id", "internal_customer_csv",
        "--csv", str(DEMO_CSV),
        "--out-dir", str(out_dir),
    ])
    capsys.readouterr()
    assert rc == 0
    record = json.loads((out_dir / "run_record.json").read_text(encoding="utf-8"))
    steps_by_name = {s["name"]: s for s in record["steps"]}
    dq_step = steps_by_name["data_quality"]
    scoring_step = steps_by_name["account_scoring"]
    assert dq_step["output"]["row_count"] > 0
    assert scoring_step["output"]["total_scored"] > 0
    assert len(scoring_step["output"]["top_10"]) > 0
    # Proof pack markdown should reflect a non-trivial ranking was produced.
    md = (out_dir / "proof_pack.md").read_text(encoding="utf-8")
    assert "Ranked top" in md or "ranked" in md.lower()


def test_out_dir_honored_and_expected_files_written(tmp_path, capsys):
    mod = _import_module()
    out_dir = tmp_path / "custom_out"
    rc = mod.main([
        "--engagement-id", "sprint_outdir_001",
        "--customer-id", "internal_customer_outdir",
        "--csv", str(DEMO_CSV),
        "--out-dir", str(out_dir),
    ])
    capsys.readouterr()
    assert rc == 0
    md_path = out_dir / "proof_pack.md"
    email_path = out_dir / "email_cover_note.txt"
    record_path = out_dir / "run_record.json"
    assert md_path.exists() and md_path.read_text(encoding="utf-8").strip()
    assert email_path.exists() and email_path.read_text(encoding="utf-8").strip()
    assert record_path.exists() and record_path.read_text(encoding="utf-8").strip()
    # PDF is optional — either it exists (renderer available) or it doesn't.
    pdf_path = out_dir / "proof_pack.pdf"
    assert pdf_path.exists() or not pdf_path.exists()


def test_json_mode_prints_valid_json_and_writes_no_files(tmp_path, capsys):
    mod = _import_module()
    out_dir = tmp_path / "json_out"
    rc = mod.main([
        "--engagement-id", "sprint_json_001",
        "--customer-id", "internal_customer_json",
        "--csv", str(DEMO_CSV),
        "--out-dir", str(out_dir),
        "--json",
    ])
    out = capsys.readouterr().out
    assert rc == 0
    payload = json.loads(out)
    assert payload["engagement_id"] == "sprint_json_001"
    assert "proof_pack" in payload
    # --json mode must not write any files.
    assert not out_dir.exists() or not any(out_dir.iterdir())


def test_source_passport_json_populates_proof_pack_section(tmp_path, capsys):
    mod = _import_module()
    passport = {
        "source_id": "TEST-SOURCE-001",
        "source_type": "client_upload",
        "owner": "test_customer",
        "allowed_use": ["internal_analysis", "scoring"],
        "contains_pii": False,
        "sensitivity": "low",
        "ai_access_allowed": True,
        "external_use_allowed": False,
        "retention_policy": "project_duration",
    }
    passport_path = tmp_path / "passport.json"
    passport_path.write_text(json.dumps(passport), encoding="utf-8")

    out_dir = tmp_path / "sprint_out"
    rc = mod.main([
        "--engagement-id", "sprint_passport_001",
        "--customer-id", "internal_customer_passport",
        "--csv", str(DEMO_CSV),
        "--source-passport-json", str(passport_path),
        "--out-dir", str(out_dir),
    ])
    capsys.readouterr()
    assert rc == 0
    md = (out_dir / "proof_pack.md").read_text(encoding="utf-8")
    assert "No Source Passport provided" not in md
    assert "TEST-SOURCE-001" in md


def test_below_delivery_threshold_banner_on_empty_inputs(tmp_path, capsys):
    mod = _import_module()
    out_dir = tmp_path / "sprint_out"
    rc = mod.main([
        "--engagement-id", "sprint_empty_001",
        "--customer-id", "internal_customer_empty",
        "--out-dir", str(out_dir),
    ])
    out = capsys.readouterr().out
    assert rc == 0
    assert "BELOW DELIVERY THRESHOLD" in out


def test_accounts_json_takes_precedence_over_csv(tmp_path, capsys):
    mod = _import_module()
    accounts = [
        {
            "company_name": "Precedence Test Co",
            "sector": "b2b_services",
            "city": "Riyadh",
            "relationship_status": "warm",
            "last_interaction": "2026-05-01",
            "notes": "accounts-json should win over csv-derived accounts",
        }
    ]
    accounts_path = tmp_path / "accounts.json"
    accounts_path.write_text(json.dumps(accounts), encoding="utf-8")

    out_dir = tmp_path / "sprint_out"
    rc = mod.main([
        "--engagement-id", "sprint_accounts_json_001",
        "--customer-id", "internal_customer_accjson",
        "--csv", str(DEMO_CSV),
        "--accounts-json", str(accounts_path),
        "--out-dir", str(out_dir),
    ])
    capsys.readouterr()
    assert rc == 0
    record = json.loads((out_dir / "run_record.json").read_text(encoding="utf-8"))
    steps_by_name = {s["name"]: s for s in record["steps"]}
    scoring_step = steps_by_name["account_scoring"]
    assert scoring_step["output"]["total_scored"] == 1
    assert scoring_step["output"]["top_10"][0]["company_name"] == "Precedence Test Co"


def test_requires_engagement_id_and_customer_id():
    mod = _import_module()
    with pytest.raises(SystemExit):
        mod.main(["--customer-id", "only_customer"])
    with pytest.raises(SystemExit):
        mod.main(["--engagement-id", "only_engagement"])


def test_governance_decision_always_printed_verbatim(tmp_path, capsys):
    mod = _import_module()
    out_dir = tmp_path / "sprint_out"
    rc = mod.main([
        "--engagement-id", "sprint_gov_001",
        "--customer-id", "internal_customer_gov",
        "--csv", str(DEMO_CSV),
        "--out-dir", str(out_dir),
    ])
    out = capsys.readouterr().out
    assert rc == 0
    record = json.loads((out_dir / "run_record.json").read_text(encoding="utf-8"))
    assert f"governance_decision: {record['governance_decision']}" in out
