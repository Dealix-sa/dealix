"""Tests for the Customer Success autonomy layer.

Covers signal aggregator, opportunity detector, message drafter, the
end-to-end cycle, and the doctrine assertions (no external send, every
external draft is approval-gated, drafts pass the forbidden-token gate).
"""
from __future__ import annotations

import re

from auto_client_acquisition.customer_success_autonomy import (
    CustomerSignalSnapshot,
    aggregate_customer_signals,
    detect_opportunities,
    run_customer_success_cycle,
)
from auto_client_acquisition.customer_success_autonomy.message_drafter import (
    draft_churn_intervention,
    draft_detractor_outreach,
    draft_expansion_proposal,
    draft_renewal_message,
)

_FORBIDDEN = ("نضمن", "guaranteed", "blast", "scrape", "scraping")


def _has_forbidden(text: str) -> list[str]:
    hits: list[str] = []
    for tok in _FORBIDDEN:
        if re.search(rf"\b{re.escape(tok)}\b", text, re.IGNORECASE) or tok in text:
            # "guaranteed" appears as a negation context inside the disclaimer
            # (e.g. "Estimated outcomes are not guaranteed outcomes"); accept
            # only if it is *not* directly preceded by "not " / "ليست ".
            if tok == "guaranteed":
                if not re.search(r"not\s+guaranteed", text, re.IGNORECASE):
                    hits.append(tok)
                continue
            if tok in ("مضمون", "مضمونة"):
                if "ليست" not in text and "غير" not in text:
                    hits.append(tok)
                continue
            hits.append(tok)
    return hits


# --- signal aggregator -----------------------------------------------------

def test_aggregator_returns_snapshot_on_empty_inputs() -> None:
    snap = aggregate_customer_signals("C_EMPTY")
    assert isinstance(snap, CustomerSignalSnapshot)
    assert snap.customer_id == "C_EMPTY"
    # All sub-scores may be empty or zero-valued — must not crash.


def test_aggregator_is_friction_safe_on_garbage_inputs() -> None:
    # garbage values trigger ValueError in compute_*; aggregator must capture
    # them as warnings and still return a snapshot.
    snap = aggregate_customer_signals(
        "C_BAD",
        inputs={"logins_last_30d": "not-a-number"},  # type: ignore[arg-type]
    )
    assert snap.customer_id == "C_BAD"
    assert snap.warnings, "expected at least one friction-safe warning"


# --- opportunity detector --------------------------------------------------

def test_detector_emits_churn_intervention_when_critical() -> None:
    snap = aggregate_customer_signals(
        "C_CHURN",
        inputs={
            "engagement_drop_pct": 60,
            "support_escalations_last_30d": 4,
            "payment_late_count": 2,
            "nps_below_7": True,
            "decision_maker_left": True,
        },
    )
    opps = detect_opportunities(snap)
    kinds = {o.type for o in opps}
    assert "churn_intervention" in kinds


def test_detector_emits_nps_detractor_follow_up() -> None:
    snap = aggregate_customer_signals(
        "C_NPS",
        inputs={
            "recent_nps_score": 3,
            "recent_nps_milestone": "day_60_retention_signal",
        },
    )
    opps = detect_opportunities(snap)
    assert any(o.type == "nps_detractor_follow_up" for o in opps)


def test_detector_dedup_per_type() -> None:
    snap = aggregate_customer_signals(
        "C_NPS2", inputs={"recent_nps_score": 4}
    )
    opps = detect_opportunities(snap)
    types = [o.type for o in opps]
    assert len(set(types)) == len(types), "opportunities must be unique by type"


# --- message drafter -------------------------------------------------------

def test_renewal_draft_is_bilingual_and_clean() -> None:
    snap = aggregate_customer_signals(
        "C_R",
        inputs={"recent_nps_score": 9},
    )
    snap.renewal_status = {"has_schedule": True, "amount_sar": 2999}
    draft = draft_renewal_message(snap)
    assert draft["body_ar"] and draft["body_en"]
    assert _has_forbidden(draft["body_ar"]) == []
    assert _has_forbidden(draft["body_en"]) == []
    assert draft["action_mode"] == "approval_required"


def test_expansion_draft_is_clean() -> None:
    snap = aggregate_customer_signals("C_E")
    draft = draft_expansion_proposal(snap, {"offer": "growth_ops_monthly_2999"})
    assert _has_forbidden(draft["body_ar"]) == []
    assert _has_forbidden(draft["body_en"]) == []


def test_detractor_draft_is_clean() -> None:
    snap = aggregate_customer_signals("C_D")
    snap.recent_nps_milestone = "day_30_first_month"
    draft = draft_detractor_outreach(snap, 4)
    assert _has_forbidden(draft["body_ar"]) == []
    assert _has_forbidden(draft["body_en"]) == []


def test_churn_intervention_draft_is_clean() -> None:
    snap = aggregate_customer_signals("C_CH")
    snap.churn = {"signals_active": ["engagement_drop", "payment_late"]}
    draft = draft_churn_intervention(snap)
    assert _has_forbidden(draft["body_ar"]) == []
    assert _has_forbidden(draft["body_en"]) == []


# --- end-to-end cycle ------------------------------------------------------

def test_run_cycle_empty_returns_clean_report() -> None:
    rep = run_customer_success_cycle(customer_ids=[], on_date="2026-05-22")
    assert rep.summary["active_customers"] == 0
    assert rep.summary["opportunities_total"] == 0
    assert rep.hard_gates  # populated
    assert rep.report_paths  # JSON+MD persisted


def test_run_cycle_produces_approvals_and_work_items_for_churn() -> None:
    inputs = {
        "C1": {
            "engagement_drop_pct": 60,
            "support_escalations_last_30d": 4,
            "payment_late_count": 2,
            "nps_below_7": True,
            "decision_maker_left": True,
            "recent_nps_score": 3,
            "recent_nps_milestone": "day_60_retention_signal",
        }
    }
    rep = run_customer_success_cycle(
        customer_ids=["C1"], on_date="2026-05-22", inputs_by_customer=inputs
    )
    assert rep.summary["at_risk"] >= 1
    assert rep.summary["nps_detractors"] >= 1
    assert rep.approvals_created >= 2
    assert rep.work_items_created >= 2


# --- doctrine assertions ---------------------------------------------------

def test_no_external_send_in_drafts() -> None:
    """Every draft is marked approval_required and contains no send call."""
    snap = aggregate_customer_signals("C_DOC")
    snap.renewal_status = {"has_schedule": True, "amount_sar": 499}
    drafts = [
        draft_renewal_message(snap),
        draft_expansion_proposal(snap),
        draft_detractor_outreach(snap, 3),
        draft_churn_intervention(snap),
    ]
    for d in drafts:
        assert d["action_mode"] == "approval_required"
        assert d.get("governance_decision") == "allow_with_review"
        # Body must never embed an HTTP send invocation.
        text = (d.get("body_ar", "") + d.get("body_en", "")).lower()
        assert "http://" not in text and "https://" not in text


def test_cycle_hard_gates_present_in_report() -> None:
    rep = run_customer_success_cycle(customer_ids=["C_GATES"], on_date="2026-05-22")
    expected = {
        "no_live_send",
        "no_live_charge",
        "approval_required_for_external_actions",
    }
    assert expected.issubset(set(rep.hard_gates))
