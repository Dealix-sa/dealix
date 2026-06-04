import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _v5util import run, load_drafts


def test_no_send_static_check():
    assert run("api_commercial_static_check.py").returncode == 0


def test_every_draft_blocks_external_send():
    for d in load_drafts():
        assert d["send_allowed"] is False
        assert d["external_send_blocked"] is True
        assert d["requires_founder_approval"] is True
        assert d["no_auto_send"] is True
