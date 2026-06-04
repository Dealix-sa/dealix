"""Every draft is review-only: the mandatory no-send flags are always set."""

from __future__ import annotations

import commercial_generate_400_drafts as gen
from _launch_util import SEED, TEST_DAY


def test_mandatory_safety_flags_on_every_draft():
    drafts = gen.generate(target=400, day=TEST_DAY, seed_path=SEED)["drafts"]
    for d in drafts:
        assert d["send_allowed"] is False
        assert d["external_send_blocked"] is True
        assert d["requires_founder_approval"] is True
        assert d["no_auto_send"] is True


def test_verify_safety_rejects_tampered_draft():
    import pytest

    drafts = gen.generate(target=400, day=TEST_DAY, seed_path=SEED)["drafts"]
    drafts[0]["send_allowed"] = True
    with pytest.raises(AssertionError):
        gen._verify_safety(drafts)


def test_common_mandatory_flags_constant():
    from _commercial_common import MANDATORY_SAFETY_FLAGS

    assert MANDATORY_SAFETY_FLAGS == {
        "send_allowed": False,
        "external_send_blocked": True,
        "requires_founder_approval": True,
        "no_auto_send": True,
    }
