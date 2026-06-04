"""Contract: the quality gate rejects weak drafts and accepts well-formed ones."""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "scripts"))

import commercial_launch_core as core

CFG = core.load_all_configs()


def _base_draft(**over):
    d = {
        "subject": "Facilities: tackling reactive maintenance",
        "body": ("Hi Facilities Director at Acme. We help facilities teams tackle "
                 "reactive maintenance with a system fully under your control, you decide. "
                 "We start with the Entry Diagnostic."),
        "cta": "Would a short 15-minute call work for you?",
        "opt_out": "Reply STOP to opt out.",
        "channel": "cold_email",
        "vertical": "facilities_management",
        "pain_angle": "reactive maintenance",
        "offer_name": "Entry Diagnostic",
        "language": "en",
    }
    d.update(over)
    return d


def test_well_formed_draft_passes():
    passed, score, reasons = core.quality_gate(_base_draft(), CFG)
    assert passed, reasons
    assert score >= 70


def test_missing_pain_fails():
    passed, _, reasons = core.quality_gate(_base_draft(pain_angle="nonexistent unique pain xyz"), CFG)
    assert not passed
    assert "missing_pain_or_vertical" in reasons


def test_missing_cta_fails():
    passed, _, reasons = core.quality_gate(_base_draft(cta="No call to action here."), CFG)
    assert not passed
    assert "not_single_cta" in reasons


def test_two_questions_is_not_single_cta():
    body = ("Hi at Acme, do you struggle with reactive maintenance? "
            "We help with a system you decide.")
    passed, _, reasons = core.quality_gate(_base_draft(body=body), CFG)
    assert not passed
    assert "not_single_cta" in reasons


def test_missing_opt_out_fails_for_email():
    passed, _, reasons = core.quality_gate(_base_draft(opt_out=""), CFG)
    assert not passed
    assert "missing_opt_out" in reasons


def test_generated_drafts_pass_quality_except_stress():
    drafts = core.generate_drafts(target=200, leads=core.load_seed_leads(),
                                  configs=CFG, date_str="2026-01-03")
    primary = [d for d in drafts if "STRESS" not in d["draft_id"]]
    failed = [d for d in primary if d["status"] == "rejected_quality"]
    assert not failed, f"primary drafts should pass quality, got {len(failed)} failures"
