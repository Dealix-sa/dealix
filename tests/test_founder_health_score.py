"""Founder Health Score — compose-only signal aggregation.

Tests cover the deterministic scoring logic for each sub-score and the
weighted overall score / verdict mapping. Side-effecting modules
(strongest plan, PDPL pass, first-paid tracker, lead inbox) are
monkeypatched at module-attribute level so the test runs in seconds
without filesystem dependencies.
"""

from __future__ import annotations

from typing import Any

import pytest

from dealix.commercial_ops import founder_health_score as fhs


# ─── Fixtures ─────────────────────────────────────────────────────


@pytest.fixture
def patched_signals(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Reset all signal sources to a neutral baseline so each test
    can override only what it cares about."""
    state: dict[str, Any] = {
        "paid_verdict": "OPEN",
        "pdpl_verdict": "OPEN",
        "pdpl_done": 0,
        "pdpl_total": 6,
        "plan_ok": True,
        "plan_task_count": 138,
        "plan_min_tasks": 138,
        "plan_missing": [],
        "leads": [],
    }

    def fake_paid() -> dict[str, Any]:
        return {"verdict": state["paid_verdict"], "dod_doc": "docs/x.md"}

    def fake_pdpl() -> dict[str, Any]:
        return {
            "verdict": state["pdpl_verdict"],
            "done": state["pdpl_done"],
            "total": state["pdpl_total"],
        }

    def fake_plan() -> dict[str, Any]:
        return {
            "ok": state["plan_ok"],
            "task_count": state["plan_task_count"],
            "min_task_count": state["plan_min_tasks"],
            "missing_paths": list(state["plan_missing"]),
        }

    class _FakeLeadInbox:
        @staticmethod
        def list_leads(limit: int = 500) -> list[dict[str, Any]]:
            return list(state["leads"])

    monkeypatch.setattr(fhs, "analyze_first_paid_diagnostic", fake_paid)
    monkeypatch.setattr(fhs, "analyze_pdpl_compliance_pass", fake_pdpl)
    monkeypatch.setattr(fhs, "strongest_plan_status", fake_plan)
    # Importable as auto_client_acquisition.lead_inbox — patch via module
    import auto_client_acquisition.lead_inbox as real_inbox  # noqa

    monkeypatch.setattr(
        "auto_client_acquisition.lead_inbox.list_leads",
        _FakeLeadInbox.list_leads,
    )
    return state


# ─── Evidence flow ────────────────────────────────────────────────


def test_evidence_flow_zero_events_scores_zero() -> None:
    result = fhs._evidence_flow_score([])
    assert result["score"] == 0
    assert result["week_total"] == 0
    assert result["is_estimate"] is True
    assert any("سجّل" in a["ar"] for a in result["actions"])


def test_evidence_flow_high_volume_caps_at_hundred() -> None:
    # Build 12 events spread across types within the rolling 7-day window.
    from datetime import UTC, date

    today = date.today().isoformat()
    rows = [
        {"event_type": "message_sent_manual", "event_date": today, "company": "X"},
    ] * 6 + [
        {"event_type": "reply_received", "event_date": today, "company": "Y"},
    ] * 4 + [
        {"event_type": "demo_booked", "event_date": today, "company": "Z"},
    ] * 2
    result = fhs._evidence_flow_score(rows)
    assert result["score"] == 100
    assert result["week_total"] == 12
    assert result["active_types_count"] >= 3


def test_evidence_flow_diversity_bonus_applied_for_three_types() -> None:
    from datetime import date

    today = date.today().isoformat()
    rows = [
        {"event_type": "message_sent_manual", "event_date": today, "company": "A"},
        {"event_type": "reply_received", "event_date": today, "company": "B"},
        {"event_type": "demo_booked", "event_date": today, "company": "C"},
    ]
    result = fhs._evidence_flow_score(rows)
    # 3 events → base 60, +5 diversity bonus.
    assert result["score"] == 65


# ─── Paid traction ────────────────────────────────────────────────


def test_paid_traction_closed_scores_hundred(patched_signals: dict[str, Any]) -> None:
    patched_signals["paid_verdict"] = "CLOSED"
    result = fhs._paid_traction_score()
    assert result["score"] == 100
    assert result["verdict"] == "CLOSED"
    assert result["actions"] == []


def test_paid_traction_in_progress_scores_fifty(patched_signals: dict[str, Any]) -> None:
    patched_signals["paid_verdict"] = "IN_PROGRESS"
    result = fhs._paid_traction_score()
    assert result["score"] == 50
    assert "Article 13" in result["actions"][0]["en"]


def test_paid_traction_open_scores_zero(patched_signals: dict[str, Any]) -> None:
    patched_signals["paid_verdict"] = "OPEN"
    result = fhs._paid_traction_score()
    assert result["score"] == 0


# ─── Compliance ───────────────────────────────────────────────────


def test_compliance_full_pass_scores_hundred(patched_signals: dict[str, Any]) -> None:
    patched_signals["pdpl_verdict"] = "PASS"
    patched_signals["pdpl_done"] = 6
    patched_signals["pdpl_total"] = 6
    result = fhs._compliance_score()
    assert result["score"] == 100
    assert result["actions"] == []


def test_compliance_partial_scales_linearly(patched_signals: dict[str, Any]) -> None:
    patched_signals["pdpl_verdict"] = "IN_PROGRESS"
    patched_signals["pdpl_done"] = 3
    patched_signals["pdpl_total"] = 6
    result = fhs._compliance_score()
    # 3/6 → 45 (linear up to 90 ceiling), capped at 90 only when full pass.
    assert result["score"] == 45
    assert result["actions"]


def test_compliance_empty_config_scores_zero(patched_signals: dict[str, Any]) -> None:
    patched_signals["pdpl_verdict"] = "OPEN"
    patched_signals["pdpl_done"] = 0
    patched_signals["pdpl_total"] = 0
    result = fhs._compliance_score()
    assert result["score"] == 0


# ─── Plan wiring ──────────────────────────────────────────────────


def test_plan_wiring_ok_scores_hundred(patched_signals: dict[str, Any]) -> None:
    result = fhs._plan_wiring_score()
    assert result["score"] == 100
    assert result["actions"] == []


def test_plan_wiring_few_missing_drops_to_sixty(patched_signals: dict[str, Any]) -> None:
    patched_signals["plan_ok"] = False
    patched_signals["plan_missing"] = ["a.md", "b.md"]
    result = fhs._plan_wiring_score()
    assert result["score"] == 60
    assert result["missing_paths_count"] == 2


def test_plan_wiring_many_missing_drops_to_ten(patched_signals: dict[str, Any]) -> None:
    patched_signals["plan_ok"] = False
    patched_signals["plan_missing"] = [f"f{i}.md" for i in range(15)]
    result = fhs._plan_wiring_score()
    assert result["score"] == 10
    assert "15" in result["actions"][0]["en"]


# ─── Inbox freshness ──────────────────────────────────────────────


def test_inbox_freshness_no_leads_scores_hundred(patched_signals: dict[str, Any]) -> None:
    result = fhs._inbox_freshness_score()
    assert result["score"] == 100
    assert result["stale_count"] == 0


def test_inbox_freshness_stale_leads_reduce_score(patched_signals: dict[str, Any]) -> None:
    from datetime import UTC, datetime, timedelta

    old = (datetime.now(UTC) - timedelta(hours=48)).isoformat()
    patched_signals["leads"] = [
        {"status": "new", "created_at": old},
        {"status": "new", "created_at": old},
        {"status": "contacted_pending", "created_at": old},
    ]
    result = fhs._inbox_freshness_score()
    # 3 stale → 50
    assert result["score"] == 50
    assert result["stale_count"] == 3


def test_inbox_freshness_replied_leads_excluded(patched_signals: dict[str, Any]) -> None:
    from datetime import UTC, datetime, timedelta

    old = (datetime.now(UTC) - timedelta(hours=48)).isoformat()
    patched_signals["leads"] = [
        {"status": "replied", "created_at": old},
        {"status": "closed_won", "created_at": old},
    ]
    result = fhs._inbox_freshness_score()
    assert result["score"] == 100
    assert result["stale_count"] == 0


# ─── Overall score & verdict ──────────────────────────────────────


def test_compute_overall_healthy_when_all_strong(
    patched_signals: dict[str, Any],
) -> None:
    from datetime import date

    today = date.today().isoformat()
    patched_signals["paid_verdict"] = "CLOSED"
    patched_signals["pdpl_verdict"] = "PASS"
    patched_signals["pdpl_done"] = 6
    patched_signals["pdpl_total"] = 6
    rows = [
        {"event_type": "message_sent_manual", "event_date": today, "company": "A"},
        {"event_type": "reply_received", "event_date": today, "company": "B"},
        {"event_type": "demo_booked", "event_date": today, "company": "C"},
        {"event_type": "payment_received", "event_date": today, "company": "D"},
    ]
    snap = fhs.compute_founder_health_score(evidence_rows=rows)
    assert snap["overall_score"] >= 80
    assert snap["verdict"] == "HEALTHY"
    assert snap["is_estimate"] is True
    assert snap["schema_version"] == "1.0"


def test_compute_overall_action_needed_when_all_weak(
    patched_signals: dict[str, Any],
) -> None:
    snap = fhs.compute_founder_health_score(evidence_rows=[])
    assert snap["overall_score"] < 50
    assert snap["verdict"] == "ACTION_NEEDED"
    assert len(snap["top_actions"]) > 0
    # Doctrine note must be present.
    assert "Article" in snap["doctrine_note_ar"]


def test_compute_top_actions_prioritize_paid_then_compliance(
    patched_signals: dict[str, Any],
) -> None:
    # Empty evidence, OPEN paid, OPEN PDPL → first action should mention Article 13.
    snap = fhs.compute_founder_health_score(evidence_rows=[])
    first = snap["top_actions"][0]
    assert "Article 13" in first["en"] or "13" in first["en"]


def test_custom_weights_renormalize_to_hundred(
    patched_signals: dict[str, Any],
) -> None:
    snap = fhs.compute_founder_health_score(
        evidence_rows=[],
        weights={"evidence_flow": 50, "paid_traction": 50, "compliance": 0, "plan_wiring": 0, "inbox_freshness": 0},
    )
    assert sum(snap["weights"].values()) == 100
    # All-zero signals with collapsed weights → still 0.
    assert snap["overall_score"] == 0


def test_render_brief_includes_score_and_actions(
    patched_signals: dict[str, Any],
) -> None:
    snap = fhs.compute_founder_health_score(evidence_rows=[])
    md = fhs.render_health_brief_markdown(snap)
    assert "Dealix Founder Health" in md
    assert "/100" in md
    assert "Article 4" in md
    assert "Article 8" in md
    assert "Article 11" in md
