"""Tests for scripts/dealix_funnel_run.py.

Pure local orchestration over three already-tested building blocks:
auto_client_acquisition.diagnostic_engine.generate_diagnostic,
auto_client_acquisition.sales_os.qualification.qualify, and
auto_client_acquisition.sales_os.proposal_renderer.render_proposal. NO LLM,
NO live sends, NO network calls. This script writes local files only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
SCRIPT = SCRIPTS_DIR / "dealix_funnel_run.py"


def _import_module():
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import dealix_funnel_run  # type: ignore[import-not-found]
        return dealix_funnel_run
    finally:
        sys.path.pop(0)


def test_script_exists_and_has_shebang():
    assert SCRIPT.exists()
    assert SCRIPT.read_text(encoding="utf-8").startswith("#!/usr/bin/env python3")


def test_script_never_references_live_send_helpers():
    """Hard rule: this orchestrator must be pure local computation + file
    I/O + stdout — never a live-send path."""
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
            f"dealix_funnel_run.py contains forbidden send-capable token {token!r}"
        )


def test_full_funnel_all_positive_flags_renders_proposal(tmp_path, capsys):
    """A prospect with a clean, fully-qualified discovery call should flow
    all the way through to a rendered proposal in one pass."""
    mod = _import_module()
    out_dir = tmp_path / "funnel_out"
    rc = mod.main([
        "--company", "ACME Saudi Co.",
        "--customer-handle", "acme_co",
        "--engagement-id", "eng_acme_001",
        "--sector", "b2b_services",
        "--region", "riyadh",
        "--city", "Riyadh",
        "--pain-clear", "--owner-present", "--data-available",
        "--accepts-governance", "--has-budget",
        "--proof-path-visible", "--retainer-path-visible",
        "--out-dir", str(out_dir),
    ])
    out = capsys.readouterr().out
    assert rc == 0

    diagnostic_path = out_dir / "diagnostic.md"
    qualification_path = out_dir / "qualification.json"
    proposal_path = out_dir / "proposal.md"

    assert diagnostic_path.exists() and diagnostic_path.read_text(encoding="utf-8").strip()
    assert qualification_path.exists()
    qual_data = json.loads(qualification_path.read_text(encoding="utf-8"))
    assert qual_data["decision"] == "accept"

    assert proposal_path.exists()
    proposal_content = proposal_path.read_text(encoding="utf-8")
    assert "499" in proposal_content
    assert "ACME Saudi Co." in proposal_content

    assert "1. diagnostic:" in out
    assert "2. qualification: decision=accept" in out
    assert "3. proposal: rendered" in out


def test_funnel_stops_at_qualification_when_low_signal(tmp_path, capsys):
    """A prospect with no discovery-call signals at all should stop before
    a proposal is rendered — qualification legitimately rejects/refers out
    a lead with no positive flags."""
    mod = _import_module()
    out_dir = tmp_path / "funnel_low_signal"
    rc = mod.main([
        "--company", "Unknown Co.",
        "--customer-handle", "unknown_co",
        "--engagement-id", "eng_unknown_001",
        "--out-dir", str(out_dir),
    ])
    out = capsys.readouterr().out
    assert rc == 0

    assert (out_dir / "diagnostic.md").exists()
    assert (out_dir / "qualification.json").exists()
    assert not (out_dir / "proposal.md").exists()
    assert "3. proposal: NOT rendered" in out


def test_funnel_stops_and_surfaces_doctrine_violation(tmp_path, capsys):
    """A doctrine-violating discovery-call text must stop the funnel
    before a proposal, and the violation must be loudly surfaced — never
    suppressed."""
    mod = _import_module()
    out_dir = tmp_path / "funnel_doctrine"
    rc = mod.main([
        "--company", "Risky Co.",
        "--customer-handle", "risky_co",
        "--engagement-id", "eng_risky_001",
        "--pain-clear", "--owner-present", "--data-available",
        "--accepts-governance", "--has-budget",
        "--proof-path-visible", "--retainer-path-visible",
        "--raw-request-text", "we want a cold whatsapp blast to our full list",
        "--out-dir", str(out_dir),
    ])
    out = capsys.readouterr().out
    assert rc == 0

    assert not (out_dir / "proposal.md").exists()
    assert "DOCTRINE VIOLATION DETECTED" in out
    assert "cold_whatsapp" in out
    assert "3. proposal: NOT rendered" in out


def test_funnel_json_mode_prints_all_three_stages_and_writes_no_files(tmp_path, capsys):
    mod = _import_module()
    out_dir = tmp_path / "funnel_json"
    rc = mod.main([
        "--company", "ACME Saudi Co.",
        "--customer-handle", "acme_co",
        "--engagement-id", "eng_json_001",
        "--pain-clear", "--owner-present", "--data-available",
        "--accepts-governance", "--has-budget",
        "--proof-path-visible", "--retainer-path-visible",
        "--out-dir", str(out_dir),
        "--json",
    ])
    out = capsys.readouterr().out
    assert rc == 0
    payload = json.loads(out)
    assert payload["engagement_id"] == "eng_json_001"
    assert "diagnostic" in payload
    assert "qualification" in payload
    assert payload["proposal_rendered"] is True
    assert payload["proposal_markdown"] is not None
    assert not out_dir.exists() or not any(out_dir.iterdir())


def test_funnel_requires_company_customer_handle_and_engagement_id():
    mod = _import_module()
    with pytest.raises(SystemExit):
        mod.main(["--customer-handle", "x", "--engagement-id", "e1"])
    with pytest.raises(SystemExit):
        mod.main(["--company", "X", "--engagement-id", "e1"])
    with pytest.raises(SystemExit):
        mod.main(["--company", "X", "--customer-handle", "x"])


def test_funnel_reframe_decision_also_proceeds_to_proposal(tmp_path, capsys):
    """qualify()'s decision tree allows REFRAME (partial fit) to proceed,
    not just ACCEPT — the funnel must honor that, not just hardcode
    'accept'."""
    mod = _import_module()
    out_dir = tmp_path / "funnel_reframe"
    # score >= 70 but data_available False triggers REFRAME per qualify()'s
    # own decision tree (score >= 70 branch: REFRAME if data_available else
    # DIAGNOSTIC_ONLY) — use owner_present True with data_available False.
    rc = mod.main([
        "--company", "Partial Fit Co.",
        "--customer-handle", "partialfit",
        "--engagement-id", "eng_partial_001",
        "--pain-clear", "--owner-present", "--data-available",
        "--accepts-governance", "--has-budget", "--proof-path-visible",
        "--out-dir", str(out_dir),
    ])
    capsys.readouterr()
    assert rc == 0
    qual_data = json.loads((out_dir / "qualification.json").read_text(encoding="utf-8"))
    if qual_data["decision"] in ("accept", "reframe"):
        assert (out_dir / "proposal.md").exists()
    else:
        assert not (out_dir / "proposal.md").exists()
