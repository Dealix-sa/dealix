"""Contract: the compliance gate rejects banned phrases, missing opt-out, and
sensitive-sector privacy gaps; accepts clean privacy-first drafts."""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "scripts"))

import commercial_launch_core as core

CFG = core.load_all_configs()


def _clean(**over):
    d = {
        "subject": "Consulting: tackling proposal bottleneck",
        "body": ("Hi Managing Director at Acme. We help consulting teams tackle the "
                 "proposal bottleneck with a system fully under your control, you decide, "
                 "and your data stays with you. We start with the Entry Diagnostic."),
        "cta": "Would a short call work for you?",
        "opt_out": "Reply STOP to opt out.",
        "channel": "cold_email",
        "vertical": "consulting_training_b2b",
        "pain_angle": "proposal bottleneck",
        "offer_name": "Entry Diagnostic",
        "language": "en",
        "research_required": False,
    }
    d.update(over)
    return d


def test_clean_draft_passes():
    passed, score, reasons = core.compliance_gate(_clean(), CFG)
    assert passed, reasons
    assert score >= 70


def test_banned_phrase_rejected():
    body = "We guarantee 100% results and will replace your team."
    passed, _, reasons = core.compliance_gate(_clean(body=body), CFG)
    assert not passed
    assert "banned_phrase" in reasons


def test_fake_familiarity_rejected():
    body = "As discussed, we want to talk about your workflow."
    passed, _, reasons = core.compliance_gate(_clean(body=body), CFG)
    assert not passed
    assert "banned_phrase" in reasons


def test_data_access_implication_rejected():
    body = "We found your data from our database and reached out."
    passed, _, reasons = core.compliance_gate(_clean(body=body), CFG)
    assert not passed


def test_missing_opt_out_rejected_for_email():
    passed, _, reasons = core.compliance_gate(_clean(opt_out=""), CFG)
    assert not passed
    assert "no_opt_out" in reasons


def test_sensitive_vertical_needs_privacy_language():
    body = "Hi Partner at Acme. We help legal teams tackle intake workload quickly."
    passed, _, reasons = core.compliance_gate(
        _clean(vertical="legal_professional_services", pain_angle="intake workload", body=body), CFG)
    assert not passed
    assert "sensitive_no_privacy_language" in reasons


def test_generated_primary_drafts_pass_compliance():
    drafts = core.generate_drafts(target=200, leads=core.load_seed_leads(),
                                  configs=CFG, date_str="2026-01-04")
    primary = [d for d in drafts if "STRESS" not in d["draft_id"]]
    failed = [d for d in primary if d["status"] == "rejected_compliance"]
    assert not failed, f"primary drafts should pass compliance, got {len(failed)}"
