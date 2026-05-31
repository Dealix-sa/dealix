"""Workflow rules whitelist actions and cap record counts."""

from __future__ import annotations

from dealix.hermes.governance_reasoning.workflow_rules import clear, evaluate, set_workflow_rule


def test_workflow_rules_enforce_whitelist_and_caps() -> None:
    clear()
    set_workflow_rule("wf_export", {"allowed_actions": {"export_report"}, "max_records": 100})
    assert evaluate("wf_export", "export_report", {"record_count": 50}).allowed is True
    assert evaluate("wf_export", "export_report", {"record_count": 200}).allowed is False
    assert evaluate("wf_export", "delete_all", {}).allowed is False
