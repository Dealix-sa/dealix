"""Compliance gate blocks banned phrases, missing opt-out, and unsafe drafts."""

from __future__ import annotations

from scripts.commercial_compliance_gate import compliance_check
from scripts.commercial_launch_core import generate_drafts, load_all_configs, load_seed_leads


def _good_draft():
    result = generate_drafts(target=400, leads=load_seed_leads(), cfg=load_all_configs())
    return next(d for d in result.drafts if d["status"] == "founder_review")


def test_good_draft_is_compliant():
    _score, risk, reasons = compliance_check(_good_draft())
    assert reasons == []
    assert risk == "low"


def test_banned_phrase_is_blocked():
    draft = {
        "channel": "cold_email",
        # contains a banned claim and no opt-out
        "body": "We offer guaranteed ROI and will replace your team. Reply yes?",
        "_sensitive": False,
    }
    _score, risk, reasons = compliance_check(draft)
    assert reasons, "banned phrase must produce a block reason"
    assert risk == "high"


def test_missing_opt_out_is_blocked():
    draft = {
        "channel": "cold_email",
        "body": "A clean note with no way to stop. Useful?",
        "_sensitive": False,
    }
    _, _, reasons = compliance_check(draft)
    assert "no_opt_out" in reasons


def test_sensitive_sector_requires_privacy_language():
    draft = {
        "channel": "cold_email",
        "body": 'A note about legal ops. Useful? To opt out, reply "unsubscribe".',
        "_sensitive": True,
    }
    _, _, reasons = compliance_check(draft)
    assert "missing_privacy_first_language" in reasons
