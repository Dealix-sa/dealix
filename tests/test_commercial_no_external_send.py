"""The non-negotiable: nothing the factory produces can be sent externally."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import commercial_launch_lib as lib  # noqa: E402


def test_every_draft_is_non_sendable():
    drafts = lib.generate_drafts(target=400)
    for d in drafts:
        assert d["send_allowed"] is False
        assert d["external_send_blocked"] is True
        assert d["requires_founder_approval"] is True
        assert d["no_auto_send"] is True


def test_assert_safety_does_not_raise():
    lib.assert_safety(lib.generate_drafts(target=400))


def test_assert_safety_catches_violation():
    drafts = lib.generate_drafts(target=400)
    drafts[0]["send_allowed"] = True
    try:
        lib.assert_safety(drafts)
    except AssertionError:
        return
    raise AssertionError("assert_safety must reject a sendable draft")


def test_no_send_libraries_imported_in_lib():
    text = (SCRIPTS / "commercial_launch_lib.py").read_text(encoding="utf-8").lower()
    for forbidden in ("import smtplib", "import sendgrid", "from twilio", "import selenium", "import playwright"):
        assert forbidden not in text


def test_launch_config_safety_contract():
    safety = lib.load_config("commercial_launch.json")["safety"]
    assert safety["send_allowed"] is False
    assert safety["external_send_blocked"] is True
    assert safety["requires_founder_approval"] is True
    assert safety["no_auto_send"] is True
