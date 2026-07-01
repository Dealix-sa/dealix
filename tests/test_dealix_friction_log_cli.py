"""Tests for scripts/dealix_friction_log.py.

Pure local generation over the already-tested friction log store and
aggregator (auto_client_acquisition.friction_log.store / .aggregator).
NO LLM, NO live sends, NO network calls. The script only ever appends
to / reads a local JSONL file and prints to stdout.

Every test isolates the friction log path via DEALIX_FRICTION_LOG_PATH
so tests never touch or corrupt the real repo's var/friction-log.jsonl.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
SCRIPT = SCRIPTS_DIR / "dealix_friction_log.py"


def _import_module():
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import dealix_friction_log  # type: ignore[import-not-found]
        return dealix_friction_log
    finally:
        sys.path.pop(0)


@pytest.fixture()
def _isolated(tmp_path, monkeypatch):
    """Redirect the friction log store to tmp_path so tests never touch
    the real repo's var/friction-log.jsonl."""
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "test_friction.jsonl"))
    yield tmp_path


def test_script_exists_and_has_shebang():
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
            f"dealix_friction_log.py contains forbidden send-capable token {token!r}"
        )


def test_log_with_required_kind_only_succeeds(_isolated, capsys):
    mod = _import_module()
    rc = mod.main(["log", "--kind", "manual_override"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "manual_override" in out
    assert mod.DEFAULT_WORKFLOW_ID in out
    assert "founder_manual_cli" in out
    assert mod.DEFAULT_CUSTOMER_ID in out
    assert "dealix_internal" in out


def test_log_with_invalid_kind_raises_system_exit(_isolated):
    mod = _import_module()
    with pytest.raises(SystemExit):
        mod.main(["log", "--kind", "not_a_real_kind"])


def test_log_writes_event_retrievable_via_list_events(_isolated):
    mod = _import_module()
    rc = mod.main([
        "log",
        "--kind", "support_ticket",
        "--customer-id", "dealix_internal",
    ])
    assert rc == 0

    from auto_client_acquisition.friction_log.store import list_events

    events = list_events(customer_id="dealix_internal")
    assert len(events) == 1
    assert events[0].kind == "support_ticket"


def test_log_with_custom_workflow_id_overrides_default(_isolated):
    mod = _import_module()
    rc = mod.main([
        "log",
        "--kind", "manual_override",
        "--workflow-id", "sprint_acme_001_kickoff_call",
    ])
    assert rc == 0

    from auto_client_acquisition.friction_log.store import list_events

    events = list_events(customer_id="dealix_internal")
    assert len(events) == 1
    assert events[0].workflow_id == "sprint_acme_001_kickoff_call"
    assert events[0].workflow_id != mod.DEFAULT_WORKFLOW_ID


def test_log_with_cost_minutes_and_evidence_ref_persist(_isolated):
    mod = _import_module()
    rc = mod.main([
        "log",
        "--kind", "retry",
        "--cost-minutes", "45",
        "--evidence-ref", "ticket-1234",
    ])
    assert rc == 0

    from auto_client_acquisition.friction_log.store import list_events

    events = list_events(customer_id="dealix_internal")
    assert len(events) == 1
    assert events[0].cost_minutes == 45
    assert events[0].evidence_ref == "ticket-1234"


def test_report_with_zero_events_prints_clear_message(_isolated, capsys):
    mod = _import_module()
    rc = mod.main(["report", "--customer-id", "dealix_internal", "--window-days", "14"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "no friction events found" in out.lower()


def test_report_after_logging_events_shows_totals_and_high_severity_callout(_isolated, capsys):
    mod = _import_module()
    mod.main(["log", "--kind", "manual_override", "--severity", "low"])
    mod.main(["log", "--kind", "governance_block", "--severity", "med"])
    mod.main(["log", "--kind", "approval_delay", "--severity", "high"])
    capsys.readouterr()

    rc = mod.main(["report", "--customer-id", "dealix_internal", "--window-days", "14"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "total: 3" in out
    assert "by_kind" in out
    assert "HIGH SEVERITY" in out
    assert "1 high-severity friction event" in out


def test_report_json_prints_valid_json_with_expected_keys(_isolated, capsys):
    mod = _import_module()
    mod.main(["log", "--kind", "schema_failure"])
    capsys.readouterr()

    rc = mod.main(["report", "--customer-id", "dealix_internal", "--json"])
    out = capsys.readouterr().out
    assert rc == 0
    payload = json.loads(out)
    for key in (
        "customer_id",
        "window_days",
        "total",
        "by_kind",
        "by_severity",
        "top_3_kinds",
        "total_cost_minutes",
        "week_over_week_delta",
    ):
        assert key in payload
    assert payload["total"] == 1


def test_report_with_kind_filters_detailed_listing(_isolated, capsys):
    mod = _import_module()
    mod.main(["log", "--kind", "manual_override", "--notes", "override one"])
    mod.main(["log", "--kind", "retry", "--notes", "retry one"])
    mod.main(["log", "--kind", "retry", "--notes", "retry two"])
    capsys.readouterr()

    rc = mod.main([
        "report",
        "--customer-id", "dealix_internal",
        "--kind", "retry",
    ])
    out = capsys.readouterr().out
    assert rc == 0
    # Aggregate breakdown still reflects everything in the window.
    assert '"manual_override": 1' in out or "'manual_override': 1" in out
    # But the itemized detail listing should only include the filtered kind.
    assert "retry one" in out
    assert "retry two" in out
    assert "override one" not in out


def test_default_workflow_id_distinct_from_automated_tag():
    mod = _import_module()
    assert mod.DEFAULT_WORKFLOW_ID != "delivery_sprint"
    assert mod.DEFAULT_WORKFLOW_ID == "founder_manual_cli"
