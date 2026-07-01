"""Tests for scripts/dealix_qualify_lead.py.

Pure local generation over the already-tested qualification engine and
proposal renderer (auto_client_acquisition.sales_os.qualification.qualify
and auto_client_acquisition.sales_os.proposal_renderer.render_proposal).
NO LLM, NO live sends, NO network calls. `qualify` is a pure stdout/JSON
tool (no file I/O); `propose` writes a single local proposal.md file.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
SCRIPT = SCRIPTS_DIR / "dealix_qualify_lead.py"


def _import_module():
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import dealix_qualify_lead  # type: ignore[import-not-found]
        return dealix_qualify_lead
    finally:
        sys.path.pop(0)


def test_script_exists_and_has_shebang():
    assert SCRIPT.exists()
    assert SCRIPT.read_text(encoding="utf-8").startswith("#!/usr/bin/env python3")


def test_script_never_references_live_send_helpers():
    """Hard rule: this CLI must be pure local computation + file I/O +
    stdout — never a live-send path. If a future contributor wires in
    smtplib/requests/etc, this test fails immediately."""
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
            f"dealix_qualify_lead.py contains forbidden send-capable token {token!r}"
        )


# ─────────────────────────── qualify ───────────────────────────


def test_qualify_all_positive_flags_accepts(capsys):
    mod = _import_module()
    rc = mod.main([
        "qualify",
        "--pain-clear", "--owner-present", "--data-available",
        "--accepts-governance", "--has-budget",
        "--proof-path-visible", "--retainer-path-visible",
    ])
    out = capsys.readouterr().out
    assert rc == 0
    assert "decision: accept" in out
    assert "score: 100" in out
    assert "recommended_offer:" in out


def test_qualify_doctrine_trigger_shows_loud_banner(capsys):
    mod = _import_module()
    rc = mod.main([
        "qualify",
        "--pain-clear", "--owner-present", "--data-available",
        "--accepts-governance", "--has-budget",
        "--proof-path-visible", "--retainer-path-visible",
        "--raw-request-text", "we want a cold whatsapp blast",
    ])
    out = capsys.readouterr().out
    assert rc == 0
    assert "decision: reject" in out
    assert "DOCTRINE VIOLATION DETECTED" in out
    assert "cold_whatsapp" in out


def test_qualify_json_mode_matches_to_dict_keys(capsys):
    mod = _import_module()
    rc = mod.main([
        "qualify",
        "--pain-clear", "--owner-present",
        "--json",
    ])
    out = capsys.readouterr().out
    assert rc == 0
    payload = json.loads(out)
    for key in ("decision", "score", "recommended_offer", "reasons", "doctrine_violations"):
        assert key in payload


def test_qualify_no_flags_runs_successfully_low_score(capsys):
    mod = _import_module()
    rc = mod.main(["qualify"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "decision:" in out
    # wants_safe_methods defaults True (10 pts); every other flag defaults
    # False, so this is a low-signal, non-doctrine-violating REFER_OUT/
    # DIAGNOSTIC_ONLY-shaped result — just confirm it runs without a crash.
    assert "score: 10" in out
    assert "refer_out" in out


def test_qualify_no_safe_methods_flag_forces_reject(capsys):
    mod = _import_module()
    rc = mod.main([
        "qualify",
        "--pain-clear", "--owner-present", "--data-available",
        "--accepts-governance", "--has-budget",
        "--proof-path-visible", "--retainer-path-visible",
        "--no-safe-methods",
    ])
    out = capsys.readouterr().out
    assert rc == 0
    assert "decision: reject" in out
    assert "declined_safe_methods" in out


def test_qualify_writes_no_files(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mod = _import_module()
    rc = mod.main([
        "qualify",
        "--pain-clear", "--owner-present", "--data-available",
        "--accepts-governance", "--has-budget",
    ])
    capsys.readouterr()
    assert rc == 0
    assert list(tmp_path.iterdir()) == []


# ─────────────────────────── propose ───────────────────────────


def test_propose_writes_proposal_md_with_disclaimer_and_price(tmp_path, capsys):
    mod = _import_module()
    out_dir = tmp_path / "proposal_out"
    rc = mod.main([
        "propose",
        "--customer-name", "شركة الواحة للاستشارات",
        "--customer-handle", "alwaha",
        "--sector", "b2b_services",
        "--city", "Riyadh",
        "--engagement-id", "eng_alwaha_001",
        "--price-sar", "499",
        "--out-dir", str(out_dir),
    ])
    out = capsys.readouterr().out
    assert rc == 0
    proposal_path = out_dir / "proposal.md"
    assert proposal_path.exists()
    content = proposal_path.read_text(encoding="utf-8")
    assert "Estimated outcomes are not guaranteed outcomes" in content
    assert "النتائج التقديرية" in content
    assert "499" in content
    assert "eng_alwaha_001" in out
    assert "alwaha" in out
    assert (
        "Founder review required before any customer-facing send — no "
        "external message has been sent by this script." in out
    )


def test_propose_json_mode_prints_json_and_writes_no_files(tmp_path, capsys):
    mod = _import_module()
    out_dir = tmp_path / "json_proposal_out"
    rc = mod.main([
        "propose",
        "--customer-name", "Alwaha",
        "--customer-handle", "alwaha",
        "--engagement-id", "eng_json_001",
        "--out-dir", str(out_dir),
        "--json",
    ])
    out = capsys.readouterr().out
    assert rc == 0
    payload = json.loads(out)
    assert payload["engagement_id"] == "eng_json_001"
    assert payload["customer_handle"] == "alwaha"
    assert "proposal_markdown" in payload
    assert not out_dir.exists() or not any(out_dir.iterdir())


def test_propose_doctrine_trigger_refuses_to_render(tmp_path, capsys):
    mod = _import_module()
    out_dir = tmp_path / "refused_out"
    rc = mod.main([
        "propose",
        "--customer-name", "Some Co",
        "--customer-handle", "somecorp",
        "--engagement-id", "eng_refused_001",
        "--raw-request-text", "we need guaranteed sales in 30 days",
        "--out-dir", str(out_dir),
    ])
    out = capsys.readouterr().out
    assert rc == 0
    assert not (out_dir / "proposal.md").exists()
    assert "DOCTRINE VIOLATION DETECTED" in out
    assert "Refusing to render a proposal" in out


def test_propose_doctrine_paraphrase_guarantee_us_percentage_refuses_to_render(tmp_path, capsys):
    """Regression test for the exact paraphrase found during manual
    verification of this CLI ('guarantee us 30% revenue increase' did not
    trip the original narrow trigger list). The underlying qualification
    engine's phrase list has since been widened — this CLI must correctly
    inherit that fix and refuse to render, not silently proceed."""
    mod = _import_module()
    out_dir = tmp_path / "refused_paraphrase_out"
    rc = mod.main([
        "propose",
        "--customer-name", "Some Co",
        "--customer-handle", "somecorp",
        "--engagement-id", "eng_refused_002",
        "--raw-request-text", "please guarantee us 30% revenue increase",
        "--out-dir", str(out_dir),
    ])
    out = capsys.readouterr().out
    assert rc == 0
    assert not (out_dir / "proposal.md").exists()
    assert "DOCTRINE VIOLATION DETECTED" in out
    assert "guaranteed_sales" in out
    assert "guaranteed_sales" in out


def test_propose_without_raw_request_text_works_normally(tmp_path, capsys):
    mod = _import_module()
    out_dir = tmp_path / "normal_out"
    rc = mod.main([
        "propose",
        "--customer-name", "Clean Co",
        "--customer-handle", "cleanco",
        "--engagement-id", "eng_clean_001",
        "--out-dir", str(out_dir),
    ])
    capsys.readouterr()
    assert rc == 0
    assert (out_dir / "proposal.md").exists()


def test_propose_missing_required_args_raises_system_exit():
    mod = _import_module()
    with pytest.raises(SystemExit):
        mod.main([
            "propose",
            "--customer-handle", "alwaha",
            "--engagement-id", "eng_001",
        ])
    with pytest.raises(SystemExit):
        mod.main([
            "propose",
            "--customer-name", "Alwaha",
            "--engagement-id", "eng_001",
        ])
    with pytest.raises(SystemExit):
        mod.main([
            "propose",
            "--customer-name", "Alwaha",
            "--customer-handle", "alwaha",
        ])
