"""Quality gate rewards complete drafts and penalizes empty / generic ones."""

from __future__ import annotations

from scripts.commercial_launch_core import generate_drafts, load_all_configs, load_seed_leads
from scripts.commercial_quality_gate import quality_check


def _good_draft():
    result = generate_drafts(target=400, leads=load_seed_leads(), cfg=load_all_configs())
    return next(d for d in result.drafts if d["status"] == "founder_review")


def test_good_draft_passes_threshold():
    score, reasons = quality_check(_good_draft())
    assert score >= 70, reasons


def test_empty_draft_fails():
    draft = {
        "channel": "cold_email",
        "subject": "",
        "body": "",
        "pain_angle": "",
        "_sector_en": "Facilities Management & Maintenance",
        "_sector_ar": "إدارة المرافق والصيانة",
        "_sensitive": False,
        "_all_offer_names": [],
    }
    _score, reasons = quality_check(draft)
    assert _score < 70
    assert "no_pain" in reasons
    assert "no_opt_out" in reasons


def test_missing_opt_out_is_penalized():
    draft = {
        "channel": "cold_email",
        "subject": "Facilities: AI Workflow Audit",
        "body": (
            "Hi Operations Director, many Facilities Management & Maintenance teams "
            "struggle when work orders are scattered. Would a short audit be useful?"
        ),
        "pain_angle": "work orders are scattered",
        "_sector_en": "Facilities Management & Maintenance",
        "_sector_ar": "إدارة المرافق والصيانة",
        "_sensitive": False,
        "_all_offer_names": [],
    }
    _score, reasons = quality_check(draft)
    assert "no_opt_out" in reasons
