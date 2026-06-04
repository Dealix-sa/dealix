"""Compliance gate: no overclaim language, PDPL flags set, consent-first."""

from __future__ import annotations


from launch_os.drafts import generate_drafts
from launch_os.compliance import find_forbidden_claims, FORBIDDEN_CLAIMS


def test_no_forbidden_claims_in_any_draft():
    for d in generate_drafts(target=400):
        text = f"{d['subject_en']} {d['subject_ar']} {d['body_en']} {d['body_ar']}"
        assert find_forbidden_claims(text) == []


def test_compliance_flags_set():
    for d in generate_drafts(target=400):
        c = d["compliance"]
        assert c["pdpl_ok"] is True
        assert c["no_sensitive_data"] is True
        assert c["no_overclaim"] is True
        assert c["consent_required_before_send"] is True


def test_forbidden_claims_detector_works():
    assert "guaranteed roi" in find_forbidden_claims("We offer Guaranteed ROI today")
    assert "replace your team" in find_forbidden_claims("This will replace your team")
    assert FORBIDDEN_CLAIMS  # non-empty list
