"""Tests for the draft -> approval auto-wire (M9)."""
from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center import (
    ApprovalStatus,
    get_default_approval_store,
)
from auto_client_acquisition.approval_center.approval_store import (
    reset_default_approval_store,
)
from auto_client_acquisition.sales_os.draft_approval_bridge import (
    queue_draft_for_approval,
    queue_follow_up_for_approval,
)


@pytest.fixture(autouse=True)
def _fresh_store():
    reset_default_approval_store()
    yield
    reset_default_approval_store()


def test_queue_draft_lands_in_pending_queue() -> None:
    req = queue_draft_for_approval(
        action_type="draft_email",
        object_type="outreach_message",
        object_id="msg_1",
        summary_en="Intro email to a Saudi SaaS lead",
        channel="email",
        lead_id="lead_42",
    )
    pending = get_default_approval_store().list_pending()
    assert any(p.approval_id == req.approval_id for p in pending)
    assert req.lead_id == "lead_42"


def test_follow_up_wrapper_uses_follow_up_action_type() -> None:
    req = queue_follow_up_for_approval(
        task_id="fut_9", lead_id="lead_9", attempt=2, channel="email",
        draft_en="Second touch — checking in.",
    )
    assert req.action_type == "follow_up_task"
    assert req.lead_id == "lead_9"
    assert "fut_9" == req.object_id


def test_whatsapp_draft_is_never_auto_approved() -> None:
    # whatsapp has no auto-approve path — the draft must stay pending.
    req = queue_follow_up_for_approval(
        task_id="fut_w", lead_id="lead_w", attempt=1, channel="whatsapp",
        draft_en="hi",
    )
    assert ApprovalStatus(req.status) == ApprovalStatus.PENDING
