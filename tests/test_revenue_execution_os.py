"""Tests for the Revenue Execution OS distribution layer.

Covers every public function plus the doctrine alignment that mirrors the
11 non-negotiables: approval-first drafts, a governance_decision on every
output, guaranteed-claim blocking, no forbidden-channel language, and
payment handoffs that cannot be ready without explicit founder approval.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import PROOF_PACK_V2_SECTIONS
from auto_client_acquisition.revenue_execution_os import (
    draft_factory,
    draft_quality,
    followup_engine,
    metrics,
    offers,
    payment_handoff,
    proof_pack_factory,
    proposal_factory,
    renewal_engine,
    sectors,
    stores,
    win_loss,
)
from auto_client_acquisition.revenue_execution_os.daily_report import (
    DISCLAIMER,
    render_daily_report,
    render_draft_quality_report,
    render_followup_queue_report,
    render_metrics_report,
)
from auto_client_acquisition.revenue_execution_os.models import (
    Channel,
    Draft,
    DraftStatus,
    DraftType,
    Outcome,
    Proposal,
    ProposalStatus,
    Prospect,
    now_iso,
)

FIXED_NOW = datetime(2026, 6, 2, 12, 0, tzinfo=UTC)


@pytest.fixture(autouse=True)
def _isolated_stores(tmp_path, monkeypatch):
    """Point every store at a temp dir so tests never touch real data."""
    mapping = {
        "DEALIX_REVX_PROSPECTS_PATH": "prospects.jsonl",
        "DEALIX_REVX_DRAFTS_PATH": "drafts.jsonl",
        "DEALIX_REVX_FOLLOWUPS_PATH": "followups.jsonl",
        "DEALIX_REVX_PROPOSALS_PATH": "proposals.jsonl",
        "DEALIX_REVX_PROOF_PACKS_PATH": "proof_packs.jsonl",
        "DEALIX_REVX_PAYMENT_HANDOFFS_PATH": "payment_handoffs.jsonl",
        "DEALIX_REVX_RENEWALS_PATH": "renewals.jsonl",
        "DEALIX_REVX_WIN_LOSS_PATH": "win_loss.jsonl",
        "DEALIX_REVX_SECTORS_PATH": "sectors_missing.yaml",
    }
    for env, name in mapping.items():
        monkeypatch.setenv(env, str(tmp_path / name))
    yield


def _prospect(
    pid: str = "p1", company: str = "Acme", sector: str = "marketing_agencies"
) -> Prospect:
    return stores.PROSPECTS.add(
        Prospect(
            prospect_id=pid,
            company=company,
            contact_name="Sara",
            sector=sector,
            lead_source="inbound",
            created_at=now_iso(),
        )
    )


# ── offers ──────────────────────────────────────────────────────────────────


def test_offer_ladder_has_canonical_prices():
    assert offers.offer_by_key("revenue_sprint").one_time_min == 499
    assert offers.offer_by_key("data_revenue_pack").one_time_min == 1500
    managed = offers.offer_by_key("managed_revenue_ops")
    assert managed.recurring and managed.monthly_min == 2999 and managed.monthly_max == 4999
    assert offers.offer_by_key("free_diagnostic").one_time_max == 0


def test_offer_price_labels_and_next():
    assert offers.price_label(offers.offer_by_key("free_diagnostic"), "en") == "Free"
    assert "SAR" in offers.price_label(offers.offer_by_key("revenue_sprint"), "en")
    assert offers.next_offer("free_diagnostic").key == "revenue_sprint"
    # enterprise rung is terminal
    assert offers.next_offer("ai_governance_review") is None


# ── sectors ─────────────────────────────────────────────────────────────────


def test_sector_weights_sum_to_100_and_score_bounds():
    assert sum(sectors.SECTOR_WEIGHTS.values()) == 100
    assert sectors.score_sector(dict.fromkeys(sectors.CRITERIA, 1.0)) == 100.0
    assert sectors.score_sector({}) == 0.0
    assert sectors.score_sector(dict.fromkeys(sectors.CRITERIA, 5.0)) == 100.0  # clamped


def test_rank_sectors_puts_marketing_first():
    ranked = sectors.rank_sectors()
    assert ranked[0].key == "marketing_agencies"
    assert sectors.top_sector().key == "marketing_agencies"


# ── models / stores ─────────────────────────────────────────────────────────


def test_model_round_trip():
    d = Draft(draft_id="x", prospect_id="p", issues=["a"], evidence_level=2)
    assert Draft.from_dict(d.to_dict()) == d
    # resilient to unknown / missing keys
    assert Draft.from_dict({"draft_id": "y", "unknown": 1}).draft_id == "y"


def test_store_crud():
    _prospect("p1")
    assert stores.PROSPECTS.count() == 1
    got = stores.PROSPECTS.get("p1")
    assert got is not None and got.company == "Acme"
    stores.PROSPECTS.update("p1", stage="qualified")
    assert stores.PROSPECTS.get("p1").stage == "qualified"
    assert stores.PROSPECTS.get("missing") is None


# ── draft factory ───────────────────────────────────────────────────────────


def test_generated_drafts_are_approval_first_and_governed():
    p = _prospect()
    drafts = draft_factory.generate_drafts(p)
    assert len(drafts) == len(draft_factory.OUTREACH_SEQUENCE)
    for d in drafts:
        assert d.status == DraftStatus.PENDING_APPROVAL
        assert d.approval_required is True
        assert d.governance_decision  # non-empty — non-negotiable #8
        assert d.governance_decision != "BLOCK"


def test_render_draft_supports_all_types():
    p = _prospect()
    for dtype in draft_factory.DRAFT_TYPES:
        d = draft_factory.render_draft(p, dtype)
        assert d.subject and (d.body_ar or d.body_en)
        assert "scraping" not in (d.body_ar + d.body_en).lower()


def test_unknown_draft_type_raises():
    with pytest.raises(ValueError):
        draft_factory.render_draft(_prospect(), "nope")


def test_assess_draft_text_blocks_guarantee_and_flags_channel():
    block, issues = draft_factory.assess_draft_text("نضمن لك نتائج مبيعات")
    assert str(block) == "BLOCK"
    assert any(i.startswith("forbidden_claim:") for i in issues)
    draft_only, _ch = draft_factory.assess_draft_text("we will use cold whatsapp blast")
    assert str(draft_only) == "DRAFT_ONLY"
    clean, none = draft_factory.assess_draft_text("Hello, can we book a short call?")
    assert str(clean) == "REQUIRE_APPROVAL" and none == []


# ── draft quality ───────────────────────────────────────────────────────────


def test_quality_clean_draft_passes_and_claim_fails():
    p = _prospect()
    clean = draft_factory.render_draft(p, DraftType.OUTREACH_FIRST)
    q = draft_quality.score_draft(clean, p)
    assert q.passed and q.score >= draft_quality.PASS_THRESHOLD

    bad = Draft(
        draft_id="b",
        prospect_id=p.prospect_id,
        draft_type=DraftType.OUTREACH_FIRST,
        subject="x",
        body_ar="نضمن لك نتائج مبيعات",
        governance_decision="BLOCK",
        issues=["forbidden_claim:نضمن لك"],
        approval_required=True,
    )
    qb = draft_quality.score_draft(bad, p)
    assert qb.passed is False  # hard gate regardless of score


def test_review_drafts_summary():
    p = _prospect()
    drafts = draft_factory.generate_drafts(p)
    report = draft_quality.review_drafts(drafts, {p.prospect_id: p})
    assert report.total == len(drafts)
    assert report.passed + report.failed == report.total


# ── follow-up engine ────────────────────────────────────────────────────────


def test_followup_cadence_first_to_followup1():
    p = _prospect()
    first = Draft(
        draft_id="d1",
        prospect_id=p.prospect_id,
        draft_type=DraftType.OUTREACH_FIRST,
        created_at=(FIXED_NOW - timedelta(days=3)).isoformat(),
    )
    due = followup_engine.due_followups_for_prospect(p, [first], now=FIXED_NOW)
    assert len(due) == 1
    assert due[0].suggested_draft_type == DraftType.OUTREACH_FOLLOWUP_1
    assert due[0].reason == "no_reply_day2"


def test_followup_reply_switches_to_discovery():
    p = _prospect()
    replied = Draft(
        draft_id="d1",
        prospect_id=p.prospect_id,
        draft_type=DraftType.OUTREACH_FIRST,
        status=DraftStatus.REPLIED,
        created_at=FIXED_NOW.isoformat(),
    )
    due = followup_engine.due_followups_for_prospect(p, [replied], now=FIXED_NOW)
    assert any(f.suggested_draft_type == DraftType.DISCOVERY_INVITE for f in due)


def test_followup_proposal_nudge():
    p = _prospect()
    prop = Proposal(
        proposal_id="pr1",
        prospect_id=p.prospect_id,
        status=ProposalStatus.SENT,
        created_at=(FIXED_NOW - timedelta(days=3)).isoformat(),
    )
    due = followup_engine.due_followups_for_prospect(p, [], proposals=[prop], now=FIXED_NOW)
    assert any(f.reason == "proposal_followup_48h" for f in due)


def test_build_followup_queue_from_stores():
    p = _prospect()
    stores.DRAFTS.add(
        Draft(
            draft_id="d1",
            prospect_id=p.prospect_id,
            draft_type=DraftType.OUTREACH_FIRST,
            created_at=(datetime.now(UTC) - timedelta(days=3)).isoformat(),
        )
    )
    queue = followup_engine.build_followup_queue()
    assert any(f.prospect_id == p.prospect_id for f in queue)


# ── proposal factory ────────────────────────────────────────────────────────


def test_proposal_is_governed_and_priced():
    p = _prospect()
    prop = proposal_factory.generate_proposal(p, "revenue_sprint")
    assert prop.status == ProposalStatus.PENDING_APPROVAL
    assert prop.governance_decision == "REQUIRE_APPROVAL"  # not falsely BLOCKed
    assert prop.price_label == "499 ريال"
    assert prop.scope and prop.out_of_scope


def test_proposal_with_guarantee_in_solution_blocks():
    p = _prospect()
    prop = proposal_factory.build_proposal(p, "revenue_sprint", solution="نضمن لك مبيعات مضاعفة")
    assert prop.governance_decision == "BLOCK"


# ── proof pack factory ──────────────────────────────────────────────────────


def test_proof_pack_completeness_and_bar():
    partial = proof_pack_factory.build_proof_pack(prospect_id="p1", sections={"problem": "x"})
    assert partial.score < proof_pack_factory.PROOF_BAR
    assert proof_pack_factory.proof_pack_meets_bar(partial) is False

    full = proof_pack_factory.build_proof_pack(
        prospect_id="p1", sections=dict.fromkeys(PROOF_PACK_V2_SECTIONS, "done")
    )
    assert full.sections_complete is True
    assert full.score == 100
    assert proof_pack_factory.proof_pack_meets_bar(full) is True


# ── payment handoff ─────────────────────────────────────────────────────────


def test_payment_handoff_blocked_without_preconditions():
    p = _prospect()
    prop = Proposal(
        proposal_id="pr1",
        prospect_id=p.prospect_id,
        offer_key="revenue_sprint",
        status=ProposalStatus.PENDING_APPROVAL,
    )
    h = payment_handoff.build_payment_handoff(prop)
    assert payment_handoff.handoff_is_ready(h) is False
    assert "proposal_approved" in h.blocking_reasons
    assert h.governance_decision == "REQUIRE_APPROVAL"


def test_payment_handoff_ready_only_with_all_preconditions():
    p = _prospect()
    prop = Proposal(
        proposal_id="pr1",
        prospect_id=p.prospect_id,
        offer_key="revenue_sprint",
        status=ProposalStatus.APPROVED,
    )
    h = payment_handoff.build_payment_handoff(
        prop,
        price_confirmed=True,
        scope_confirmed=True,
        terms_confirmed=True,
        founder_approved=True,
    )
    assert payment_handoff.handoff_is_ready(h) is True
    assert h.amount_label == "499 ريال"


# ── renewal / win-loss / metrics ────────────────────────────────────────────


def test_renewal_ladder_and_next():
    ladder = renewal_engine.renewal_ladder()
    assert ladder[0] == "free_diagnostic"
    r = renewal_engine.build_renewal("c1", "revenue_sprint", trigger="after_quick_win")
    assert r.next_offer_key == "data_revenue_pack"


def test_win_loss_weekly_learning():
    win_loss.record_outcome(
        company="A",
        sector="clinics",
        channel="email",
        offer_key="revenue_sprint",
        outcome=Outcome.WON,
    )
    win_loss.record_outcome(
        company="B",
        sector="clinics",
        channel="email",
        offer_key="revenue_sprint",
        outcome=Outcome.LOST,
        objection="price",
    )
    learning = win_loss.weekly_learning()
    assert learning["won"] == 1 and learning["lost"] == 1
    assert learning["close_rate"] == 0.5
    assert "price" in learning["top_objections"]


def test_daily_and_weekly_metrics():
    p = _prospect()
    draft_factory.generate_drafts(p)
    dm = metrics.daily_metrics()
    assert dm["drafts_generated"] == len(draft_factory.OUTREACH_SEQUENCE)
    assert dm["drafts_open"] >= 1
    wm = metrics.weekly_metrics()
    assert 0.0 <= wm["approval_rate"] <= 1.0
    assert "pipeline_value_estimated_sar" in wm


# ── reports ─────────────────────────────────────────────────────────────────


def test_reports_render_with_disclaimer_even_when_empty():
    for render in (
        render_daily_report,
        render_draft_quality_report,
        render_followup_queue_report,
        render_metrics_report,
    ):
        out = render()
        assert isinstance(out, str) and out
        assert DISCLAIMER in out


def test_daily_report_lists_top_sector_and_drafts():
    p = _prospect()
    draft_factory.generate_drafts(p)
    report = render_daily_report()
    assert "القطاع الأفضل" in report
    assert "pending_approval" not in report.lower() or "بانتظار الموافقة" in report


# ── doctrine alignment ──────────────────────────────────────────────────────


def test_no_generated_draft_contains_forbidden_channel_language():
    p = _prospect()
    for dtype in draft_factory.DRAFT_TYPES:
        d = draft_factory.render_draft(p, dtype)
        blob = f"{d.subject}\n{d.body_ar}\n{d.body_en}".lower()
        for marker in ("cold whatsapp", "linkedin automation", "scraping", "blast"):
            assert marker not in blob
        assert "forbidden_channel_language" not in d.issues


def test_every_factory_output_carries_governance_decision():
    p = _prospect()
    draft = draft_factory.render_draft(p, DraftType.OUTREACH_FIRST)
    prop = proposal_factory.build_proposal(p, "revenue_sprint")
    prop_ok = Proposal(
        proposal_id="x",
        prospect_id=p.prospect_id,
        offer_key="revenue_sprint",
        status=ProposalStatus.APPROVED,
    )
    handoff = payment_handoff.build_payment_handoff(prop_ok)
    for obj in (draft, prop, handoff):
        assert obj.governance_decision
