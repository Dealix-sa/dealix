"""Full-Ops doctrine guards — WS5 non-negotiable tests.

The 11 non-negotiables enforced on the operating-loop surface:
external action without approval is blocked; cold WhatsApp / LinkedIn
automation / scraping / bulk outreach are rejected; a blocked request can
never be approved; no fake proof; no guaranteed-sales claim.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import clear_for_test
from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.full_ops.operating_loop import gate, run_tick
from auto_client_acquisition.full_ops.work_item import WorkItem
from auto_client_acquisition.full_ops.work_queue import WorkQueue


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    monkeypatch.setenv(
        "DEALIX_FULL_OPS_LEDGER_PATH", str(tmp_path / "ticks.jsonl")
    )
    clear_for_test()
    get_default_approval_store().clear()
    yield
    clear_for_test()
    get_default_approval_store().clear()


def _flagged_item(flag: str) -> WorkItem:
    return WorkItem.make(
        os_type="sales",
        title_ar="إجراء خارجي يحمل علم مخاطرة",
        title_en="External action with risk flag",
        source="test",
        priority="p1",
        action_mode="approval_required",
        risk_flags=[flag],
        customer_id="cust_x",
    )


def _clean_external_item() -> WorkItem:
    return WorkItem.make(
        os_type="sales",
        title_ar="مسودة متابعة نظيفة",
        title_en="Clean follow-up draft",
        source="test",
        priority="p2",
        action_mode="approval_required",
    )


# ── External action funnels through the approval gate ──────────────


def test_external_action_creates_approval_required() -> None:
    q = WorkQueue()
    q.add(_clean_external_item())
    summary = run_tick(queue=q)
    assert summary["approvals_required"]
    assert summary["approvals_required"][0]["action_mode"] == "approval_required"


def test_loop_never_sends_or_charges() -> None:
    q = WorkQueue()
    q.add(_clean_external_item())
    summary = run_tick(queue=q)
    assert summary["sends"] == 0
    assert summary["charges"] == 0


# ── Doctrine violations → blocked, never approvable ────────────────


@pytest.mark.parametrize(
    "flag",
    [
        "cold_whatsapp",
        "whatsapp_automation",
        "linkedin_automation",
        "scraping",
        "bulk_outreach",
        "fake_proof",
        "guaranteed_sales",
        "external_send_without_approval",
    ],
)
def test_doctrine_flag_blocks_the_action(flag: str) -> None:
    gated = gate(
        [{"work_item": _flagged_item(flag), "agent_id": "fo-qualifier", "artifact": {}}]
    )
    assert gated[0]["gate"] == "blocked"
    assert gated[0]["approval"]["action_mode"] == "blocked"
    assert gated[0]["approval"]["status"] == "blocked"
    assert gated[0]["doctrine_violation"]


def test_blocked_request_cannot_be_approved() -> None:
    gated = gate(
        [
            {
                "work_item": _flagged_item("cold_whatsapp"),
                "agent_id": "fo-qualifier",
                "artifact": {},
            }
        ]
    )
    approval_id = gated[0]["approval"]["approval_id"]
    store = get_default_approval_store()
    with pytest.raises(ValueError, match="blocked"):
        store.approve(approval_id, who="founder")


def test_run_tick_reports_doctrine_violations() -> None:
    q = WorkQueue()
    q.add(_flagged_item("scraping"))
    summary = run_tick(queue=q)
    assert summary["approvals_blocked"]
    assert summary["doctrine_violations"]
    assert summary["approvals_blocked"][0]["action_mode"] == "blocked"


def test_cold_whatsapp_is_rejected() -> None:
    q = WorkQueue()
    q.add(_flagged_item("cold_whatsapp"))
    summary = run_tick(queue=q)
    assert summary["approvals_blocked"]
    detail = summary["doctrine_violations"][0]["detail"]
    assert "no_cold_whatsapp" in detail


def test_linkedin_automation_is_rejected() -> None:
    q = WorkQueue()
    q.add(_flagged_item("linkedin_automation"))
    summary = run_tick(queue=q)
    assert "no_linkedin_automation" in summary["doctrine_violations"][0]["detail"]


def test_guaranteed_sales_claim_is_rejected() -> None:
    q = WorkQueue()
    q.add(_flagged_item("guaranteed_sales"))
    summary = run_tick(queue=q)
    assert "no_guaranteed_sales_claims" in summary["doctrine_violations"][0]["detail"]


def test_fake_proof_is_rejected() -> None:
    q = WorkQueue()
    q.add(_flagged_item("fake_proof"))
    summary = run_tick(queue=q)
    assert "no_fake_proof" in summary["doctrine_violations"][0]["detail"]


def test_clean_external_action_is_not_blocked() -> None:
    gated = gate(
        [
            {
                "work_item": _clean_external_item(),
                "agent_id": "fo-qualifier",
                "artifact": {},
            }
        ]
    )
    assert gated[0]["gate"] == "approval_required"
    assert gated[0]["approval"]["action_mode"] == "approval_required"
