"""Quality gate scores completeness, length, CTA, opt-out, and personalization."""

from __future__ import annotations

from _commercial_common import load_config
from _launch_util import SEED, TEST_DAY
from commercial_quality_gate import evaluate_quality

GATES = load_config("commercial_quality_gates.json")


def _good_draft():
    return {
        "channel": "cold_email",
        "subject": "Faster work-order dispatch at Acme FM Riyadh",
        "body": "Hi Acme FM Riyadh team, " + ("we help facilities teams in Riyadh. " * 6),
        "cta": "Request an AI Workflow Audit",
        "opt_out": "Reply unsubscribe to stop.",
        "company_name": "Acme FM Riyadh",
        "city": "Riyadh",
        "vertical": "facilities_management",
    }


def test_good_draft_passes():
    result = evaluate_quality(_good_draft(), GATES)
    assert result["passed"]
    assert result["score"] >= GATES["min_quality_score"]


def test_short_body_fails():
    d = _good_draft()
    d["body"] = "too short"
    result = evaluate_quality(d, GATES)
    assert not result["passed"]
    assert "body_too_short" in result["reasons"]


def test_missing_cta_penalized():
    d = _good_draft()
    d["cta"] = ""
    assert "missing_cta" in evaluate_quality(d, GATES)["reasons"]


def test_missing_opt_out_penalized_for_email():
    d = _good_draft()
    d["opt_out"] = ""
    assert "missing_opt_out" in evaluate_quality(d, GATES)["reasons"]
