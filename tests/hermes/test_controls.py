"""Trust controls library — evaluate_all behavior with various ctx shapes."""

from __future__ import annotations

from dealix.hermes.trust import default_library


def _verdicts_by_id(verdicts: list) -> dict[str, object]:
    return {v.control_id: v for v in verdicts}


def test_nothing_in_scope_all_controls_pass_or_info() -> None:
    library = default_library()
    # The two ownership controls always require an owner; provide them so
    # "nothing else in scope" really means scope is empty.
    ctx = {"agent_owner": "founder", "tool_owner": "founder"}
    verdicts = library.evaluate_all(ctx)
    assert all(v.passed for v in verdicts), [
        (v.control_id, v.detail) for v in verdicts if not v.passed
    ]


def test_external_action_without_approval_fails_gov_003() -> None:
    library = default_library()
    verdicts = _verdicts_by_id(
        library.evaluate_all({"is_external_action": True})
    )
    assert "CTRL-GOV-003" in verdicts
    assert verdicts["CTRL-GOV-003"].passed is False


def test_external_action_with_approval_passes_gov_003() -> None:
    library = default_library()
    verdicts = _verdicts_by_id(
        library.evaluate_all(
            {
                "is_external_action": True,
                "approval_ticket_id": "apr_X",
            }
        )
    )
    assert verdicts["CTRL-GOV-003"].passed is True


def test_sensitive_data_leaving_workspace_fails_sec_001_critical() -> None:
    library = default_library()
    verdicts = _verdicts_by_id(
        library.evaluate_all(
            {
                "contains_sensitive_data": True,
                "leaving_workspace": True,
            }
        )
    )
    assert "CTRL-SEC-001" in verdicts
    assert verdicts["CTRL-SEC-001"].passed is False
    assert verdicts["CTRL-SEC-001"].severity.value == "critical"
