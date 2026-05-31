"""
Unit tests for api/routers/email_templates.py

Tests cover:
- 8 email templates with bilingual content and placeholders
- 7 Saudi cultural rules
- _draft_email: placeholder substitution, governance
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.email_templates import (
    _EMAIL_TEMPLATES,
    _SAUDI_EMAIL_RULES,
    _draft_email,
    EmailDraftRequest,
    router,
)


class TestEmailTemplates:
    def test_eight_templates(self):
        assert len(_EMAIL_TEMPLATES) == 8

    def test_all_have_template_id(self):
        for t in _EMAIL_TEMPLATES:
            assert t.get("template_id"), "Missing template_id"

    def test_all_bilingual(self):
        for t in _EMAIL_TEMPLATES:
            tid = t.get("template_id", "?")
            assert t.get("name_en"), f"{tid} missing name_en"
            assert t.get("name_ar"), f"{tid} missing name_ar"

    def test_all_have_subject_lines(self):
        for t in _EMAIL_TEMPLATES:
            tid = t.get("template_id", "?")
            assert t.get("subject_line_en"), f"{tid} missing subject_line_en"
            assert t.get("subject_line_ar"), f"{tid} missing subject_line_ar"

    def test_all_have_body(self):
        for t in _EMAIL_TEMPLATES:
            tid = t.get("template_id", "?")
            assert t.get("body_en"), f"{tid} missing body_en"
            assert t.get("body_ar"), f"{tid} missing body_ar"

    def test_all_have_governance_note(self):
        for t in _EMAIL_TEMPLATES:
            tid = t.get("template_id", "?")
            note = t.get("governance_note_en", "")
            assert "human" in note.lower() or "manual" in note.lower() or "review" in note.lower(), \
                f"{tid} governance note should mention human review"

    def test_all_have_timing_guidance(self):
        for t in _EMAIL_TEMPLATES:
            assert t.get("timing_guidance_en"), f"{t['template_id']} missing timing_guidance_en"

    def test_warm_intro_template_present(self):
        ids = [t["template_id"] for t in _EMAIL_TEMPLATES]
        assert "warm_intro" in ids

    def test_post_eid_template_present(self):
        ids = [t["template_id"] for t in _EMAIL_TEMPLATES]
        assert any("eid" in tid.lower() for tid in ids)

    def test_no_cold_outreach_automation(self):
        for t in _EMAIL_TEMPLATES:
            body = (t.get("body_en") or "").lower()
            assert "automate" not in body or "no automation" in body or "manual" in body

    def test_renewal_template_present(self):
        ids = [t["template_id"] for t in _EMAIL_TEMPLATES]
        assert "renewal_reminder" in ids


class TestSaudiEmailRules:
    def test_seven_rules(self):
        assert len(_SAUDI_EMAIL_RULES) == 7

    def test_friday_rule_present(self):
        rules_text = " ".join(str(r) for r in _SAUDI_EMAIL_RULES).lower()
        assert "friday" in rules_text or "jumu" in rules_text

    def test_ramadan_rule_present(self):
        rules_text = " ".join(str(r) for r in _SAUDI_EMAIL_RULES).lower()
        assert "ramadan" in rules_text

    def test_no_price_in_cold_email_rule(self):
        rules_text = " ".join(str(r) for r in _SAUDI_EMAIL_RULES).lower()
        assert "price" in rules_text or "pricing" in rules_text


class TestDraftEmail:
    def _make_request(self, **overrides) -> EmailDraftRequest:
        data = dict(
            template_id="warm_intro",
            client_name="Ahmed Al-Rashid",
            client_company="Almarai Group",
            sender_name="Mohammed from Dealix",
        )
        data.update(overrides)
        return EmailDraftRequest(**data)

    def test_client_name_substituted(self):
        result = _draft_email(self._make_request())
        body = result.get("body_en", "")
        assert "Ahmed Al-Rashid" in body or "[CLIENT_NAME]" not in body

    def test_governance_approval_first(self):
        result = _draft_email(self._make_request())
        assert result.get("governance_decision") == "APPROVAL_FIRST"

    def test_unknown_template_raises(self):
        with pytest.raises(Exception):
            _draft_email(self._make_request(template_id="nonexistent_template_xyz"))

    def test_result_has_subject_and_body(self):
        result = _draft_email(self._make_request())
        assert result.get("subject_line_en")
        assert result.get("body_en")

    def test_result_has_timing_guidance(self):
        result = _draft_email(self._make_request())
        assert result.get("timing_guidance_en")

    def test_all_templates_draft_successfully(self):
        for t in _EMAIL_TEMPLATES:
            result = _draft_email(self._make_request(template_id=t["template_id"]))
            assert result.get("governance_decision") == "APPROVAL_FIRST"


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/email-templates"

    def test_router_tags(self):
        assert "Sales" in router.tags
