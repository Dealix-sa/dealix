"""Quality gate rejects drafts that lack CTA / opt-out / use generic phrasing."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import commercial_launch_lib as lib  # noqa: E402


def _quality_cfg():
    return lib.load_config("commercial_quality_gates.json")


def test_missing_cta_penalized():
    cfg = _quality_cfg()
    draft = {"subject": "Hi", "body": "no call to action here", "cta": "", "opt_out": "stop", "vertical": "x"}
    score, reasons = lib.quality_score(draft, cfg, requires_opt_out=True)
    assert "missing_cta" in reasons
    assert score < 1.0


def test_missing_opt_out_penalized_when_required():
    cfg = _quality_cfg()
    draft = {"subject": "Hi", "body": "let's talk", "cta": "book a call", "opt_out": "", "vertical": "x"}
    _score, reasons = lib.quality_score(draft, cfg, requires_opt_out=True)
    assert "missing_opt_out" in reasons


def test_generic_phrase_penalized():
    cfg = _quality_cfg()
    draft = {
        "subject": "Hi",
        "body": "I hope this email finds you well, let's unlock the power of synergy",
        "cta": "book a call",
        "opt_out": "stop",
        "vertical": "x",
    }
    _score, reasons = lib.quality_score(draft, cfg, requires_opt_out=True)
    assert any(r.startswith("generic_phrase") for r in reasons)


def test_misleading_subject_penalized():
    cfg = _quality_cfg()
    draft = {"subject": "Re: your invoice", "body": "hello", "cta": "call", "opt_out": "stop", "vertical": "x"}
    _score, reasons = lib.quality_score(draft, cfg, requires_opt_out=True)
    assert "misleading_subject" in reasons


def test_generated_accepted_drafts_pass_quality():
    drafts = lib.generate_drafts(target=400)
    accepted = [d for d in drafts if d["status"] == "founder_review"]
    cfg = _quality_cfg()
    for d in accepted:
        assert d["quality_score"] >= cfg["min_quality_score"]
    assert len(accepted) > 0
