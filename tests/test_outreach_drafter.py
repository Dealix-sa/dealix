"""Tests for engine #6 — Sprint Day-4 outreach drafter."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from auto_client_acquisition.data_os.account_ranker import ICPProfile, rank_accounts
from auto_client_acquisition.sales_os.outreach_drafter import (
    DEFAULT_TEMPLATE,
    FORBIDDEN_LANGUAGE,
    OutreachDraft,
    OutreachDrafterError,
    OutreachTemplate,
    generate_outreach_drafts,
)


def _ranking():
    rows = [
        {"company_name": "Acme", "sector": "fintech", "city": "Riyadh",
         "source": "crm_export", "email": "ceo@acme.sa", "phone": "+966500000001"},
        {"company_name": "Beta", "sector": "fintech", "city": "Riyadh",
         "source": "crm_export", "email": "ceo@beta.sa", "phone": "+966500000002"},
        {"company_name": "Gamma & Co", "sector": "health", "city": "Jeddah",
         "source": "crm_export", "email": "ceo@gamma.sa", "phone": "+966500000003"},
    ]
    icp = ICPProfile(preferred_sectors=("fintech",), preferred_cities=("riyadh",))
    return rank_accounts(rows, icp=icp, top_n=3)


def test_generates_one_draft_per_account() -> None:
    drafts = generate_outreach_drafts(
        ranking=_ranking(),
        offer_name="Revenue Intelligence",
        founder_name="Sami",
    )
    assert len(drafts) == 3
    assert all(isinstance(d, OutreachDraft) for d in drafts)


def test_empty_ranking_yields_empty_list() -> None:
    drafts = generate_outreach_drafts(
        ranking=[],
        offer_name="Revenue Intelligence",
        founder_name="Sami",
    )
    assert drafts == []


def test_drafts_are_bilingual() -> None:
    drafts = generate_outreach_drafts(
        ranking=_ranking()[:1],
        offer_name="Revenue Intelligence",
        founder_name="Sami",
    )
    d = drafts[0]
    assert "السلام عليكم" in d.body_ar
    assert "Hi," in d.body_en
    assert "تشخيص إيرادات" in d.subject_ar
    assert "revenue diagnostic" in d.subject_en


def test_substitution_replaces_variables() -> None:
    drafts = generate_outreach_drafts(
        ranking=_ranking()[:1],
        offer_name="Revenue Intelligence",
        founder_name="Sami",
    )
    d = drafts[0]
    assert d.company_name == "Acme"
    assert "Acme" in d.subject_ar
    assert "Acme" in d.subject_en
    assert "Sami" in d.body_en
    assert "Riyadh" in d.body_en
    assert "fintech" in d.body_en
    assert "{" not in d.body_ar  # all tokens substituted
    assert "{" not in d.body_en


def test_drafts_default_to_approval_required() -> None:
    drafts = generate_outreach_drafts(
        ranking=_ranking()[:1],
        offer_name="Revenue Intelligence",
        founder_name="Sami",
    )
    assert drafts[0].requires_approval is True


def test_default_template_has_no_guarantee_language() -> None:
    DEFAULT_TEMPLATE.validate()  # must not raise


def test_default_template_includes_non_guarantee_disclaimer() -> None:
    assert "ليست نتائج مضمونة" in DEFAULT_TEMPLATE.body_ar
    assert "not guaranteed" in DEFAULT_TEMPLATE.body_en


def test_template_with_forbidden_language_is_refused() -> None:
    bad = OutreachTemplate(
        name="bad",
        subject_ar="عرض",
        subject_en="Offer",
        body_ar="نضمن لك زيادة 30%",
        body_en="We guarantee a 30% lift.",
    )
    with pytest.raises(OutreachDrafterError, match="forbidden"):
        generate_outreach_drafts(
            ranking=_ranking()[:1],
            offer_name="x",
            founder_name="Sami",
            template=bad,
        )


def test_each_forbidden_term_is_detected() -> None:
    for term in FORBIDDEN_LANGUAGE:
        bad = OutreachTemplate(
            name=f"bad-{term}",
            subject_ar="x",
            subject_en="x",
            body_ar=f"حسناً {term}",
            body_en=f"Well {term}",
        )
        with pytest.raises(OutreachDrafterError):
            bad.validate()


def test_drafts_written_to_disk_with_approval_gate(tmp_path: Path) -> None:
    drafts = generate_outreach_drafts(
        ranking=_ranking(),
        offer_name="Revenue Intelligence",
        founder_name="Sami",
        drafts_root=tmp_path,
    )
    assert len(drafts) == 3
    md_files = {p.name for p in tmp_path.glob("*.md")}
    gate_files = {p.name for p in tmp_path.glob("*.approval_required.json")}
    assert len(md_files) == len(drafts), "expected one .md draft per ranked account"
    assert len(gate_files) == len(drafts), "expected one approval gate per draft"
    sample = json.loads(next(tmp_path.glob("*.approval_required.json")).read_text(encoding="utf-8"))
    assert sample["state"] == "draft_only"
    assert sample["requires_approval_before_send"] is True


def test_slug_handles_special_characters(tmp_path: Path) -> None:
    generate_outreach_drafts(
        ranking=_ranking(),
        offer_name="Revenue Intelligence",
        founder_name="Sami",
        drafts_root=tmp_path,
    )
    files = {p.name for p in tmp_path.glob("*.md")}
    assert any("gamma-co" in name for name in files)  # special chars normalized


def test_blank_offer_name_raises() -> None:
    with pytest.raises(OutreachDrafterError, match="offer_name"):
        generate_outreach_drafts(
            ranking=_ranking()[:1],
            offer_name="",
            founder_name="Sami",
        )


def test_blank_founder_name_raises() -> None:
    with pytest.raises(OutreachDrafterError, match="founder_name"):
        generate_outreach_drafts(
            ranking=_ranking()[:1],
            offer_name="x",
            founder_name="   ",
        )


def test_to_markdown_includes_draft_warning() -> None:
    drafts = generate_outreach_drafts(
        ranking=_ranking()[:1],
        offer_name="Revenue Intelligence",
        founder_name="Sami",
    )
    md = drafts[0].to_markdown()
    assert "DRAFT" in md
    assert "requires founder approval" in md
    assert "## القسم العربي" in md
    assert "## English Section" in md


def test_to_dict_is_serializable() -> None:
    drafts = generate_outreach_drafts(
        ranking=_ranking()[:1],
        offer_name="Revenue Intelligence",
        founder_name="Sami",
    )
    payload = drafts[0].to_dict()
    assert payload["requires_approval"] is True
    json.dumps(payload, ensure_ascii=False)
