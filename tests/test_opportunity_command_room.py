"""Tests for the Saudi Opportunity Command Room (draft-first, approval-guarded)."""

from __future__ import annotations

from pathlib import Path

import pytest

from dealix.opportunity_graph.collectors.csv_importer import _parse_csv_text, import_companies_csv
from dealix.opportunity_graph.collectors.manual_seed_loader import load_seed_companies
from dealix.opportunity_graph.drafting import generate_draft_for_company
from dealix.opportunity_graph.pipeline import (
    decide_draft,
    mark_sent,
    run_daily_targeting,
    score_and_segment,
)
from dealix.opportunity_graph.reports import build_daily_report, build_weekly_proof_pack
from dealix.opportunity_graph.schemas import OpportunityCompany
from dealix.opportunity_graph.scoring import classify, score_company
from dealix.opportunity_graph.segmentation import segment_company
from dealix.opportunity_graph.store import OpportunityGraphStore


@pytest.fixture
def store(tmp_path: Path) -> OpportunityGraphStore:
    """Isolated store seeded with a copy of the committed seed CSV."""
    data_dir = tmp_path / "og"
    data_dir.mkdir(parents=True, exist_ok=True)
    repo_seed = Path(__file__).resolve().parents[1] / "data" / "opportunity_graph" / "companies.seed.csv"
    (data_dir / "companies.seed.csv").write_text(
        repo_seed.read_text(encoding="utf-8"), encoding="utf-8"
    )
    return OpportunityGraphStore(data_dir=data_dir)


@pytest.fixture
def empty_store(tmp_path: Path) -> OpportunityGraphStore:
    """Isolated store with no seed CSV at all."""
    return OpportunityGraphStore(data_dir=tmp_path / "empty_og")


# ── Scoring ─────────────────────────────────────────────────────────────────


def test_scoring_hot_for_strong_foreign_signal() -> None:
    fields = {
        "name": "Acme AI",
        "sector": "saas",
        "country": "UK",
        "company_type": "foreign",
        "saudi_signal": "Riyadh expansion, now hiring, Vision 2030",
        "buyer_persona": "CEO",
        "pain_hypothesis": "no local pipeline",
        "estimated_deal_size": "50k SAR enterprise",
        "website": "acme.ai",
        "consent_to_contact": True,
    }
    result = score_company(fields)
    assert result["score_class"] == "hot"
    assert result["total_score"] >= 80


def test_scoring_not_fit_for_empty_company() -> None:
    result = score_company({"name": "Curious Person", "pain_hypothesis": ""})
    assert result["score_class"] == "not_fit"
    assert result["total_score"] < 40


def test_scoring_is_deterministic() -> None:
    fields = {"name": "X", "sector": "clinics", "country": "Saudi Arabia"}
    assert score_company(fields) == score_company(fields)


def test_classify_bands() -> None:
    assert classify(80) == "hot"
    assert classify(60) == "warm"
    assert classify(40) == "research"
    assert classify(39) == "not_fit"


# ── Segmentation ────────────────────────────────────────────────────────────


def test_segmentation_foreign_saas() -> None:
    seg = segment_company(
        {"company_type": "foreign", "sector": "saas", "saudi_signal": "riyadh"}
    )
    assert seg == "foreign_saas_ai_entering_saudi"


def test_segmentation_saudi_clinic() -> None:
    seg = segment_company({"company_type": "saudi", "sector": "clinics", "country": "Saudi Arabia"})
    assert seg == "saudi_clinic_revenue_leak"


def test_segmentation_b2g() -> None:
    seg = segment_company({"sector": "consulting", "pain_hypothesis": "bidding on public RFP"})
    assert seg == "b2g_readiness_candidate"


# ── Drafting (safe messages) ────────────────────────────────────────────────


def test_draft_generator_produces_safe_message() -> None:
    company = score_and_segment(
        OpportunityCompany(
            id="co_test",
            name="Nordic SaaS",
            sector="saas",
            country="Sweden",
            company_type="foreign",
            saudi_signal="Riyadh expansion",
            buyer_persona="VP",
            pain_hypothesis="no pipeline",
            consent_to_contact=True,
        )
    )
    draft = generate_draft_for_company(company)
    assert draft is not None
    assert draft.approval_status == "pending"
    assert draft.sent_at is None
    lowered = draft.draft_text.lower()
    assert "guaranteed" not in lowered
    assert "مضمون" not in draft.draft_text


def test_draft_skipped_for_not_fit() -> None:
    company = OpportunityCompany(id="co_x", name="X", score_class="not_fit")
    assert generate_draft_for_company(company) is None


# ── Approval gate ───────────────────────────────────────────────────────────


def test_approval_gate_blocks_unapproved_send(store: OpportunityGraphStore) -> None:
    run_daily_targeting(store=store, limit=50)
    draft = store.load_drafts()[0]
    with pytest.raises(PermissionError):
        mark_sent(draft.id, human_sender="Sami", store=store)


def test_approval_then_manual_send(store: OpportunityGraphStore) -> None:
    run_daily_targeting(store=store, limit=50)
    draft = store.load_drafts()[0]
    decide_draft(draft.id, "approve", actor="Sami", store=store)
    sent = mark_sent(draft.id, human_sender="Sami Assiri", store=store)
    assert sent.sent_at is not None
    assert sent.human_sender == "Sami Assiri"
    # Audit trail recorded both events.
    kinds = {a["kind"] for a in store.load_approvals()}
    assert "draft_decision" in kinds
    assert "manual_send_recorded" in kinds


def test_decide_requires_actor(store: OpportunityGraphStore) -> None:
    run_daily_targeting(store=store, limit=50)
    draft = store.load_drafts()[0]
    with pytest.raises(ValueError):
        decide_draft(draft.id, "approve", actor="", store=store)


def test_run_daily_targeting_rejects_live_mode(store: OpportunityGraphStore) -> None:
    with pytest.raises(ValueError):
        run_daily_targeting(store=store, mode="live")


# ── CSV / seed loader resilience ────────────────────────────────────────────


def test_csv_importer_handles_empty() -> None:
    assert _parse_csv_text("") == []
    assert _parse_csv_text("name,website\n") == []


def test_csv_importer_missing_file(tmp_path: Path) -> None:
    assert import_companies_csv(tmp_path / "nope.csv") == []


def test_seed_loader_handles_missing_seed(empty_store: OpportunityGraphStore) -> None:
    # No seed CSV in tmp store dir → falls back to (empty) store contents.
    assert load_seed_companies(empty_store) == []


def test_committed_seed_csv_parses() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    seed = repo_root / "data" / "opportunity_graph" / "companies.seed.csv"
    companies = import_companies_csv(seed)
    assert len(companies) >= 5
    assert all(c.name for c in companies)


# ── Reports ─────────────────────────────────────────────────────────────────


def test_daily_report_builds(store: OpportunityGraphStore) -> None:
    run_daily_targeting(store=store, limit=50)
    report = build_daily_report(store=store)
    assert report.total_companies_scored >= 1
    assert report.pending_approvals >= 1


def test_weekly_proof_pack_no_fabricated_metrics(store: OpportunityGraphStore) -> None:
    run_daily_targeting(store=store, limit=50)
    pack = build_weekly_proof_pack(store=store)
    # Metrics are counts derived from the store, never invented.
    assert pack.metrics["companies_scored"] >= 1
    assert pack.acceptance_status == "draft"
