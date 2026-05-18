"""Tests for the Full Ops autonomous daily cycle."""
from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.full_ops.autonomous_cycle import (
    CycleReport,
    latest_report,
    run_cycle,
)
from auto_client_acquisition.full_ops.work_queue import WorkQueue


_SYNTHETIC_LEADS = [
    {
        "company_name": "Najd Logistics",
        "sector": "logistics",
        "city": "Riyadh",
        "source": "warm_intro",
        "relationship_status": "warm_intro",
        "employee_count": 220,
        "last_contact_days": 5,
        "notes": "Owner asked for a revenue diagnostic after a referral call.",
    },
    {
        "company_name": "Hijaz Retail Group",
        "sector": "retail",
        "city": "Jeddah",
        "source": "inbound_form",
        "employee_count": 80,
        "notes": "Inbound form submission with a clear data-quality pain.",
    },
    {
        "company_name": "Sparse Lead",
        "source": "warm_intro",
    },
]


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "friction.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    get_default_approval_store().clear()
    yield
    get_default_approval_store().clear()


def test_run_cycle_end_to_end() -> None:
    queue = WorkQueue()
    report = run_cycle(
        leads=_SYNTHETIC_LEADS,
        on_date="2026-05-18",
        customer_id="test_full_ops",
        work_queue=queue,
    )
    assert isinstance(report, CycleReport)
    assert report.cycle_id.startswith("foc_")
    assert report.on_date == "2026-05-18"
    stages = report.stages
    assert stages["intake"] == 3
    assert stages["enriched"] == 3
    assert stages["scored"] == 3
    qualified = stages["qualified"]
    assert (
        qualified["accept"] + qualified["diagnostic"] + qualified["reject"]
        == 3
    )


def test_run_cycle_creates_approval_per_draft() -> None:
    queue = WorkQueue()
    store = get_default_approval_store()
    report = run_cycle(
        leads=_SYNTHETIC_LEADS,
        on_date="2026-05-18",
        customer_id="test_full_ops",
        work_queue=queue,
    )
    drafts = report.stages["drafts"]
    pending = store.list_pending()
    # one pending approval per external draft
    assert report.approvals_pending["count"] == drafts
    assert len(pending) == drafts
    for req in pending:
        assert req.action_mode == "approval_required"
        assert req.status == "pending"


def test_run_cycle_emits_work_items() -> None:
    queue = WorkQueue()
    report = run_cycle(
        leads=_SYNTHETIC_LEADS,
        on_date="2026-05-18",
        customer_id="test_full_ops",
        work_queue=queue,
    )
    assert report.work_items["count"] >= 1
    assert report.work_items["count"] == len(queue.list_all(tenant_id="dealix"))
    # at least the cycle orchestration item exists
    assert any(
        it.source.startswith("full_ops_cycle:")
        for it in queue.list_all(tenant_id="dealix")
    )


def test_run_cycle_no_external_send() -> None:
    """Cycle must produce only draft / approval-required outputs."""
    queue = WorkQueue()
    store = get_default_approval_store()
    run_cycle(
        leads=_SYNTHETIC_LEADS,
        on_date="2026-05-18",
        customer_id="test_full_ops",
        work_queue=queue,
    )
    for req in store.list_pending():
        assert req.action_mode in ("draft_only", "approval_required")
        assert req.status == "pending"
    for it in queue.list_all(tenant_id="dealix"):
        assert it.action_mode in (
            "suggest_only",
            "draft_only",
            "approval_required",
        )


def test_cycle_report_to_dict_shape() -> None:
    queue = WorkQueue()
    report = run_cycle(
        leads=_SYNTHETIC_LEADS,
        on_date="2026-05-18",
        customer_id="test_full_ops",
        work_queue=queue,
    )
    data = report.to_dict()
    expected_keys = {
        "cycle_id",
        "generated_at",
        "on_date",
        "title_ar",
        "title_en",
        "stages",
        "approvals_pending",
        "work_items",
        "next_actions",
        "hard_gates",
        "report_paths",
        "warnings",
    }
    assert expected_keys.issubset(data.keys())
    assert "no_live_send" in data["hard_gates"]
    assert "no_live_charge" in data["hard_gates"]
    assert isinstance(data["next_actions"], list)
    assert data["next_actions"]
    for action in data["next_actions"]:
        assert set(action) == {"ar", "en"}


def test_run_cycle_empty_leads_does_not_crash() -> None:
    queue = WorkQueue()
    report = run_cycle(
        leads=[],
        on_date="2026-05-18",
        customer_id="test_full_ops",
        work_queue=queue,
    )
    assert report.stages["intake"] == 0
    assert report.stages["drafts"] == 0
    assert report.next_actions  # always at least one


def test_latest_report_returns_newest() -> None:
    queue = WorkQueue()
    run_cycle(
        leads=_SYNTHETIC_LEADS,
        on_date="2026-05-18",
        customer_id="test_full_ops",
        work_queue=queue,
    )
    latest = latest_report()
    assert latest is not None
    assert "cycle_id" in latest
    assert "stages" in latest
