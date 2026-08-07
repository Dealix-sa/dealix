"""Distribution OS — prospect qualification + draft factory + quality gate."""

from __future__ import annotations

import pytest

from auto_client_acquisition.distribution_os import draft_factory, draft_quality, prospect
from auto_client_acquisition.distribution_os.draft_factory import DraftStatus, DraftType
from auto_client_acquisition.distribution_os.prospect import Prospect, ProspectStatus


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_PROSPECTS_PATH", str(tmp_path / "prospects.jsonl"))
    monkeypatch.setenv("DEALIX_DRAFTS_PATH", str(tmp_path / "drafts.jsonl"))


def _good_prospect(**over) -> Prospect:
    base = {
        "company": "Acme",
        "sector": "marketing_agencies",
        "pain_hypothesis": "leads تضيع بعد الحملة",
        "offer_angle": "prod_sprint_v1",
        "preferred_channel": "email",
        "risk": "medium",
        "decision_maker": "Sara",
        "evidence_level": 1,
    }
    base.update(over)
    return prospect.add_prospect(**base)


# ── qualification ───────────────────────────────────────────────────────────


def test_qualify_passes_complete_prospect() -> None:
    result = prospect.qualify(_good_prospect())
    assert result.qualified is True
    assert result.reasons == ()


def test_qualify_blocks_missing_fields_and_high_risk() -> None:
    p = Prospect(
        company="X",
        sector="",
        pain_hypothesis="",
        offer_angle="",
        preferred_channel="email",
        risk="high",
    )
    result = prospect.qualify(p)
    assert result.qualified is False
    assert "missing_sector" in result.reasons
    assert "missing_pain_hypothesis" in result.reasons
    assert "missing_offer_angle" in result.reasons
    assert "risk_too_high" in result.reasons


def test_add_prospect_rejects_invalid_channel() -> None:
    with pytest.raises(ValueError):
        prospect.add_prospect(company="X", sector="s", preferred_channel="carrier_pigeon")


def test_update_status_roundtrip() -> None:
    p = _good_prospect()
    prospect.update_status(p.id, ProspectStatus.QUALIFIED)
    got = prospect.get_prospect(p.id)
    assert got is not None and got.status == ProspectStatus.QUALIFIED.value


def test_update_status_rejects_unknown() -> None:
    p = _good_prospect()
    with pytest.raises(ValueError):
        prospect.update_status(p.id, "teleported")


# ── draft factory ─────────────────────────────────────────────────────────────


def test_generated_clean_draft_is_pending_approval_and_linked_to_product() -> None:
    p = _good_prospect()
    d = draft_factory.generate_draft(prospect=p, draft_type=DraftType.OUTREACH_FIRST, locale="ar")
    assert d.status == DraftStatus.PENDING_APPROVAL.value
    assert d.governance_status == "pending_approval"
    assert d.product_id == "prod_sprint_v1"
    assert "Acme" in d.subject
    assert d.quality_issues == []


def test_draft_with_guaranteed_claim_is_blocked_and_cannot_be_approved() -> None:
    bad = _good_prospect(company="Bad", pain_hypothesis="نضمن لك نتائج مبيعات مضمونة")
    d = draft_factory.generate_draft(
        prospect=bad, draft_type=DraftType.DIAGNOSTIC_SUMMARY, locale="ar"
    )
    assert d.governance_status == "blocked"
    assert any(i.startswith("forbidden_claim") for i in d.quality_issues)
    with pytest.raises(ValueError):
        draft_factory.approve_draft(d.id)


def test_draft_approval_then_copy_flow() -> None:
    p = _good_prospect()
    d = draft_factory.generate_draft(prospect=p, draft_type=DraftType.OUTREACH_FIRST)
    approved = draft_factory.approve_draft(d.id)
    assert approved.status == DraftStatus.APPROVED.value
    copied = draft_factory.mark_copied(d.id)
    assert copied.status == DraftStatus.COPIED_MANUALLY.value


def test_reject_and_request_edit() -> None:
    p = _good_prospect()
    d = draft_factory.generate_draft(prospect=p, draft_type=DraftType.OUTREACH_FIRST)
    rej = draft_factory.reject_draft(d.id, reason="off-tone")
    assert rej.status == DraftStatus.REJECTED.value
    d2 = draft_factory.generate_draft(prospect=p, draft_type=DraftType.OUTREACH_FOLLOWUP_1)
    edited = draft_factory.request_edit(d2.id, note="shorten")
    assert edited.status == DraftStatus.NEEDS_EDIT.value


def test_draft_has_no_send_capability() -> None:
    # Doctrine: no external send exists in v1. The factory exposes no sender.
    public = set(draft_factory.__all__)
    assert not any("send" in name.lower() for name in public)
    assert not hasattr(draft_factory, "send_draft")


def test_english_locale_renders_english_template() -> None:
    p = _good_prospect()
    d = draft_factory.generate_draft(prospect=p, draft_type=DraftType.OUTREACH_FIRST, locale="en")
    assert d.locale == "en"
    assert "Hi" in d.body


def test_invalid_draft_type_and_channel_raise() -> None:
    p = _good_prospect()
    with pytest.raises(ValueError):
        draft_factory.generate_draft(prospect=p, draft_type="telepathy")
    with pytest.raises(ValueError):
        draft_factory.generate_draft(
            prospect=p, draft_type=DraftType.OUTREACH_FIRST, channel="smoke_signal"
        )


# ── quality gate (unit) ─────────────────────────────────────────────────────


def test_quality_gate_clean_text_allows() -> None:
    r = draft_quality.check_draft(text="مرحباً، فكرة قصيرة حول ترتيب البيانات.")
    assert r.decision == "allow"
    assert r.passed is True


def test_quality_gate_blocks_guarantee_and_flags_channel() -> None:
    blocked = draft_quality.check_draft(text="We guarantee ROI in 30 days")
    assert blocked.decision == "block"
    chan = draft_quality.check_draft(text="we will use linkedin automation to reach them")
    assert chan.decision == "draft_only"
    assert "forbidden_channel_language" in chan.issues


def test_quality_gate_flags_length_and_pii() -> None:
    long_pii = "x" * 1300 + " call +966512345678 or a@b.com or c@d.com or e@f.com"
    r = draft_quality.check_draft(text=long_pii)
    assert r.too_long is True
    assert r.pii_count >= 3
    assert r.decision in {"draft_only", "block"}


def test_quality_gate_report_aggregates() -> None:
    report = draft_quality.quality_gate_report(
        ["clean note", "We guarantee revenue", "x" * 1300],
    )
    assert report["drafts_checked"] == 3
    assert report["blocked_drafts"] == 1
    assert report["approved_for_review"] == 1
