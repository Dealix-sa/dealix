"""Founder Action Inbox — prioritized aggregator across subsystems."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

from dealix.commercial_ops import founder_action_inbox as fai


# ─── Fixtures ─────────────────────────────────────────────────────


@pytest.fixture
def patched_sources(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Neutralize all signal sources; tests override individually."""
    state: dict[str, Any] = {
        "approvals": [],
        "leads": [],
        "pdpl_verdict": "PASS",
        "pdpl_done": 6,
        "pdpl_total": 6,
        "first_paid_verdict": "CLOSED",
        "plan_ok": True,
        "plan_missing": [],
        "plan_task_count": 138,
        "plan_min_tasks": 138,
    }

    class _FakeApprovalReq:
        def __init__(self, **kw: Any) -> None:
            self.approval_id = kw.get("approval_id", "apr_test")
            self.object_type = kw.get("object_type", "outreach")
            self.object_id = kw.get("object_id", "obj_1")
            self.risk_level = kw.get("risk_level", "low")
            self.summary_ar = kw.get("summary_ar", "")
            self.summary_en = kw.get("summary_en", "")
            self.created_at = kw.get("created_at", datetime.now(UTC))

    def fake_list_pending() -> list[Any]:
        return [_FakeApprovalReq(**a) for a in state["approvals"]]

    def fake_pdpl() -> dict[str, Any]:
        return {
            "verdict": state["pdpl_verdict"],
            "done": state["pdpl_done"],
            "total": state["pdpl_total"],
        }

    def fake_first_paid() -> dict[str, Any]:
        return {"verdict": state["first_paid_verdict"]}

    def fake_plan() -> dict[str, Any]:
        return {
            "ok": state["plan_ok"],
            "task_count": state["plan_task_count"],
            "min_task_count": state["plan_min_tasks"],
            "missing_paths": list(state["plan_missing"]),
        }

    monkeypatch.setattr(
        "auto_client_acquisition.approval_center.list_pending", fake_list_pending
    )
    monkeypatch.setattr(fai, "analyze_pdpl_compliance_pass", fake_pdpl)
    monkeypatch.setattr(fai, "analyze_first_paid_diagnostic", fake_first_paid)
    monkeypatch.setattr(fai, "strongest_plan_status", fake_plan)
    monkeypatch.setattr(
        "auto_client_acquisition.lead_inbox.list_leads",
        lambda limit=500: list(state["leads"]),
    )
    return state


# ─── Verdict + shape ──────────────────────────────────────────────


def test_inbox_clear_when_all_healthy(patched_sources: dict[str, Any]) -> None:
    # Provide evidence rows so evidence gap doesn't trigger.
    from datetime import date

    today = date.today().isoformat()
    rows = [
        {"event_type": "message_sent_manual", "event_date": today, "company": "A"},
        {"event_type": "reply_received", "event_date": today, "company": "B"},
        {"event_type": "demo_booked", "event_date": today, "company": "C"},
    ]
    snap = fai.build_action_inbox(evidence_rows=rows)
    assert snap["verdict"] == "CLEAR"
    assert snap["total_items"] == 0
    assert snap["schema_version"] == "1.0"
    assert snap["is_estimate"] is True


def test_inbox_blocked_when_pdpl_open(patched_sources: dict[str, Any]) -> None:
    patched_sources["pdpl_verdict"] = "OPEN"
    patched_sources["pdpl_done"] = 0
    patched_sources["pdpl_total"] = 6
    snap = fai.build_action_inbox(evidence_rows=[])
    assert snap["verdict"] == "BLOCKED"
    assert snap["by_priority"]["P0"] >= 1
    pdpl_items = [i for i in snap["items"] if i["source"] == "pdpl_compliance"]
    assert pdpl_items, "expected PDPL item"
    assert pdpl_items[0]["legal_review_required"] is True


def test_inbox_blocked_when_first_paid_open(patched_sources: dict[str, Any]) -> None:
    patched_sources["first_paid_verdict"] = "OPEN"
    snap = fai.build_action_inbox(evidence_rows=[])
    paid_items = [i for i in snap["items"] if i["source"] == "first_paid_tracker"]
    assert paid_items
    assert paid_items[0]["priority"] == "P0"
    assert snap["by_priority"]["P0"] >= 1


def test_inbox_active_day_for_p1(patched_sources: dict[str, Any]) -> None:
    patched_sources["approvals"] = [
        {"risk_level": "medium", "summary_ar": "مراجعة مسودة", "summary_en": "Review draft"}
    ]
    snap = fai.build_action_inbox(evidence_rows=[])
    # Evidence gap will also add P1 for "no events today"
    assert snap["verdict"] in ("ACTIVE_DAY", "BLOCKED")
    assert snap["by_priority"]["P1"] >= 1


# ─── Approval items ───────────────────────────────────────────────


def test_approval_high_risk_is_p0(patched_sources: dict[str, Any]) -> None:
    patched_sources["approvals"] = [
        {"risk_level": "high", "summary_ar": "إرسال خارجي", "summary_en": "External send"}
    ]
    snap = fai.build_action_inbox(evidence_rows=[])
    appr = [i for i in snap["items"] if i["source"] == "approval_center"]
    assert appr
    assert appr[0]["priority"] == "P0"
    assert "إرسال خارجي" in appr[0]["title_ar"]


# ─── Stale lead items ─────────────────────────────────────────────


def test_stale_lead_48h_is_p0(patched_sources: dict[str, Any]) -> None:
    old = (datetime.now(UTC) - timedelta(hours=72)).isoformat()
    patched_sources["leads"] = [
        {"id": "l1", "status": "new", "company": "Acme", "created_at": old},
    ]
    snap = fai.build_action_inbox(evidence_rows=[])
    leads = [i for i in snap["items"] if i["source"] == "lead_inbox"]
    assert leads
    assert leads[0]["priority"] == "P0"
    assert leads[0]["age_hours"] >= 72
    assert "Acme" in leads[0]["title_ar"]


def test_stale_lead_under_threshold_excluded(patched_sources: dict[str, Any]) -> None:
    fresh = (datetime.now(UTC) - timedelta(hours=1)).isoformat()
    patched_sources["leads"] = [
        {"id": "l1", "status": "new", "company": "Fresh", "created_at": fresh},
    ]
    snap = fai.build_action_inbox(evidence_rows=[], stale_hours=24)
    leads = [i for i in snap["items"] if i["source"] == "lead_inbox"]
    assert not leads


def test_replied_lead_excluded(patched_sources: dict[str, Any]) -> None:
    old = (datetime.now(UTC) - timedelta(hours=72)).isoformat()
    patched_sources["leads"] = [
        {"id": "l1", "status": "replied", "company": "X", "created_at": old},
    ]
    snap = fai.build_action_inbox(evidence_rows=[])
    leads = [i for i in snap["items"] if i["source"] == "lead_inbox"]
    assert not leads


# ─── Evidence gap ─────────────────────────────────────────────────


def test_no_events_today_creates_p1(patched_sources: dict[str, Any]) -> None:
    snap = fai.build_action_inbox(evidence_rows=[])
    evid = [i for i in snap["items"] if i["source"] == "evidence_csv"]
    assert evid
    assert evid[0]["priority"] == "P1"


# ─── Sorting & limit ──────────────────────────────────────────────


def test_items_sorted_by_priority(patched_sources: dict[str, Any]) -> None:
    patched_sources["first_paid_verdict"] = "OPEN"  # P0
    patched_sources["plan_ok"] = False
    patched_sources["plan_missing"] = ["a.md"]  # P1
    snap = fai.build_action_inbox(evidence_rows=[])
    priorities = [i["priority"] for i in snap["items"]]
    # Ensure P0 items come before P1 items.
    if "P0" in priorities and "P1" in priorities:
        assert priorities.index("P0") < priorities.index("P1")


def test_limit_truncates_items(patched_sources: dict[str, Any]) -> None:
    # Many leads → enough items.
    old = (datetime.now(UTC) - timedelta(hours=48)).isoformat()
    patched_sources["leads"] = [
        {"id": f"l{i}", "status": "new", "company": f"Co{i}", "created_at": old}
        for i in range(60)
    ]
    snap = fai.build_action_inbox(evidence_rows=[], limit=10)
    assert len(snap["items"]) == 10
    assert snap["truncated"] is True
    assert snap["total_items"] >= 60


# ─── Markdown render ──────────────────────────────────────────────


def test_render_inbox_markdown_includes_actions(patched_sources: dict[str, Any]) -> None:
    patched_sources["first_paid_verdict"] = "OPEN"
    snap = fai.build_action_inbox(evidence_rows=[])
    md = fai.render_inbox_markdown(snap)
    assert "Founder Action Inbox" in md
    assert "P0" in md
    assert "Article 4" in md
    assert "Article 8" in md
    assert "Article 11" in md
