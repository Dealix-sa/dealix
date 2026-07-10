"""Commercial trust tests for warm outreach drafts."""

from __future__ import annotations

from dealix.commercial.warm_intro_generator import (
    WarmIntroGenerator,
    WarmIntroRequest,
)


FORBIDDEN = (
    "80%",
    "حلّت هذه المشكلة لشركات مشابهة",
    "solved this for similar companies",
    "ZATCA Wave 24",
    "30 يونيو 2026",
    "June 30, 2026",
    "نتائج مضمونة",
    "guaranteed results",
    "وصول حكومي",
    "government access",
)


def _all_text(result) -> str:
    drafts = result.whatsapp_drafts + result.email_drafts
    return "\n".join(
        "\n".join((draft.subject_line, draft.body_ar, draft.body_en))
        for draft in drafts
    )


def test_default_founder_identity_is_full_name(monkeypatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    request = WarmIntroRequest(prospect_name="أحمد", company_name="شركة اختبار")
    assert request.founder_name == "سامي محمد عسيري"


def test_templates_do_not_contain_unverified_or_expired_claims(monkeypatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = WarmIntroGenerator().generate(
        WarmIntroRequest(
            prospect_name="سارة",
            company_name="شركة اختبار",
            sector="b2b_services",
            pain_context="بطء المتابعة",
        )
    )
    text = _all_text(result)
    for marker in FORBIDDEN:
        assert marker.casefold() not in text.casefold()


def test_offer_is_evidence_first_and_approval_gated(monkeypatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = WarmIntroGenerator().generate(
        WarmIntroRequest(prospect_name="محمد", company_name="شركة اختبار")
    )
    text = _all_text(result)
    assert "499" in text
    assert "لا نعد بنتيجة قبل القياس" in text
    assert result.approval_status == "approval_required"
    assert all(
        draft.approval_status == "approval_required"
        for draft in result.whatsapp_drafts + result.email_drafts
    )


def test_personal_phone_is_not_embedded_in_public_drafts(monkeypatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("DEALIX_FOUNDER_PHONE", "private-test-value")
    result = WarmIntroGenerator().generate(
        WarmIntroRequest(prospect_name="نورة", company_name="شركة اختبار")
    )
    assert "private-test-value" not in _all_text(result)
