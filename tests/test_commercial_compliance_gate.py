"""Compliance gate rejects forbidden claims, fake urgency/familiarity, and unsafe flags."""

from __future__ import annotations

from _commercial_common import load_config
from _launch_util import SEED, TEST_DAY
from commercial_compliance_gate import evaluate_compliance

GATES = load_config("commercial_compliance_gates.json")


def _clean():
    return {
        "channel": "cold_email",
        "subject": "A quick idea for your operations",
        "body": "Hi team, we help your operations with AI you approve. Reply unsubscribe to stop.",
        "cta": "Book a Diagnostic",
        "opt_out": "Reply unsubscribe to stop.",
        "vertical": "facilities_management",
        "send_allowed": False,
        "external_send_blocked": True,
        "no_auto_send": True,
    }


def test_clean_draft_passes():
    assert evaluate_compliance(_clean(), GATES)["passed"]


def test_guaranteed_roi_rejected():
    d = _clean()
    d["body"] += " We offer guaranteed ROI."
    result = evaluate_compliance(d, GATES)
    assert not result["passed"]
    assert any("forbidden_phrase" in r for r in result["reasons"])


def test_fake_familiarity_rejected():
    d = _clean()
    d["body"] = "As discussed, here is the plan. Reply unsubscribe to stop."
    assert not evaluate_compliance(d, GATES)["passed"]


def test_missing_opt_out_rejected_for_email():
    d = _clean()
    d["opt_out"] = ""
    assert "missing_opt_out" in evaluate_compliance(d, GATES)["reasons"]


def test_send_allowed_true_is_non_compliant():
    d = _clean()
    d["send_allowed"] = True
    result = evaluate_compliance(d, GATES)
    assert not result["passed"]
    assert "send_allowed_true" in result["reasons"]


def test_legal_vertical_requires_privacy_language():
    d = _clean()
    d["vertical"] = "legal_professional_services"
    assert "missing_privacy_first_language" in evaluate_compliance(d, GATES)["reasons"]
