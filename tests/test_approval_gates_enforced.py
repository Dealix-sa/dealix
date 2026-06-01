"""Verify approval gate logic: protected actions require approval, free ones do not."""
from __future__ import annotations

import pytest

from os_runtime.approval_gate import GateCheckResult, check_action


def test_send_first_email_requires_approval() -> None:
    result = check_action("send_first_email")
    assert isinstance(result, GateCheckResult)
    assert result.requires_approval is True
    assert result.gate_id is not None


def test_send_followup_email_requires_approval() -> None:
    result = check_action("send_followup_email")
    assert result.requires_approval is True


def test_share_pricing_requires_approval() -> None:
    result = check_action("share_pricing")
    assert result.requires_approval is True


def test_send_proposal_requires_approval() -> None:
    result = check_action("send_proposal")
    assert result.requires_approval is True


def test_delete_client_data_requires_approval() -> None:
    result = check_action("delete_client_data")
    assert result.requires_approval is True


def test_read_file_does_not_require_approval() -> None:
    result = check_action("read_file")
    assert isinstance(result, GateCheckResult)
    assert result.requires_approval is False


def test_score_company_does_not_require_approval() -> None:
    result = check_action("score_company")
    assert result.requires_approval is False


def test_build_company_brief_does_not_require_approval() -> None:
    result = check_action("build_company_brief")
    assert result.requires_approval is False


def test_create_email_draft_does_not_require_approval() -> None:
    result = check_action("create_email_draft")
    assert result.requires_approval is False


def test_result_has_reason_string() -> None:
    result = check_action("send_first_email")
    assert isinstance(result.reason, str)
    assert len(result.reason) > 0


def test_unknown_action_does_not_require_approval() -> None:
    result = check_action("totally_unknown_action_xyz")
    assert result.requires_approval is False
    assert result.gate_id is None
