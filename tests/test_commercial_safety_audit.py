"""Safety audit passes for clean drafts and fails on tampered ones."""

from __future__ import annotations

from tests._lc_util import REPO_ROOT  # noqa: F401

from launch_os.drafts import generate_drafts
from launch_os.safety import audit


def test_clean_drafts_pass():
    result = audit(generate_drafts(target=400))
    assert result["pass"] is True
    assert result["counts"]["send_allowed_true"] == 0
    assert result["counts"]["external_send_blocked_false"] == 0
    assert result["counts"]["no_auto_send_false"] == 0
    assert result["counts"]["overclaim_drafts"] == 0
    assert result["counts"]["contact_field_drafts"] == 0


def test_send_allowed_tamper_fails():
    drafts = generate_drafts(target=400)
    drafts[0]["send_allowed"] = True
    result = audit(drafts)
    assert result["pass"] is False
    assert result["counts"]["send_allowed_true"] == 1


def test_overclaim_tamper_fails():
    drafts = generate_drafts(target=400)
    drafts[3]["body_en"] += " guaranteed ROI 100% replace your team"
    result = audit(drafts)
    assert result["pass"] is False
    assert result["counts"]["overclaim_drafts"] >= 1


def test_contact_field_tamper_fails():
    drafts = generate_drafts(target=400)
    drafts[5]["email"] = "someone@example.com"
    result = audit(drafts)
    assert result["pass"] is False
    assert result["counts"]["contact_field_drafts"] >= 1
