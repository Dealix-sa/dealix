"""Distribution OS — approval-first contract tests.

These prove the non-negotiables structurally:
  * every generated draft is pending_approval + approval_required
  * the model has NO status that means an automated external send
  * the quality gate reuses governance_os and fails closed
  * blocked ingestion sources are rejected at intake
"""

from __future__ import annotations

import json
from datetime import date

import pytest

from auto_client_acquisition.distribution_os import (
    Draft,
    DraftStatus,
    Prospect,
    build_followups,
    check_drafts,
    compute_metrics,
    due_followups,
    generate_drafts,
    generate_proposals,
    load_prospects,
    render_proposal_markdown,
    store,
    validate_prospect_dict,
)


@pytest.fixture()
def sample_prospects() -> list[Prospect]:
    return [
        Prospect(
            id="p-new",
            company="شركة جديدة",
            sector="training",
            status="new",
            source="founder_referral",
        ),
        Prospect(
            id="p-contacted",
            company="شركة تواصلنا",
            sector="retail",
            status="contacted",
            source="inbound_form",
            preferred_channel="whatsapp_manual",
            last_contact_at="2026-05-26",
        ),
        Prospect(
            id="p-disc",
            company="شركة تشخيص",
            sector="technology",
            status="discovery_booked",
            source="warm_intro",
            pain_hypothesis="تسرّب في التأهيل",
            last_contact_at="2026-05-31",
        ),
        Prospect(
            id="p-prop",
            company="شركة عرض",
            sector="real_estate",
            status="proposal_sent",
            source="event_meeting",
            last_contact_at="2026-05-29",
        ),
        Prospect(
            id="p-won",
            company="شركة فائزة",
            sector="consulting",
            status="won",
            source="warm_intro",
            last_contact_at="2026-05-12",
        ),
    ]


# ── draft factory ──────────────────────────────────────────────────────────


def test_every_generated_draft_is_approval_first(sample_prospects: list[Prospect]) -> None:
    drafts = generate_drafts(sample_prospects)
    assert drafts, "expected at least one draft"
    for d in drafts:
        assert d.approval_required is True
        assert d.status == DraftStatus.PENDING_APPROVAL.value
        assert d.evidence_level in {"L0", "L1", "L2", "L3", "L4", "L5"}
        assert d.body.strip()


def test_draft_ids_are_deterministic(sample_prospects: list[Prospect]) -> None:
    a = {d.id for d in generate_drafts(sample_prospects)}
    b = {d.id for d in generate_drafts(sample_prospects)}
    assert a == b


def test_no_draft_status_means_automated_send() -> None:
    """Structural doctrine: the lifecycle has no auto/integration-send state."""
    for status in DraftStatus:
        low = status.value.lower()
        assert "auto" not in low
        assert "integration" not in low
        assert "sent_via" not in low


# ── quality gate (reuses governance_os) ─────────────────────────────────────


def test_quality_gate_passes_clean_queue(sample_prospects: list[Prospect]) -> None:
    result = check_drafts(generate_drafts(sample_prospects))
    assert result.ok, [(v.draft_id, v.code, v.detail) for v in result.violations]


def test_quality_gate_blocks_guaranteed_claim() -> None:
    bad = Draft(
        id="x1",
        prospect_id="p",
        company="C",
        sector="s",
        channel="email",
        draft_type="outreach_first",
        language="ar",
        body="نضمن لك نتائج مبيعات مضاعفة خلال أسبوع",
    )
    result = check_drafts([bad])
    assert not result.ok
    codes = {v.code for v in result.violations}
    assert {"policy_block", "forbidden_claim"} & codes


def test_quality_gate_blocks_approval_required_false() -> None:
    bad = Draft(
        id="x2",
        prospect_id="p",
        company="C",
        sector="s",
        channel="email",
        draft_type="outreach_first",
        language="ar",
        body="مرحباً، نقترح تشخيصاً مجانياً.",
        approval_required=False,
    )
    result = check_drafts([bad])
    assert not result.ok
    assert any(v.code == "approval_required_false" for v in result.violations)


def test_quality_gate_fails_closed_on_foreign_send_status() -> None:
    """A tampered/foreign 'sent via integration' status must be rejected."""
    tampered = Draft(
        id="x3",
        prospect_id="p",
        company="C",
        sector="s",
        channel="whatsapp_manual",
        draft_type="outreach_first",
        language="ar",
        body="مرحباً، نقترح تشخيصاً مجانياً.",
        status="sent_via_integration",
    )
    result = check_drafts([tampered])
    assert not result.ok
    assert any(v.code == "illegal_status" for v in result.violations)


# ── prospect intake (reuses anti-waste) ─────────────────────────────────────


def test_blocked_source_rejected() -> None:
    errors = validate_prospect_dict(
        {"id": "b", "company": "C", "sector": "s", "status": "new", "source": "scraping"}
    )
    assert any(e.startswith("blocked_source") for e in errors)


def test_valid_prospect_passes() -> None:
    assert (
        validate_prospect_dict(
            {
                "id": "g",
                "company": "C",
                "sector": "s",
                "status": "new",
                "source": "founder_referral",
            }
        )
        == []
    )


# ── follow-up engine ────────────────────────────────────────────────────────


def test_followups_only_due_returned(sample_prospects: list[Prospect]) -> None:
    ref = date(2026, 6, 2)
    due = due_followups(sample_prospects, reference=ref)
    types = {f.followup_type for f in due}
    assert "day_7" in types  # contacted on 2026-05-26 → +7 = ref
    assert "proposal_followup" in types  # proposal_sent 2026-05-29 → +2
    assert "renewal" in types  # won 2026-05-12 → +21 = ref
    for f in due:
        assert f.status == "due"


def test_followups_not_yet_due_are_scheduled() -> None:
    p = [
        Prospect(
            id="p",
            company="C",
            sector="s",
            status="contacted",
            source="inbound_form",
            last_contact_at="2026-06-01",
        )
    ]
    built = build_followups(p, reference=date(2026, 6, 2))
    assert built and built[0].status == "scheduled"  # only 1 day since contact


# ── proposal factory (reuses sales_os) ──────────────────────────────────────


def test_proposal_has_required_sections_and_disclaimers(sample_prospects: list[Prospect]) -> None:
    proposals = generate_proposals(sample_prospects)
    assert proposals, "expected proposal-ready prospects"
    md = render_proposal_markdown(proposals[0])
    assert "نطاق العمل" in md
    assert "ما لا يشمله العرض" in md
    # the two non-negotiable statements from sales_os.build_proposal_skeleton
    sections = proposals[0].sections
    assert "does not promise sales outcomes" in sections["no_sales_guarantee_statement"]
    assert "No scraping" in sections["governance_boundaries"]
    assert proposals[0].approval_required is True


# ── metrics ─────────────────────────────────────────────────────────────────


def test_metrics_counts(sample_prospects: list[Prospect]) -> None:
    drafts = generate_drafts(sample_prospects)
    fus = build_followups(sample_prospects, reference=date(2026, 6, 2))
    m = compute_metrics(drafts, fus, sample_prospects)
    assert m["drafts_total"] == len(drafts)
    assert m["drafts_by_status"]["pending_approval"] == len(drafts)
    assert m["followups_total"] == len(fus)


# ── store + seed ────────────────────────────────────────────────────────────


def test_store_jsonl_roundtrip(tmp_path) -> None:
    path = tmp_path / "drafts.jsonl"
    rows = [{"id": "a", "n": 1}, {"id": "b", "n": 2}]
    store.write_jsonl(path, rows)
    assert store.read_jsonl(path) == rows


def test_seed_example_loads_and_is_clean() -> None:
    """The committed synthetic seed must load and pass the quality gate."""
    seed = store.REPO_ROOT / "data" / "distribution" / "prospects.example.json"
    prospects = load_prospects(seed)
    assert len(prospects) >= 5
    result = check_drafts(generate_drafts(prospects))
    assert result.ok, [(v.draft_id, v.code) for v in result.violations]


def test_seed_example_is_valid_json_envelope() -> None:
    seed = store.REPO_ROOT / "data" / "distribution" / "prospects.example.json"
    data = json.loads(seed.read_text(encoding="utf-8"))
    assert "prospects" in data and isinstance(data["prospects"], list)
