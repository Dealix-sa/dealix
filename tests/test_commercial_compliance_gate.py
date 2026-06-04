"""Compliance gate rejects banned phrases and enforces privacy-first language."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import commercial_launch_lib as lib  # noqa: E402


def _cfg():
    return lib.load_config("commercial_compliance_gates.json")


def test_banned_phrase_flagged():
    cfg = _cfg()
    draft = {
        "subject": "guaranteed roi for you",
        "body": "as discussed we can replace your team",
        "language": "en",
        "vertical": "consulting_training_b2b",
        "channel": "cold_email",
    }
    score, risk, reasons = lib.compliance_score(draft, cfg)
    assert risk == "high"
    assert any(r.startswith("banned_phrase") for r in reasons)
    assert score < cfg["min_compliance_score"]


def test_privacy_first_requires_consent_language():
    cfg = _cfg()
    draft = {
        "subject": "intro",
        "body": "we build workflow systems for law firms",
        "language": "en",
        "vertical": "legal_professional_services",
        "channel": "cold_email",
    }
    score, risk, reasons = lib.compliance_score(draft, cfg)
    assert "privacy_first_language_missing" in reasons


def test_privacy_first_passes_with_consent_language():
    cfg = _cfg()
    draft = {
        "subject": "intro",
        "body": "your privacy and consent matter; data minimization and you approve every step",
        "language": "en",
        "vertical": "legal_professional_services",
        "channel": "cold_email",
    }
    score, risk, reasons = lib.compliance_score(draft, cfg)
    assert "privacy_first_language_missing" not in reasons


def test_generated_accepted_drafts_pass_compliance():
    drafts = lib.generate_drafts(target=400)
    cfg = _cfg()
    accepted = [d for d in drafts if d["status"] == "founder_review"]
    for d in accepted:
        assert d["compliance_score"] >= cfg["min_compliance_score"]


def test_legal_vertical_drafts_carry_privacy_language():
    drafts = lib.generate_drafts(target=400)
    legal = [d for d in drafts if d["vertical"] == "legal_professional_services" and d["status"] == "founder_review"]
    assert legal, "expected some accepted legal-vertical drafts"
    for d in legal:
        text = (d["subject"] + d["body"]).lower()
        # EN drafts carry "privacy"; AR drafts carry the consent marker "تحت سيطرتك".
        assert ("privacy" in text) or ("تحت سيطرتك" in d["body"])
