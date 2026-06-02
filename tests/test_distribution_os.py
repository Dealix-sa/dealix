"""Revenue Execution OS (distribution layer) — unit + doctrine tests.

These tests are the doctrine guardrails for the distribution layer: they prove
the layer reuses the canonical non-negotiables, never auto-sends, keeps drafts
approval-first, and respects the L0–L5 evidence ladder. They run fully offline
and are isolated to ``tmp_path`` (they never touch a founder's real ledgers).
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
import yaml

from dealix.distribution import (
    day,
    drafts,
    followups,
    metrics,
    paths,
    payments,
    proof_packs,
    proposals,
    quality,
    renewals,
    sectors,
    win_loss,
)
from dealix.distribution import doctrine as dctr
from dealix.distribution.prospects import load_prospects, validate_prospects
from dealix.distribution.schemas import SCHEMA_FILES, load_schema, validate_record

_LEDGER_ATTRS = {
    drafts: "DRAFTS_LEDGER",
    quality: "DRAFTS_LEDGER",
    followups: "FOLLOWUPS_LEDGER",
    proposals: "PROPOSALS_LEDGER",
    proof_packs: "PROOF_PACKS_LEDGER",
    renewals: "RENEWALS_LEDGER",
    win_loss: "WIN_LOSS_LEDGER",
}


@pytest.fixture(autouse=True)
def _isolate_ledgers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Redirect every ledger + report path to tmp_path (non-destructive)."""
    files = {
        "DRAFTS_LEDGER": tmp_path / "drafts.jsonl",
        "FOLLOWUPS_LEDGER": tmp_path / "followups.jsonl",
        "PROPOSALS_LEDGER": tmp_path / "proposals.jsonl",
        "PROOF_PACKS_LEDGER": tmp_path / "proof.jsonl",
        "PAYMENTS_LEDGER": tmp_path / "payments.jsonl",
        "RENEWALS_LEDGER": tmp_path / "renewals.jsonl",
        "WIN_LOSS_LEDGER": tmp_path / "win_loss.jsonl",
    }
    for name, p in files.items():
        monkeypatch.setattr(paths, name, p, raising=False)
    for mod, attr in _LEDGER_ATTRS.items():
        monkeypatch.setattr(mod, attr, files[attr], raising=False)
    monkeypatch.setattr(payments, "PAYMENTS_LEDGER", files["PAYMENTS_LEDGER"])
    monkeypatch.setattr(payments, "PROPOSALS_LEDGER", files["PROPOSALS_LEDGER"])
    for name, p in files.items():
        monkeypatch.setattr(metrics, name, p, raising=False)
    monkeypatch.setattr(day, "REPORTS_DIR", tmp_path / "reports")


# ── Doctrine reuse ──────────────────────────────────────────────────────
def test_assert_distribution_safe_clean_passes() -> None:
    dctr.assert_distribution_safe()  # no flags → no raise


@pytest.mark.parametrize(
    "flag",
    [
        "request_cold_whatsapp",
        "request_linkedin_automation",
        "request_scraping",
        "request_bulk_outreach",
        "request_guaranteed_sales_claim",
        "request_fake_proof",
        "request_external_send_without_approval",
    ],
)
def test_assert_distribution_safe_blocks_each_violation(flag: str) -> None:
    with pytest.raises(ValueError):
        dctr.assert_distribution_safe(**{flag: True})


def test_channel_policy_yaml_matches_module() -> None:
    data = yaml.safe_load(paths.CHANNEL_POLICY_YAML.read_text(encoding="utf-8"))
    for channel, spec in data["channels"].items():
        assert dctr.CHANNEL_AUTOMATION_POLICY[channel]["allow"] == spec["allow"]
        assert dctr.CHANNEL_AUTOMATION_POLICY[channel]["deny"] == spec["deny"]


def test_channel_allows_deny_wins() -> None:
    assert dctr.channel_allows("email", "generate_draft") is True
    assert dctr.channel_allows("whatsapp", "cold_whatsapp_automation") is False
    assert dctr.channel_allows("linkedin", "linkedin_automation") is False


def test_banned_phrase_scan() -> None:
    assert dctr.scan_text_for_banned_claims("نضمن لك زيادة 300%")
    assert dctr.scan_text_for_banned_claims("clean professional draft") == []


def test_no_autosend_or_network_tokens_in_package() -> None:
    """Defense in depth: the distribution package must never send externally."""
    forbidden = ("linkedin_api", "unipile", "smtplib", "twilio", "requests.post(", "requests.get(")
    pkg = Path(dctr.__file__).resolve().parent
    offenders: list[str] = []
    for py in pkg.rglob("*.py"):
        text = py.read_text(encoding="utf-8")
        for tok in forbidden:
            if tok in text:
                offenders.append(f"{py.name}:{tok}")
    assert not offenders, f"distribution layer must not send/network: {offenders}"


# ── Sectors ─────────────────────────────────────────────────────────────
def test_sectors_loaded_and_scored() -> None:
    secs = sectors.load_sectors()
    assert len(secs) >= 8
    # sorted descending by computed priority
    priorities = [s["priority"] for s in secs]
    assert priorities == sorted(priorities, reverse=True)
    # priority is the bounded sum of component scores
    mk = sectors.get_sector("marketing_agencies")
    assert mk is not None
    assert mk["priority"] == sectors.compute_priority(mk["scores"])
    assert 0 <= mk["priority"] <= 100
    assert mk["offer_ref"]


# ── Prospects + schemas ─────────────────────────────────────────────────
def test_example_prospects_valid() -> None:
    summary = validate_prospects(load_prospects())
    assert summary["ok"], summary["errors"]
    assert summary["total"] >= 5


def test_all_schemas_load() -> None:
    for name in SCHEMA_FILES:
        schema = load_schema(name)
        assert schema["title"].startswith("Dealix")


def test_schema_validation_catches_errors() -> None:
    good = {
        "id": "draft_x",
        "prospect_id": "p1",
        "company": "Co",
        "sector": "clinics",
        "channel": "email",
        "language": "ar",
        "status": "draft_pending_approval",
        "body": "نص",
        "created_at": "2026-06-02T00:00:00Z",
    }
    assert validate_record(good, "draft") == []
    bad = {**good, "status": "sent_to_everyone", "channel": "carrier_pigeon"}
    errs = validate_record(bad, "draft")
    assert any("status" in e for e in errs)
    assert any("channel" in e for e in errs)
    assert validate_record({"company": "Co"}, "draft")  # missing required


# ── Draft factory + quality gate ────────────────────────────────────────
def test_draft_generation_dedupe_and_transitions() -> None:
    s1 = drafts.run_generation()
    assert s1["new_drafts"] >= 5
    for d in drafts.all_drafts():
        assert d["status"] == dctr.STATUS_PENDING
        assert d["policy"] == dctr.OPERATING_MODE
        assert dctr.scan_text_for_banned_claims(d["body"]) == []
    # idempotent
    s2 = drafts.run_generation()
    assert s2["new_drafts"] == 0
    # transitions
    did = drafts.pending_drafts()[0]["id"]
    assert drafts.approve_draft(did)["status"] == dctr.STATUS_APPROVED
    assert drafts.mark_copied(did)["status"] == dctr.STATUS_COPIED


def test_quality_gate_pass_and_fail() -> None:
    drafts.run_generation()
    gate = quality.run_quality_gate()
    assert gate["ok"], gate["failures"]

    bad_banned = {
        "id": "d_bad",
        "prospect_id": "p",
        "company": "C",
        "sector": "clinics",
        "channel": "email",
        "language": "ar",
        "status": dctr.STATUS_PENDING,
        "policy": dctr.OPERATING_MODE,
        "evidence_level": 0,
        "body": "نضمن لك نتائج مضمونة 100% ✅",
        "created_at": "2026-06-02T00:00:00Z",
    }
    res = quality.check_draft(bad_banned)
    assert res["passed"] is False
    assert any("banned" in e for e in res["errors"])

    no_cta = {
        **bad_banned,
        "id": "d2",
        "body": "مرحبا هذا نص عربي طويل بما يكفي ليتجاوز الحد الأدنى للطول المطلوب في البوابة دون أي دعوة",
    }
    res2 = quality.check_draft(no_cta)
    assert "missing_cta" in res2["errors"]


# ── Follow-ups ──────────────────────────────────────────────────────────
def test_followups_cadence_deterministic() -> None:
    prospects = [
        {"id": "a", "company": "A", "sector": "clinics", "status": "new", "last_contact": None},
        {
            "id": "b",
            "company": "B",
            "sector": "clinics",
            "status": "contacted",
            "last_contact": "2026-05-19",
        },
        {
            "id": "c",
            "company": "C",
            "sector": "clinics",
            "status": "qualified",
            "last_contact": "2026-05-31",
        },
        {
            "id": "d",
            "company": "D",
            "sector": "clinics",
            "status": "won",
            "last_contact": "2026-01-01",
        },
    ]
    due = followups.compute_due(prospects, today=date(2026, 6, 2))
    by_id = {f["prospect_id"]: f for f in due}
    assert by_id["a"]["reason"] == "first_touch" and by_id["a"]["priority"] == "high"
    assert by_id["b"]["priority"] == "high"  # 14 days
    assert "c" not in by_id  # only 2 days < threshold
    assert "d" not in by_id  # won never due


# ── Proposals ───────────────────────────────────────────────────────────
def test_proposal_pulls_pricing_from_offers() -> None:
    prospect = {
        "id": "p",
        "company": "Co",
        "sector": "logistics_companies",
        "status": "qualified",
        "evidence_level": 1,
    }
    prop = proposals.build_proposal(prospect)
    assert prop["status"] == dctr.STATUS_PENDING
    assert prop["offer_ref"]
    assert "SAR" in prop["price_range_sar"]
    assert prop["scope"]
    assert validate_record(prop, "proposal") == []


# ── Proof packs + public gate ───────────────────────────────────────────
def test_proof_pack_defaults_internal_and_public_gate() -> None:
    pk = proof_packs.build_proof_pack(
        {"id": "p", "company": "Co", "sector": "clinics", "status": "contacted"}
    )
    assert pk["evidence_level"] == 1
    assert pk["consent_public"] is False
    assert validate_record(pk, "proof_pack") == []

    proof_packs.run_generation()  # seed ledger
    some = proof_packs.all_proof_packs()[0]["id"]
    with pytest.raises(ValueError):
        proof_packs.promote_to_public(some, level=2, consent_public=True)
    with pytest.raises(ValueError):
        proof_packs.promote_to_public(some, level=4, consent_public=False)
    ok = proof_packs.promote_to_public(some, level=4, consent_public=True)
    assert ok["status"] == "approved" and ok["evidence_level"] == 4


# ── Payment handoff ─────────────────────────────────────────────────────
def test_payment_handoff_only_from_approved_and_requires_approval() -> None:
    approved = {
        "id": "prop1",
        "company": "Co",
        "offer_ref": "ai_workflow_audit",
        "status": "approved",
    }
    draft_prop = {
        "id": "prop2",
        "company": "Co2",
        "offer_ref": "ai_workflow_audit",
        "status": "draft_pending_approval",
    }
    summary = payments.run_generation(proposals=[approved, draft_prop])
    assert summary["new_handoffs"] == 1
    h = payments.all_handoffs()[0]
    assert h["approval_required"] is True
    assert h["status"] == dctr.STATUS_PENDING
    assert h["amount_sar"] > 0
    assert validate_record(h, "payment_handoff") == []


# ── Renewals ────────────────────────────────────────────────────────────
def test_renewal_no_upsell_before_proof() -> None:
    no_proof = {"company": "Co", "sector": "clinics", "evidence_level": 0}
    assert renewals.build_renewal(no_proof, today=date(2026, 6, 2)) is None
    with_proof = {
        "company": "Co",
        "sector": "clinics",
        "evidence_level": 2,
        "current_offer": "ai_workflow_audit",
    }
    rec = renewals.build_renewal(with_proof, today=date(2026, 6, 2))
    assert rec is not None
    assert rec["next_offer"]
    assert rec["status"] == "upcoming"


# ── Win/Loss + metrics ──────────────────────────────────────────────────
def test_win_loss_learning() -> None:
    win_loss.record_outcome(
        company="A", outcome="lost", reason="price", sector="clinics", lesson="L1"
    )
    win_loss.record_outcome(company="B", outcome="won", reason="proof", sector="clinics")
    summary = win_loss.learning_summary()
    assert summary["total"] == 2
    assert summary["by_outcome"]["lost"] == 1
    assert summary["win_rate_pct"] == 50.0
    assert any("Diagnostic" in c or "السعر" in c for c in summary["next_changes"])


def test_win_loss_rejects_bad_outcome() -> None:
    with pytest.raises(ValueError):
        win_loss.record_outcome(company="A", outcome="maybe", reason="x")


def test_metrics_funnel_aggregates() -> None:
    drafts.run_generation()
    snap = metrics.compute_metrics()
    assert snap["kpis"]["pending_drafts"] >= 5
    assert snap["funnel"]["drafts"] >= 5
    assert "drafts" in snap["by_status"]


# ── Day orchestrator ────────────────────────────────────────────────────
def test_distribution_day_passes() -> None:
    result = day.run_day(today=date(2026, 6, 2), write_report=True)
    assert result["verdict"] == "PASS"
    assert result["operating_mode"] == dctr.OPERATING_MODE
    assert result["steps"]["3_quality_gate"]["ok"] is True
    assert result["steps"]["2_drafts"]["new_drafts"] >= 5
    assert (day.REPORTS_DIR / "DISTRIBUTION_DAY.md").is_file()
