import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _v5util import load_drafts

REQUIRED = ["draft_id", "batch_id", "created_at", "company_name", "source_lead_id", "vertical",
            "country", "city", "channel", "language", "buyer_persona", "buyer_title", "offer_stage",
            "offer_name", "pain_angle", "trigger_event", "subject", "body", "cta", "opt_out",
            "quality_score", "compliance_score", "fit_score", "priority_score", "risk_level",
            "research_required", "founder_notes", "rejection_reason", "status",
            "send_allowed", "external_send_blocked", "requires_founder_approval", "no_auto_send"]


def test_at_least_400_drafts():
    assert len(load_drafts()) >= 400


def test_every_draft_has_required_fields():
    for d in load_drafts():
        for k in REQUIRED:
            assert k in d, f"missing {k}"


def test_channel_mix_present():
    channels = {d["channel"] for d in load_drafts()}
    assert {"cold_email", "follow_up", "linkedin_manual", "website_form"} <= channels
